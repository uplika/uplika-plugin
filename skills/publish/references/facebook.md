# Facebook (Page)

## Options

- `options.facebook.contentType`: `feed`, `reel` or `story`. Leave it out and a single video becomes a reel, anything else a feed post.
- `options.facebook.title`: a reel's title, separate from the caption.
- `options.facebook.link`: makes a link post with a preview card. Cannot be combined with media.
- `options.facebook.firstComment`: a comment posted right after publishing. Not on stories or scheduled posts.
- `options.facebook.scheduledPublishTime`: Facebook's own scheduling for feed posts. For scheduling across channels use `scheduledAt` on the post instead.
- `options.facebook.feedTargeting`: a preferred audience hint for text and link posts only. Facebook does not keep it on photo posts or reels.

## Always ask

- Which Page, when more than one is connected.
- For a story: Facebook rejects any text on a story, so publish it with no content and put the words in a feed post.

## Not available

Read `list_platforms` and its features table. Editing depends on the kind of post (the features table says which kinds). Hiding works on other people's comments; the Page's own comment is deleted instead of hidden.

## Pitfalls

- `feedTargeting` is a hint, not a limit: everyone can still see the post.
- A link post and media cannot go together; choose one.
