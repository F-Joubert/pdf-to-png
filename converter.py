import fitz
import pikepdf
from datetime import datetime
from PIL import Image

from db_functions import add_event_to_database_table
from settings import settings_dict
 
def pdfs_to_single_png(pdf_path, output_path, dpi=300):
    try:
        all_images = []

        # Open the PDF file
        pdf_document = fitz.open(pdf_path)
        for page_num in range(len(pdf_document)):
            # Get the page
            page = pdf_document.load_page(page_num)
            # Render page to an image
            pix = page.get_pixmap(dpi=dpi)
            # Convert to PIL Image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            all_images.append(img)
    
        # Find the maximum width and sum of heights of all images
        max_width = max(image.width for image in all_images)
        total_height = sum(image.height for image in all_images)
    
        # Create a new blank image with the appropriate size
        combined_image = Image.new("RGB", (max_width, total_height))
    
        # Paste each image into the combined image
        y_offset = 0
        for image in all_images:
            combined_image.paste(image, (0, y_offset))
            y_offset += image.height
    
        # Save the combined image as a PNG file
        combined_image.save(output_path, "PNG")
        print(f"Saved combined image to {output_path}")
        if settings_dict["Log PNG"]:
            add_event_to_database_table(f"{datetime.today()}", "PNG", f"Saved combined image to {output_path}", "logs")
    except Exception as e:
        print(f"PDF Conversion error: {e}\nAttempting to remove DRM and try again.")
        if settings_dict["Log Errors"]:
            add_event_to_database_table(f"{datetime.today()}", "Error", fr"Failed to Convert {pdf_path} - Error: {e}", "logs")
        try:
            with pikepdf.open(pdf_path, allow_overwriting_input=True) as pdf:
                print(fr"File {pdf_path} opened correctly.")
                pdf.save(pdf_path)
                print(fr"File {pdf_path} unlocked.")
            all_images = []

            pdf_document = fitz.open(pdf_path)
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                pix = page.get_pixmap(dpi=dpi)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                all_images.append(img)
        
            max_width = max(image.width for image in all_images)
            total_height = sum(image.height for image in all_images)
        
            combined_image = Image.new("RGB", (max_width, total_height))
        
            y_offset = 0
            for image in all_images:
                combined_image.paste(image, (0, y_offset))
                y_offset += image.height
        
            combined_image.save(output_path, "PNG")
            print(f"Saved combined image to {output_path}")
            if settings_dict["Log PNG"]:
                add_event_to_database_table(f"{datetime.today()}", "PNG", fr"Saved combined image to {output_path}", "logs")
        except Exception as e:
            print(f"PDF Conversion error: {e}\nSecond attempt without DRM. Aborting.")
