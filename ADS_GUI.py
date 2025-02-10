import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import ImageTk,Image
from tkinter import filedialog
from getADS import *
import time
import threading
import os
import sys
import webbrowser

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

root = tk.Tk()
# title
root.title("Alternate Data Stream Detection Tool")
root.iconbitmap(resource_path('C:\\Users\\Public\\Alternate_Data_Streams\\venv\\ADS_Test_file\\img\\icon.ico'))
root.configure(background='white')
root.geometry('1060x600')
root.resizable(width=False, height=False)
# ----------------------------------------------------


def browse_files():
    file_path = filedialog.askdirectory()
    selected_folder.set(file_path)

# ----------------------------------------------------
# -------------file_dialog----------------------------
# ---------------------------------------------------


def listing_ADS_files_on_table():
    global toStop
    global label_done, label_path ,label_noPath,label_numberOfADS

    # label_waitting = ttk.Label(root, text="Please wait...", background="White")
    # label_waitting.place(x=20, y=480)
    if selected_folder.get():
        handler1 = ADS(selected_folder.get())
        SubDir = handler1.SubDirectory() #[C:\Users\OJCYS\OneDrive\Desktop\NormalFile\myhiddenstuff, C:\Users\OJCYS\OneDrive\Desktop\NormalFile\important files...]
        count=0
        numberOfADSfile=0
        # label_waitting.place_forget()
        #label_noPath.place_forget()
        for path in SubDir:
            if toStop == 1:
                print("stop")
                label_done = ttk.Label(root, text="The process is stopped", background="White")
                label_done.place(x=20, y=480)
                break;
            label_path = ttk.Label(root, text=f"`{path}` sending to Virus-Total, Please wait...", background="White")

            label_path.place(x=20, y=530)
            listADS = handler1.get_final_result(path) # sending to getADS() ====>>
            numberOfADSfile+=len(listADS)
            count += 1
            progress['value'] = (count / len(SubDir)) * 100
            root.update_idletasks()
            for i in listADS:
                data = (i[3], i[0], i[1], i[2], i[6], i[5], i[4], i[7])
                treeview.insert(parent='', index='end', values=data)

            for i, row_id in enumerate(treeview.get_children()):
                infected = treeview.item(row_id)["values"][-1]

                if infected =='True':
                    bg_color = "salmon"
                else:
                    bg_color = "pale green"
                treeview.tag_configure(f"row{i}", background=bg_color)
                treeview.item(row_id, tags=f"row{i}")

            # selected_folder.trace('w', ADS_paths)
            # selected_folder.trace('w', ADS_paths_fordelete)
            time.sleep(0.05)
            label_path.place_forget()


        if count == len(SubDir):
            print("successfull!")
            label_done = ttk.Label(frame_1, text="The search is completed successfully!", background="White")
            label_done.place(x=20, y=490)
            label_numberOfADS = ttk.Label(root, text=f"The  of ADS file: {numberOfADSfile}", background="White")
            label_numberOfADS.place(x=20, y=530)


    else:
        label_noPath = ttk.Label(frame_1, text="No path entered!", foreground='red', background="White")
        label_noPath.place(x=20, y=490)

    # this for listing all ADS path in drop Widget



def StopBp():
    global toStop
    toStop= 1

def startPBThread():
    global toStop
    toStop=0
    th1=threading.Thread(target=listing_ADS_files_on_table)
    th1.start()

