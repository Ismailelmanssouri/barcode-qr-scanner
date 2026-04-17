# multi_scanner.py
# Step 4: Detect multiple codes + save results to file

import cv2
import numpy as np
import matplotlib.pyplot as plt
from pyzbar import pyzbar
import csv
import datetime
import os

def scan_and_save(image_path):
    """
    Enhanced scanner:
    - Detects ALL codes in an image
    - Draws unique color per code
    - Saves results to TXT and CSV
    """

    # ── 1. Load image ──────────────────────────────────────────
    image = cv2.imread(image_path)
    if image is None:
        print("❌ Image not found!")
        return

    print(f"✅ Image loaded: {image_path}")
    print(f"📐 Size: {image.shape[1]}x{image.shape[0]} px\n")

    # ── 2. Grayscale for better detection ─────────────────────
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # ── 3. Decode all codes ────────────────────────────────────
    codes = pyzbar.decode(gray)

    if not codes:
        print("⚠️  No codes found.")
        return

    print(f"🎯 Found {len(codes)} code(s):\n")

    # ── 4. Color palette for multiple codes ───────────────────
    # Each code gets a different color
    colors = [
        (0,   255, 0),    # green
        (0,   0,   255),  # red
        (255, 0,   0),    # blue
        (0,   255, 255),  # yellow
        (255, 0,   255),  # magenta
        (255, 165, 0),    # orange
    ]

    # ── 5. Prepare results storage ─────────────────────────────
    results = []
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ── 6. Process each code ───────────────────────────────────
    for i, code in enumerate(codes):

        # Extract info
        data    = code.data.decode("utf-8")
        c_type  = code.type
        rect    = code.rect
        polygon = code.polygon

        # Pick color for this code
        color = colors[i % len(colors)]

        print(f"  Code #{i+1}")
        print(f"  Type    : {c_type}")
        print(f"  Data    : {data}")
        print(f"  Position: x={rect.left}, y={rect.top}")
        print(f"  Size    : {rect.width}x{rect.height} px")
        print()

        # ── Draw polygon ───────────────────────────────────────
        pts = np.array([[p.x, p.y] for p in polygon], dtype=np.int32)
        cv2.polylines(image, [pts], isClosed=True, color=color, thickness=3)

        # ── Fill polygon with transparent color ────────────────
        overlay = image.copy()
        cv2.fillPoly(overlay, [pts], color)
        cv2.addWeighted(overlay, 0.15, image, 0.85, 0, image)

        # ── Draw bounding box ──────────────────────────────────
        x, y, w, h = rect.left, rect.top, rect.width, rect.height
        cv2.rectangle(image, (x, y), (x+w, y+h), color, 2)

        # ── Draw label background ──────────────────────────────
        label     = f"#{i+1} {c_type}: {data[:25]}"
        (lw, lh), _ = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
        )
        cv2.rectangle(
            image,
            (x, y - lh - 14),
            (x + lw + 6, y),
            color,
            thickness=-1        # filled rectangle
        )

        # ── Draw label text ────────────────────────────────────
        cv2.putText(
            image, label,
            (x + 3, y - 8),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6, (255, 255, 255),   # white text
            thickness=2
        )

        # ── Store result ───────────────────────────────────────
        results.append({
            "id"       : i + 1,
            "type"     : c_type,
            "data"     : data,
            "x"        : rect.left,
            "y"        : rect.top,
            "width"    : rect.width,
            "height"   : rect.height,
            "timestamp": timestamp
        })

    # ── 7. Display result ──────────────────────────────────────
    result_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(12, 8))
    plt.imshow(result_rgb)
    plt.title(f"Found {len(codes)} code(s) — Step 4", fontsize=14)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

    # ── 8. Save result image ───────────────────────────────────
    os.makedirs("outputs", exist_ok=True)
    img_out = "outputs/multi_result.png"
    cv2.imwrite(img_out, image)
    print(f"💾 Result image saved : {img_out}")

    # ── 9. Save results to TXT ─────────────────────────────────
    txt_out = "outputs/results.txt"
    with open(txt_out, "w") as f:
        f.write(f"Scan Results — {timestamp}\n")
        f.write(f"Image: {image_path}\n")
        f.write(f"Total codes found: {len(results)}\n")
        f.write("=" * 40 + "\n\n")
        for r in results:
            f.write(f"Code #{r['id']}\n")
            f.write(f"  Type : {r['type']}\n")
            f.write(f"  Data : {r['data']}\n")
            f.write(f"  Position: ({r['x']}, {r['y']})\n")
            f.write(f"  Size    : {r['width']}x{r['height']} px\n\n")
    print(f"📄 TXT results saved  : {txt_out}")

    # ── 10. Save results to CSV ────────────────────────────────
    csv_out = "outputs/results.csv"
    with open(csv_out, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)
    print(f"📊 CSV results saved  : {csv_out}")

    return results


# ── Run ────────────────────────────────────────────────────────
if __name__ == "__main__":
    scan_and_save("images/test_qr.png")