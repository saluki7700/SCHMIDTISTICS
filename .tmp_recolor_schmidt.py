import numpy as np
from PIL import Image

SRC_BG = np.array([235, 237, 226], dtype=np.float64)   # archive sage-green (#EBEDE2)
DST_BG = np.array([237, 230, 214], dtype=np.float64)   # public-site paper (#EDE6D6)

path = "images/schmidt-line-pedigree.png"
im = Image.open(path).convert("RGB")
arr = np.array(im, dtype=np.float64)

dist = np.sqrt(((arr - SRC_BG) ** 2).sum(axis=2))

# hard replace near-exact background
hard_mask = dist < 3
# blend anti-aliased edges, linear falloff over distance 3-40
blend_mask = (dist >= 3) & (dist < 40)
weight = np.clip(1.0 - (dist - 3) / (40 - 3), 0, 1)  # 1 at dist=3, 0 at dist=40

out = arr.copy()
out[hard_mask] = DST_BG

w = weight[blend_mask][:, None]
out[blend_mask] = arr[blend_mask] * (1 - w) + DST_BG * w

out_img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), mode="RGB")
out_img.save(path)

# verify
check = Image.open(path).convert("RGB")
print("corner pixel after:", check.getpixel((5, 5)))
print("size:", check.size)
print("hard-replaced pixels:", int(hard_mask.sum()), "blended pixels:", int(blend_mask.sum()))
