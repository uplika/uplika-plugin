# Naver Clip

Naver Clip posts are written by the Uplika extension in the person's own browser, the same way as Naver Blog. Call `bridge_status` before publishing.

## Options

- `options.naver_clip.categoryId`: required. Pick from `naverClip.categories` in `list_accounts` (or pass `options.naver_clip.category` with the name). Ask the person; do not pick for them.
- `options.naver_clip.tags`: hashtags without `#`. Naver Clip has no tag field, so they are appended to the description; #words already in the description count too.
- `options.naver_clip.visibility`: `public` or `private`. A private clip is still posted, only the owner sees it.
- `options.naver_clip.aiGenerated`: Naver Clip's AI-use label. Media uploaded with `aiGenerated` turns it on by itself.
- `options.naver_clip.adDisclosure`: ad and sponsorship label. A legal statement; ask the person.
- `options.naver_clip.disableComments`: turn comments off for this clip.
- `options.naver_clip.draftOnly`: upload and keep it as a draft in Naver Clip Creators instead of posting.

## Always ask

- Whether it is an ad or sponsored, and which category it belongs to.

## Not available

Read `list_platforms` and its features table. uplika posts clips, reads one back (`get_post`), lists them (`list_channel_posts`), deletes them (`delete_post`) and reads views and likes (`get_insights`). Editing a clip and comments are done in Naver Clip Creators.

- Reading, listing, deleting and metrics need a newer browser extension than posting. With an older one they answer `extension_outdated`; tell the person to update the extension in that browser.
- A clip is looked up among the profile's most recent clips. An older clip answers 409 and nothing is changed; send the person to Naver Clip Creators.
- Deleting a clip that was already deleted in Naver Clip Creators clears uplika's record.

## Pitfalls

- One video per clip. Photos and text-only posts are refused for Naver Clip.
- The person needs a Naver Clip profile; uplika does not create one. `clip_no_profile` means they make it in Naver Clip Creators and connect Naver Clip again.
- `clip_unconfirmed` means Post was pressed but the clip was not found in the list. Check Naver Clip Creators before sending again, or it may go up twice.
