# scanner.pyDetect, Localize and Decode QR codes & Barcodes

import cv2
import numpy as np
import matplotlib.pyplot as plt
from pyzbar import pyzbar

def scan_codes(image_path):
    """
    Main scanning function:
    - Loads image
    - Detects & decodes all QR codes and barcodes
    - Draws bounding boxes and polygons
    - Displays results
    """

    # ── 1. Load the image ──────────────────────────────────────
    image = cv2.imread(image_path)

    if image is None:
        print("❌ Image not found! Check the path.")
        return

    print(f"✅ Image loaded: {image_path}")
    print(f"📐 Size: {image.shape[1]}x{image.shape[0]} px\n")

    # ── 2. Convert to grayscale ────────────────────────────────
    # pyzbar works better on grayscale images
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # ── 3. Decode all codes in the image ──────────────────────
    codes = pyzbar.decode(gray)

    # ── 4. Check if anything was found ────────────────────────
    if not codes:
        print("⚠️  No QR codes or barcodes found in this image.")
        return

    print(f"🎯 Found {len(codes)} code(s):\n")

    # ── 5. Loop through each detected code ────────────────────
    for i, code in enumerate(codes):

        # ── 5a. Decode the data ────────────────────────────────
        data    = code.data.decode("utf-8")   # bytes → string
        c_type  = code.type                   # "QRCODE" or "EAN13" etc.
        rect    = code.rect                   # bounding rectangle
        polygon = code.polygon                # exact corner points

        print(f"  Code #{i+1}")
        print(f"  Type : {c_type}")
        print(f"  Data : {data}")
        print(f"  Rect : x={rect.left}, y={rect.top}, "
              f"w={rect.width}, h={rect.height}")
        print()

        # ── 5b. Draw the polygon (quadrilateral) ───────────────
        # Convert polygon points to numpy array
        pts = np.array([[p.x, p.y] for p in polygon], dtype=np.int32)
        cv2.polylines(
            image,
            [pts],
            isClosed=True,
            color=(0, 255, 0),      # green
            thickness=3
        )

        # ── 5c. Draw the bounding box ──────────────────────────
        x, y, w, h = rect.left, rect.top, rect.width, rect.height
        cv2.rectangle(
            image,
            (x, y),
            (x + w, y + h),
            color=(0, 0, 255),      # red
            thickness=2
        )

        # ── 5d. Put label above the code ──────────────────────
        label = f"{c_type}: {data[:30]}"   # limit to 30 chars
        cv2.putText(
            image,
            label,
            (x, y - 10),            # position above box
            cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=0.6,
            color=(255, 0, 0),      # blue
            thickness=2
        )

    # ── 6. Display the result ──────────────────────────────────
    result_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    plt.figure(figsize=(10, 8))
    plt.imshow(result_rgb)
    plt.title(f"Detected {len(codes)} code(s)", fontsize=14)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

    # ── 7. Save the result image ───────────────────────────────
    output_path = "outputs/result.png"
    cv2.imwrite(output_path, image)
    print(f"💾 Result saved to: {output_path}")

    return codes


# ── Run the scanner ────────────────────────────────────────────
if __name__ == "__main__":
    scan_codes("images/test_qr.png")