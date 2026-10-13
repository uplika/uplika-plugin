# Bluesky

## Options

- `options.bluesky.langs`: the language codes of the text, like `["ko"]` or `["en", "ko"]`. Language feeds filter on this, so set it. Bluesky has no editing, so it cannot be fixed later.

## Always ask

- The language, when the text mixes languages.

## Not available

Read `list_platforms` and its features table. Bluesky posts cannot be edited.

## Pitfalls

- Links in the text become clickable because the server builds the link annotations; just write the URL.
- Image counts and sizes come from `list_platforms`; a video and images do not go together.
- After `delete_post`, the post can still show in the Bluesky app for a while because the app view lags. Uplika confirms the deletion against the person's own server (PDS), so trust `delete_post` and `get_post`, not what the app shows right away.
