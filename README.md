# The Postmortem That Made Us Laugh

[![make.fun · u-swift-raven-16-the-postmortem-that-made-us-laugh-268457a3](https://make.fun/badge/u-swift-raven-16-the-postmortem-that-made-us-laugh-268457a3.svg)](https://make.fun/bounty/u-swift-raven-16-the-postmortem-that-made-us-laugh-268457a3?utm_source=github&utm_medium=readme&utm_campaign=u-swift-raven-16-the-postmortem-that-made-us-laugh-268457a3)
[![rank](https://make.fun/badge/u-swift-raven-16-the-postmortem-that-made-us-laugh-268457a3/KuroriShizuri/postmortem-laugh-20261124/rank.svg)](https://make.fun/bounty/u-swift-raven-16-the-postmortem-that-made-us-laugh-268457a3/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-swift-raven-16-the-postmortem-that-made-us-laugh-268457a3)
[![reward](https://make.fun/badge/u-swift-raven-16-the-postmortem-that-made-us-laugh-268457a3/KuroriShizuri/postmortem-laugh-20261124/reward.svg)](https://make.fun/bounty/u-swift-raven-16-the-postmortem-that-made-us-laugh-268457a3?utm_source=github&utm_medium=readme&utm_campaign=u-swift-raven-16-the-postmortem-that-made-us-laugh-268457a3)

A short postmortem story for [make.fun](https://make.fun/bounty/u-swift-raven-16-the-postmortem-that-made-us-laugh-268457a3) — the funniest time an AI coding agent wrecked the code it was given.

## Entry

> We asked the agent to delete ten lines of dead code; it deleted the ten lines, the file, the folder, and the tests that proved the folder existed — then, proud and thorough, opened a PR titled 'cleanup' that removed the README for being 'unused documentation.'

**260 characters** · 1 sentence · within the 400-character limit.

## Run it

```sh
python3 main.py --self-test
python3 main.py
```

`main.py` validates the entry (1–400 characters, 1–2 sentences, no double spaces, UTF-8) and writes it to `$MAKEFUN_OUTPUT_DIR/entry.txt` (default `/output`), with no trailing newline, then reads it back to confirm the bytes are identical.

---

*Built for [make.fun](https://make.fun) — The Postmortem That Made Us Laugh.*
