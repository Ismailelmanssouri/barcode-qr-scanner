# app.py
# Step 5: GUI Application using Tkinter

import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
from pyzbar import pyzbar
import csv
import datetime
import os

class BarcodeScannerApp:
    def __init__(self, root):
        self.root  = root
        self.root.title("🔍 Barcode & QR Code Scanner")
        self.root.geometry("900x650")
        self.root.resizable(True, True)
        self.root.configure(bg="#1e1e2e")

        # Store current results
        self.current_results = []
        self.current_image   = None

        self.build_ui()

    # ──────────────────────────────────────────────────────────
    def build_ui(self):
        """Build all UI components"""

        # ── Title bar ─────────────────────────────────────────
        title = tk.Label(
            self.root,
            text="🔍 Barcode & QR Code Scanner",
            font=("Helvetica", 18, "bold"),
            bg="#1e1e2e", fg="#cdd6f4"
        )
        title.pack(pady=12)

        # ── Main frame (image left | results right) ────────────
        main_frame = tk.Frame(self.root, bg="#1e1e2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=16, pady=4)

        # ── Left panel: image display ──────────────────────────
        left = tk.Frame(main_frame, bg="#313244", bd=2, relief=tk.RIDGE)
        left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0,8))

        tk.Label(
            left, text="Image Preview",
            font=("Helvetica", 11, "bold"),
            bg="#313244", fg="#cdd6f4"
        ).pack(pady=6)

        self.image_label = tk.Label(
            left, bg="#1e1e2e",
            text="No image loaded\nClick 'Load Image' to start",
            fg="#6c7086", font=("Helvetica", 11)
        )
        self.image_label.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # ── Right panel: results ───────────────────────────────
        right = tk.Frame(main_frame, bg="#313244", bd=2, relief=tk.RIDGE)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(
            right, text="Scan Results",
            font=("Helvetica", 11, "bold"),
            bg="#313244", fg="#cdd6f4"
        ).pack(pady=6)

        self.results_box = scrolledtext.ScrolledText(
            right,
            font=("Courier", 10),
            bg="#1e1e2e", fg="#a6e3a1",
            insertbackground="white",
            wrap=tk.WORD,
            state=tk.DISABLED
        )
        self.results_box.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # ── Status bar ─────────────────────────────────────────
        self.status_var = tk.StringVar(value="Ready — load an image to start")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Helvetica", 9),
            bg="#181825", fg="#6c7086",
            anchor=tk.W, padx=10
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        # ── Buttons ────────────────────────────────────────────
        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(pady=10)

        buttons = [
            ("📂  Load Image",   "#89b4fa", self.load_image),
            ("🔍  Scan Codes",   "#a6e3a1", self.scan_image),
            ("💾  Save Results", "#fab387", self.save_results),
            ("🗑️  Clear",        "#f38ba8", self.clear_all),
        ]

        for text, color, cmd in buttons:
            tk.Button(
                btn_frame,
                text=text,
                font=("Helvetica", 11, "bold"),
                bg=color, fg="#1e1e2e",
                activebackground=color,
                width=14, height=1,
                bd=0, cursor="hand2",
                command=cmd
            ).pack(side=tk.LEFT, padx=6)

    # ──────────────────────────────────────────────────────────
    def load_image(self):
        """Open file dialog and load image"""
        path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff"),
                ("All files",   "*.*")
            ]
        )

        if not path:
            return

        # Load with OpenCV
        self.current_image = cv2.imread(path)
        self.image_path    = path

        if self.current_image is None:
            messagebox.showerror("Error", "Could not load image!")
            return

        # Display in GUI
        self.display_image(self.current_image)
        self.status_var.set(f"✅ Loaded: {os.path.basename(path)}")
        self.log_result(f"📂 Image loaded: {path}\n")

    # ──────────────────────────────────────────────────────────
    def display_image(self, cv_image):
        """Convert OpenCV image → Tkinter format and display"""
        rgb   = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        pil   = Image.fromarray(rgb)

        # Resize to fit panel (max 420x380)
        pil.thumbnail((420, 380), Image.LANCZOS)
        photo = ImageTk.PhotoImage(pil)

        self.image_label.configure(image=photo, text="")
        self.image_label.image = photo   # keep reference!

    # ──────────────────────────────────────────────────────────
    def scan_image(self):
        """Scan loaded image for QR codes and barcodes"""
        if self.current_image is None:
            messagebox.showwarning("Warning", "Please load an image first!")
            return

        self.status_var.set("🔍 Scanning...")
        self.root.update()

        # Work on a copy
        image = self.current_image.copy()
        gray  = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        codes = pyzbar.decode(gray)

        if not codes:
            self.log_result("⚠️  No codes found in this image.\n")
            self.status_var.set("⚠️  No codes detected")
            return

        self.current_results = []
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        colors = [
            (0,255,0),(0,0,255),(255,0,0),
            (0,255,255),(255,0,255),(255,165,0)
        ]

        self.log_result(f"🕒 Scanned at: {timestamp}\n")
        self.log_result(f"🎯 Found {len(codes)} code(s):\n")
        self.log_result("─" * 35 + "\n")

        for i, code in enumerate(codes):
            data    = code.data.decode("utf-8")
            c_type  = code.type
            rect    = code.rect
            polygon = code.polygon
            color   = colors[i % len(colors)]

            # Log to results panel
            self.log_result(f"\n  Code #{i+1}\n")
            self.log_result(f"  Type : {c_type}\n")
            self.log_result(f"  Data : {data}\n")
            self.log_result(f"  Pos  : ({rect.left}, {rect.top})\n")
            self.log_result(f"  Size : {rect.width}x{rect.height}\n")

            # Draw polygon
            pts = np.array([[p.x, p.y] for p in polygon], dtype=np.int32)
            cv2.polylines(image, [pts], True, color, 3)

            # Fill with transparency
            overlay = image.copy()
            cv2.fillPoly(overlay, [pts], color)
            cv2.addWeighted(overlay, 0.15, image, 0.85, 0, image)

            # Bounding box
            x, y, w, h = rect.left, rect.top, rect.width, rect.height
            cv2.rectangle(image, (x,y), (x+w, y+h), color, 2)

            # Label
            label = f"#{i+1} {c_type}"
            (lw, lh), _ = cv2.getTextSize(
                label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2
            )
            cv2.rectangle(image, (x, y-lh-14), (x+lw+6, y), color, -1)
            cv2.putText(
                image, label, (x+3, y-8),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (255,255,255), 2
            )

            self.current_results.append({
                "id": i+1, "type": c_type, "data": data,
                "x": rect.left, "y": rect.top,
                "width": rect.width, "height": rect.height,
                "timestamp": timestamp
            })

        # Update image display with annotations
        self.display_image(image)
        self.status_var.set(f"✅ Found {len(codes)} code(s)")
        self.log_result("\n" + "─"*35 + "\n")
        self.log_result("✅ Scan complete!\n")

    # ──────────────────────────────────────────────────────────
    def save_results(self):
        """Save results to TXT and CSV"""
        if not self.current_results:
            messagebox.showwarning("Warning", "No results to save!")
            return

        os.makedirs("outputs", exist_ok=True)
        ts  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save TXT
        txt = f"outputs/results_{ts}.txt"
        with open(txt, "w") as f:
            for r in self.current_results:
                f.write(f"Code #{r['id']}\n")
                f.write(f"  Type : {r['type']}\n")
                f.write(f"  Data : {r['data']}\n\n")

        # Save CSV
        csv_path = f"outputs/results_{ts}.csv"
        with open(csv_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.current_results[0].keys())
            writer.writeheader()
            writer.writerows(self.current_results)

        self.log_result(f"\n💾 Saved: {txt}\n")
        self.log_result(f"📊 Saved: {csv_path}\n")
        self.status_var.set("💾 Results saved!")
        messagebox.showinfo("Saved!", f"Results saved to outputs/ folder")

    # ──────────────────────────────────────────────────────────
    def clear_all(self):
        """Clear image and results"""
        self.current_image   = None
        self.current_results = []
        self.image_label.configure(
            image="", text="No image loaded\nClick 'Load Image' to start"
        )
        self.results_box.configure(state=tk.NORMAL)
        self.results_box.delete("1.0", tk.END)
        self.results_box.configure(state=tk.DISABLED)
        self.status_var.set("Ready — load an image to start")

    # ──────────────────────────────────────────────────────────
    def log_result(self, text):
        """Append text to results box"""
        self.results_box.configure(state=tk.NORMAL)
        self.results_box.insert(tk.END, text)
        self.results_box.see(tk.END)
        self.results_box.configure(state=tk.DISABLED)


# ── Launch the app ─────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app  = BarcodeScannerApp(root)
    root.mainloop()