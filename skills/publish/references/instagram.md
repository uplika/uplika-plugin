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
- `options.instagram.audio`: music, or another reel's original sound, on a reel: `{ "id": "<from search_instagram_audio>", "volume": 20, "videoVolume": 100 }`. Reels only, and only on accounts connected via Facebook. `volume` is the added audio and `videoVolume` the video's own sound, each a whole number from 0 to 100; Instagram defaults both to 100, which drowns a voice-over.

## Always ask

- Feed, reel or story when the person did not say and the media fits more than one.
- Collaborators, if the person mentions a partner account.
- The audio and both volumes, if the person wants music on a reel. Instagram cannot preview the mix before it is published. The audio plays once from its beginning (the start cannot be chosen) and is not repeated, so pick one at least as long as the reel.

## Not available

Read `list_platforms` and its features table. Instagram posts cannot be edited after publishing (`update_post` refuses), and deleting depends on how the account was connected: the features table and `list_accounts` say which. Stories show no caption.

## Pitfalls

- A feed image outside the aspect range Instagram accepts is not rejected: the server crops it to the nearest allowed shape, centered, and the result carries a warning. Tell the person before publishing if the edges matter.
- Instagram has two connection paths (through Instagram, through Facebook). Some actions exist on one path only; the reconnect link in a refusal says what to do.
- Direct messages and comment-to-DM are the `inbox` and `automations` skills, not this one.
- Audio search with a word finds only royalty-free music from Meta's Sound Collection, so an artist or song name will not find that song. Popular songs are in the trending list (search without a word), and that list differs per account. Use an id from the same account's results.
