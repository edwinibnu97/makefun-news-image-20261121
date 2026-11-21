# makefun-news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/edwinibnu97/makefun-news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/edwinibnu97/makefun-news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

Sum up 21 November's world news in one image
([news-image-20261121](https://make.fun/bounty/news-image-20261121)): a
front-page style PNG of Saturday 21 November 2026 — Russian missiles hit
Poland, the World Court rules Myanmar committed genocide against the Rohingya,
the UK and EU strike a landmark post-Brexit deal, Wall Street slumps into
correction, a 6.8 quake shakes Peru, plus the Shenzhen trilateral summit,
COP31 in overtime, and more. The image is rendered by `generate.py`
(Pillow, no network, deterministic) and copied to `/output/entry.png` by
`main.ts`.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

To re-render the image from scratch (needs Pillow):

```sh
python3 generate.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=q17yfxs8&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
