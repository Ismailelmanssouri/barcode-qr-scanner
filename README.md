# 🔍 Barcode & QR Code Scanner

> A Computer Vision project built with Python and OpenCV
> that detects, localizes, and decodes QR codes and barcodes
> from images — with a full GUI application.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.13-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Example Output](#example-output)
- [Technologies Used](#technologies-used)

---

## 📌 Overview

This project implements a complete pipeline for detecting
and decoding QR codes and barcodes from images using
Python, OpenCV, and pyzbar.

Built as part of a Computer Vision course project for
Big Data & AI Engineering.

---

## ✨ Features

- ✅ Detect QR codes and barcodes from any image
- ✅ Localize codes with bounding boxes and polygons
- ✅ Decode the content (URL, text, numbers)
- ✅ Handle multiple codes in one image
- ✅ Save results to TXT and CSV files
- ✅ Interactive GUI application (Tkinter)
- ✅ Jupyter Notebook with full explanation
- ✅ Clean modular Python scripts

---

## 📁 Project Structure
barcode_qr_scanner/
│
├── images/                 # Input test images
│   └── test_qr.png
│
├── outputs/                # Scan results saved here
│   ├── result.png          # Annotated image
│   ├── results.txt         # Human readable results
│   └── results.csv         # Spreadsheet results
│
├── app.py                  # GUI application (Tkinter)
├── scanner.py              # Core scanner script
├── multi_scanner.py        # Multi-code scanner
├── load_image.py           # Image loading demo
├── notebook.ipynb          # Jupyter notebook
├── check_install.py        # Installation checker
├── requirements.txt        # Dependencies
└── README.md               # This file


---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/barcode-qr-scanner.git
cd barcode-qr-scanner
```

### 2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

> **Linux users** also need:
> ```bash
> sudo apt-get install libzbar0
> ```

### 4. Verify installation
```bash
python check_install.py
```

---

## 🚀 Usage

### Option 1 — GUI Application (recommended)
```bash
python app.py
```
1. Click **Load Image** to select any image
2. Click **Scan Codes** to detect and decode
3. Click **Save Results** to export TXT + CSV

### Option 2 — Command Line
```bash
# Scan a single image
python scanner.py

# Scan image with multiple codes
python multi_scanner.py
```

### Option 3 — Jupyter Notebook
```bash
jupyter notebook notebook.ipynb
```

---

## 🧠 How It Works
Image Input
↓
Grayscale Conversion    → removes color noise
↓
pyzbar Decoding         → detects & decodes all codes
↓
Polygon Extraction      → gets exact corner points
↓
Draw Annotations        → bounding boxes + labels
↓
Save Results            → PNG + TXT + CSV output\

### Key CV Concepts Used

| Concept | Function | Purpose |
|---------|----------|---------|
| Grayscale | `cv2.cvtColor` | Simplify image |
| Thresholding | `cv2.threshold` | Isolate patterns |
| Edge detection | `cv2.Canny` | Find boundaries |
| Contours | `cv2.findContours` | Identify shapes |
| Polygon drawing | `cv2.polylines` | Localize codes |

---

## 📷 Example Output

| Original | Detected |
|----------|----------|
| Plain QR image | QR with green polygon + red box + label |

Results are saved to the `outputs/` folder automatically.

---

## 🛠️ Technologies Used

| Library | Version | Role |
|---------|---------|------|
| Python | 3.10+ | Core language |
| OpenCV | 4.13 | Image processing |
| pyzbar | 0.1.9 | QR/barcode decoding |
| NumPy | 2.4 | Array operations |
| Matplotlib | 3.10 | Visualization |
| Pillow | 11.x | Image format handling |
| Tkinter | built-in | GUI framework |

---

## 👤 Author

**Your Name**
Big Data & AI Engineering Student

---

## 📄 License

This project is for educational purposes.
