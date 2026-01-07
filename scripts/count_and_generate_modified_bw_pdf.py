import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

PDF = sys.argv[1]
THRESHOLD = float(sys.argv[2]) if len(sys.argv) > 2 else 0.005

# Generate output PDF path automatically with _bw suffix
pdf_path = Path(PDF)
OUT_PDF = str(pdf_path.parent / f"{pdf_path.stem}_bw{pdf_path.suffix}")

# Step 1: run ink coverage
proc = subprocess.run(
    ["gs", "-q", "-o", "-", "-sDEVICE=inkcov", PDF],
    capture_output=True,
    text=True,
    check=True,
)

bw_pages = []
color_pages = []

for i, line in enumerate(proc.stdout.splitlines(), start=1):
    parts = line.split()
    if len(parts) < 4:
        continue
    c, m, y, k = map(float, parts[:4])
    if c + m + y <= THRESHOLD:
        bw_pages.append(i)
    else:
        color_pages.append(i)

print(f"Threshold (C+M+Y): {THRESHOLD}")
print(f"B&W pages ({len(bw_pages)}): {bw_pages}")
print(f"Color pages ({len(color_pages)}): {color_pages}")

# Step 2: rewrite PDF with BW pages converted to grayscale
temp_dir = Path(tempfile.mkdtemp())

try:
    # Convert full PDF to grayscale
    gray_pdf = temp_dir / "grayscale.pdf"
    subprocess.run([
        "gs",
        "-sDEVICE=pdfwrite",
        "-dProcessColorModel=/DeviceGray",
        "-dColorConversionStrategy=/Gray",
        "-dOverrideICC",
        "-dQUIET",
        "-o", str(gray_pdf),
        PDF
    ], check=True)
    
    # Extract individual pages
    print("\nExtracting pages...")
    page_files = []
    total_pages = max(bw_pages + color_pages) if (bw_pages or color_pages) else 0
    
    for page_num in range(1, total_pages + 1):
        page_file = temp_dir / f"page_{page_num:04d}.pdf"
        source_pdf = str(gray_pdf) if page_num in bw_pages else PDF
        
        subprocess.run([
            "gs",
            "-sDEVICE=pdfwrite",
            "-dQUIET",
            "-dFirstPage=%d" % page_num,
            "-dLastPage=%d" % page_num,
            "-o", str(page_file),
            source_pdf
        ], check=True, stderr=subprocess.DEVNULL)
        
        page_files.append(str(page_file))
    
    # Merge all pages
    print("Merging pages...")
    subprocess.run([
        "gs",
        "-sDEVICE=pdfwrite",
        "-dQUIET",
        "-o", OUT_PDF,
        *page_files
    ], check=True, stderr=subprocess.DEVNULL)
    
    print(f"\nOutput written to: {OUT_PDF}")

finally:
    # Clean up temp directory
    import shutil
    shutil.rmtree(temp_dir, ignore_errors=True)
