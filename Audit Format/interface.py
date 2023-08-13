from tkinter import *
from tkinter import ttk, filedialog
import typing, inspect
var_dict = {}

class LabelEntry:
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
        self.frame.grid(row=row, column=column, columnspan=2, padx=3, pady=3, sticky=W)

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
        self.frame.grid(row=row, column=column, columnspan=self.columnspan)

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
        var_dict[f'{self.name}_EVar'] = self.entry_var
        self.e = Entry(self.frame, textvariable=self.entry_var, width=self.entryWidth)
        self.e.grid(row=0, column=3)

    def indicatError(self):
        bgColour = '#f8c0c0'
        self.l.configure(fg='#fa1302', bg=bgColour)
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
        var_dict[f'{self.name}_CBVar'] = self.checkButton_var
        self.CB = Checkbutton(self.frame, name=self.name, variable=self.checkButton_var, onvalue=True, offvalue=False)
        self.CB.select()
        self.CB.grid(row=0, column=0, padx=2, pady=3)



if __name__ == '__main__':
    import os
    import datetime
    import openpyxl
    from dateutil.relativedelta import relativedelta

    from GSTR1DataCollection import getGSTR1Data
    from GSTR3BDataCollection import getGSTR3BData
    from auditFormatExcelEntry import startAuditFormatEntry


    root = Tk()

    templetPath_Element = LabelEntry(root, name='templetPath', text='           Audit Templet Path  :', row=0, column=0, lableWidth=23, browseButton=True, browsingType='File', title='Select Audit Templet', fileType='*.xlsx')
    gstr1Path_Element = LabelEntry(root, name='gstr1Path', text='GSTR-1 Folder Path   :', row=1, column=0, lableWidth=18, checkButton=True, browseButton=True, browsingType='Directory', title='Select GSTR-1 Folder')
    gstr3bPath_Element = LabelEntry(root, name='gstr3bPath', text='GSTR-3B Folder Path :', row=2, column=0, lableWidth=18, checkButton=True, browseButton=True, browsingType='Directory', title='Select GSTR-3B Folder')

    fromDate_Element = LabelEntry(root, name='fromDate', text='From :', row=3, column=0, entryWidth=13)
    toDate_Element = LabelEntry(root, name='toDate', text='To   :', row=4, column=0, entryWidth=13)
    #---Date Format lable-------------------
    fdf_L = Label(root, text='e.g. :dd/mm/yyyy')
    fdf_L.grid(row=3, column=2)
    tdf_L = Label(root, text='e.g. :dd/mm/yyyy')
    tdf_L.grid(row=4, column=2)


