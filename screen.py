from tkinter import *
from tkinter import ttk

from saving_csv_files import tweet_analyzer
t =tweet_analyzer()


def search_button():
    s = []
    s.append(search1.get())
    s.append(search2.get())
    print(s)
    t.get_tweet(s)

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="search1").grid(column=0, row=0, padx=10, pady=10)
ttk.Label(frm, text="search2").grid(column=0, row=1, padx=10, pady=10)
ttk.Button(frm, text="Search",command=search_button).grid(column=4, row=0)
search1 = ttk.Entry(frm)
search1.grid(column = 1, row = 0)
search2 = ttk.Entry(frm)
search2.grid(column = 1, row = 1)


s1 = Scale( frm, 
           from_ = 1, to = 100, 
           orient = HORIZONTAL) 
s1.grid(column= 2, row = 0, padx=20, pady=0)
l3 = Label(frm, text = "Tweet scaler")
l3.grid(column= 2, row = 1)
root.mainloop()