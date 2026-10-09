#!/usr/bin/env bash
# 모노레포 plugin/ 을 공개 저장소 uplika/uplika-plugin 으로 내보낸다 (ADR 0033). 공개 저장소에서 직접 고치지 않는다.
#
#   plugin/scripts/export.sh            # 검사 → (없으면 저장소 생성) → 사본 push → 트리 해시 대조
#   plugin/scripts/export.sh --dry-run  # push 없이 사본만 만들어 차이를 보인다
#
# **gh 를 안 쓴다.** 이 저장소의 계정 가드(.claude/hooks/account-guard.sh)가 gh auth login/switch 를 막는다 — 전역 활성 계정을
# 바꾸면 이 맥의 다른 프로젝트가 남의 계정으로 push 한다. 그래서 GitHub uplika 계정의 클래식 토큰(public_repo 범위, 만료 있음)을
# 프로젝트 .secrets/github-uplika.env (git 밖, GITHUB_UPLIKA_TOKEN=…)에 두고 git · REST 에만 싣는다. 전역 상태를 안 건드린다.
# 토큰이 만료되면 uplika 로 로그인된 크롬에서 github.com/settings/tokens 로 다시 발급한다 (sudo 인증은 support@ 메일 코드).
# 커밋 author 는 uplika 계정 메일이다 (목록 주인과 push 권한이 그 계정이다).
# 기획: docs/plans/2026-10-09-agent-plugin-design.md 「사본을 내보내는 길」 · 구현 계획 Task 2 · 8
set -euo pipefail

ROOT="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
PLUGIN="$ROOT/plugin"
REPO="uplika/uplika-plugin"
OWNER="uplika"
# 워크트리에서 돌면 ROOT 가 워크트리라 .secrets 가 비어 있다. 메인 체크아웃의 것을 쓴다
MAIN_ROOT="$(dirname "$(git -C "$ROOT" rev-parse --path-format=absolute --git-common-dir)")"
TOKEN_FILE="${UPLIKA_GITHUB_TOKEN_FILE:-$MAIN_ROOT/.secrets/github-uplika.env}"
DRY_RUN=0
[ "${1:-}" = "--dry-run" ] && DRY_RUN=1

DESC="$(node -e 'process.stdout.write(require(process.argv[1]).description)' "$PLUGIN/.claude-plugin/plugin.json")"

node "$PLUGIN/scripts/check.mjs"

# 내보내는 것은 커밋된 plugin/ 이다. 고친 채로 내보내면 사본이 원본 어디에도 없는 상태가 된다
if [ -n "$(git -C "$ROOT" status --porcelain -- plugin)" ]; then
  echo "[export] plugin/ 에 커밋 안 한 변경이 있다. 먼저 커밋한다." >&2
  git -C "$ROOT" status --short -- plugin >&2
  exit 1
fi

# gitignore 에 걸린 파일은 `git status` 에 안 보여서 커밋된 트리(= 사본)에서 조용히 빠진다. 아이콘 PNG 가 그렇게 빠질 뻔했다
# (루트 .gitignore 의 `*.png`, 2026-10-10). 시험이 남기는 __pycache__ 만 빼고 하나라도 있으면 멈춘다
IGNORED="$(git -C "$ROOT" ls-files --others --ignored --exclude-standard -- plugin | grep -v '__pycache__' || true)"
if [ -n "$IGNORED" ]; then
  echo "[export] plugin/ 에 gitignore 로 무시된 파일이 있다. 사본에 안 들어간다 (.gitignore 에 예외를 더하고 커밋한다):" >&2
  echo "$IGNORED" >&2
  exit 1
fi

if [ ! -f "$TOKEN_FILE" ]; then
  echo "[export] 토큰 파일이 없다: $TOKEN_FILE (GITHUB_UPLIKA_TOKEN=…)" >&2
  exit 1
fi
# shellcheck disable=SC1090
TOKEN="$(set -a; . "$TOKEN_FILE"; printf '%s' "${GITHUB_UPLIKA_TOKEN:-}")"
[ -n "$TOKEN" ] || { echo "[export] GITHUB_UPLIKA_TOKEN 이 비었다" >&2; exit 1; }

api() {
  curl -fsS -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" -H "X-GitHub-Api-Version: 2022-11-28" "$@"
}

