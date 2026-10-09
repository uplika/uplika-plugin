# Threads

## Options

- `options.threads.topicTag`: one topic for the post, like a category. Threads takes one and rejects periods and ampersands in it. On a chain it goes on the first piece. Leave it out unless the person asked for a topic.

## Always ask

- Whether a long text should be one post or a chain. A chain goes in `threadItems` on `publish`; the first item is the root and the rest are replies under it, in order.

## Not available

Read `list_platforms` and its features table instead of assuming. At the time of writing Threads has no direct messages at all (`faq:threads-no-dm`); mentions and liking depend on a permission that may still be in review (`faq:feature-in-review`).

## Pitfalls

- The character limit counts the way `list_platforms` says (`charCount`). Check each chain piece, not just the total.
- Reply approval: when the account holds replies for approval, they wait in a queue; the `comments` skill handles it.
- Write the hook first: the first line is all most people see in the feed. The `threads` skill has the routine.
