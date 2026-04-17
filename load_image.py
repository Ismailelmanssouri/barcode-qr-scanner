# load_image.py
# Step 2: Learn how OpenCV loads and displays images

import cv2
import numpy as np
import matplotlib.pyplot as plt

# ── 1. Load the image ──────────────────────────────────────────
image = cv2.imread("images/test_qr.png")

# ── 2. Check if image loaded correctly ─────────────────────────
if image is None:
    print("❌ Image not found! Check the path.")
else:
    print("✅ Image loaded successfully!")

    # ── 3. Print basic info ────────────────────────────────────
    print(f"📐 Shape  : {image.shape}")        # (height, width, channels)
    print(f"📏 Height : {image.shape[0]} px")
    print(f"📏 Width  : {image.shape[1]} px")
    print(f"🎨 Channels: {image.shape[2]}")    # 3 = BGR
    print(f"🔢 Data type: {image.dtype}")      # uint8 = values 0-255

    # ── 4. Convert BGR → RGB for correct colors in Matplotlib ──
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # ── 5. Convert to Grayscale ────────────────────────────────
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # ── 6. Display all 3 versions ──────────────────────────────
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    axes[0].set_title("Original (BGR→RGB)")
    axes[0].axis("off")

    axes[1].imshow(image_rgb)
    axes[1].set_title("Correct Colors (RGB)")
    axes[1].axis("off")

    axes[2].imshow(image_gray, cmap="gray")
    axes[2].set_title("Grayscale")
    axes[2].axis("off")

    plt.suptitle("Step 2: Image Loading with OpenCV", fontsize=14)
    plt.tight_layout()
    plt.show()

    # ── 7. Peek at raw pixel values ────────────────────────────
    print(f"\n🔍 Top-left 3x3 pixel values (BGR):")
    print(image[0:3, 0:3])