from tkinter import *
from tkinter import filedialog
import typing, inspect


class LabelEntry:
    var_dict = {}

    def __init__(self, master: Tk, name: str, text: str, row: int, column: int,
                 lableWidth: int = 15, entryWidth: int = 50,
                 browseButton: bool = False, browsingType: typing.Literal['File', 'Directory'] = ...,
                 title: str = ..., fileType: str = ...,
                 checkButton: bool = False):
        if browsingType is not ...:
            self.enforce_literals(self.__init__)
        if " " in name:
            raise SyntaxError(f'SyntaxError: invalid syntax (Can\'t use space in name) : \'{name}\'')

        self.columnspan = 2
        self.master = master
        self.name = name
        self.text = text
        self.labelWidth = lableWidth
        self.entryWidth = entryWidth
        self.frame = LabelFrame(self.master)#, width=self.master.winfo_width())
       # self.frame.grid(row=row, column=column, columnspan=self.columnspan, padx=3, pady=3, sticky=W)

        self.addWidget()

        if browseButton:
            self.title = title
            self.browsingType = browsingType
            self.columnspan += 1
            if self.browsingType == 'File':
                self.fileType = fileType
                if self.fileType is ...:
                    raise TypeError(": LabelEntry.__init__() missing 1 required positional argument: fileType")
                else:
                    self.addBrowseButton()
            else:
                self.addBrowseButton()

        if checkButton:
            self.columnspan += 1
            self.addCheckButton()
        self.frame.grid(row=row, column=column, columnspan=self.columnspan, padx=3, pady=3, sticky=W)

    def enforce_literals(self, function):
        frame = inspect.stack()[1].frame
        *_, parameters = inspect.getargvalues(frame)
        for name, literal in function.__annotations__.items():
            if typing.get_origin(literal) is typing.Literal and name in parameters:
                value = parameters[name]
                assert value in typing.get_args(literal), f"'{value}' is invalid - valid options are {typing.get_args(literal)}"

    def addWidget(self):
        self.l = Label(self.frame, text=self.text, width=self.labelWidth, anchor=W)
        self.l.grid(row=0, column=1, sticky=W)

        self.entry_var = Variable()
        self.addVariable(f'{self.name}_EVar', self.entry_var)
        self.e = Entry(self.frame, textvariable=self.entry_var, width=self.entryWidth)
        self.e.grid(row=0, column=3)

    def indicatError(self):
        bgColour = '#f8c0c0'
        fgColour = '#fa1302'
        self.l.configure(fg=fgColour, bg=bgColour)
        self.frame.configure(background=bgColour)
        try:
            self.CB.configure(bg=bgColour)
        except AttributeError:
            pass

    def noError(self):
        self.l.configure(fg='#000000', bg='#F0F0F0')
        self.frame.configure(background='#F0F0F0')
        try:
            self.CB.configure(bg='#f0f0f0')
        except AttributeError:
            pass

    def browse(self, title: str, fileType: str = None):
        if fileType is None:
            folderPath = filedialog.askdirectory(title=title)
            self.entry_var.set(folderPath)
        else:
            filePath = filedialog.askopenfilename(title=title, filetypes=((f"{fileType.replace('*', '')}", fileType),))
            self.entry_var.set(filePath)

    def getTitle(self, title):
        if title is ...:
            if self.browsingType == 'File':
                return 'Select A File'
            else:
                return 'Select A Folder'
        else:
            return title

    def addBrowseButton(self):
        if self.browsingType == 'File':
            self.BB = Button(self.frame, text='Browse', command=lambda title=self.getTitle(self.title), fileType=self.fileType: self.browse(fileType=fileType, title=title))
            self.BB.grid(row=0, column=4, pady=2, padx=3)
        else:
            self.BB = Button(self.frame, text='Browse', command=lambda title=self.getTitle(self.title): self.browse(title=title))
            self.BB.grid(row=0, column=4, pady=2, padx=3)


    def addCheckButton(self):
        self.checkButton_var = BooleanVar()
        self.checkButton_var.set(True)
        self.addVariable(f'{self.name}_CBVar', self.checkButton_var)
        self.CB = Checkbutton(self.frame, name=self.name, variable=self.checkButton_var, onvalue=True, offvalue=False)
        self.CB.select()
        self.CB.grid(row=0, column=0, padx=2, pady=3)


    @classmethod
    def addVariable(cls, name, var):
        cls.var_dict[name] = var

