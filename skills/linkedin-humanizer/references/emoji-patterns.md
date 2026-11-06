# Emoji Patterns: AI vs. Human

Pattern data from MagicPost LinkedIn analysis (Feb 2026, viral post with 220 engagement).

Source frequencies measured across a corpus of AI-generated vs. human-authored LinkedIn posts. The percentage column shows how often each emoji appears in AI-generated content.

## AI-correlated emojis (the "tells")

| Emoji | Name | AI Frequency | Why it's a tell | Human-pattern alternative |
|-------|------|--------------|-----------------|---------------------------|
| :bulb: | lightbulb | 2.57% | ChatGPT signature for "insight" / "tip", most diagnostic single emoji | :screwdriver: (screwdriver) for fix-it posts, :round_pushpin: (pin) for highlights, or remove |
| :rocket: | rocket | 3.28% | Highest-frequency AI emoji. Signals "launch" / "growth" in template fashion | :package: (box) for shipping, :airplane_departure: (takeoff) for travel, or remove |
| :sparkles: | sparkles | 3.11% | "Magic AI" / "transformation" cliché. Almost never appears in human ops content | Remove. No clean substitute |
| :recycle: | recycling | 2.93% | Used to flag re-shares and "lessons learned" loops. AI overuses for filler | :repeat: (repeat) only if literally about repetition, or remove |
| :dart: | target | 2.07% | "Goals" / "objectives" cliché | :pushpin: (pushpin) for specific items, or remove |
| :chart_with_upwards_trend: | chart_increasing | 1.89% | "Growth" / "metrics" template signal | Use a real number in plain text instead |
| :key: | key | 1.74% | "Key takeaway" / "key insight" template | Skip the emoji, write the takeaway in plain prose |
| :dart: | dart | 1.68% | Same family as target above, both flag templated structure | Same as target |
| :muscle: | muscle | 1.45% | "Strength" / "resilience" platitude | Remove or replace with concrete detail |
| :fire: | fire | 1.31% | Borderline, used in human content too, but flagged when clustered with others | Keep if standalone, swap to :hot_pepper: (chili) or :hot_face: (hot face) for variety |

## Cluster rules

- 1 AI-pattern emoji in isolation: usually fine
- 2 in one post: borderline, flag in `--strict` mode
- 3+ in one post: AI-likely, flag in all modes
- Same emoji 2+ times: repetition tell, flag in all modes

## Position rules

AI-generated posts tend to put emojis at:
- End of opening hook line (lightbulb, rocket, sparkles)
- Start of every bullet in a list (target, key, fire)
- End of CTA line (rocket, fire, muscle)

If the draft has emojis at all three positions, treat as AI-likely regardless of which emojis they are.

## Human-pattern emojis (sub-1% AI correlation)

These appear at much lower frequency in AI-generated content. Not "human-proof", just less of a tell:

| Emoji | Name | Notes |
|-------|------|-------|
| :coffee: | coffee | Concrete, mundane, AI rarely uses |
| :pizza: | pizza | Specific food, AI rarely uses |
| :package: | package | Shipping / ops, concrete |
| :screwdriver: | screwdriver | Fix-it posts, newer emoji, AI training lags |
| :hot_pepper: | chili | "Spicy take" replacement for fire |
| :round_pushpin: | round_pushpin | Specific location / item highlight |
| :airplane_departure: | airplane_departure | Travel / launch, more specific than rocket |
| :hot_face: | hot_face | Reaction emoji, less templated than fire |
| :window: | window | Newer emoji, AI training lags |
| :beverage_box: | beverage_box | Newer emoji, AI training lags |

## What this data does NOT prove

- It doesn't prove these emojis are "wrong", humans use :bulb: and :rocket: too
- It proves they appear 2-3x more often in AI-generated content than baseline
- A single AI-pattern emoji in a post is not a verdict, the cluster + repetition pattern is the tell
- New emojis released after model training cutoffs are mechanically less likely to appear in AI output, which is why the human-pattern list skews toward newer Unicode additions

## Update cadence

Frequencies should be re-measured quarterly as AI training data shifts. Last update: Feb 2026 (MagicPost).
