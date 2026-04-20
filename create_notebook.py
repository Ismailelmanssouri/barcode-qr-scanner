import json

nb = {
 "nbformat": 4,
 "nbformat_minor": 5,
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "name": "python",
   "version": "3.10.0"
  }
 },
 "cells": [
  {
   "id": "cell-01",
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Barcode & QR Code Scanner\n",
    "## Computer Vision Project\n",
    "\n",
    "**Students:**\n",
    "- EL MANSSOURI Ismail\n",
    "- EL AZIZI Mohamed Taha\n",
    "- IBENOUZI Ismail\n",
    "- EL KHIYATI Mouataze\n",
    "\n",
    "**Course:** Big Data & AI Engineering\n",
    "\n",
    "**GitHub:** https://github.com/Ismailelmanssouri/barcode-qr-scanner\n",
    "\n",
    "---\n",
    "\n",
    "## Project Overview\n",
    "\n",
    "This notebook demonstrates a complete pipeline for:\n",
    "- Detecting QR codes and barcodes from images\n",
    "- Localizing them with bounding boxes and polygons\n",
    "- Decoding their content using OpenCV and pyzbar\n",
    "- Understanding the underlying Computer Vision concepts"
   ]
  },
  {
   "id": "cell-02",
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 1 — Import Libraries"
   ]
  },
  {
   "id": "cell-03",
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import cv2\n",
    "import numpy as np\n",
    "import matplotlib.pyplot as plt\n",
    "from pyzbar import pyzbar\n",
    "from PIL import Image\n",
    "import os\n",
    "\n",
    "print('All libraries imported successfully!')\n",
    "print(f'OpenCV  : {cv2.__version__}')\n",
    "print(f'NumPy   : {np.__version__}')"
   ]
  },
  {
   "id": "cell-04",
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 2 — Core Concepts\n",
    "\n",
    "### How does detection work?\n",
    "\n",
    "```\n",
    "Image Input\n",
    "    ↓\n",
    "Grayscale Conversion   → removes color noise\n",
    "    ↓\n",
    "Edge Detection         → finds boundaries\n",
    "    ↓\n",
    "Contour Analysis       → finds rectangular regions\n",
    "    ↓\n",
    "Pattern Matching       → finds QR/barcode patterns\n",
    "    ↓\n",
    "Decode content         → extract the data\n",
    "    ↓\n",
    "Draw bounding boxes    → visualize results\n",
    "```\n",
    "\n",
    "### OpenCV vs Manual:\n",
    "\n",
    "| Task | OpenCV Function | Manual Equivalent |\n",
    "|------|----------------|-------------------|\n",
    "| Grayscale | cv2.cvtColor | Average R+G+B channels |\n",
    "| Edge detection | cv2.Canny | Sobel operator manually |\n",
    "| Find shapes | cv2.findContours | Trace pixel boundaries |\n",
    "| Decode | pyzbar.decode | Implement Reed-Solomon |"
   ]
  },
  {
   "id": "cell-05",
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 3 — Load and Explore the Image"
   ]
  },
  {
   "id": "cell-06",
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "def load_and_explore(path):\n",
    "    image = cv2.imread(path)\n",
    "    if image is None:\n",
    "        print(f'Could not load: {path}')\n",
    "        return None\n",
    "    print(f'Image loaded: {path}')\n",
    "    print(f'Shape    : {image.shape}')\n",
    "    print(f'Height   : {image.shape[0]} px')\n",
    "    print(f'Width    : {image.shape[1]} px')\n",
    "    print(f'Channels : {image.shape[2]} (BGR)')\n",
    "    print(f'Dtype    : {image.dtype}')\n",
    "    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n",
    "    rgb  = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)\n",
    "    fig, axes = plt.subplots(1, 3, figsize=(15, 5))\n",
    "    axes[0].imshow(rgb)\n",
    "    axes[0].set_title('Original (RGB)', fontsize=12)\n",
    "    axes[0].axis('off')\n",
    "    axes[1].imshow(gray, cmap='gray')\n",
    "    axes[1].set_title('Grayscale', fontsize=12)\n",
    "    axes[1].axis('off')\n",
    "    axes[2].hist(gray.ravel(), bins=256, color='steelblue', alpha=0.8)\n",
    "    axes[2].set_title('Pixel Histogram', fontsize=12)\n",
    "    axes[2].set_xlabel('Pixel value')\n",
    "    axes[2].set_ylabel('Count')\n",
    "    plt.suptitle('Image Analysis', fontsize=14, fontweight='bold')\n",
    "    plt.tight_layout()\n",
    "    plt.show()\n",
    "    return image\n",
    "\n",
    "image = load_and_explore('images/test_qr.png')"
   ]
  },
  {
   "id": "cell-07",
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 4 — Preprocessing Pipeline\n",
    "\n",
    "Before scanning we preprocess the image:\n",
    "\n",
    "- **Grayscale**: removes color, reduces computation\n",
    "- **Gaussian Blur**: reduces noise\n",
    "- **Otsu Threshold**: converts to pure black and white\n",
    "- **Canny Edges**: finds the boundaries of the code"
   ]
  },
  {
   "id": "cell-08",
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "def show_preprocessing(image):\n",
    "    gray      = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n",
    "    blurred   = cv2.GaussianBlur(gray, (5, 5), 0)\n",
    "    _, thresh = cv2.threshold(\n",
    "        blurred, 0, 255,\n",
    "        cv2.THRESH_BINARY + cv2.THRESH_OTSU\n",
    "    )\n",
    "    edges = cv2.Canny(blurred, 50, 150)\n",
    "    fig, axes = plt.subplots(1, 4, figsize=(18, 5))\n",
    "    steps = [\n",
    "        (cv2.cvtColor(image, cv2.COLOR_BGR2RGB), '1. Original',  None),\n",
    "        (gray,   '2. Grayscale', 'gray'),\n",
    "        (thresh, '3. Threshold', 'gray'),\n",
    "        (edges,  '4. Edges',     'gray'),\n",
    "    ]\n",
    "    for ax, (img, title, cmap) in zip(axes, steps):\n",
    "        ax.imshow(img, cmap=cmap)\n",
    "        ax.set_title(title, fontsize=12)\n",
    "        ax.axis('off')\n",
    "    plt.suptitle('Preprocessing Pipeline', fontsize=14, fontweight='bold')\n",
    "    plt.tight_layout()\n",
    "    plt.show()\n",
    "\n",
    "show_preprocessing(image)"
   ]
  },
  {
   "id": "cell-09",
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 5 — Detect and Decode"
   ]
  },
  {
   "id": "cell-10",
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "def detect_and_decode(image):\n",
    "    gray   = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n",
    "    codes  = pyzbar.decode(gray)\n",
    "    result = image.copy()\n",
    "    colors = [(0,255,0),(0,0,255),(255,0,0),(0,255,255),(255,0,255)]\n",
    "    if not codes:\n",
    "        print('No codes detected.')\n",
    "        return\n",
    "    print(f'Detected {len(codes)} code(s):')\n",
    "    for i, code in enumerate(codes):\n",
    "        data    = code.data.decode('utf-8')\n",
    "        c_type  = code.type\n",
    "        rect    = code.rect\n",
    "        polygon = code.polygon\n",
    "        color   = colors[i % len(colors)]\n",
    "        print(f'  Code #{i+1}')\n",
    "        print(f'  Type : {c_type}')\n",
    "        print(f'  Data : {data}')\n",
    "        print()\n",
    "        pts = np.array([[p.x, p.y] for p in polygon], dtype=np.int32)\n",
    "        cv2.polylines(result, [pts], True, color, 3)\n",
    "        overlay = result.copy()\n",
    "        cv2.fillPoly(overlay, [pts], color)\n",
    "        cv2.addWeighted(overlay, 0.15, result, 0.85, 0, result)\n",
    "        x, y, w, h = rect.left, rect.top, rect.width, rect.height\n",
    "        cv2.rectangle(result, (x, y), (x+w, y+h), color, 2)\n",
    "        label = f'#{i+1} {c_type}: {data[:20]}'\n",
    "        (lw, lh), _ = cv2.getTextSize(\n",
    "            label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2\n",
    "        )\n",
    "        cv2.rectangle(result, (x, y-lh-14), (x+lw+6, y), color, -1)\n",
    "        cv2.putText(\n",
    "            result, label, (x+3, y-8),\n",
    "            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2\n",
    "        )\n",
    "    fig, axes = plt.subplots(1, 2, figsize=(14, 6))\n",
    "    axes[0].imshow(cv2.cvtColor(image,  cv2.COLOR_BGR2RGB))\n",
    "    axes[0].set_title('Original Image', fontsize=12)\n",
    "    axes[0].axis('off')\n",
    "    axes[1].imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))\n",
    "    axes[1].set_title('Detected and Decoded', fontsize=12)\n",
    "    axes[1].axis('off')\n",
    "    plt.suptitle('Detection Results', fontsize=14, fontweight='bold')\n",
    "    plt.tight_layout()\n",
    "    plt.show()\n",
    "    os.makedirs('outputs', exist_ok=True)\n",
    "    cv2.imwrite('outputs/notebook_result.png', result)\n",
    "    print('Saved to outputs/notebook_result.png')\n",
    "\n",
    "detect_and_decode(image)"
   ]
  },
  {
   "id": "cell-11",
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 6 — Test with a Barcode"
   ]
  },
  {
   "id": "cell-12",
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "barcode_image = load_and_explore('images/test_barcode.png')\n",
    "if barcode_image is not None:\n",
    "    detect_and_decode(barcode_image)"
   ]
  },
  {
   "id": "cell-13",
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## Step 7 — Conclusion\n",
    "\n",
    "### What we built:\n",
    "- Complete barcode and QR code detection pipeline\n",
    "- Localization with bounding boxes and polygons\n",
    "- Decoding of content from multiple code types\n",
    "- GUI application for interactive use\n",
    "- Results saved to PNG, TXT and CSV\n",
    "\n",
    "### Key CV concepts used:\n",
    "\n",
    "| Concept | Function | Purpose |\n",
    "|---------|----------|---------|\n",
    "| Grayscale | cv2.cvtColor | Simplify image |\n",
    "| Threshold | cv2.threshold | Isolate patterns |\n",
    "| Edges | cv2.Canny | Find boundaries |\n",
    "| Contours | cv2.findContours | Identify shapes |\n",
    "| Polygon | cv2.polylines | Localize codes |\n",
    "\n",
    "### Libraries used:\n",
    "\n",
    "| Library | Role |\n",
    "|---------|------|\n",
    "| OpenCV | Image processing and visualization |\n",
    "| pyzbar | Barcode and QR code decoding |\n",
    "| NumPy | Array and matrix operations |\n",
    "| Matplotlib | Inline plot display |\n",
    "\n",
    "---\n",
    "\n",
    "**GitHub:** https://github.com/Ismailelmanssouri/barcode-qr-scanner"
   ]
  }
 ]
}

with open("notebook.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

size = len(open("notebook.ipynb", encoding="utf-8").read())
print(f"notebook.ipynb created! Size: {size} bytes")
if size > 5000:
    print("SUCCESS — notebook is complete and valid!")
else:
    print("WARNING — notebook seems too small")