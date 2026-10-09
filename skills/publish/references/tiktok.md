# TikTok

## Options

- `options.tiktok.privacyLevel`: who can see the post. **Required and has no default.** Use one of the values `get_publish_options` returns for this account, and ask the person every time; do not pick for them.
- `options.tiktok.postMode`: `direct` posts to the profile; `draft` sends it to the creator's TikTok inbox to finish in the app (then no privacy value is sent).
- `options.tiktok.title`: required for a photo post; a video post has no title field.
- `options.tiktok.disableComment`, `options.tiktok.disableDuet`, `options.tiktok.disableStitch`: turn those off for this post.
- `options.tiktok.brandContentToggle`: paid partnership declaration (cannot be private).
- `options.tiktok.brandOrganicToggle`: promotes the creator's own brand. Leave it out rather than sending false.
- `options.tiktok.isAigc`: AI-generated content declaration. Media uploaded with `aiGenerated` turns it on by itself.
- `options.tiktok.videoCoverTimestampMs`: the cover frame. TikTok takes no cover image file.

## Always ask

- Call `get_publish_options` before every TikTok post: it returns the creator name the post goes out as, the privacy levels allowed right now, whether the account can post at all, and its video length limit. Show the creator name and ask for the privacy level.
- Whether it is branded content or the creator's own brand, if the post promotes anything.

## Not available

Read `list_platforms` and its features table. TikTok's API offers no deleting and no comments, so those requests are refused.

## Pitfalls

- The allowed privacy levels differ per account and change when the person edits their TikTok settings, so never reuse yesterday's answer.
- `list_channel_posts` reads public videos only.