def Rest_All():
    global label_done, label_path, label_noPath, label_add, label_extract, label_remove, treeview
    global label_path, file_entry ,file_entry2 ,file_entry3, drop , file_entry4, remove_label, progress,label_numberOfADS
    ######################################|
    # rest Select folder:                #|
    if (file_entry != None):             #|
        file_entry.delete(0, tk.END)     #|
    if (file_entry2 != None):            #|
        file_entry2.delete(0, tk.END)    #|
                                         #|
    if (file_entry3 != None):            #|
        file_entry3.delete(0, tk.END)    #|
                                         #|
    if (drop != None):                   #|
        drop.delete(0, tk.END)           #|
                                         #|
    if (file_entry4 != None):            #|
        file_entry4.delete(0, tk.END)    #|
                                         #|
    # if (remove_label != ""):           #|
    #     remove_label.delete(0,tk.END)    #|
                                         #|
    # rest table                         #|
    for row in treeview.get_children():  #|
        treeview.delete(row)             #|
                                         #|
    # rest labels                        #|
    if (label_done != None):             #|
        label_done.place_forget()        #|
                                         #|
    if(label_path != None):              #|
        label_path.place_forget()        #|
                                         #|
    if(label_noPath != None):            #|
        label_noPath.place_forget()      #|
    ######################################|
    # rest progress bar                  #|
    progress['value'] = 1                #|
    ######################################|
    if (label_add != None):              #|
        label_add.grid_remove()          #|
                                         #|
    if (label_extract != None):          #|
        label_extract.grid_remove()      #|
                                         #|
    if (label_remove != None):           #|
        label_remove.grid_remove()
    if (label_numberOfADS != None):
        label_numberOfADS.place_forget() #|
    ######################################|
# ---------------------------------------------------
# ----------------------end file_dialog -------------
# ---------------------------------------------------


logo = ImageTk.PhotoImage(Image.open(resource_path('img\\ADS2.png')).resize((240, 80), Image.LANCZOS))
label_logo = ttk.Label(image=logo, background="White")
label_logo.place(x=830, y=5,anchor="n",)

logo_yarmuk = ImageTk.PhotoImage(Image.open(resource_path('img\\yarmuk.png')).resize((100, 85), Image.LANCZOS))
label_yarmuk = ttk.Label(image=logo_yarmuk, background="White")
label_yarmuk.place(x=1010, anchor="n")


selected_folder = tk.StringVar()


frame_1 = tk.Frame(root, background="White")
frame_1.place(x=5, y=5, width=680, height=525)

file_label = ttk.Label(frame_1, text="Select folder:", background="White")
file_label.grid(row=0, column=0, pady=5, padx=15, sticky="w")

file_entry = ttk.Entry(frame_1, textvariable=selected_folder, width=75)
file_entry.grid(row=0, column=1)

browse_button = ttk.Button(frame_1, width=15, text="Browse", command=browse_files)
browse_button.grid(row=0, column=2, padx=5)

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
treeview_frame = ttk.Frame(frame_1)
#treeview_frame.configure(bg="white")
treeview_frame.place(x=20, y=50, width=660, height=390)

treeview = ttk.Treeview(treeview_frame,
                        columns=("File Name", "Date", "Time", "File Size", "Path","ADS Name", "ADS Size", "Infected?"),
                        show="headings")

treeview.column("Date", minwidth=100, width=100)
treeview.column("Time", minwidth=100, width=100)
treeview.column("File Size", minwidth=100, width=100)
treeview.column("File Name", minwidth=100, width=100)
treeview.column("ADS Size", minwidth=100, width=100)
treeview.column("ADS Name", minwidth=150, width=100)
treeview.column("Path", minwidth=400, width=400)
treeview.column("Infected?", minwidth=100, width=100)

treeview.heading("Date", text="Date", anchor=tk.W)
treeview.heading("Time", text="Time", anchor=tk.W)
treeview.heading("File Size", text="File Size(byte)", anchor=tk.W)
treeview.heading("File Name", text="File Name", anchor=tk.W)
treeview.heading("ADS Size", text="ADS Size(byte)", anchor=tk.W)
treeview.heading("ADS Name", text="ADS Name", anchor=tk.W)
treeview.heading("Path", text="Path", anchor=tk.W)
treeview.heading("Infected?", text="Infected?", anchor=tk.W)
treeview.pack(fill=tk.BOTH, expand=tk.YES)

# sample = [['03/25/2023', '10:19 PM', '1,593', 'Calculator.lnk', '27', 'Calculator.lnk:hidden2.txt', 'C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\myhiddenstuff',True],
#          ['03/10/2023', '02:03 AM', '986,847', 'Lake.jpg', '27', 'Lake.jpg:hidden.txt', 'C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\myhiddenstuff',False],
#          ['03/12/2023', '01:48 AM', '23', 'test.txt', '986,847', 'test.txt:Lake.jpg', 'C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\myhiddenstuff','maybe malicious'],
#          ['03/25/2023', '10:19 PM', '1,593', 'Calculator.lnk', '27', 'Calculator.lnk:hidden2.txt', 'C:\\Users\\OJCYS\\OneDrive\\Desktop\\NormalFile\\myhiddenstuff',True]]