#--------- Validation -----------------------------
    def validateDateFormet(date):
        format = "%d/%m/%Y"
        res = True

        try:
            res = bool(datetime.datetime.strptime(date, format))
        except ValueError:
            res = False
        return res

    def validateDateRange(fromDate, toDate):
        fromDate = datetime.datetime.strptime(fromDate, '%d/%m/%Y').date()
        toDate = datetime.datetime.strptime(toDate, '%d/%m/%Y').date()
        diff = toDate - fromDate

        if diff < (datetime.datetime.today()-datetime.datetime.today()):
            return False
        else:
            return True

    def validateFields():
        global templetPath, gstr1Path, gstr3bPath, fromDate, toDate, gstr1ToBeFilled, gstr3bToBeFilled
        isThereError = False
        templetPath = templetPath_Element.entry_var.get()
        gstr1Path = gstr1Path_Element.entry_var.get()
        gstr3bPath = gstr3bPath_Element.entry_var.get()

        gstr1ToBeFilled = gstr1Path_Element.checkButton_var.get()
        gstr3bToBeFilled = gstr3bPath_Element.checkButton_var.get()

        if not os.path.exists(templetPath):
            templetPath_Element.indicatError()
            isThereError = True
        else:
            templetPath_Element.noError()

        if gstr1ToBeFilled:
            if not os.path.exists((gstr1Path)):
                gstr1Path_Element.indicatError()
                isThereError = True
            else:
                gstr1Path_Element.noError()

        else:
            gstr1Path_Element.noError()

        if gstr3bToBeFilled:
            if not os.path.exists(gstr3bPath):
                gstr3bPath_Element.indicatError()
                isThereError = True
            else:
                gstr3bPath_Element.noError()
        else:
            gstr3bPath_Element.noError()

        fromDate = fromDate_Element.entry_var.get()
        toDate = toDate_Element.entry_var.get()

        if not validateDateFormet(fromDate):
            fromDate_Element.indicatError()
            fdf_L.configure(fg='#fa1302', bg='#f8c0c0')
            isThereError = True
        else:
            fromDate_Element.noError()
            fdf_L.configure(fg='#000000', bg='#f0f0f0')

        if not validateDateFormet(toDate):
            toDate_Element.indicatError()
            tdf_L.configure(fg='#fa1302', bg='#f8c0c0')
            isThereError = True
        else:
            toDate_Element.noError()
            tdf_L.configure(fg='#000000', bg='#f0f0f0')
        if validateDateFormet(fromDate) and validateDateFormet(toDate):
            global error_L
            if not validateDateRange(fromDate, toDate):
                fromDate_Element.indicatError()
                toDate_Element.indicatError()
                error_L = Label(root, text='Date Range Invalid')
                error_L.grid(row=4, column=1)
                error_L.configure(fg='#fa1302', bg='#f8c0c0')
                isThereError = True
            else:
                fromDate_Element.noError()
                toDate_Element.noError()
                try:
                    error_L.destroy()
                except:
                    pass


        return isThereError

    def getClaimPeriodList(fromDate, toDate):
        claimPeriod_list = []

        toDate = toDate.split('/')
        toDate[0] = '01'
        toDate = toDate[0] + '/' + toDate[1] + '/' + toDate[2]

        fromDate = datetime.datetime.strptime(fromDate, '%d/%m/%Y')
        toDate = datetime.datetime.strptime(toDate, '%d/%m/%Y')

        iterDate = fromDate

        while iterDate != toDate:
            claimPeriod_list.append(iterDate.strftime('%b-%y'))
            iterDate = iterDate + relativedelta(months=1)
        claimPeriod_list.append(iterDate.strftime('%b-%y'))

        claimPeriod_list_temp = []
        for idx in range(0, len(claimPeriod_list), 3):
            claimPeriod_list_temp.append([claimPeriod_list[idx], claimPeriod_list[idx + 1], claimPeriod_list[idx + 2]])

        return claimPeriod_list_temp
#---------------------------------------------------------


    def generateSGSTClaims():
        global gstr1_df, gstr3b_df
        error = validateFields()
        if not error:
            if gstr1ToBeFilled:
                gstr1_df = getGSTR1Data(gstr1Path)
            if gstr3bToBeFilled:
                gstr3b_df = getGSTR3BData(gstr3bPath)

            claimPeriod_list = getClaimPeriodList(fromDate, toDate)
            for claimPeriod in claimPeriod_list:
                startAuditFormatEntry(templetPath, claimPeriod, gstr1ToBeFilled, gstr1_df, gstr3bToBeFilled, gstr3b_df)


        # for k in var_dict.keys():
        #     print(var_dict[k].get())

    Button(root, text='Generate SGST Claims', command=generateSGSTClaims).grid()


#------------- Test Data---------------------------------------------------
    templetPath_Element.entry_var.set(r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\Lex Polytex\Audit format\test\SGST Claim Apr-21 to Jun-21 (templet).xlsx')
    gstr1Path_Element.entry_var.set(r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\Lex Polytex\Lex Polytex GSTR 1')
    gstr3bPath_Element.entry_var.set(r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\Lex Polytex\GSTR 3B')

    fromDate_Element.entry_var.set('01/07/2021')
    toDate_Element.entry_var.set('30/06/2022')
#--------------------------------------------------------------------------


    root.mainloop()