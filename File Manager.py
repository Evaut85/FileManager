import os
import re
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText


# PROGRAM LOGIC
def write_file(file_name, content):
    if not check_extension(file_name):
        return
    try:
        with open(file_name, 'a') as write_to_file:
            write_to_file.write(content)
        messagebox.showinfo("Success", "Your text was successfully written to the file.")
        log_operation(file_name, "WRITE", content)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def read_file(file_name, content_text):
    if not check_extension(file_name):
        return
    try:
        with open(file_name, 'r') as read_the_file:
            content = read_the_file.read()
            content_text.delete('1.0', END)
            content_text.insert('1.0', content)
        log_operation(file_name, "READ")
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{file_name}' not found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def rename_file(file_name, new_filename):
    file_name = check_extension(file_name)
    new_filename = check_extension(new_filename)
    if file_name is None or new_filename is None:
        return
    if not os.path.exists(file_name):
        messagebox.showerror("Error", f"File {file_name} does not exist.")
        return
    os.rename(file_name, new_filename)
    log_operation(file_name, "rename", f"Renamed to: {new_filename}")
    old_log_filename = f"{file_name}_operations.log"
    new_log_filename = f"{new_filename}_operations.log"
    if os.path.exists(old_log_filename):
        os.rename(old_log_filename, new_log_filename)


