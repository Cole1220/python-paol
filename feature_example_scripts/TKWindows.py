import tkinter as tk
from tkinter import ttk

#setup
window = tk.Tk()
window.title('Testing GUI')
window.geometry('600x400')

def button_func():
    print('a basic button')
    print(radio_1_var.get())

button = ttk.Button(window, text = 'Simple Button', command= button_func)
button.pack()

button_string = tk.StringVar(value = 'button with string var')
button_with_param = ttk.Button(window, text = 'Simple Button', command= button_func, textvariable=button_string)
button_with_param.pack()

check_var = tk.BooleanVar()#tk.IntVar(value=3) #could be tk.BooleanVar() too
check = ttk.Checkbutton(
    window, 
    text='Checkbox: ', 
    command = lambda: print(check_var.get()),
    variable = check_var,
    onvalue = 2,
    offvalue = 3)
check.pack()

#Radio Button
radio_1_var = tk.StringVar()
radio_1 = ttk.Radiobutton(
    window, 
    text='Radio Button 1', 
    value=1,
    variable = radio_1_var,
    command = lambda: print(radio_1_var.get()))
radio_2 = ttk.Radiobutton(
    window, 
    text='Radio Button 2', 
    value=2,
    variable = radio_1_var,
    command = lambda: print(radio_1_var.get()))
radio_1.pack()
radio_2.pack()

#Radio Button Set 2
def radio_func():
    print(check_bool.get())
    check_bool.set(False)

radio_alt_var = tk.StringVar()
check_bool = tk.BooleanVar()

radio_1_alt = ttk.Radiobutton(window, text = 'Radio A', value = 'A', command=radio_func, variable= radio_alt_var)
radio_2_alt = ttk.Radiobutton(window, text = 'Radio B', value = 'B', command=radio_func, variable= radio_alt_var)
check_alt = ttk.Checkbutton(window, text='Checkbox Alt: ', variable=check_bool, command=lambda: print(radio_alt_var.get()))

radio_1_alt.pack()
radio_2_alt.pack()
check_alt.pack()

#run
window.mainloop()