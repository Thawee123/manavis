# from tkinter import *
# import tkinter as tk
# from tkinter import messagebox
# from cap import cap_pic
# from PIL import Image, ImageTk
# import os

# def openenv():
        
#     # Function to load existing .env values (if any)
#     def load_env_file():
#         try:
#             with open('.env', 'r') as file:
#                 lines = file.readlines()
#                 for line in lines:
#                     if line.strip():  # Ignore empty lines
#                         key, value = line.strip().split('=', 1)
#                         if key == "RTSP_LINK":
#                             rtsp_link_entry.insert(0, value)
#                         elif key == "MONGO_URI":
#                             mongo_uri_entry.insert(0, value)
#                         elif key == "ZONES_FILE":
#                             zones_file_entry.insert(0, value)
#                         elif key == "MYDB":
#                             mydb_entry.insert(0, value)
#                         elif key == "MYCOL":
#                             mycol_entry.insert(0, value)
#         except FileNotFoundError:
#             pass  # If the file doesn't exist, skip loading

#     # Function to save the input values back to the .env file
#     def save_pic_file():
#         rtsp_link = rtsp_link_entry.get()
#         mongo_uri = mongo_uri_entry.get()
#         zones_file = zones_file_entry.get()
#         mydb = mydb_entry.get()
#         mycol = mycol_entry.get()

#         # Create the .env file content
#         env_content = (
#             f"RTSP_LINK={rtsp_link}\n"
#             f"MONGO_URI={mongo_uri}\n"
#             f"ZONES_FILE={zones_file}\n"
#             f"MYDB={mydb}\n"
#             f"MYCOL={mycol}\n"
#         )

#         # Write the content to the .env file
#         try:
#             with open('.env', 'w') as file:
#                 file.write(env_content)
#             print("save image")
#         except Exception as e:
#             print("can not save image")


#     # Function to save the input values back to the .env file
#     def save_env_file():
#         rtsp_link = rtsp_link_entry.get()
#         mongo_uri = mongo_uri_entry.get()
#         zones_file = zones_file_entry.get()
#         mydb = mydb_entry.get()
#         mycol = mycol_entry.get()

#         # Create the .env file content
#         env_content = (
#             f"RTSP_LINK={rtsp_link}\n"
#             f"MONGO_URI={mongo_uri}\n"
#             f"ZONES_FILE={zones_file}\n"
#             f"MYDB={mydb}\n"
#             f"MYCOL={mycol}\n"
#         )

#         # Write the content to the .env file
#         try:
#             with open('.env', 'w') as file:
#                 file.write(env_content)
#             messagebox.showinfo("Success", "File saved successfully!")
#             root.destroy()
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to save the file: {e}")

#     # Function to capture the picture and display it
#     def capture_and_show_image():
#         save_pic_file()
#         # Capture the image (assuming cap_pic function creates 'frame_1.png')
#         cap_pic()
#         # Use after() method to update the image after root window is initialized
#         root.after(100, update_image_display)

#     def update_image_display():
#         try:
#             # Load and display the captured image
#             image = Image.open("frame_1.jpg")  # Replace with the captured image
#             image = image.resize((640, 360), Image.LANCZOS)
#             img = ImageTk.PhotoImage(image)
#             image_label.config(image=img)
#             image_label.image = img  # Keep a reference to avoid garbage collection
#         except FileNotFoundError:
#             messagebox.showerror("Error", "Captured image not found. Please capture again.")
#         except Exception as e:
#             messagebox.showerror("Error", f"Failed to load image: {e}")
        

#     # Create the main window
#     root = tk.Tk()
#     root.title("Edit .env File")
#     root.geometry('925x600+300+200')
#     root.configure(bg='#fff')
#     root.resizable(False,False)


#     frame = Frame(root,width=640,height=410,bg='white')
#     frame.place(x=100,y=200)

#     # Labels and Entry fields for each key
#     tk.Label(root, text="RTSP_LINK:").grid(row=0, column=0, padx=10, pady=5)
#     rtsp_link_entry = tk.Entry(root, width=50)
#     rtsp_link_entry.grid(row=0, column=1, padx=10, pady=5)

#     tk.Label(root, text="MONGO_URI:").grid(row=1, column=0, padx=10, pady=5)
#     mongo_uri_entry = tk.Entry(root, width=50)
#     mongo_uri_entry.grid(row=1, column=1, padx=10, pady=5)

#     tk.Label(root, text="ZONES_FILE:").grid(row=2, column=0, padx=10, pady=5)
#     zones_file_entry = tk.Entry(root, width=50)
#     zones_file_entry.grid(row=2, column=1, padx=10, pady=5)

#     tk.Label(root, text="MYDB:").grid(row=3, column=0, padx=10, pady=5)
#     mydb_entry = tk.Entry(root, width=50)
#     mydb_entry.grid(row=3, column=1, padx=10, pady=5)

#     tk.Label(root, text="MYCOL:").grid(row=4, column=0, padx=10, pady=5)
#     mycol_entry = tk.Entry(root, width=50)
#     mycol_entry.grid(row=4, column=1, padx=10, pady=5)

#     # Save button to write changes back to the .env file
#     save_button = tk.Button(root, text="Save", command=save_env_file)
#     save_button.grid(row=5, column=0, columnspan=2, pady=10)

#     # Save button to write changes back to the .env file
#     pic = tk.Button(root, text="get Picture", command=capture_and_show_image)
#     pic.place(x=390,y=565)


#     # Default image (noframe.png) shown initially
#     image = Image.open("noframe.png")
#     image = image.resize((640, 360), Image.LANCZOS)  # Resize image to 640x360
#     img = ImageTk.PhotoImage(image)

