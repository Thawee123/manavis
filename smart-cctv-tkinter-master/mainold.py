from tkinter import *
import tkinter as tk
from tkinter import messagebox
import tkinter.font as font
from in_out import in_out
from rect_noise import rect_noise
from record import record
from openenvaddCameraCap import openenv
from login2 import root, login_success  # Import the root window and login status
from pdfShow import pdfshow
from uploadJsonToS3 import upload
from PIL import Image, ImageTk


def main_app():
    if login_success:            
        window = tk.Tk()
        window.title("Smart cctv")
        window.iconphoto(False, tk.PhotoImage(file='mn.png'))
        # window.geometry('1080x760')
        # Get screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Set window size to full screen
        window.geometry(f"{screen_width}x{screen_height}")

        # Optionally, to remove the window borders and make it full-screen
        # window.overrideredirect(True)  # This will hide the title bar
        window.configure(bg="#fff")


        # Load the background image using Pillow
        background_img = Image.open('background-blue-fade.jpg')  # Make sure this image exists in the path
        background_img = background_img.resize((screen_width, screen_height), Image.LANCZOS)  # Resize it to match the window size
        bg_image = ImageTk.PhotoImage(background_img)
        # Add a label with the background image
        bg_label = tk.Label(window, image=bg_image)
        bg_label.place(relwidth=1, relheight=1)  # Set the label to cover the entire frame

        # Create frame and set the background
        frame1 = tk.Frame(window,bg='white')

        # Load the custom background image for frame1
        frame_bg = Image.open('bg2.png')  # Your uploaded image
        frame_bg = frame_bg.resize((screen_width, screen_height), Image.LANCZOS)
        frame_bg_image = ImageTk.PhotoImage(frame_bg)

        # Add the background to frame1
        frame_bg_label = tk.Label(frame1, image=frame_bg_image)
        frame_bg_label.place(relwidth=1, relheight=1)  # Cover the entire frame1

        label_title = tk.Label(frame1, text="Smart cctv Camera")
        label_font = font.Font(size=35, weight='bold',family='Helvetica')
        label_title['font'] = label_font
        label_title.grid(pady=(10,10), column=2)


        # icon = Image.open('icons/spy.png')
        icon = Image.open('Baksters_logo.png')
        icon = icon.resize((150,150), Image.LANCZOS)
        icon = ImageTk.PhotoImage(icon)
        label_icon = tk.Label(frame1, image=icon)
        label_icon.grid(row=1, pady=(5,10), column=2)

        # btn1_image = Image.open('icons/lamp.png')
        btn1_image = Image.open('icons/setting.png')
        btn1_image = btn1_image.resize((50,50), Image.LANCZOS)
        btn1_image = ImageTk.PhotoImage(btn1_image)

        btn2_image = Image.open('icons/rectangle-of-cutted-line-geometrical-shape.png')
        btn2_image = btn2_image.resize((50,50), Image.LANCZOS)
        btn2_image = ImageTk.PhotoImage(btn2_image)

        btn5_image = Image.open('icons/exit.png')
        btn5_image = btn5_image.resize((50,50), Image.LANCZOS)
        btn5_image = ImageTk.PhotoImage(btn5_image)

        btn3_image = Image.open('icons/security-camera.png')
        btn3_image = btn3_image.resize((50,50), Image.LANCZOS)
        btn3_image = ImageTk.PhotoImage(btn3_image)

        btn6_image = Image.open('icons/MANAVIS.png')
        btn6_image = btn6_image.resize((50,50), Image.LANCZOS)
        btn6_image = ImageTk.PhotoImage(btn6_image)

        btn4_image = Image.open('icons/recording.png')
        btn4_image = btn4_image.resize((50,50), Image.LANCZOS)
        btn4_image = ImageTk.PhotoImage(btn4_image)

        # --------------- Button -------------------#

        # btn1 = tk.Button(frame1, text='Monitor', height=90, width=180, fg='green', image=btn1_image, compound='left')
        btn1 = tk.Button(frame1, text='Configuration', font=('Microsoft YaHei UI Light',25,'bold') ,height=90, width=300, fg='green',  image=btn1_image, compound='left', command=openenv)
        btn1.grid(row=3, pady=(10,10))

        btn2 = tk.Button(frame1, text='Rectangle', font=('Microsoft YaHei UI Light',25,'bold') , height=90, width=300, fg='orange', command=lambda: rect_noise('entrance'), compound='left', image=btn2_image)
        # btn2.grid(row=3, pady=(20,10), column=3, padx=(20,5))
        btn2.grid(row=3, pady=(10,10), column=2)

        btn_font = font.Font(size=25)
        btn3 = tk.Button(frame1, text='Report', font=('Microsoft YaHei UI Light',25,'bold') , height=90, width=300, fg='green', command=pdfshow, image=btn3_image, compound='left')
        btn3.grid(row=4, pady=(10,10))

        btn4 = tk.Button(frame1, text='Record', font=('Microsoft YaHei UI Light',25,'bold') , height=90, width=300, fg='orange', command=record, image=btn4_image, compound='left')
        btn4.grid(row=4, pady=(10,10), column=2)


        btn6 = tk.Button(frame1, text='In Out', font=('Microsoft YaHei UI Light',25,'bold') , height=90, width=300, fg='green', command=in_out, image=btn6_image, compound='left')
        btn6.grid(row=3, pady=(10,10), column=3)

        btn5 = tk.Button(frame1, height=90, width=300, fg='red', command=window.quit, image=btn5_image)
        btn5.grid(row=4, pady=(10,10), column=3)

        btn8 = tk.Button(frame1, text='Export', font=('Microsoft YaHei UI Light',10,'bold') , height=1, width=6, fg='black', command=upload , compound='left')
        btn8.grid(row=5, pady=(10,10), column=3)


        frame1.pack()
        # frame1.pack(fill='both', expand=True)
        window.mainloop()

    else:
        messagebox.showerror("Error", "You must log in first to access the application.")

# Start the login window
root.mainloop()

# After the login window is closed, start the main app
main_app()  # Call your main application after login