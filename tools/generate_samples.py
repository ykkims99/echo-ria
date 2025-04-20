import os
import cv2
import numpy as np
import random
from pathlib import Path
from PIL import Image, ImageDraw

def load_images_from_folder(folder, limit=None):
    images = []
    paths = list(Path(folder).glob("*.jpg"))
    for i, path in enumerate(paths):
        if limit and i >= limit:
            break
        img = cv2.imread(str(path))
        if img is not None:
            images.append((img, str(path.name)))
    return images

def add_freckle(image, position=None, radius=3):
    h, w, _ = image.shape
    if position is None:
        position = (random.randint(50, w - 50), random.randint(50, h - 50))
    color = (random.randint(30, 80), random.randint(20, 50), random.randint(20, 50))
    cv2.circle(image, position, radius, color, -1)
    return image, position

def generate_mask(image_shape, position, radius=3):
    mask = np.zeros(image_shape[:2], dtype=np.uint8)
    cv2.circle(mask, position, radius, 255, -1)
    return mask

def save_sample(image, filename, out_dir):
    cv2.imwrite(str(Path(out_dir) / filename), image)

def create_samples(raw_dir, out_aug, out_clean, out_mask, label_file, limit=10):
    os.makedirs(out_aug, exist_ok=True)
    os.makedirs(out_clean, exist_ok=True)
    os.makedirs(out_mask, exist_ok=True)

    images = load_images_from_folder(raw_dir, limit)
    with open(label_file, "w") as f:
        f.write("id,filename,transformation,position,size,class,cleaned_path,mask_path\n")
        for i, (img, name) in enumerate(images):
            sample_id = f"{i+1:05d}"
            aug_img = img.copy()
            aug_img, pos = add_freckle(aug_img)
            mask = generate_mask(aug_img.shape, pos)

            aug_name = f"{sample_id}_aug.jpg"
            clean_name = f"{sample_id}_cleaned.jpg"
            mask_name = f"{sample_id}_mask.png"

            save_sample(aug_img, aug_name, out_aug)
            save_sample(img, clean_name, out_clean)
            cv2.imwrite(str(Path(out_mask) / mask_name), mask)

            f.write(f"{sample_id},{name},freckle,{pos},small,synthetic,{clean_name},{mask_name}\n")
