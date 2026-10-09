#!/usr/bin/env node
/**
 * 플러그인 제출 상한 검사 (2026-10-10). 의존성 0. `node plugin/scripts/check.mjs` · 종료 0 = 통과.
 *
 * 기획: docs/plans/2026-10-09-agent-plugin-design.md 「드리프트 시험」 · 구현 계획 Task 2
 *
 * 디렉터리(Anthropic · OpenAI)와 각 CLI 가 거절하는 모양을 **올리기 전에** 여기서 잡는다. 도구 이름 · 템플릿 · FAQ · 옵션 칸이
 * 서버와 맞는지는 이 파일이 아니라 `api/src/plugin-skills.test.ts` 가 잰다 (서버 코드를 import 해야 해서다).
 *
 * - 파일 512개 이하 · 이미지 · 폰트 외 파일 256 KiB 미만 · 바이너리(PDF · zip · 실행파일) · 심볼릭 링크 없음
 * - `skills/<이름>/SKILL.md` 마다 frontmatter `name`(폴더 이름과 같음) · `description`(1 ~ 150자)
 *   150자: Codex 가 스킬 목록을 8,000자로 자른다. 스킬 수로 나누면 하나가 그 안이어야 목록이 안 잘린다
 * - MCP 주소가 세 매니페스트에서 글자까지 같다 (커넥터 주소와 다르면 사용자에게 도구가 두 벌 보인다)
 * - 비밀값 모양이 없다 · `hooks/` · `.app.json` 이 없다 (OpenAI 공개 제출이 hooks 를 막는다)
 * - 문장 속 em-dash 가 없다 (저장소 카피 규칙)
 */
import { lstatSync, readdirSync, readFileSync, existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const MCP_URL = "https://api.uplika.com/mcp";
const MAX_FILES = 512;
const MAX_BYTES = 256 * 1024;
const MAX_DESCRIPTION = 150;
const IMAGE_EXT = new Set([".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp", ".woff", ".woff2"]);
const BANNED_EXT = new Set([".pdf", ".zip", ".exe", ".dylib", ".so", ".ico", ".dll", ".bin", ".jar"]);
const SECRET_RE = /(sk|pk|rk)_(live|test)_[A-Za-z0-9]{8,}|Bearer [A-Za-z0-9._-]{20,}|-----BEGIN/;
/* 스크립트 자신은 비밀값 정규식 · 금지 모양을 글자로 든다 */
const SELF = path.relative(ROOT, fileURLToPath(import.meta.url));

const problems = [];
const fail = (file, message) => problems.push(`${file}: ${message}`);

/** 숨김 폴더도 돈다 (`.claude-plugin` · `.agents`). `.git` 만 뺀다 */
function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    if (name === ".git" || name === "node_modules" || name === "__pycache__") continue;
    const full = path.join(dir, name);
    const stat = lstatSync(full);
    if (stat.isSymbolicLink()) {
      fail(path.relative(ROOT, full), "symbolic link (not allowed)");
      continue;
    }
    if (stat.isDirectory()) walk(full, out);
    else out.push({ full, rel: path.relative(ROOT, full), size: stat.size });
  }
  return out;
}

const files = walk(ROOT);
if (files.length > MAX_FILES) fail(".", `${files.length} files, limit ${MAX_FILES}`);

for (const file of files) {
  const ext = path.extname(file.rel).toLowerCase();
  if (BANNED_EXT.has(ext)) fail(file.rel, `binary type ${ext} is not allowed`);
  if (!IMAGE_EXT.has(ext) && file.size >= MAX_BYTES) fail(file.rel, `${file.size} bytes, limit is under ${MAX_BYTES}`);
  if (path.basename(file.rel) === ".app.json") fail(file.rel, ".app.json is not allowed");
  if (file.rel.split(path.sep).includes("hooks") && file.rel.split(path.sep)[0] === "hooks") {
    fail(file.rel, "hooks/ is not allowed (OpenAI public submission rejects hooks)");
  }
  if (IMAGE_EXT.has(ext) || file.rel === SELF) continue;
  const text = readFileSync(file.full, "utf8");
  if (SECRET_RE.test(text)) fail(file.rel, "looks like a secret");
  if ((ext === ".md" || ext === ".json") && /\S — \S/.test(text)) fail(file.rel, "em-dash inside a sentence");
}
if (existsSync(path.join(ROOT, "hooks"))) fail("hooks", "hooks/ is not allowed");

/* ── 스킬 frontmatter ─────────────────────────────────────────── */

/**
 * frontmatter 를 **엄격한 YAML 파서가 읽는 그대로** 읽는다. 따옴표 없는 값에 `: ` · ` #` 이 있거나 YAML 지시 문자로 시작하면
 * PyYAML · serde_yaml 같은 엄격 파서가 frontmatter 째 거부한다 (Claude Code 는 관대해서 통과해 놓친다, 2026-10-10 실측).
 * 그런 값은 큰따옴표(JSON 이스케이프)로 감싼다. 감싼 값은 JSON 으로 풀어서 길이를 잰다.
 */