progress = ttk.Progressbar(frame_1, length=660, mode="determinate")
progress.place(x=20, y=450)
progress.step()

# Create buttons Start/Stop
toStop=0
Stop_button = ttk.Button(frame_1, width=15, text="Stop", command=StopBp)
Stop_button.place(x=470, y=490)


Go_button = ttk.Button(frame_1, width=15, text="Start", command=startPBThread)
Go_button.place(x=580, y=490)

# ---------------------Rest-All-Button--------------------

button = ttk.Button(frame_1, width=15, text="Rest", command=Rest_All)
button.place(x=360, y=490)

x_scrollbar = ttk.Scrollbar(treeview_frame, orient=tk.HORIZONTAL, command=treeview.xview)
treeview.configure(xscrollcommand=x_scrollbar.set)
x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

label_done = None
label_path = None
label_noPath = None

# ---------------------Functions-OPTIONS-FRAME-----------------
selected_file = tk.StringVar()
selected_payload = tk.StringVar()

def open_file_dialog():
    file_path2 = filedialog.askopenfilename()

    file_entry2.delete(0, tk.END)
    file_entry2.insert(0, file_path2)

    file_path3 = filedialog.askopenfilename()

    file_entry3.delete(0, tk.END)
    file_entry3.insert(0, file_path3)

def Add_ADS():
    global label_add
    handler2= ADS_options(selected_file.get())
    if handler2.addStream(selected_payload.get()):
        label_add=ttk.Label(option_frame, text='The payload add to file successfuly!',foreground="red", background="White")
        label_add.grid(row=6, column=0, padx=5, sticky='w')
    else:
        label_add = ttk.Label(option_frame, text='The payload did not added!',foreground="red", background="White")
        label_add.grid(row=6, column=0, padx=5, sticky='w')

def ADS_paths(*args):
    directory_path = selected_folder.get()
    if os.path.isdir(directory_path):
        handler3 = ADS(directory_path)
        SubDir = handler3.SubDirectory()
        listFullpath = []
        for path in SubDir:
            filePath=handler3.listpath(path)
            for path2 in filePath:
                listFullpath.append(path2)
        drop['values'] = listFullpath

    else:
        drop['values'] = []

selected_folder.trace('w', ADS_paths)

def ADS_paths_fordelete(*args):
    directory_path = selected_folder.get()
    if os.path.isdir(directory_path):
        handler3 = ADS(directory_path)
        SubDir = handler3.SubDirectory()
        listFullpath = []
        for path in SubDir:
            filePath = handler3.listpath2(path)
            for path2 in filePath:
                listFullpath.append(path2)
        drop2['values'] = listFullpath

    else:
        drop2['values'] = []
selected_folder.trace('w', ADS_paths_fordelete)

def browse_files_toSave():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("All files", "*.*"),
                                                        ("Text files", "*.txt"),
                                                        ("Python","*.py"),
                                                        ("Executable","*.exe")])
    if file_path:
        save_location.set(file_path)

def Extract_ADS():
    global label_extract
    extracte_file = drop.get()
    handler4 = ADS_options(extracte_file)
    if handler4.extractStream(save_location.get()):
        label_extract = ttk.Label(option_frame, text='The payload extracted successfuly!',foreground="red", background="White")
        label_extract.grid(row=13, column=0, padx=5, sticky='w')
    else:
        label_extract = ttk.Label(option_frame, text='The payload did not extract!', foreground="red", background="White")
        label_extract.grid(row=13, column=0, padx=5, sticky='w')

def Remove_ADS():
    global label_remove
    delete_file = drop2.get()
    handler5 = ADS_options(delete_file.strip())
    if handler5.removeStream():
        label_remove = ttk.Label(option_frame, text='The payload deleted successfuly!',foreground="red", background="White")
        label_remove.grid(row=17, column=0, padx=5, sticky='w')
    else:
        label_remove = ttk.Label(option_frame, text='The payload did not remove!', foreground="red", background="White")
        label_remove.grid(row=17, column=0, padx=5, sticky='w')



