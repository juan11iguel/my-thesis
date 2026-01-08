#!/usr/bin/env python3
# /// script
# dependencies = [
#   "pikepdf",
# ]
# ///

"""
Script to combine book cover PDFs: back-cover | spine | front-cover

This script takes three inputs:
1. Path to the front cover PDF
2. Path to the back cover PDF
3. Path to a spine PDF file or folder containing multiple spine PDFs

It creates a single-page PDF with components laid out horizontally:
back-cover | spine | front-cover

If the spine height differs from the covers, it will be scaled to match.
If front and back covers have different dimensions, an error is raised.
If multiple spines are provided, it creates a separate combined PDF for each spine.

This script should be run with:
    uv run scripts/combine_covers.py [arguments]
"""

import argparse
import os
import sys
from pathlib import Path
import pikepdf
from pikepdf import Pdf, Dictionary, Name, Array


def get_spine_files(spine_path):
    """
    Get list of spine PDF files from a path.
    
    Args:
        spine_path: Path to a PDF file or directory containing PDFs
        
    Returns:
        List of Path objects pointing to spine PDF files
    """
    spine_path = Path(spine_path)
    
    if not spine_path.exists():
        raise FileNotFoundError(f"Spine path does not exist: {spine_path}")
    
    if spine_path.is_file():
        if spine_path.suffix.lower() == '.pdf':
            return [spine_path]
        else:
            raise ValueError(f"File is not a PDF: {spine_path}")
    
    elif spine_path.is_dir():
        spine_files = sorted([f for f in spine_path.glob('*.pdf') 
                             if f.is_file()])
        if not spine_files:
            raise ValueError(f"No PDF files found in directory: {spine_path}")
        return spine_files
    
    else:
        raise ValueError(f"Invalid path: {spine_path}")


def combine_pdfs(back_cover_path, spine_path, front_cover_path, output_path):
    """
    Combine three PDFs horizontally: back cover | spine | front cover.
    
    Creates a single-page PDF with all components side-by-side.
    Spine is scaled if necessary to match the height of the covers.
    
    Args:
        back_cover_path: Path to back cover PDF
        spine_path: Path to spine PDF
        front_cover_path: Path to front cover PDF
        output_path: Path for the output combined PDF
        
    Raises:
        ValueError: If front and back covers have different dimensions
    """
    # Open the PDFs
    back_pdf = Pdf.open(back_cover_path)
    spine_pdf = Pdf.open(spine_path)
    front_pdf = Pdf.open(front_cover_path)
    
    # Get the first page of each PDF
    back_page = back_pdf.pages[0]
    spine_page = spine_pdf.pages[0]
    front_page = front_pdf.pages[0]
    
    # Get dimensions
    back_box = back_page.mediabox
    spine_box = spine_page.mediabox
    front_box = front_page.mediabox
    
    # Get width and height, accounting for possible non-zero origin
    back_x0, back_y0 = float(back_box[0]), float(back_box[1])
    back_width = float(back_box[2] - back_box[0])
    back_height = float(back_box[3] - back_box[1])
    
    spine_x0, spine_y0 = float(spine_box[0]), float(spine_box[1])
    spine_width = float(spine_box[2] - spine_box[0])
    spine_height = float(spine_box[3] - spine_box[1])
    
    front_x0, front_y0 = float(front_box[0]), float(front_box[1])
    front_width = float(front_box[2] - front_box[0])
    front_height = float(front_box[3] - front_box[1])
    
    # Check if front and back covers have the same dimensions
    tolerance = 0.1  # Allow small floating-point differences
    if abs(back_width - front_width) > tolerance or abs(back_height - front_height) > tolerance:
        raise ValueError(
            f"Front and back covers have different dimensions!\n"
            f"  Back cover:  {back_width:.2f} x {back_height:.2f} pts\n"
            f"  Front cover: {front_width:.2f} x {front_height:.2f} pts"
        )
    
    # Check if spine needs scaling
    spine_scale = 1.0
    if abs(spine_height - back_height) > tolerance:
        spine_scale = back_height / spine_height
        print(f"Warning: Spine height ({spine_height:.2f} pts) differs from covers ({back_height:.2f} pts).")
        print(f"         Scaling spine by factor {spine_scale:.4f}")
    
    # Calculate scaled spine width
    scaled_spine_width = spine_width * spine_scale
    
    # Create output PDF and import pages as form XObjects
    back_pdf = Pdf.open(back_cover_path)
    spine_pdf = Pdf.open(spine_path)
    front_pdf = Pdf.open(front_cover_path)
    
    output_pdf = Pdf.new()
    
    # Import pages as form XObjects
    back_page_obj = back_pdf.pages[0].as_form_xobject()
    spine_page_obj = spine_pdf.pages[0].as_form_xobject()
    front_page_obj = front_pdf.pages[0].as_form_xobject()
    
    # Create a new PDF with a blank page
    combined_width = back_width + scaled_spine_width + front_width
    combined_height = back_height
    
    # Create the combined page
    combined_page = output_pdf.add_blank_page(page_size=(combined_width, combined_height))
    
    # Add XObjects to resources
    if '/Resources' not in combined_page:
        combined_page.Resources = Dictionary()
    if '/XObject' not in combined_page.Resources:
        combined_page.Resources.XObject = Dictionary()
    
    combined_page.Resources.XObject.BackCover = output_pdf.copy_foreign(back_page_obj)
    combined_page.Resources.XObject.Spine = output_pdf.copy_foreign(spine_page_obj)
    combined_page.Resources.XObject.FrontCover = output_pdf.copy_foreign(front_page_obj)
    
    # Build content stream
    # Note: Form XObjects maintain their original bounding box, so we need to account for offsets
    # The transformation matrix is: [a b c d e f] where the transformation is:
    # x' = a*x + c*y + e
    # y' = b*x + d*y + f
    # For our case: [scale_x 0 0 scale_y translate_x translate_y]
    
    content_stream = (
        b"q\n"  # Back cover at origin
        # No translation needed if back starts at origin, but account for its bbox offset
        + f"1 0 0 1 {-back_x0} {-back_y0} cm\n".encode()
        + b"/BackCover Do\n"
        + b"Q\n"
        + b"q\n"  # Spine scaled and translated
        # Scale the spine, translate to position, and account for spine bbox offset
        + f"{spine_scale} 0 0 {spine_scale} {back_width - spine_x0 * spine_scale} {-spine_y0 * spine_scale} cm\n".encode()
        + b"/Spine Do\n"
        + b"Q\n"
        + b"q\n"  # Front cover translated
        # Translate to position and account for front bbox offset
        + f"1 0 0 1 {back_width + scaled_spine_width - front_x0} {-front_y0} cm\n".encode()
        + b"/FrontCover Do\n"
        + b"Q\n"
    )
    
    combined_page.Contents = output_pdf.make_stream(content_stream)
    
    # Save the output
    output_pdf.save(output_path)
    
    back_pdf.close()
    spine_pdf.close()
    front_pdf.close()
    output_pdf.close()
    
    print(f"Created: {output_path}")
    print(f"  Dimensions: {combined_width:.2f} x {combined_height:.2f} pts")
    print(f"  Layout: Back ({back_width:.2f}) | Spine ({scaled_spine_width:.2f}) | Front ({front_width:.2f})")


