---
name: ig-reel
description: Write an Instagram Reel from one idea (scored hooks, spoken script, on-screen text, timed beat sheet), then publish or schedule it after approval.
---

Adapted from Jakeschincariol/instagram-agent-skill (MIT). Not affiliated with the original author.

# ig-reel

Turns one raw idea into a Reel that somebody finishes. Use it whenever the person wants a Reel, a short-form video script, a hook or a voiceover ("make a reel about X", "what should I say in this video"), or is about to record and does not have the first line yet.

Two scripts live in this skill's `scripts/` folder and they both actually run. Use them. Do not eyeball the hook and do not guess at the length. Run them from this skill's folder:

```bash
python3 scripts/hookscore.py hooks.txt              # rank your hook options
python3 scripts/hookscore.py --hook "one line"      # score a single one
python3 scripts/beats.py script.txt --target 30     # timed beat sheet before you shoot
```

Both count English words. On Korean or other non-Latin text they see almost nothing (a Korean hook gets scored on its digits alone), so the score and the timings mean nothing there: say so, skip the numbers, and time the script by having the person read it out loud. An agent without a terminal cannot run them either; apply the rules below by reading and say that no score was computed.

## Before you write

1. Read the voice file `~/.uplika/<workspace-slug>/voice.md` if it exists: how the person talks on camera, what they never say, who they are talking to. If it does not exist, ask three questions (tone, how they end a line, words they avoid), or ask for three of their own reels and infer the voice from them, then offer to save it with the `voice-profile` skill. A script in the wrong voice is unusable, because they have to say it out loud.
2. Read `scripts/hooks.json`: 26 formulas, each with a template, a filled example, the on-screen version, what it is for, and how it gets ruined. Four of them are in there because they kept turning up in real hooks, not because they completed a pattern. The `hooks` skill lists the same formulas next to other platforms' formulas and Korean patterns, when the person wants a wider menu.
3. If the idea is thin, do not pad it. Ask one batched question: what happened, to whom, and what did it cost or return. A Reel needs one specific true thing. Get it before writing.
4. If the person has a swipe file from `ig-viral`, ask where it is and read it. It is their own evidence about which formulas are working in their niche right now, and it beats the defaults in this file.

## The shape

A Reel is decided in the first two seconds and kept by the next five.

```
0:00 - 0:02   HOOK        the claim. Spoken line and on-screen line, written
                          separately. Motion in the first frame, not a static face.
0:02 - 0:07   THE STAKE   why this matters to the person watching. One line.
0:07 - ...    THE BODY    one idea per beat, and the frame changes every beat.
LAST 3s       THE PAYOFF  deliver what the hook promised, then the single ask.
LAST LINE     THE LOOP    echo one word from the hook so the replay lands clean.
```

Length: 15 to 45 seconds is the working range. The longest a Reel may run is in `list_platforms`, and almost nobody should go near it. Under 7 seconds the loop counts inflate and nothing else does.

## The loop

**1. Pick three hooks, not one.** Run the idea through `scripts/hooks.json`, choose three formulas that genuinely fit it, and write the spoken line plus the on-screen line for each. Different formulas, not three rewrites of one.

**2. Score them.** Put the three spoken lines in a file, one per line, and run `scripts/hookscore.py`. Show the person the ranking. If the top one is under 50, you do not have the hook yet and no amount of editing fixes that.

**3. Write the script** on the winning hook. Plain spoken language, the way the person actually talks. Contractions. Short lines. No sentence they would have to rehearse.

**4. Time it.** Run `scripts/beats.py script.txt --target {length}`, with `--wpm` from the voice file if the person has timed themselves reading. Fix every flag it prints: a hook that runs too long, a beat long enough to lose people, a run of beats with nothing concrete in them, no loop. Re-run until it is clean.

**5. Humanize it.** Run the script through `ig-human` before showing it. A written-sounding line is obvious the moment someone says it out loud.

**6. Print the block.** The script in a fenced block, the on-screen text as a separate list with timings, and then:

```
REEL READY
hook:       #3 Nobody Tells You, scored 86 STRONG
length:     28.4s across 9 beats at 165 wpm
on-screen:  6 cards
humanizer:  4 artefacts stripped, human score 81 PASS
caption:    write it with ig-caption next

Reply "yes" to keep it, or tell me what to change.
```

**7. The person shoots it.** This skill produces a script. Publishing the finished video is the Uplika section below, and only after the person approves.

## On-screen text is a separate script

Write it separately, every time. It is read before it is heard.

- **Six words or fewer per card.** It is being read at arm's length by someone who is not listening yet.
- **The hook card is up at frame 1**, not after a beat of silence.
- **Keep it inside the middle of the frame.** The top band holds the profile row, the bottom band holds the caption and the audio strip, and the action rail runs down the right edge. Anything under them is covered.
- **Never put the hook where the caption sits.** That is the bottom of the frame and it is covered.
- **Burn in captions for the body.** Most people watch muted first.

## Rules that make the difference

- **One idea per Reel.** If the script has two, you have two Reels. Say so.
- **Numbers over adjectives.** "$4,200" beats "a lot". If the person has not given a number, ask for one rather than writing around the hole.
- **Cut the intro.** No greeting, no "in this video", no name, no logo sting. The video starts at the sentence you would normally reach at second six.
- **Change the frame every beat.** A static shot for 8 seconds is where people leave, and `scripts/beats.py` will flag it.
- **One ask at the end.** Comment a keyword, save it, or follow. One.
- **Never fabricate.** No invented metrics, clients, revenue or outcomes under the person's name, even as a placeholder. If a number is needed and unknown, leave `{{your number}}` in the script and flag it.
- **Do not write a script around a trending audio the person cannot use.** If the idea needs the person's own voice, say so. With Uplika connected, check `search_instagram_audio` first: only audio in this account's results can go on the reel.

