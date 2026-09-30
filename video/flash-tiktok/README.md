# FLASH 15s TikTok promo (1080x1920, 30fps)

- `scene.html` – the animation; `render(t)` draws frame at time t. Shot list and copy live at the top of the script.
- `music.py` – synthesizes the original 120 BPM track (`music.wav`), no licensed samples.
- `render.py` – renders frames with Chromium and muxes to MP4 with ffmpeg.
- `fetch_images.sh` – pulls product photos from Shopify into `img/` (missing photos render as placeholders).

```sh
npm install                       # fonts (Anton, Inter via @fontsource)
pip install playwright imageio-ffmpeg numpy
./fetch_images.sh
python3 music.py && python3 render.py FLASH_tiktok.mp4
```