def main():
    parser = argparse.ArgumentParser(
        description='Combine book cover PDFs: back-cover -> spine -> front-cover',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single spine file
  %(prog)s front.pdf back.pdf spine.pdf
  
  # Multiple spines from folder
  %(prog)s front.pdf back.pdf spines/ -o output_dir/
  
  # Custom output path
  %(prog)s front.pdf back.pdf spine.pdf -o custom_cover.pdf
        """
    )
    
    parser.add_argument('front_cover', type=str,
                       help='Path to the front cover PDF')
    parser.add_argument('back_cover', type=str,
                       help='Path to the back cover PDF')
    parser.add_argument('spine', type=str,
                       help='Path to spine PDF file or folder containing spine PDFs')
    parser.add_argument('-o', '--output', type=str, default=None,
                       help='Output path (file or directory). If not specified, uses the directory of the back cover')
    
    args = parser.parse_args()
    
    # Validate input files
    front_cover = Path(args.front_cover)
    back_cover = Path(args.back_cover)
    
    if not front_cover.exists():
        print(f"Error: Front cover not found: {front_cover}", file=sys.stderr)
        return 1
    
    if not back_cover.exists():
        print(f"Error: Back cover not found: {back_cover}", file=sys.stderr)
        return 1
    
    # Get spine files
    try:
        spine_files = get_spine_files(args.spine)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = back_cover.parent
    
    # Process each spine file
    for spine_file in spine_files:
        spine_name = spine_file.stem  # filename without extension
        
        # Determine final output file path
        if len(spine_files) == 1:
            # Single spine: use output path as-is
            if output_path.is_dir() or not output_path.suffix:
                # Output is a directory
                output_path.mkdir(parents=True, exist_ok=True)
                final_output = output_path / f"combined_cover_{spine_name}.pdf"
            else:
                # Output is a file
                output_path.parent.mkdir(parents=True, exist_ok=True)
                final_output = output_path
        else:
            # Multiple spines: always create separate files
            if output_path.is_dir() or not output_path.suffix:
                output_path.mkdir(parents=True, exist_ok=True)
                final_output = output_path / f"combined_cover_{spine_name}.pdf"
            else:
                # User specified a file but we have multiple spines
                # Use the directory and create multiple files
                output_dir = output_path.parent
                output_dir.mkdir(parents=True, exist_ok=True)
                final_output = output_dir / f"combined_cover_{spine_name}.pdf"
        
        # Combine the PDFs
        try:
            combine_pdfs(back_cover, spine_file, front_cover, final_output)
        except Exception as e:
            print(f"Error combining PDFs with spine {spine_file}: {e}", file=sys.stderr)
            return 1
    
    print(f"\nSuccessfully created {len(spine_files)} combined cover(s)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
