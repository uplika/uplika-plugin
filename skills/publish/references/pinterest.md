# Pinterest

## Options

- `options.pinterest.boardId`: the board to pin to. `list_accounts` lists the boards of each Pinterest account. Leave it out to use the default board the person picked when they connected Pinterest.
- `options.pinterest.title`: the Pin title. The text (content) becomes the Pin description.
- `options.pinterest.link`: where the Pin leads when someone opens it. It must be an `https://` address.
- `options.pinterest.altText`: alt text for the image.
- `options.pinterest.isAiGenerated`: Pinterest shows an AI label on the Pin.
- `options.pinterest.coverMediaId`: a JPEG or PNG used as the cover of a video Pin.
- `options.pinterest.coverKeyFrameSeconds`: which second of the video becomes the cover when no cover image is given.

## Always ask

- Which board, when the person has not said and the default board is not the one they mean.
- The link the Pin should open, if they want one. A Pin without a link is allowed.

## Not available

Read `list_platforms` and its features table. Pinterest has no API for comments, so replies and comment lists are refused. Editing a Pin after it goes out is refused too: Pinterest only lets apps on its beta list do that.

## Pitfalls

- A Pin is exactly one image or one video. Text alone cannot be published.
- A board created on Pinterest after connecting appears only after `refresh_account`.
- While Uplika's Pinterest app is on Trial access, Pins it creates are visible only to the account that made them.
- Video Pins take a while to process. Pass `wait: true` and report the permalink only when the post is out.
