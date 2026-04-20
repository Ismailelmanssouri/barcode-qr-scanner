# scanner.py — detects QR codes AND barcodes

import cv2
import numpy as np
import matplotlib.pyplot as plt
from pyzbar import pyzbar

def scan_codes(image_path):

    # ── 1. Load image ──────────────────────────────────────────
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Image not found: {image_path}")
        return

    print(f"✅ Image loaded: {image_path}")
    print(f"📐 Size: {image.shape[1]}x{image.shape[0]} px\n")

    # ── 2. Try multiple preprocessing methods ──────────────────
    # Method 1: simple grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Method 2: increase contrast (helps with barcodes)
    clahe     = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    enhanced  = clahe.apply(gray)

    # Method 3: sharpen the image
    kernel    = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
    sharpened = cv2.filter2D(gray, -1, kernel)

    # ── 3. Try decoding with all methods ───────────────────────
    codes = pyzbar.decode(gray)

    if not codes:
        print("🔄 Trying enhanced contrast...")
        codes = pyzbar.decode(enhanced)

    if not codes:
        print("🔄 Trying sharpened image...")
        codes = pyzbar.decode(sharpened)

    if not codes:
        print("🔄 Trying with threshold...")
        _, thresh = cv2.threshold(
            gray, 0, 255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        codes = pyzbar.decode(thresh)

    # ── 4. Check results ───────────────────────────────────────
    if not codes:
        print("⚠️  No QR codes or barcodes found.")
        print("💡 Tips:")
        print("   - Make sure the image is clear and not blurry")
        print("   - Try a higher resolution image")
        print("   - Make sure the barcode is fully visible")
        return

    print(f"🎯 Found {len(codes)} code(s):\n")

    # ── 5. Color per code type ─────────────────────────────────
    type_colors = {
        "QRCODE"  : (0,   255, 0),    # green
        "EAN13"   : (0,   0,   255),  # red
        "EAN8"    : (255, 0,   0),    # blue
        "CODE128" : (0,   255, 255),  # yellow
        "CODE39"  : (255, 0,   255),  # magenta
        "UPCA"    : (255, 165, 0),    # orange
        "UPCE"    : (128, 0,   128),  # purple
    }
    default_color = (0, 200, 200)

    # ── 6. Process each code ───────────────────────────────────
    for i, code in enumerate(codes):
        data    = code.data.decode("utf-8")
        c_type  = code.type
        rect    = code.rect
        polygon = code.polygon
        color   = type_colors.get(c_type, default_color)

        print(f"  Code #{i+1}")
        print(f"  Type    : {c_type}")
        print(f"  Data    : {data}")
        print(f"  Position: x={rect.left}, y={rect.top}")
        print(f"  Size    : {rect.width}x{rect.height} px")
        print()

        # Draw polygon
        if polygon:
            pts = np.array(
                [[p.x, p.y] for p in polygon],
                dtype=np.int32
            )
            cv2.polylines(image, [pts], True, color, 3)
            overlay = image.copy()
            cv2.fillPoly(overlay, [pts], color)
            cv2.addWeighted(overlay, 0.15, image, 0.85, 0, image)
        else:
            # fallback to bounding box if no polygon
            x, y, w, h = rect.left, rect.top, rect.width, rect.height
            cv2.rectangle(image, (x,y), (x+w,y+h), color, 3)

        # Bounding box
        x, y, w, h = rect.left, rect.top, rect.width, rect.height
        cv2.rectangle(image, (x,y), (x+w,y+h), color, 2)

        # Label with background
        label = f"#{i+1} {c_type}: {data[:25]}"
        (lw, lh), _ = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
        )
        cv2.rectangle(
            image,
            (x, y - lh - 14),
            (x + lw + 6, y),
            color, -1
        )
        cv2.putText(
            image, label, (x+3, y-8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6, (255,255,255), 2
        )

    # ── 7. Display results ─────────────────────────────────────
    result_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(12, 8))
    plt.imshow(result_rgb)
    plt.title(
        f"Found {len(codes)} code(s) — "
        f"Types: {', '.join(set(c.type for c in codes))}",
        fontsize=14
    )
    plt.axis("off")
    plt.tight_layout()
    plt.show()

    # ── 8. Save output ─────────────────────────────────────────
    import os, csv, datetime
    os.makedirs("outputs", exist_ok=True)
    cv2.imwrite("outputs/result.png", image)
    print(f"💾 Image saved: outputs/result.png")

    # Save to CSV
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("outputs/results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id","type","data","x","y","width","height","timestamp"])
        for i, code in enumerate(codes):
            writer.writerow([
                i+1,
                code.type,
                code.data.decode("utf-8"),
                code.rect.left,
                code.rect.top,
                code.rect.width,
                code.rect.height,
                timestamp
            ])
    print(f"📊 CSV saved  : outputs/results.csv")

    return codes


# ── Run ────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys

    # You can pass image path as argument or use default
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = "images/test_qr.png"

    scan_codes(path)