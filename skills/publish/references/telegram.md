# Telegram

## Options

No channel-specific fields besides `options.telegram.content` (its own text). The bot and the chat it posts to were chosen when the account was connected.

## Always ask

- Which chat, when more than one Telegram account is connected (each account is one bot in one chat).

## Not available

Read `list_platforms` and its features table. Telegram's bot API gives no view counts, comments or post history, so insights, replies and channel post lists are refused there.

## Pitfalls

- The text limit depends on whether the message carries media (a caption is shorter than a text message). `list_platforms` gives both; check the one that applies.
- Several images go out as one album. Deleting removes every message of the album.
