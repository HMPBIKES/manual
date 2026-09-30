"""Cut FLASH bikes out of the white studio photos -> cut/*.png (transparent)."""
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd
SRCS = {'gray_side': 'Flashgray_03', 'black_side': 'Flashblack_02', 'gray_34': 'Flashgray_02', 'black_34': 'Flashblack_04'}
for k, f in SRCS.items():
    im = np.asarray(Image.open(f'img/{f}.webp').convert('RGB')).astype(int)
    mx, mn, lum = im.max(2), im.min(2), im.mean(2)
    H = im.shape[0]
    white = (mn >= 228) & (mx - mn < 12)
    lab, n = nd.label(white)
    border = set(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]])) - {0}
    sizes = nd.sum(white, lab, range(1, n + 1))
    cy = np.array(nd.center_of_mass(white, lab, range(1, n + 1)))[:, 0] if n else []
    drop = [i + 1 for i in range(n) if (i + 1) in border or
            (sizes[i] > 150 and cy[i] > 0.62 * H)]  # enclosed backdrop holes
    fg = ~np.isin(lab, drop)
    # floor shadow: light unsaturated pixels near the tyre contact line
    dark = (lum < 70) & fg; ground = np.where(dark.sum(1) > 3)[0].max()
    band = np.zeros_like(fg); band[ground - 170:] = True
    fg &= ~(band & (lum > 198) & (mx - mn < 18))
    fg = nd.binary_opening(fg, iterations=2)
    lab2, n2 = nd.label(fg); s2 = nd.sum(fg, lab2, range(1, n2 + 1))
    fg = np.isin(lab2, 1 + np.where(s2 > 3000)[0])
    a = np.asarray(Image.fromarray((fg * 255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.0))).astype(float)
    top = np.zeros_like(fg); top[:int(H * 0.45)] = True
    a = np.where(top & (lum > 225), a * 0.35, a)          # windscreen reads as glass
    out = Image.fromarray(im.astype('uint8')).convert('RGBA'); out.putalpha(Image.fromarray(a.astype('uint8')))
    out.crop(out.getbbox()).save(f'cut/{k}.png')
    print(k)

# Same-pose colour variants from the gray side shot, so beat-synced colour swaps don't jump.
g = np.asarray(Image.open('cut/gray_side.png')).astype(float)
rgb, alpha = g[..., :3], g[..., 3:]
lum = rgb.mean(2, keepdims=True); sat = rgb.max(2, keepdims=True) - rgb.min(2, keepdims=True)
panel = np.clip((lum - 105) / 30, 0, 1) * np.clip((lum - 238) / -20, 0, 1) * (sat < 22)   # gray bodywork only
for name, f in {'white_swap': lambda l: np.clip(118 + l * 0.78, 0, 250), 'black_swap': lambda l: l * 0.22 + 8,
                'gray_swap': lambda l: l}.items():
    out = rgb * (1 - panel) + f(lum) * panel
    Image.fromarray(np.concatenate([out, alpha], 2).clip(0, 255).astype('uint8')).save(f'cut/{name}.png')
