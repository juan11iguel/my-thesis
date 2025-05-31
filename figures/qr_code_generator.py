# /// script
# dependencies = [
#   "Pillow",
#   "qrcode",
# ]
# ///
from pathlib import Path
from PIL import Image
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
import argparse


def generate_qr_code(url: str, size: int) -> Image.Image:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)

    qr_img = qr.make_image(
        image_factory=StyledPilImage,
        module_drawer=RoundedModuleDrawer(),
        fill_color="black",
        back_color="white",
    ).convert("RGBA")

    return qr_img.resize((size, size), Image.Resampling.LANCZOS)


def add_qr_to_image(image_path: Path, base_url: str) -> None:
    image = Image.open(image_path).convert("RGBA")
    filename_stem = image_path.stem
    target_url = f"{base_url.rstrip('/')}/{filename_stem}.html"

    # QR is 1/5 of the image width
    qr_size = image.width // 5
    qr = generate_qr_code(target_url, qr_size)

    # New canvas: extend width by qr size
    new_width = image.width + qr_size
    new_height = max(image.height, qr_size)
    new_img = Image.new("RGBA", (new_width, new_height), (255, 255, 255, 0))

    # Paste image and QR code
    new_img.paste(image, (0, 0))
    new_img.paste(qr, (image.width, 0), qr)

    # Save
    output_path = image_path.with_name(f"qr_{image_path.name}")
    new_img.convert("RGB").save(output_path, format="PNG")
    print(f"Saved: {output_path}")


def process_directory(directory: Path, base_url: str) -> None:
    for image_path in directory.glob("*.png"):
        if image_path.stem.startswith("qr_"):
            continue
        add_qr_to_image(image_path, base_url)


def main() -> None:
    parser = argparse.ArgumentParser(description="Add QR codes to PNG images.")
    parser.add_argument(
        "directory", type=str, nargs="?", default=".",
        help="Directory with .png files (default: current)"
    )
    parser.add_argument(
        "--base_url", type=str,
        default="https://github.com/juan11iguel/my-thesis/blob/main/",
        help="Base URL for QR code links"
    )
    args = parser.parse_args()
    directory = Path(args.directory)

    if not directory.is_dir():
        raise NotADirectoryError(f"{directory} is not a valid directory")

    process_directory(directory, args.base_url)


if __name__ == "__main__":
    main()