function frontmatter(text, rel) {
  const match = /^---\n([\s\S]*?)\n---\n/.exec(text);
  if (!match) return null;
  const out = {};
  for (const line of match[1].split("\n")) {
    const kv = /^([A-Za-z_-]+):\s*(.*)$/.exec(line);
    if (!kv) continue;
    const raw = kv[2];
    if (raw.startsWith('"')) {
      try {
        out[kv[1]] = JSON.parse(raw);
      } catch {
        fail(rel, `${kv[1]} is not a valid double-quoted string`);
      }
      continue;
    }
    if (raw.startsWith("'")) {
      if (!/^'(?:[^']|'')*'$/.test(raw)) fail(rel, `${kv[1]} is not a valid single-quoted string`);
      out[kv[1]] = raw.slice(1, -1).replace(/''/g, "'");
      continue;
    }
    if (/: |\s#/.test(raw) || /^[\[\]{}&*!|>%@`,?:-]/.test(raw)) {
      fail(rel, `${kv[1]} must be double-quoted for strict YAML parsers (contains ": ", " #" or starts with an indicator)`);
    }
    out[kv[1]] = raw;
  }
  return out;
}

const skillsDir = path.join(ROOT, "skills");
const skillNames = existsSync(skillsDir)
  ? readdirSync(skillsDir).filter((name) => lstatSync(path.join(skillsDir, name)).isDirectory())
  : [];
for (const name of skillNames) {
  const rel = path.join("skills", name, "SKILL.md");
  const full = path.join(ROOT, rel);
  if (!existsSync(full)) {
    fail(rel, "missing SKILL.md");
    continue;
  }
  const fm = frontmatter(readFileSync(full, "utf8"), rel);
  if (!fm) {
    fail(rel, "no frontmatter");
    continue;
  }
  if (fm.name !== name) fail(rel, `frontmatter name "${fm.name ?? ""}" is not the folder name "${name}"`);
  const description = fm.description ?? "";
  if (description.length < 1 || description.length > MAX_DESCRIPTION) {
    fail(rel, `description is ${description.length} characters (1 to ${MAX_DESCRIPTION})`);
  }
}

/* ── MCP 주소 ─────────────────────────────────────────────────── */

const readJson = (rel) => JSON.parse(readFileSync(path.join(ROOT, rel), "utf8"));
const urls = {
  ".mcp.json": readJson(".mcp.json").mcpServers?.uplika?.url,
  "mcp.json": readJson("mcp.json").mcpServers?.uplika?.url,
  "gemini-extension.json": readJson("gemini-extension.json").mcpServers?.uplika?.httpUrl,
};
for (const [rel, url] of Object.entries(urls)) {
  if (url !== MCP_URL) fail(rel, `MCP url is "${url}", expected "${MCP_URL}"`);
}

/* 매니페스트끼리 이름 · 판이 같다 */
const versions = {
  ".claude-plugin/plugin.json": readJson(".claude-plugin/plugin.json").version,
  ".claude-plugin/marketplace.json": readJson(".claude-plugin/marketplace.json").metadata?.version,
  "plugin.json": readJson("plugin.json").version,
  "gemini-extension.json": readJson("gemini-extension.json").version,
  ".kimi-plugin/plugin.json": readJson(".kimi-plugin/plugin.json").version,
  ".grok-plugin/plugin.json": readJson(".grok-plugin/plugin.json").version,
};

/*
  Anthropic 디렉터리 목록 칸 (2026-10-10). `icon` 은 플러그인 안의 이미지 경로, URL 넷은 https. 포털 「검증」 이 아이콘을 요구한다.
  아이콘 바이트는 `brand/scripts/export.mjs` 가 512 PNG 에서 복사하고 `brand/icon-drift.test.mjs` 가 해시로 지킨다
*/
const listing = readJson(".claude-plugin/plugin.json");
if (typeof listing.icon !== "string" || !listing.icon.startsWith("./") || !IMAGE_EXT.has(path.extname(listing.icon).toLowerCase())) {
  fail(".claude-plugin/plugin.json", `icon must be a ./ path to an image inside the plugin, got "${listing.icon ?? ""}"`);
} else if (!existsSync(path.join(ROOT, listing.icon))) {
  fail(".claude-plugin/plugin.json", `icon file ${listing.icon} does not exist`);
}
for (const key of ["privacyPolicyUrl", "termsOfServiceUrl", "documentationUrl", "supportUrl"]) {
  if (typeof listing[key] !== "string" || !listing[key].startsWith("https://")) fail(".claude-plugin/plugin.json", `${key} must be an https:// URL`);
}
const distinct = new Set(Object.values(versions));
if (distinct.size !== 1) fail("manifests", `versions differ: ${JSON.stringify(versions)}`);

if (problems.length) {
  for (const line of problems) console.error(line);
  console.error(`\n${problems.length} problem(s)`);
  process.exit(1);
}
console.log(`plugin check passed: ${files.length} files, ${skillNames.length} skills, version ${[...distinct][0]}`);
