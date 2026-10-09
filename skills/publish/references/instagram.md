# Instagram

## Options

- `options.instagram.contentType`: `feed`, `reel` or `story`. Leave it out and a single video becomes a reel, anything else a feed post. Several images in a feed post make a carousel.
- `options.instagram.coverMediaId`: a reel's cover image (media id). Reels only.
- `options.instagram.thumbOffsetMs`: a reel's cover frame instead of an image.
- `options.instagram.shareToFeed`: reels only; false keeps the reel out of the main feed.
- `options.instagram.collaborators`: public professional accounts invited as collaborators. They appear only after accepting. Not on stories.
- `options.instagram.userTags`: tag accounts on the media.
- `options.instagram.firstComment`: a comment posted right after publishing, often for hashtags. Not on stories.
- `options.instagram.isAiGenerated`: the AI label. Media uploaded with `aiGenerated` turns it on by itself.

## Always ask

- Feed, reel or story when the person did not say and the media fits more than one.
- Collaborators, if the person mentions a partner account.

## Not available

Read `list_platforms` and its features table. Instagram posts cannot be edited after publishing (`update_post` refuses), and deleting depends on how the account was connected: the features table and `list_accounts` say which. Stories show no caption.

## Pitfalls

- A feed image outside the aspect range Instagram accepts is not rejected: the server crops it to the nearest allowed shape, centered, and the result carries a warning. Tell the person before publishing if the edges matter.
- Instagram has two connection paths (through Instagram, through Facebook). Some actions exist on one path only; the reconnect link in a refusal says what to do.
- Direct messages and comment-to-DM are the `inbox` and `automations` skills, not this one.
