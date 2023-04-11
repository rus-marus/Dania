import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import askopenfile

import sqlite3
import base64
import os

def upload_file():
    f_types = [('Jpg Files', '*.jpg'), ('Png Files', '*.png')]
    filename = filedialog.askopenfilename(filetypes=f_types)
    img_label_entry.insert(0,filename)

def enter_data():
    # User info
    par = parent_id_entry.get()
    title = name_entry.get()
    path_img= img_label_entry.get()

    if os.path.exists(path_img):
        # Open a file in binary mode
        img_blob = open(path_img,'rb').read()
    else:
        img_blob=None

    if id and par:
        print("par_id: ", par, "Title: ", title,"Image: ", not not img_blob)

        # Create Table
        conn = sqlite3.connect('data.db')
        table_create_query = '''CREATE TABLE IF NOT EXISTS Student_Data 
            (id INTEGER PRIMARY KEY, par INTEGER, title TEXT, img_blob LONGBLOB)'''
        conn.execute(table_create_query)
        # Insert Data
        data_insert_query = '''INSERT INTO Student_Data (par, title, img_blob) VALUES 
        (?, ?, ?)'''
        data_insert_tuple = (par, title, img_blob)
        cursor = conn.cursor()
        cursor.execute(data_insert_query, data_insert_tuple)
        conn.commit()
        conn.close()
    else:
        tkinter.messagebox.showwarning(
            title="Error", message="id and par_id are required.")


window = tkinter.Tk()
window.title("Data Entry Form")

frame = tkinter.Frame(window)
frame.pack()

# Saving User Info
user_info_frame = tkinter.LabelFrame(frame, text="User Information")
user_info_frame.grid(row=0, column=0, padx=20, pady=10)
parent_id = tkinter.Label(user_info_frame, text="parent_id")
parent_id.grid(row=0, column=1)
name = tkinter.Label(user_info_frame, text="name")
name.grid(row=0, column=2)
img = tkinter.Label(user_info_frame, text="img")
img.grid(row=2, column=1)

parent_id_entry = tkinter.Entry(user_info_frame)
img_label_entry=tkinter.Entry(user_info_frame)
name_entry = tkinter.Entry(user_info_frame)
img_entry = tkinter.Button(user_info_frame, text="Upload image", command=upload_file)

b4=tkinter.Button(user_info_frame,text='Paste',
	command=lambda:name_entry.event_generate("<<Paste>>"),font=20)
b4.grid(row=2,column=3)

parent_id_entry.grid(row=1, column=1)
name_entry.grid(row=1, column=2)
img_entry.grid(row=3, column=1, padx=20, pady=10)
img_label_entry.grid(row=3, column=2)


# Button
button = tkinter.Button(frame, text="Enter data", command=enter_data)
button.grid(row=3, column=0, sticky="news", padx=20, pady=10)

window.mainloop()
