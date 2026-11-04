# X

Read `list_platforms` first. While X's status there is not `live`, X cannot be connected yet: tell the person so and do not try to publish there. Everything below applies once X is `live`.

## Options

- `options.x.poll`: a poll with 2 to 4 choices and how many minutes it stays open. X does not allow a poll on a post with photos or a video, so leave media out.
- `options.x.replySettings`: who can reply. Leave it out and anyone can reply.
- A chain (`threadItems`) goes out on X as one post per piece, each a reply to the piece before it.

## Always ask

- Which X account, when the person has several. Each one needs its own text (Pitfalls).

## Credits

- X charges per API call, so posting to X through Uplika is paid from X credits the person buys in advance (prepaid). Uplika passes X's rate on with no markup. Each post, reply, attached file (photo, GIF or video), alt text on each image, delete and metrics read on X is charged; reading the current prices is free in `list_platforms`.
- Each piece of a chain (`threadItems`) after the first goes out as a reply and is charged the reply price, with or without a link.
- A single post, or the first piece of a chain, costs more when its text has a link that starts with `http://` or `https://`, because X prices link posts higher. A bare domain such as `uplika.com` is charged as a plain post. Read both prices from `list_platforms` before you add a link the person did not ask for.
- When the balance is too low, the call answers 402 `x_credits_insufficient` with `topUpUrl` and nothing reaches X. Give the person that `topUpUrl` and stop. Do not retry. After they top up, send the post again. See `faq:x-credits-ran-out`.
- A thread can stop partway instead: a later part fails with `x_credits_insufficient` while the first parts are already public. Parts already up stay up. Top up, then call retry_post; it continues from this part. Do not send the whole chain again.

## Not available

Read `list_platforms` and its features table. Quote posts and likes are refused: Uplika does not offer them on X. X posts cannot be edited after they go out (X lets only Premium subscribers edit), so delete and publish again. Uplika does not read posts or replies back from X; the permalink comes back when the post is published and `get_insights` returns its numbers.

## Pitfalls

- Do not send the same text to two X accounts within 24 hours. X's automation rules forbid it, and Uplika refuses the second one with `x_duplicate_across_accounts` before X is called. Texts that differ only in the number of spaces or line breaks, or in letter case, count as the same. Write a different text for each account.
- X counts characters with weights: Korean, Chinese and Japanese characters and emoji count 2, and every link counts 23. Write to the limit `select_channels` returns, not to a character count you did yourself.
- A reply goes through only when the post's author mentioned or quoted the connected account. X refuses other replies from apps.
- Metrics are switched on per X connection by the person, on the Connections page. While they are off, `get_insights` answers with a note and charges nothing.
