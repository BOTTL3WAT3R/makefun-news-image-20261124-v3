# makefun-news-image-20261124-v3

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/BOTTL3WAT3R/makefun-news-image-20261124-v3/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/BOTTL3WAT3R/makefun-news-image-20261124-v3/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One image that sums up the world's news of Tuesday 24 November 2026, drawn as a one-page newspaper poster. The program copies the committed poster (`poster.png`, drawn at build time by `tools/make_poster.py`) to `/output/entry.png`, byte for byte, on every run.

## The poster

Under a masthead dated **Tuesday 24 November 2026**, the poster carries the day's six stories:

1. **Nvidia leaps 31%** — Jensen Huang reinstated as CEO.
2. **Ukrainian sea drones sink Russian corvette Merkury** — off Benghazi, Libya.
3. **COP31 talks collapse without a deal.**
4. **Factory fire kills 24 in Banten, Indonesia.**
5. **Mexico captures 'Chapo Isidro'.**
6. **US Democrats win biggest House majority since 1992.**

`python3 main.py --check` validates the poster against the bounty gate (PNG, at most 1 MiB and 1024×1024, every chunk CRC correct) without writing an entry.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=beyt0vmy&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
