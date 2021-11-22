from os import pipe
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

compiler = Tk()
compiler.title('Drac compiler')
file_path = ''
code=''

def set_file_path(path):
    global file_path
    file_path = path

def open_file():
    path = askopenfilename(filetypes=[('Drac files', '*.drac')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)
        
def save_file_as():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Drac files', '*.drac')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        set_file_path(path)
    
def run():
    global code
    code = editor.get('1.0', END)
    #print(code) #type: <class 'str'> codigo de entrada
    #exec(code) #ejecutar el código de entrada
    if file_path == '':
        save_prompt = Toplevel()
        text = Label(save_prompt, text='Please save your own code')
        text.pack()
        return
    # command = f'python {file_path}'
    # process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # output, error = process.communicate()
    # code_output.insert('1.0', output)
    # code_output.insert('1.0', error)
    code_output.insert('1.0', code)
    code_output.insert(END, 'Hola mundo 2'+'\n')
    
menu_bar = Menu(compiler)

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_file_as)
file_menu.add_command(label='Save As', command=save_file_as)
file_menu.add_command(label='Exit', command=exit)
menu_bar.add_cascade(label='File', menu=file_menu)

run_bar = Menu(menu_bar, tearoff=0)
run_bar.add_command(label='Run Drac Code', command=run)
menu_bar.add_cascade(label='Run', menu=run_bar)

compiler.config(menu=menu_bar)

editor = Text(height=30, bg="black", fg="white", font='Consolas')
editor.pack()

code_output = Text(height=10, bg="black", fg="white", font='Consolas')
code_output.pack()

compiler.mainloop()
