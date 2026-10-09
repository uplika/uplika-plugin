---
name: ig-dm
description: Draft Instagram DMs that get replies (keyword delivery, first message to someone who engaged, collab pitch, two follow-ups). Drafts only.
---

Adapted from Jakeschincariol/instagram-agent-skill (MIT). Not affiliated with the original author.

# ig-dm

Use when the person says "DM this person", "what do I send them", "outreach message", "how do I follow up", "pitch this brand", or is reaching out to someone specific. This skill writes drafts and sends nothing; see "With Uplika connected" for where sending happens.

Instagram DMs are the only place on the platform where money actually changes hands, and they are also where most accounts burn the goodwill their content earned. The difference is entirely about who moved first.

Read the voice file `~/.uplika/<workspace-slug>/voice.md` first if it exists. If it does not, ask three questions (tone, how they end a line, words they avoid) and offer to save the answers with the `voice-profile` skill.

## The three kinds of DM, and only three are worth writing

**1. The reply to a hand raised.** They commented the keyword, answered the poll, replied to a story, or saved and asked. They moved first. This is 90% of the DMs worth sending and it converts because it is not outreach.

**2. The warm approach.** Someone whose posts the person has genuinely been commenting on for weeks. There is a shared thread of conversation already.

**3. The collab or brand pitch.** A specific proposal to a specific account, with a reason it is them.

Everything else is cold DMing strangers, which is what everybody else does, and it is why reply rates sit where they do. If the person is asking for a cold sequence, say plainly that it is the lowest-yield thing they could do with the same hour, and offer the alternative: comment on those ten accounts for two weeks first. Then write it if they still want it.

## Before writing, get the specifics

Ask in one batched question:

1. **Who**: handle, what they do, and what they posted or did that started this.
2. **The trigger**: the actual reason to message today. A keyword they commented, a story they replied to, a post they published. Not "they fit the ICP".
3. **What the person wants**: a conversation, a sale, a collab, a referral. Be honest internally, even if the message does not lead with it.

If there is no trigger, there is no message. Say so.

## The keyword delivery

The most common DM in this pack and the easiest to ruin. They commented one word. They are expecting the thing. So:

```
{their name}, here it is: {the thing, or the link}.

{one line on how to use it}

{one question they can answer in four words}
```

Send the thing **first**, in message one, with no gate. A keyword post that delivers a "before I send it, can I ask what you do?" is a bait and switch and it is remembered. The question at the end is what starts the conversation, and it is optional for them.

Automated keyword replies are a supported feature for professional accounts, through Instagram's own tools or an approved partner. Using that is fine. Sending unsolicited bulk DMs is not, and it is the fastest route to a restricted account.

## The first message to someone warm

- **Two to four sentences.** A screen of text is a delete.
- **Reference the specific thing.** The comment, the post, the reply. In their words.
- **Give before asking.** A number, a template, a name, an answer.
- **One ask, small.** "Worth a quick call?" beats "let me walk you through the platform".
- **No link and no calendar in message one.** It reads as a funnel because it is one.
- **No voice note to a stranger.** It is a great tool and it is for people who already know the person's voice.

## The collab pitch

Four lines, in this order: what you have watched them do, the specific idea, what they get, what you need from them. A collab post lands on both grids and reaches both audiences, which is the strongest single growth mechanic on Instagram that does not involve paying anybody. Pitch it as that and be concrete about who does what.

## Follow-ups

Two. That is the number.

- **+4 days**: add something new. Never "just bumping this". If there is nothing new, there is no follow-up.
- **+10 days**: the close-the-loop message. Say you will stop, and mean it. This one gets a surprising share of the total replies, because it removes the pressure.

Then stop. A third converts nobody and costs the relationship.

## Never

- Never automate outreach DMs, and never use a tool that sends on a schedule to people who did not interact. It violates Instagram's Terms of Use and restricts the account.
- Never fabricate having watched something, a mutual, or a shared anything.
- Never open with "Hey! Quick question" and then not ask a question.
- Never send the pitch in the same message as the compliment.

## Output

The message, the character count, and the two follow-ups with the day each goes out, all run through `ig-human`. Nothing is sent from here: the person approves each one and sends it the way the next section describes.

## With Uplika connected

This skill still only drafts. Uplika can send in some of these cases and not in others, and the difference is Meta's messaging rules:

- **Replying inside an open conversation.** Hand the approved draft to the `inbox` skill. It reads the conversation, checks the messaging window and sends after the person approves. Outside the window nothing can be sent until the other person writes again (`faq:dm-24h-window`).
- **Follow-ups.** When the other person has not answered, the follow-ups fall outside the messaging window, so Uplika refuses them. The person sends those by hand from the Instagram app.
- **Keyword delivery.** That is an automation, not a typed message: the `automations` skill sets up `template:comment_to_dm` for a keyword comment and `template:keyword_dm` for a keyword someone sends in a DM. Use the draft above as its message. Uplika cannot open a conversation with someone who only commented; the one automatic way in is a single private reply to that comment (`faq:private-reply-once`).
- **Non-followers.** A DM to someone who does not follow the account lands in their message requests, where Instagram refuses buttons, cards and files and Uplika sends the text alone (`faq:dm-non-follower-media`). Write the keyword delivery so the text alone does the job.
- **Warm approaches and collab pitches** start a conversation, so the person types them in the Instagram app.

## Without Uplika

The person sends every message by hand, or through their own approved automation for keyword replies only.

## Tools

None. This skill drafts; the `inbox` skill sends inside the messaging window and the `automations` skill sets up keyword delivery.
