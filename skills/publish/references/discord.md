# Discord

## Options

- `options.discord.mentions`: who a mention in the text notifies. Leave it out and nobody is pinged, even by @everyone or @here. Only set `all` when the person asked to notify the whole server.
- `options.discord.silent`: post without a push notification.
- `options.discord.suppressEmbeds`: no link previews for URLs in the text.
- `options.discord.username`: the sender name on this one message. Leave it out to use the webhook's name.

## Always ask

- Whether this post should notify people. The default notifies nobody.
- Which channel, when more than one Discord account is connected (each account is one webhook in one channel).

## Not available

Read `list_platforms` and its features table. A webhook cannot read replies or a channel's post history, so replies and channel post lists are refused there.

## Pitfalls

- A forum or media channel's webhook is refused, because those channels need a new thread for every post.
- Attachments must add up to 25 MB or less in one message. `list_platforms` gives the per-file limit.
- Editing changes the text only; attachments stay as they were.
