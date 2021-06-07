from tkinter import *

root = Tk()
# turns off title bar, geometry
root.overrideredirect(True)
# set new geometry
root.geometry('400x100+200+200')
# set background color of title bar
back_ground = "#2c2c2c"

# set background of window
content_color = "#ffffff"
# make a frame for the title bar
title_bar = Frame(root, bg=back_ground, relief='raised', bd=1, highlightcolor=back_ground,highlightthickness=0)

# put a close button on the title bar
close_button = Button(title_bar, text='x',  command=root.destroy,bg=back_ground, padx=5, pady=2, activebackground="red", bd=0,    font="bold", fg='white',        activeforeground="white", highlightthickness=0)
 # window title
title_window = "Title Name"
title_name = Label(title_bar, text=title_window, bg=back_ground, fg="white")
# a canvas for the main area of the window
window = Canvas(root, bg="white", highlightthickness=0)

# pack the widgets
title_bar.pack(expand=1, fill=X)
title_name.pack(side=LEFT)
close_button.pack(side=RIGHT)
window.pack(expand=1, fill=BOTH)
x_axis = None
y_axis = None
# bind title bar motion to the move window function


def move_window(event):
    root.geometry('+{0}+{1}'.format(event.x_root, event.y_root))


def change_on_hovering(event):
    global close_button
    close_button['bg'] = 'red'


def return_to_normal_state(event):
   global close_button
   close_button['bg'] = back_ground


title_bar.bind('<B1-Motion>', move_window)
close_button.bind('<Enter>', change_on_hovering)
close_button.bind('<Leave>', return_to_normal_state)
root.mainloop()