# ---------------------OPTIONS-FRAME-----------------
option_frame = tk.Frame(root, background="White")
#option_frame.configure(background='White')
option_frame.place(x=700, y=90, width=350, height=500)


# ---------------------ADD ADS-----------------------
file_label2 = ttk.Label(option_frame, text="Add_ADS_To_File", font='bold 10', background="White")
file_label2.grid(row=0, column=0, padx=5, sticky='w')

entry_label2 = ttk.Label(option_frame, text='select file:', background="White")
entry_label2.grid(row=1, column=0, padx=5, sticky='w')

file_entry2 = ttk.Entry(option_frame, width=55, textvariable=selected_file)
file_entry2.grid(row=2, column=0, padx=5, pady=5)

entry_label3 = ttk.Label(option_frame, text='select payload file:', background="White")
entry_label3.grid(row=3, column=0, padx=5, sticky='w')

file_entry3 = ttk.Entry(option_frame, width=55, textvariable=selected_payload)
file_entry3.grid(row=4, column=0, padx=5, pady=5)

browse_button = ttk.Button(option_frame, width=15, text="Browse", command=open_file_dialog)
browse_button.grid(row=5, column=0, padx=5, pady=5, sticky='e')

Go_button = ttk.Button(option_frame, width=15, text="Add", command=Add_ADS)
Go_button.grid(row=5, column=0, padx=5, pady=5, sticky='w')

label_add= None
# label_success1=ttk.Label(option_frame, text='The payload add to file successfuly!',foreground="red") #<==========================
# label_success1.grid(row=6, column=0, padx=5, sticky='w')

# ----------------------Extract_ADS------------------
save_location = tk.StringVar()

exrtact_label = ttk.Label(option_frame, text="Extract_ADS", font='bold 10', background="White")
exrtact_label.grid(row=7, column=0, padx=5, pady=5,sticky='w')

exlabel = ttk.Label(option_frame, text="select file to extract ADS file:", background="White")
exlabel.grid(row=8, column=0, padx=5,sticky='w')

drop = ttk.Combobox(option_frame, width=52)
drop.grid(row=9, column=0, padx=5,sticky='w')


save_label = ttk.Label(option_frame,text='Save In:', background="White")
save_label.grid(row=10, column=0, padx=5, pady=5,sticky='w')

file_entry4 = ttk.Entry(option_frame, width=55, textvariable=save_location)
file_entry4.grid(row=11, column=0, padx=5, pady=5)

browse_button = ttk.Button(option_frame, width=15, text="Browse", command=browse_files_toSave)
browse_button.grid(row=12, column=0, padx=5, pady=5,sticky='e')

button_extract = ttk.Button(option_frame, width=15, text="Extract", command=Extract_ADS)
button_extract.grid(row=12, column=0, padx=5, pady=5,sticky='w')

label_extract = None
# label_success2=ttk.Label(option_frame, text='The payload extracted successfuly!',foreground="red") #<==================
# label_success2.grid(row=13, column=0, padx=5, sticky='w')

# ---------------------Remove-ADS--------------------

remove_label = ttk.Label(option_frame, text="Delete_ADS", font='bold 10', background="White")
remove_label.grid(row=14, column=0, padx=5, pady=5, sticky='w')

drop2 = ttk.Combobox(option_frame, width=52)
drop2.grid(row=15, column=0, padx=5, pady=5, sticky='w')

button_remove = ttk.Button(option_frame, width=15, text="Delete", command=Remove_ADS)
button_remove.grid(row=16, column=0, padx=5, pady=5,sticky='w')

label_remove = None
# label_success3=ttk.Label(option_frame, text='The payload removed successfuly!',foreground="red")#<=====================
# label_success3.grid(row=17, column=0, padx=5, sticky='w')

# # ---------------------Rest-All-Button--------------------
#
# button = ttk.Button(option_frame, width=15, text="Rest", command=Rest_All)
# button.grid(row=17, column=0, padx=5, pady=5,sticky='w')



# ----------------------RUN--------------------------

root.mainloop()
