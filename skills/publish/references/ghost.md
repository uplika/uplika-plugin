# Ghost

## Options

- `options.ghost.title`: required. The post title.
- `options.ghost.tags`: tag names. Ghost creates any tag that does not exist yet. A name must not start with `#` (Ghost would make it a hidden internal tag) and must not contain a comma.
- `options.ghost.featureImageMediaId`: a media id to use as the feature image at the top of the post.
- `options.ghost.draftOnly`: `true` saves it as a draft in Ghost. The permalink is then the Ghost editor page for that draft, not a public address.

## Always ask

- The title, if the person did not give one.
- Whether it should go live or wait as a Ghost draft, when the person did not say.

## Body

- Write Markdown. Ghost renders it as written.
- Place a photo with `![alt](media:<id>)` on a line of its own. Uplika copies each photo to the Ghost site; photos you attach without placing them go at the end.
- Do not use Naver Blog syntax (`@group`, `@video`, `@card`, `{.small}` and other `{…}` attributes). Ghost refuses those lines.
- A post with media references cannot go to Ghost and Naver Blog in the same call; publish each on its own.

## Not available

Read `list_platforms` and its features table. Uplika does not read Ghost comments or view counts, and Ghost posts take photos only. No newsletter email is ever sent: the post only goes to the site.

## Pitfalls

- Ghost(Pro) Starter has no custom integrations, so it cannot connect (`ghost_plan_limit`). Publisher and above, or a self-hosted Ghost, can.
- The API URL is the one in the custom integration (on Ghost(Pro) it ends in `.ghost.io`), not the public site address.
- `update_post` rewrites the post in place and keeps its Ghost status; tags and the feature image you leave out are kept. If someone is editing the post in Ghost Admin at that moment, it fails with `ghost_update_collision`; ask them to close the editor and try again.
- Posts published with an integration key show the site owner as the author.
