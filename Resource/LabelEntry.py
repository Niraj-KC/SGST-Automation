from tkinter import *
from typing import Union, Any

_ScreenUnits = Union[str, float]  # Often the right type instead of int. Manual page: Tk_GetPixels

class LabelEntry:

    def __init__(self, master: Tk=None, text: str='',
                 lableWidth: int = 15, entryWidth: int = 50):

        self.columnspan = 2
        self.master = master

        self.text = text
        self.labelWidth = lableWidth
        self.entryWidth = entryWidth
        self.frame = Frame(self.master)

        self.addWidget()

    def addWidget(self):
        self.label = Label(self.frame, text=self.text, width=self.labelWidth, anchor=W)
        self.label.grid(row=0, column=0)

        self.entry_var = Variable()
        self.entry = Entry(self.frame, textvariable=self.entry_var, width=self.entryWidth)
        self.entry.grid(row=0, column=1)

    def grid(self, **kw):
        return self.frame.grid(**kw)


    # labelConfigaration = Label.configure()


if __name__ == '__main__':

    root = Tk()
    le1 = LabelEntry(root, text='Lable1')

    # print(Frame.grid.__defaults__)
    le1.grid(row=0, column=1)

    le2 = LabelEntry(root, text='Lable2')

    le2.grid(cnf={'row':0, 'column':2})

    root.mainloop()