## Example

```
/ig-reel we cut proposal time from 5 hours to 20 minutes with one template
```

```
HOOKS  (scored)
  86  STRONG  #5  Time Collapse   "Proposals used to take me five hours. Twenty minutes now."
                                  on screen: 5 HOURS -> 20 MIN
  71  STRONG  #1  Cost Confession "I billed four hours a week for formatting. For two years."
                                  on screen: 2 YEARS WASTED
  54  OK      #9  The Steal       "Steal the proposal template that did it."
                                  on screen: STEAL THIS

Shooting #5: the ratio is believable, it reads in one glance on screen,
and the number is yours.
```

## With Uplika connected

Once the person has the finished video, Uplika can publish or schedule it on their Instagram account.

1. **Account.** Call `select_channels` with the Instagram account, or with no scope and let the person choose. Never assume Instagram is connected; if it is not, send the person to https://uplika.com/dashboard/connections. If the answer is `workspace_required`, show the workspaces it lists, ask which one, and pass that `workspaceId` on every later call.
2. **Rules.** Read Instagram in `list_platforms`: video size and length, the caption limit and how it counts characters, the option schema under `options`, and the features table. Instagram posts cannot be edited after they go out (the features table says so), so the caption and every option are approved before publishing, not after.
3. **Upload the video.** With a terminal: `media_presign` with the file name, type and size, PUT the bytes to the returned `uploadUrl` with curl (same content type), then `media_complete`. Without one: `media_from_url` for a file at a public https address, or `media_upload_link` for a file on the person's device (give them the link, then poll `media_upload_status` until it is ready). Pass `aiGenerated` when the footage was made with AI.
4. **Cover.** A chosen image goes in `options.instagram.coverMediaId` (upload it the same way; the option schema says which format it takes). Its media id goes only in that option, never in `mediaIds` (that would add the image to the post itself). Otherwise pick a frame with `options.instagram.thumbOffsetMs`. A cover with a few words of text keeps the grid readable (see `ig-profile`).
5. **Audio (optional).** If the person wants music or a sound under the reel, call `search_instagram_audio` with the Instagram `accountId` (and the `workspaceId` if you were given one). Without `query` it lists what is trending for this account: popular songs are only there, and the list differs per account (some accounts only get royalty-free music). With `query` it searches Meta's royalty-free Sound Collection only, so an artist or song name will not find that song. `previewUrl` is a temporary audio file you can play; `listenUrl` opens the sound on Instagram. Put the chosen id in `options.instagram.audio` with both volumes, `{ "id": "...", "volume": 20, "videoVolume": 100 }` for a reel with a voice-over (both default to 100, which drowns speech). It works only for accounts connected via Facebook; otherwise the answer is `not_supported`, and the person reconnects through Facebook or publishes without audio. Instagram cannot preview the mix before it is published, and the audio plays once from its beginning (the start cannot be chosen) without repeating, so pick one at least as long as the reel: say so when you show the plan.
6. **Show and confirm.** Show the person everything that will go out: the account, the caption from `ig-caption`, the cover, the audio (title, artist and both volumes) if any, `options.instagram.contentType` set to `reel`, `options.instagram.shareToFeed` (false keeps the reel out of the main feed), any `options.instagram.collaborators` (they appear only after they accept), any `options.instagram.firstComment`, and the time. Publish only after they approve.
7. **Publish.** Call `publish` with the `accountIds` from `select_channels`, `content` (the caption), `mediaIds`, the options, and `wait: true`. For a later time pass `scheduledAt` with a time zone offset; ask which time zone the person means instead of guessing.
8. **Report.** Call `get_post` with the returned id and give the person the status and the permalink. A wait that runs out is not a failure: the reel is usually still processing, so check `get_post` again instead of publishing twice. If the target failed, call `get_help` with its code and pass on the answer and its url. `instagram_audio_unavailable` means Instagram did not take that audio for this account: search again and publish with another id (retrying the same post would send the same audio). A published reel whose warning says the music may be missing went up, but Instagram lists its sound as the video's original audio: ask the person to listen in the app before posting it again. `reconsent_required`, `feature_in_review` and `account_disconnected` go to the `troubleshoot` skill.

If the reel asks for a keyword comment ("Comment CONTRACT"), the delivery is an automation: set it up with the `automations` skill (`template:comment_to_dm`), using the same keyword. For a scheduled reel, attach the automation after the reel goes out, with the published post's id.

## Without Uplika

Everything before the Uplika section works with nothing connected: the scripts run locally on text and nothing is uploaded. Print the script, the on-screen list and the receipt. The person shoots the Reel and posts it from the Instagram app.

## Tools

- `select_channels`: pick the Instagram account; returns the accountIds and limits
- `list_platforms`: reel and caption rules, the option schema, the features table
- `media_presign`: upload slot when you can PUT the video yourself
- `media_complete`: confirm that upload
- `media_from_url`: attach a video or cover image from a public https address
- `media_upload_link`: let the person upload from their own device
- `media_upload_status`: wait until that upload is ready
- `search_instagram_audio`: music or sounds this Instagram account can put on a reel (accounts connected via Facebook)
- `publish`: publish or schedule the reel, only after the person approves
- `get_post`: final status and permalink
- `get_help`: the answer for an error code
