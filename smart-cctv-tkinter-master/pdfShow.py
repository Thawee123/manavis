# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive

# # Authenticate and create the PyDrive client
# gauth = GoogleAuth()
# gauth.LocalWebserverAuth()  # Creates a local webserver and automatically handles authentication.
# drive = GoogleDrive(gauth)

# # Specify the file ID and download the PDF
# file_id = '17xsIM5RKKJixCR8ZUFNUIe7sbi6f5AJn'  # Replace with the file ID from the Google Drive link
# file = drive.CreateFile({'id': file_id})
# file.GetContentFile('final_output.pdf')  # Downloads the PDF file

# print("File downloaded successfully!")

# import fitz  # PyMuPDF
# from PIL import Image

# # Open the PDF
# pdf_file = r"c:\Users\Acer\Desktop\final_output.pdf"

# try:
#     pdf_document = fitz.open(pdf_file)
# except Exception as e:
#     raise ValueError(f"Could not open the PDF file: {e}")

# # Loop through the pages
# for page_num in range(len(pdf_document)):
#     page = pdf_document.load_page(page_num)
#     pix = page.get_pixmap()
#     img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
#     # Save instead of showing to isolate the issue
#     img.save(f"page_{page_num}.png")
#     print(f"Page {page_num} saved as PNG successfully!")
#     img.show()

import fitz  # PyMuPDF
from PIL import Image
import os
import tkinter as tk
from tkinter import messagebox

def pdfshow():
    # Open the PDF
    pdf_file = r"c:\Users\Acer\Desktop\final_output.pdf"

    try:
        pdf_document = fitz.open(pdf_file)
    except Exception as e:
        messagebox.showerror("Error", f"Could not open the PDF file: {e}")
        return  # Stop execution if the PDF cannot be opened

    # Loop through the pages
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap()
        
        # Create an image from the pixmap
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Construct the image path and save it
        img_path = os.path.abspath(f"page_{page_num}.png")  # Save in the current working directory
        img.save(img_path)
        print(f"Page {page_num} saved as PNG successfully at {img_path}!")
        
        # Open the saved image using the default image viewer on the system
        os.startfile(img_path)

    # Show a message when finished
    messagebox.showinfo("Done", "All pages have been processed and displayed.")
