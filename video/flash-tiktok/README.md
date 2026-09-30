# FLASH 15s TikTok promo (1080x1920, 30fps)

Two cuts: `FLASH_tiktok_anim.mp4` (fully animated night-ride, `anim.html`) and `FLASH_tiktok.mp4` (product-photo slideshow, `scene.html`).

- `scene.html` – the animation; `render(t)` draws frame at time t. Shot list and copy live at the top of the script.
- `music.py` – synthesizes the original 120 BPM track (`music.wav`), no licensed samples.
- `anim.html` – animated cut drawn on a canvas: lightning intro, 0→75 MPH counter, beat-synced colour swaps, feature slams, end card.
- `cutout.py` – cuts the bikes out of the studio photos into `cut/` and derives same-pose gray/black/white variants.
- `render.py` – `python3 render.py OUT.mp4 [page.html] [audio.wav]`; renders frames with Chromium and muxes to MP4 with ffmpeg.
- `fetch_images.sh` – pulls product photos from Shopify into `img/` (missing photos render as placeholders).

```sh
npm install                       # fonts (Anton, Inter via @fontsource)
pip install playwright imageio-ffmpeg numpy
./fetch_images.sh
pip install scipy && python3 cutout.py
python3 music.py && python3 render.py FLASH_tiktok_anim.mp4 anim.html
```