#     # Label to display the image inside the frame
#     image_label = Label(frame, image=img)
#     image_label.place(x=0, y=0, width=640, height=360)


#     # Load the .env file values when the application starts
#     load_env_file()

#     # Run the main loop
#     root.mainloop()


#เปลี่ยน จากหน้าต่าหลัก เป็นหน้าต่างรอง(top = Toplevel()) แทนการใช้  root = tk.Tk()

from tkinter import *
import tkinter as tk
from tkinter import messagebox
from cap import cap_pic
from PIL import Image, ImageTk
import os

def openenv():
    # Function to load existing .env values (if any)
    def load_env_file():
        print("Loading .env file...")
        env_file_path = os.path.join(os.getcwd(), '.env')
        try:
            with open(env_file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if line.strip():  # Ignore empty lines
                        key, value = line.strip().split('=', 1)
                        if key == "RTSP_LINK":
                            rtsp_link_entry.insert(0, value)
                        elif key == "MONGO_URI":
                            mongo_uri_entry.insert(0, value)
                        elif key == "ZONES_FILE":
                            zones_file_entry.insert(0, value)
                        elif key == "MYDB":
                            mydb_entry.insert(0, value)
                        elif key == "MYCOL":
                            mycol_entry.insert(0, value)
        except FileNotFoundError:
            pass  # If the file doesn't exist, skip loading

    # Function to save the input values back to the .env file
    def save_pic_file():
        rtsp_link = rtsp_link_entry.get()
        mongo_uri = mongo_uri_entry.get()
        zones_file = zones_file_entry.get()
        mydb = mydb_entry.get()
        mycol = mycol_entry.get()

        # Create the .env file content
        env_content = (
            f"RTSP_LINK={rtsp_link}\n"
            f"MONGO_URI={mongo_uri}\n"
            f"ZONES_FILE={zones_file}\n"
            f"MYDB={mydb}\n"
            f"MYCOL={mycol}\n"
        )

        # Write the content to the .env file
        try:
            with open('.env', 'w') as file:
                file.write(env_content)
            print("save image")
        except Exception as e:
            print("cannot save image", e)

    # Function to save the input values back to the .env file
    def save_env_file():
        rtsp_link = rtsp_link_entry.get()
        mongo_uri = mongo_uri_entry.get()
        zones_file = zones_file_entry.get()
        mydb = mydb_entry.get()
        mycol = mycol_entry.get()

        # Create the .env file content
        env_content = (
            f"RTSP_LINK={rtsp_link}\n"
            f"MONGO_URI={mongo_uri}\n"
            f"ZONES_FILE={zones_file}\n"
            f"MYDB={mydb}\n"
            f"MYCOL={mycol}\n"
        )

        try:
            with open('.env', 'w') as file:
                file.write(env_content)
            messagebox.showinfo("Success", "File saved successfully!")
            top.destroy()  # Close the window after saving
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the file: {e}")

    # Function to capture the picture and display it
    def capture_and_show_image():
        save_pic_file()
        cap_pic()
        top.after(100, update_image_display)

    def update_image_display():
        try:
            image = Image.open("frame_1.jpg")  # Replace with the captured image
            image = image.resize((640, 360), Image.LANCZOS)
            img = ImageTk.PhotoImage(image)
            image_label.config(image=img)
            image_label.image = img  # Keep a reference to avoid garbage collection
        except FileNotFoundError:
            messagebox.showerror("Error", "Captured image not found. Please capture again.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")

    # Create a new Toplevel window instead of Tk
    top = Toplevel()
    top.title("Edit .env File")
    top.geometry('925x600+300+200')
    top.configure(bg='#fff')
    top.resizable(False, False)

    frame = Frame(top, width=640, height=410, bg='white')
    frame.place(x=100, y=200)

    # Labels and Entry fields for each key
    tk.Label(top, text="RTSP_LINK:").grid(row=0, column=0, padx=10, pady=5)
    rtsp_link_entry = tk.Entry(top, width=100)
    rtsp_link_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(top, text="MONGO_URI:").grid(row=1, column=0, padx=10, pady=5)
    mongo_uri_entry = tk.Entry(top, width=100)
    mongo_uri_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(top, text="ZONES_FILE:").grid(row=2, column=0, padx=10, pady=5)
    zones_file_entry = tk.Entry(top, width=100)
    zones_file_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(top, text="MYDB:").grid(row=3, column=0, padx=10, pady=5)
    mydb_entry = tk.Entry(top, width=100)
    mydb_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(top, text="MYCOL:").grid(row=4, column=0, padx=10, pady=5)
    mycol_entry = tk.Entry(top, width=100)
    mycol_entry.grid(row=4, column=1, padx=10, pady=5)

    # Save button
    save_button = tk.Button(top, text="Save", command=save_env_file)
    # save_button.grid(row=5, column=0, columnspan=2, pady=10)
    save_button.place(x=390, y=565)

    # Button to capture the picture
    pic_button = tk.Button(top, text="Get Picture", command=capture_and_show_image)
    # pic_button.place(x=390, y=565)
    pic_button.grid(row=5, column=0, columnspan=2, pady=10)
    #สลับตำแหน่งปุ่ม

    # Default image
    image = Image.open("noframe.png")
    image = image.resize((640, 360), Image.LANCZOS)
    img = ImageTk.PhotoImage(image)

    image_label = Label(frame, image=img)
    image_label.place(x=0, y=0, width=640, height=360)

    # Load the .env file values when the application starts
    load_env_file()

    # Run the Toplevel loop
    top.mainloop()

# if __name__ == '__main__':
#     openenv()
