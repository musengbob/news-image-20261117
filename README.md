# THE WORLD TODAY — Tuesday 17 November 2026

A make.fun entry for **news-image-20261117**: one image summing up the
world's news of Tuesday 17 November 2026.

## The image

A dense broadsheet front page, 1024×1024:

- **Lead:** the Kerch Bridge road span collapses into the strait after
  Ukraine's overnight strike — the second attack in two days.
- **50 verified stories** across six continents: the Gulf exchange
  (US strikes on Qeshm Island, Iran's drone attacks on Bahrain and Kuwait),
  the Houthi advance on Aden, Trump's Manila Quad summit, ASEAN's close,
  COP31 in Antalya, the US losing measles elimination status, Nvidia's
  record $115.8bn quarter, OpenAI's GPT-6.2 launch, and the day's sport.
- **Day in figures** strip, **10 illustrated stories**, a **world map**
  with 16 numbered markers, a **markets strip** and a footer ticker.

Every headline was verified against same-day reporting (Reuters, AP,
Bloomberg, Al Jazeera, PAHO, WHO, ASEAN, SEC filings, USA Today,
NBC Sports). All photographs are illustrations generated for this page
and are captioned as such.

## Layout

- `compose.py` — builds `entry.png` from the illustrations in `assets/`
  (run: `python3 compose.py`).
- `main.ts` — the entrypoint: copies `entry.png` to the output directory
  (`MAKEFUN_OUTPUT_DIR`, default `/output`), with a 1 MiB gate guard and
  a post-copy size check.
- `assets/` — the hero illustration and ten thumbnails, all generated
  in-session for this entry.

## Check

```sh
python3 compose.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# out/entry.png is byte-identical to entry.png across runs
```

## License

MIT — see `LICENSE`.