LOGIN="$(api https://api.github.com/user | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>process.stdout.write(JSON.parse(s).login||""))')"
if [ "$LOGIN" != "$OWNER" ]; then
  echo "[export] 토큰 주인이 $OWNER 가 아니라 ${LOGIN:-?} 이다. 남의 계정으로 공개 저장소를 만들지 않는다." >&2
  exit 1
fi

STATUS="$(curl -s -o /dev/null -w '%{http_code}' -H "Authorization: Bearer $TOKEN" "https://api.github.com/repos/$REPO")"
if [ "$STATUS" = "404" ]; then
  if [ "$DRY_RUN" = 1 ]; then
    echo "[export] (dry-run) 저장소가 없다: $REPO 를 만들 차례다"
  else
    BODY="$(node -e 'process.stdout.write(JSON.stringify({name:"uplika-plugin",description:process.argv[1],homepage:"https://uplika.com",private:false,has_wiki:false,has_projects:false}))' "$DESC")"
    api -X POST https://api.github.com/user/repos -d "$BODY" >/dev/null
    api -X PUT "https://api.github.com/repos/$REPO/topics" \
      -d '{"names":["mcp","claude-code-plugin","codex-plugin","gemini-cli-extension","social-media","agent-skills"]}' >/dev/null
    echo "[export] 저장소를 만들었다: https://github.com/$REPO"
  fi
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
# 토큰을 URL 에 싣지 않는다 (ps · git 설정에 남는다). 이 명령에만 헤더로 준다
AUTH_HEADER="Authorization: Basic $(printf 'x-access-token:%s' "$TOKEN" | base64 | tr -d '\n')"
REMOTE="https://github.com/${REPO}.git"
if [ "$STATUS" != "404" ] && git -c http.extraHeader="$AUTH_HEADER" ls-remote --exit-code "$REMOTE" HEAD >/dev/null 2>&1; then
  git -c http.extraHeader="$AUTH_HEADER" clone --quiet "$REMOTE" "$TMP/repo"
else
  git init --quiet -b main "$TMP/repo"
  git -C "$TMP/repo" remote add origin "$REMOTE"
fi

# **커밋된 트리를 내보낸다** (작업 트리가 아니라). 시험이 남긴 __pycache__ 같은 추적 안 되는 찌꺼기가 섞이지 않고,
# 아래 트리 해시 대조가 정의상 같은 것을 비교한다
mkdir -p "$TMP/stage"
git -C "$ROOT" archive --format=tar HEAD:plugin | tar -x -C "$TMP/stage"
# --checksum: 내용으로 비교한다. 클론과 압축 풀기가 같은 초에 끝나면 크기 · 수정 시각(초 단위)이 같은 파일을 rsync 가 같은 것으로 보고
# 건너뛴다. 판 숫자만 바꾼 매니페스트 다섯(0.1.0 → 0.1.1)이 그렇게 빠져서 트리 해시 대조가 잡았다 (2026-10-10, macOS openrsync)
rsync -a --checksum --delete --exclude .git "$TMP/stage/" "$TMP/repo/"
cd "$TMP/repo"
git add -A
SHORT="$(git -C "$ROOT" rev-parse --short HEAD)"
if git diff --cached --quiet; then
  echo "[export] 바뀐 것이 없다 (모노레포 $SHORT)"
else
  git -c user.name="$OWNER" -c user.email="support@uplika.com" commit --quiet -m "Copy of plugin/ at Uplika monorepo $SHORT"
  if [ "$DRY_RUN" = 1 ]; then
    git --no-pager show --stat HEAD | tail -20
    echo "[export] (dry-run) push 안 함"
    exit 0
  fi
  git -c http.extraHeader="$AUTH_HEADER" push --quiet origin HEAD:main
  echo "[export] push: $(git rev-parse --short HEAD) ← 모노레포 $SHORT"
fi

MONO_TREE="$(git -C "$ROOT" rev-parse "HEAD:plugin")"
PUB_TREE="$(git rev-parse "HEAD^{tree}")"
if [ "$MONO_TREE" != "$PUB_TREE" ]; then
  echo "[export] 트리 해시가 다르다: 모노레포 $MONO_TREE · 공개 $PUB_TREE" >&2
  exit 1
fi
echo "[export] 트리 해시 일치: $PUB_TREE"
