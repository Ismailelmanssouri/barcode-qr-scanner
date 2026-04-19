# 🔍 Barcode & QR Code Scanner

> A Computer Vision project built with Python and OpenCV  
> that detects, localizes, and decodes QR codes and barcodes  
> from images — with a full GUI application.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.13-green)
![pyzbar](https://img.shields.io/badge/pyzbar-0.1.9-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

---

## 👥 Team

| Name |
|------|
| EL MANSSOURI Ismail |
| EL AZIZI Mohamed Taha |
| IBENOUAZI Ismail |
| EL KHAYATI Mouataze |

> 📚 Big Data & AI Engineering — Computer Vision Project 2026

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [How It Works](#-how-it-works)
- [CV Concepts](#-cv-concepts)
- [Supported Code Types](#-supported-code-types)
- [Example Output](#-example-output)
- [Technologies Used](#-technologies-used)
- [License](#-license)

---

## 📌 Overview

This project implements a **complete Computer Vision pipeline** for
detecting, localizing, and decoding QR codes and barcodes from digital
images. The system is built using **Python**, **OpenCV**, and the
**pyzbar** library, and is delivered as:

- 🐍 Clean Python scripts
- 📓 Interactive Jupyter Notebook with step-by-step explanation
- 🖥️ Desktop GUI application built with Tkinter

The project was developed as part of the **Computer Vision** module
in the Big Data & AI Engineering program and demonstrates practical
application of image processing techniques.

---

## ✨ Features

- ✅ Detect **QR codes** and **barcodes** from any image
- ✅ Localize codes with **bounding boxes** and **polygons**
- ✅ **Decode** the content (URLs, text, numbers, product codes)
- ✅ Handle **multiple codes** in one image simultaneously
- ✅ Each code gets a **unique color** for easy identification
- ✅ Save results to **TXT** and **CSV** files automatically
- ✅ Interactive **GUI application** (load → scan → save)
- ✅ **Jupyter Notebook** with full pipeline explanation
- ✅ Supports **EAN-13, CODE-128, QR Code, EAN-8, CODE-39** and more

---

## 📁 Project Structure
barcode-qr-scanner/
│
├── 📁 images/                  # Input test images
│   ├── test_qr.png             # Sample QR code
│   └── test_barcode.png        # Sample barcode
│
├── 📁 outputs/                 # Scan results saved here
│   ├── result.png              # Annotated image
│   ├── results.txt             # Human readable results
│   ├── results.csv             # Spreadsheet results
│   └── report.pdf              # Project report
│
├── 📄 app.py                   # GUI application (Tkinter)
├── 📄 scanner.py               # Core scanner script
├── 📄 multi_scanner.py         # Multi-code scanner
├── 📄 load_image.py            # Image loading demo
├── 📄 generate_report.py       # PDF report generator
├── 📄 check_install.py         # Installation checker
├── 📓 notebook.ipynb           # Jupyter notebook
├── 📄 requirements.txt         # Dependencies
├── 📄 .gitignore               # Git ignore rules
└── 📄 README.md                # This file

---

## ⚙️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/Ismailelmanssouri/barcode-qr-scanner.git
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

> ⚠️ **Linux users** also need:
> ```bash
> sudo apt-get install libzbar0
> ```

> ⚠️ **Mac users** also need:
> ```bash
> brew install zbar
> ```

### 4. Verify installation
```bash
python check_install.py
```

Expected output:
✅ OpenCV version: 4.13.x
✅ NumPy version: 2.x.x
✅ Matplotlib version: 3.x.x
✅ Pillow (PIL) imported successfully
✅ pyzbar imported successfully
🎉 All libraries installed correctly!

---

## 🚀 Usage

### Option 1 — GUI Application *(recommended)*
```bash
python app.py
```
1. Click **📂 Load Image** — select any image file
2. Click **🔍 Scan Codes** — detect and decode automatically
3. Click **💾 Save Results** — export TXT + CSV to `outputs/`
4. Click **🗑️ Clear** — reset and scan a new image

### Option 2 — Command Line
```bash
# Scan a single image
python scanner.py

# Scan with specific image path
python scanner.py images/test_barcode.png

# Scan image with multiple codes
python multi_scanner.py
```

### Option 3 — Jupyter Notebook
```bash
jupyter notebook notebook.ipynb
```
Run all cells with `Shift + Enter` to see the full pipeline.

### Option 4 — Generate PDF Report
```bash
python generate_report.py
```

---

## 🧠 How It Works
📷 Image Input
↓
🔲 Grayscale Conversion    → removes color noise
↓
⚡ Contrast Enhancement    → improves barcode visibility
↓
🔍 pyzbar Decoding         → detects & decodes all codes
↓
📍 Polygon Extraction      → gets exact corner points
↓
🎨 Draw Annotations        → bounding boxes + labels + colors
↓
💾 Save Results            → PNG + TXT + CSV output

---

## 📐 CV Concepts

The project demonstrates the following Computer Vision techniques:

| Concept | OpenCV Function | Purpose |
|---------|----------------|---------|
| Grayscale conversion | `cv2.cvtColor()` | Simplify image from 3 channels to 1 |
| Contrast enhancement | `cv2.createCLAHE()` | Improve barcode visibility |
| Gaussian blur | `cv2.GaussianBlur()` | Reduce noise before detection |
| Thresholding (Otsu) | `cv2.threshold()` | Isolate code patterns |
| Edge detection | `cv2.Canny()` | Find boundaries of shapes |
| Contour analysis | `cv2.findContours()` | Identify rectangular regions |
| Polygon drawing | `cv2.polylines()` | Precise code localization |
| Transparency blend | `cv2.addWeighted()` | Semi-transparent highlights |

> 📖 **Note:** `pyzbar` internally uses the **ZBar library** which applies
> edge detection and Reed-Solomon error correction to decode codes — replacing
> the need to implement these algorithms manually.

---

## 🏷️ Supported Code Types

| Code Type | Description | Example Use |
|-----------|-------------|-------------|
| `QRCODE` | 2D matrix barcode | URLs, contact info, text |
| `EAN-13` | 13-digit product barcode | Retail products |
| `EAN-8` | 8-digit product barcode | Small packages |
| `CODE-128` | High-density linear barcode | Shipping & logistics |
| `CODE-39` | Alphanumeric barcode | Industrial use |
| `UPC-A` | Universal product code | US retail |

---

## 📷 Example Output

After scanning an image containing QR codes and barcodes:
✅ Image loaded: images/test_qr.png
📐 Size: 800x600 px
🎯 Found 2 code(s):
Code #1
Type    : QRCODE
Data    : https://github.com/Ismailelmanssouri/barcode-qr-scanner
Position: x=45, y=30
Size    : 280x280 px
Code #2
Type    : EAN13
Data    : 5901234123457
Position: x=400, y=80
Size    : 320x120 px
💾 Image saved : outputs/result.png
📄 TXT saved   : outputs/results.txt
📊 CSV saved   : outputs/results.csv

Each detected code is highlighted with:
- 🟢 **Colored polygon** — exact outline of the code
- 🔲 **Bounding box** — rectangular boundary
- 🏷️ **Label** — code type and decoded content

---

## 🛠️ Technologies Used

| Library | Version | Role |
|---------|---------|------|
| Python | 3.10+ | Core language |
| OpenCV | 4.13 | Image processing & visualization |
| pyzbar | 0.1.9 | QR code & barcode decoding |
| NumPy | 2.4+ | Array & matrix operations |
| Matplotlib | 3.10+ | Image display & visualization |
| Pillow | 11.x | Image format handling |
| Tkinter | built-in | GUI desktop application |
| ReportLab | latest | PDF report generation |

---

## 📄 License

This project is developed for **educational purposes** as part of a
university Computer Vision course.

---

<div align="center">

**🔍 Barcode & QR Code Scanner**  
Built with ❤️ by EL MANSSOURI Ismail · EL AZIZI Mohamed Taha · IBENOUAZI Ismail · EL KHAYATI Mouataze

[![GitHub](https://img.shields.io/badge/GitHub-barcode--qr--scanner-blue?logo=github)](https://github.com/Ismailelmanssouri/barcode-qr-scanner)

</div>
