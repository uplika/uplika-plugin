# LinkedIn

## Options

- `options.linkedin.visibility`: `PUBLIC` (the default, anyone on or off LinkedIn) or `CONNECTIONS` (the person's 1st-degree connections only).
- `options.linkedin.link`: an `https://` address shown as a link card under the text. Only on a post without files.
- `options.linkedin.linkTitle`: the title on the link card. Required with `link`, because LinkedIn does not read the page.
- `options.linkedin.linkDescription`: optional description sent with the card. LinkedIn's card currently shows only the title and the domain.

## Always ask

- Who should see the post, when the person has not said. The default is public.
- The card title, when they give a link.

## Not available

Read `list_platforms` and its features table. LinkedIn closed the permission to read members' posts to new apps, so reading a post, listing the profile's posts, comments and metrics are refused there. Publishing, rewriting the text and deleting work.

## Pitfalls

- This is the person's own profile, not a company page.
- The connection lasts 60 days and LinkedIn offers no way to extend it. After that the person reconnects under Connections. `list_accounts` shows when it ends; a post scheduled after that date fails.
- A post holds text, several images or one video (`list_platforms` has the counts). Images and video do not mix, and files and a link card do not mix.
- Editing changes the text only. The image, video and link card stay as they were.
- LinkedIn refuses the same text twice on one profile. Change the text instead of sending it again.
- Video takes a while to process. Pass `wait: true` and report the permalink only when the post is out.
