import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
root = tk.Tk()
root.geometry('600x400')
root.title('00이 만든 프로그램')
menubar = tk.Menu(root)
root.config(menu=menubar)
def saveFile() :
    file_path= filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path != "" :
        with open(file_path, 'w', encoding='utf-8') as f :
            f.write(_text.get("1.0", tk.END))

def loadFile() :
    file_path= filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path != "" :

def menuCommand1():
    saveFile
def menuCommand2():
    loadFile
    

file_menu = tk.Menu(menubar)
file_menu.add_command(label="저장하기",command=menuCommand1)
file_menu.add_command(label="불러오기",command=menuCommand2)
file_menu.add_command(label="창지우기",command=menuCommand1)

menubar.add_cascade(label="파일",menu=file_menu)

#file_menu.add_separator()
def cut_text():
    text.event_generate("<<Cut>>")
def copy_text():
    text.event_generate("<<Copy>>")
def paste_text():
    text.event_generate("<<Paste>>")
def undo_text():
    text.event_generate("<<Undo>>")
def redo_text():
    text.event_generate("<<Redo>>")
def exit_app():
    if messagebox.askokcancel("Exit", "Do you really want to exit?"):
        root.destroy()
        
file_menu = tk.Menu(menubar)
file_menu.add_command(label="자르기",command=cut_text)
file_menu.add_command(label="복사",command=copy_text)
file_menu.add_command(label="붙어넣기",command=paste_text)
file_menu.add_command(label="실행취소",command=undo_text)
file_menu.add_command(label="다시실행",command=redo_text)
file_menu.add_command(label="종료",command=exit_app)
menubar.add_cascade(label="편집",menu=file_menu)
root.mainloop()
