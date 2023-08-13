from tkinter import *
from tkinter import filedialog
import os

class MyFrame:
    def __init__(self, text: str, master=None, entrywidth: int=25, fileType: str = '*.pdf'):
        self.var_dict = {}
        self.entry_dict = {}
        self.bb_dict = {}
        self.rb_dict = {}

        self.fileType = fileType
        self.entryWidth = entrywidth
        self.text = text
        self.e_varCount = 0

        self.frame = LabelFrame(master)

        self.removeButtonFrame = Frame(self.frame)
        self.removeButtonFrame.grid(row=1, column=0)
        self.entryFrame = Frame(self.frame)
        self.entryFrame.grid(row=1, column=1)
        self.BBFrame = Frame(self.frame)
        self.BBFrame.grid(row=1, column=2)

        self.addCheckButton()
        self.addEntry()
        self.addAddButton()


    def addCheckButton(self):
        self.cb_var = BooleanVar()
        # self.var_dict[f"{self.text.capitalize().replace(' ', '')}_CBVar"] = self.cb_var
        self.checkbox = Checkbutton(self.frame, text=self.text, variable=self.cb_var, offvalue=False, onvalue=True)
        self.checkbox.grid(row=0, column=0, sticky=W, columnspan=3)
        self.cb_var.set(True)

    def addEntry(self):
        self.e_var = Variable()
        self.var_dict[f"{self.text.capitalize().replace(' ', '')}_{self.e_varCount}_EVar"] = self.e_var

        self.entry_dict[f"entry_{self.e_varCount}"] = Entry(self.entryFrame, textvariable=self.e_var, width=self.entryWidth)
        self.entry_dict[f"entry_{self.e_varCount}"].grid(pady=3, padx=2)

        self.addBrowseButton(self.e_var)
        self.addRemoveButton()

        self.e_varCount += 1

    def remove(self, entry, entryVar, bb, rb):
        entry.destroy()
        bb.destroy()
        rb.destroy()
        self.var_dict.pop(entryVar)

    def addRemoveButton(self):
        self.rb_dict[f"rb_{self.e_varCount}"] = Button(self.removeButtonFrame, text='✖')
        self.rb_dict[f"rb_{self.e_varCount}"].configure(command=lambda entry=self.entry_dict[f'entry_{self.e_varCount}'], entryVar=f"{self.text.capitalize().replace(' ', '')}_{self.e_varCount}_EVar", bb=self.bb_dict[f'bb_{self.e_varCount}'], rb=self.rb_dict[f"rb_{self.e_varCount}"]: self.remove(entry, entryVar, bb, rb))
        self.rb_dict[f"rb_{self.e_varCount}"].grid()

    def browse(self, title: str, fileType: str, var):
        filePath = filedialog.askopenfilename(title=title, filetypes=((f"{fileType.replace('*', '')}", fileType),))
        var.set(filePath)

    def addBrowseButton(self, e_var):
        self.bb_dict[f'bb_{self.e_varCount}'] = Button(self.BBFrame, text='Browse', command=lambda title=self.text, fileType=self.fileType, e_var=e_var: self.browse(fileType=fileType, title=title, var=e_var))
        self.bb_dict[f'bb_{self.e_varCount}'].grid(pady=2, padx=3)

    def callAddEntry(self):
        self.addEntry()
        self.browse(self.text, self.fileType, self.e_var)

    def addAddButton(self):
        self.add_B = Button(self.frame, text='Add', command=self.callAddEntry)
        self.add_B.grid(row=2, column=0)

    def getAllEntryData(self):
        return list(self.var_dict.values())

    def getKey(self, dict, value):
        for key, val in dict.items():
            if val == value:
                return key

    def indicateError(self, var):
        bgColor = '#f8c0c0'
        fgColor = '#fa1302'
        self.entry_dict[f"entry_{self.getKey(self.var_dict, var).split('_')[1]}"].configure(bg=bgColor, fg=fgColor)


    def noError(self, var):
        self.entry_dict[f"entry_{self.getKey(self.var_dict, var).split('_')[1]}"].configure(bg='#ffffff', fg='#000000')

    def grid(self, **kwargs):
        return self.frame.grid(**kwargs)


if __name__ == '__main__':


    root = Tk()




    ip_eli = MyFrame(master=root, text='Input Eligible')
    ip_eli.grid(row=1, column=0, sticky=W, padx=5, pady=3, ipady=3)

    ip_noneli = MyFrame(master=root, text='Input NonEligible')
    ip_noneli.grid(row=2, column=0, sticky=W, padx=5, pady=3, ipady=3)

    op_eli = MyFrame(master=root, text='Output Eligible')
    op_eli.grid(row=3, column=0, sticky=W, padx=5, pady=3, ipady=3)

    op_noneli = MyFrame(master=root, text='Output NonEligible')
    op_noneli.grid(row=4, column=0, sticky=W, padx=5, pady=3, ipady=3)

    ele_lis = [ip_eli, ip_noneli, op_eli, op_noneli]

    def validatFields():
        isThereError = False
        for ele in ele_lis:
            if ele.cb_var.get() == True:
                for pathVar in ele.getAllEntryData():
                    if not os.path.exists(pathVar.get()):
                        ele.indicateError(pathVar)
                        isThereError = True
                    else:
                        ele.noError(pathVar)
            else:
                for pathVar in ele.getAllEntryData():
                    ele.noError(pathVar)

        return isThereError

    def start():
        files = {
            'input_eligible': [],
            'input_nonEligible': [],
            'output_eligible': [],
            'output_nonEligible': [],
            }

        if not validatFields():
            files['input_eligible'] = [fileVar.get() for fileVar in ip_eli.getAllEntryData()]
            files['input_nonEligible'] = [fileVar.get() for fileVar in ip_noneli.getAllEntryData()]
            files['output_eligible'] = [fileVar.get() for fileVar in op_eli.getAllEntryData()]
            files['output_nonEligible'] = [fileVar.get() for fileVar in op_noneli.getAllEntryData()]

            print(files)
        else:
            print('error')


    Button(root, text='Collect Annexure-B Data', command=start).grid()
    root.mainloop()