def remove_file(file_name):
    if not check_extension(file_name):
        return
    try:
        os.remove(file_name)
        log_operation(file_name, "REMOVE")
        log_filename = f"{file_name}_operations.log"
        if os.path.exists(log_filename):
            os.remove(log_filename)
        messagebox.showinfo("Success", "File removed successfully")
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{file_name}' not found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def analyze_file(file_name, result_text):
    if not check_extension(file_name):
        return
    try:
        with open(file_name, 'r') as file:
            content = file.read()
            words = re.findall(r'\b\w+\b', content)
            word_count = {word: words.count(word) for word in set(words)}
            result_text.delete('1.0', END)
            for word, count in word_count.items():
                result_text.insert(END, f"{word}: {count}\n")
        log_operation(file_name, "ANALYZE")
    except FileNotFoundError:
        messagebox.showerror("Error", f"File '{file_name}' not found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def check_extension(file_name):
    if not re.search(r'\.\w+$', file_name):
        messagebox.showerror("Error", "Please specify the file extension (e.g., .txt, .log).")
        return None
    return file_name


def log_operation(filename, operation, extra_info=""):
    log_filename = f"{filename}_operations.log"
    with open(log_filename, "a") as log_file:
        log_file.write(f"{datetime.now()} - {operation} - {extra_info}\n")


def read_log_file(file_name, log_display):
    if not check_extension(file_name):
        return
    log_filename = f"{file_name}_operations.log"
    try:
        with open(log_filename, 'r') as log_file:
            log_content = log_file.read()
            log_display.delete('1.0', END)
            log_display.insert('1.0', log_content)
    except FileNotFoundError:
        messagebox.showerror("Error", f"Log file for '{file_name}' not found.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# GUI
def write_file_window():
    write_window = Toplevel(root)
    write_window.title("Create File")
    write_window.geometry('500x500')
    write_window.configure(bg='#ADA9BA')
    write_window.attributes('-topmost', 1)

    Label(write_window, text="ENTER FILE NAME:", font=('bahnschrift', 16),
          fg='#22222E', bg='#ADA9BA').pack(pady=10)
    file_name_entry = Entry(write_window, width=40)
    file_name_entry.pack(pady=5)

    Label(write_window, text="WRITE YOUR TEXT TO FILE:", font=('bahnschrift', 16),
          fg='#22222E', bg='#ADA9BA').pack(pady=10)
    text_entry = ScrolledText(write_window, width=50, height=17)
    text_entry.pack(pady=5)

    def save_btn():
        write_file(file_name_entry.get(), text_entry.get("1.0", END))

    save_btn = Button(write_window, text="SAVE", font=('bahnschrift', 16),
                      fg='#22222E', bg='#706F8E', activebackground='#393A5A',
                      activeforeground='#E9E9E9', relief=FLAT, command=save_btn)
    save_btn.pack(pady=20)


def read_file_window():
    read_window = Toplevel(root)
    read_window.title("Read File")
    read_window.geometry('500x500')
    read_window.configure(bg='#ADA9BA')
    read_window.attributes('-topmost', 1)

    Label(read_window, text="ENTER FILE NAME:", font=('bahnschrift', 16),
          fg='#22222E', bg='#ADA9BA').pack(pady=10)
    file_name_entry = Entry(read_window, width=40)
    file_name_entry.pack(pady=5)

    Label(read_window, text="FILE CONTENT:", font=('bahnschrift', 16),
          fg='#22222E', bg='#ADA9BA').pack(pady=10)
    content_text = ScrolledText(read_window, width=50, height=17)
    content_text.pack(pady=5)

    def load_btn():
        read_file(file_name_entry.get(), content_text)

    load_btn = Button(read_window, text="LOAD", font=('bahnschrift', 16),
                      fg='#22222E', bg='#706F8E', activebackground='#393A5A',
                      activeforeground='#E9E9E9', relief=FLAT, command=load_btn)
    load_btn.pack(pady=20)


def rename_file_window():
    rename_window = Toplevel(root)
    rename_window.title("Rename File")
    rename_window.geometry('500x250')
    rename_window.configure(bg='#ADA9BA')
    rename_window.attributes('-topmost', 1)

    Label(rename_window, text="ENTER CURRENT FILE NAME:", font=('bahnschrift', 16),
          fg='#22222E', bg='#ADA9BA').pack(pady=10)
    file_name_entry = Entry(rename_window, width=40)
    file_name_entry.pack(pady=5)

    Label(rename_window, text="ENTER NEW FILE NAME:", font=('bahnschrift', 16),
          fg='#22222E', bg='#ADA9BA').pack(pady=10)
    new_name_entry = Entry(rename_window, width=40)
    new_name_entry.pack(pady=5)

    def rename_btn():
        rename_file(file_name_entry.get(), new_name_entry.get())
        messagebox.showinfo("Success", "File renamed successfully")
        rename_window.destroy()

    rename_btn = Button(rename_window, text="RENAME", font=('bahnschrift', 16),
                        fg='#22222E', bg='#706F8E', activebackground='#393A5A',
                        activeforeground='#E9E9E9', relief=FLAT, command=rename_btn)
    rename_btn.pack(pady=20)


def remove_file_window():
    remove_window = Toplevel(root)
    remove_window.title("Remove File")
    remove_window.geometry('500x200')
    remove_window.configure(bg='#ADA9BA')
    remove_window.attributes('-topmost', 1)

    Label(remove_window, text="ENTER FILE NAME TO REMOVE:", font=('bahnschrift', 16),
          fg='#22222E', bg='#ADA9BA').pack(pady=10)
    file_name_entry = Entry(remove_window, width=40)
    file_name_entry.pack(pady=5)

    def remove_btn():
        remove_file(file_name_entry.get())

    remove_btn = Button(remove_window, text="REMOVE", font=(
        'bahnschrift', 16), fg='#22222E', bg='#706F8E', activebackground='#393A5A',
                         activeforeground='#E9E9E9', relief=FLAT, command=remove_btn)
    remove_btn.pack(pady=20)


def analyze_file_window():
    analyze_window = Toplevel(root)
    analyze_window.title("Analyze File")
    analyze_window.geometry('500x500')
    analyze_window.configure(bg='#ADA9BA')
    analyze_window.attributes('-topmost', 1)

    Label(analyze_window, text="ENTER FILE NAME:", font=('bahnschrift', 16),
          fg='#22222E', bg='#ADA9BA').pack(pady=10)
    file_name_entry = Entry(analyze_window, width=40)
    file_name_entry.pack(pady=5)

    Label(analyze_window, text="WORD COUNT:", font=('bahnschrift', 16),
          fg='#22222E', bg='#ADA9BA').pack(pady=10)
    result_text = ScrolledText(analyze_window, width=50, height=17)
    result_text.pack(pady=5)

    def analyze_btn():
        analyze_file(file_name_entry.get(), result_text)

    analyze_btn = Button(analyze_window, text="ANALYZE", font=('bahnschrift', 16),
                         fg='#22222E', bg='#706F8E', activebackground='#393A5A',
                         activeforeground='#E9E9E9', relief=FLAT, command=analyze_btn)
    analyze_btn.pack(pady=20)


def log_file_window():
    log_window = Toplevel(root)
    log_window.title("Log File")
    log_window.geometry('500x500')
    log_window.configure(bg='#ADA9BA')
    log_window.attributes('-topmost', 1)
    Label(log_window, text="ENTER FILE NAME:", font=('bahnschrift', 16),
          fg='#22222E', bg='#ADA9BA').pack(pady=10)
    file_name_entry = Entry(log_window, width=40)
    file_name_entry.pack(pady=5)
    Label(log_window, text="LOG CONTENT:", font=('bahnschrift', 16),
          fg='#22222E', bg='#ADA9BA').pack(pady=10)
    log_display = ScrolledText(log_window, width=50, height=17)
    log_display.pack(pady=5)

    def log_btn():
        read_log_file(file_name_entry.get(), log_display)

    log_btn = Button(log_window, text="SHOW LOG", font=('bahnschrift', 16),
                     fg='#22222E', bg='#706F8E', activebackground='#393A5A',
                     activeforeground='#E9E9E9', relief=FLAT, command=log_btn)
    log_btn.pack(pady=20)


# MAIN MENU
root = Tk()
root['bg'] = "#22222E"
root.title('File Manager')
root.geometry('500x500')
root.resizable(width=False, height=False)

canvas = Canvas(root, width=1000, height=1000, bg='#22222E')
canvas.pack()

frame = Frame(root, bg='#E9E9E9')
frame.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.7)

title = Label(frame, text='FILE MANAGER', font=('bahnschrift', 20, 'bold'), fg='#22222E')
title.pack()

write_file_btn = Button(frame, text='CREATE FILE', font=('bahnschrift', 16), fg='#22222E',
                        bg='#706F8E', activebackground='#393A5A',
                        relief=FLAT, padx=50, activeforeground='#E9E9E9', command=write_file_window)
write_file_btn.place(relx=.5, rely=0.16, anchor="center", width=165, bordermode=OUTSIDE)

read_file_btn = Button(frame, text='READ FILE', font=('bahnschrift', 16), fg='#22222E',
                       bg='#706F8E', activebackground='#393A5A',
                       relief=FLAT, activeforeground='#E9E9E9', command=read_file_window)
read_file_btn.place(relx=.5, rely=0.30, anchor="center", width=165, bordermode=OUTSIDE)

rename_file_btn = Button(frame, text='RENAME FILE', font=('bahnschrift', 16), fg='#22222E',
                         bg='#706F8E', activebackground='#393A5A',
                         relief=FLAT, activeforeground='#E9E9E9', command=rename_file_window)
rename_file_btn.place(relx=.5, rely=0.44, anchor="center", width=165, bordermode=OUTSIDE)

remove_file_btn = Button(frame, text='REMOVE FILE', font=('bahnschrift', 16), fg='#22222E',
                         bg='#706F8E', activebackground='#393A5A',
                         relief=FLAT, activeforeground='#E9E9E9', command=remove_file_window)
remove_file_btn.place(relx=.5, rely=0.58, anchor="center", width=165, bordermode=OUTSIDE)

analyze_file_btn = Button(frame, text='ANALYZE FILE', font=('bahnschrift', 16), fg='#22222E',
                          bg='#706F8E', activebackground='#393A5A', relief=FLAT,
                          activeforeground='#E9E9E9', command=analyze_file_window)
analyze_file_btn.place(relx=.5, rely=0.72, anchor="center", width=165, bordermode=OUTSIDE)

logs_btn = Button(frame, text='LOGS', font=('bahnschrift', 16), fg='#22222E', bg='#706F8E',
                  activebackground='#393A5A', relief=FLAT, activeforeground='#E9E9E9',
                  command=log_file_window)
logs_btn.place(relx=.5, rely=0.86, anchor="center", width=165, bordermode=OUTSIDE)

root.mainloop()
