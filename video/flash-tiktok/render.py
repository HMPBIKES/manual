"""Render scene.html frame-by-frame at 30fps and mux with music.wav -> FLASH_tiktok.mp4"""
import json, os, re, subprocess, sys, shutil, imageio_ffmpeg
from playwright.sync_api import sync_playwright
FPS, DUR = 30, 15.0
here = os.path.dirname(os.path.abspath(__file__))
html = open(os.path.join(here, 'scene.html')).read()
srcs = dict(re.findall(r"(\w+):\{src:'([^']+)'", html))
avail = {k: os.path.exists(os.path.join(here, v)) for k, v in srcs.items()}
print('images available:', sum(avail.values()), '/', len(avail))
out = sys.argv[1] if len(sys.argv) > 1 else 'FLASH_tiktok.mp4'
frames = os.path.join(here, 'frames'); shutil.rmtree(frames, ignore_errors=True); os.makedirs(frames)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--allow-file-access-from-files'])
    pg = b.new_page(viewport={'width': 1080, 'height': 1920})
    pg.add_init_script(f"window.AVAILABLE = {json.dumps(avail)};")
    pg.goto('file://' + os.path.join(here, 'scene.html'))
    pg.evaluate("document.fonts.ready"); pg.wait_for_load_state('networkidle')
    pg.evaluate("Promise.all([...document.images].map(i=>i.decode().catch(()=>{})))")
    for i in range(int(FPS * DUR)):
        pg.evaluate(f"render({i / FPS})")
        pg.screenshot(path=f"{frames}/{i:04d}.jpg", type='jpeg', quality=95)
    b.close()
ff = imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([ff, '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', f'{frames}/%04d.jpg',
                '-i', os.path.join(here, 'music.wav'), '-c:v', 'libx264', '-preset', 'slow', '-crf', '18',
                '-pix_fmt', 'yuv420p', '-profile:v', 'high', '-c:a', 'aac', '-b:a', '192k',
                '-movflags', '+faststart', '-shortest', os.path.join(here, out)], check=True)
print('wrote', out)
