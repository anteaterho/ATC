import tkinter as tk

def addTodo() :
	_todo = todo_text.get()
	_is_checked = tk.BooleanVar()

	todo_check_button = tk.Checkbutton(root, text=_todo, variable=_is_checked)
	todo_check_button.pack()
	todo_text.delete(0, tk.END)

root = tk.Tk()
root.title("Tkinter 시작")
root.geometry("600x400")
todo_list = []

todo_text = tk.Entry(root)
todo_text.pack(side="top", anchor="w", padx=10, pady=10, expand=True, fill="both")

add_todo = tk.Button(root, text="Add Todo", command=addTodo)
add_todo.pack(side="top")
