# # Step 1: Open the .env file and read its contents
# with open('.env', 'r') as file:
#     lines = file.readlines()

# # Step 2: Modify the content
# # Let's say you want to update an existing key or add a new key-value pair
# updated_lines = []
# for line in lines:
#     if line.startswith('RTSP_LINK='):
#         # Update the value of API_KEY
#         updated_lines.append('API_KEY=new_api_key_value\n')
#     else:
#         updated_lines.append(line)

# # Add a new key-value pair if it doesn't exist
# updated_lines.append('NEW_VAR=new_value\n')

# # Step 3: Write the updated content back to the .env file
# with open('.env', 'w') as file:
#     file.writelines(updated_lines)

# print("File updated successfully.")

import tkinter as tk
from tkinter import messagebox

def openenv():
    # Function to load existing .env values (if any)
    def load_env_file():
        try:
            with open('.env', 'r') as file:
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

        # Write the content to the .env file
        try:
            with open('.env', 'w') as file:
                file.write(env_content)
            messagebox.showinfo("Success", "File saved successfully!")
            root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the file: {e}")

    # Create the main window
    root = tk.Tk()
    root.title("Edit .env File")

    # Labels and Entry fields for each key
    tk.Label(root, text="RTSP_LINK:").grid(row=0, column=0, padx=10, pady=5)
    rtsp_link_entry = tk.Entry(root, width=50)
    rtsp_link_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="MONGO_URI:").grid(row=1, column=0, padx=10, pady=5)
    mongo_uri_entry = tk.Entry(root, width=50)
    mongo_uri_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="ZONES_FILE:").grid(row=2, column=0, padx=10, pady=5)
    zones_file_entry = tk.Entry(root, width=50)
    zones_file_entry.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(root, text="MYDB:").grid(row=3, column=0, padx=10, pady=5)
    mydb_entry = tk.Entry(root, width=50)
    mydb_entry.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(root, text="MYCOL:").grid(row=4, column=0, padx=10, pady=5)
    mycol_entry = tk.Entry(root, width=50)
    mycol_entry.grid(row=4, column=1, padx=10, pady=5)

    # Save button to write changes back to the .env file
    save_button = tk.Button(root, text="Save", command=save_env_file)
    save_button.grid(row=5, column=0, columnspan=2, pady=10)

    # Load the .env file values when the application starts
    load_env_file()

    # Run the main loop
    root.mainloop()
