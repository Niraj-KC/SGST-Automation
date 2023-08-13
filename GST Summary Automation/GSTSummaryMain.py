



if __name__ == '__main__':
    from tkinter import *
    from tkinter import ttk, filedialog
    import datetime
    import tkinter.messagebox

    from creditLedgerDataCollection import getCreditLedgerData
    from SGSTPaid import getSGSTPaid
    from SGSTSummaryExcelEntry import startSummaryExcelEntry

    home = Tk()

    path = {
        'GST Summary': '',
        'Credit Ledger': '',
        'GSTR 3B': ''
    }

    startingRow = 0
    fromDate = ''
    toDate = ''
    gstr3BDataToBeFilled = False
    SGSTPaid_df = ''
    creditLedgerDataToBeFilled = False
    creditLedger_df = ''


    def validateDateFormet(date):
        format = "%d/%m/%Y"
        res = True

        # using try-except to check for truth value
        try:
            res = bool(datetime.datetime.strptime(date, format))
        except ValueError:
            res = False
        return res


    def generateGSTSummary():
        global SGSTPaid_df, creditLedger_df
        if gstr3BDataToBeFilled:
            SGSTPaid_df = getSGSTPaid(path['GSTR 3B'])
        if creditLedgerDataToBeFilled:
            creditLedger_df = getCreditLedgerData(path['Credit Ledger'])
        startSummaryExcelEntry(path['GST Summary'], startingRow, fromDate, toDate, gstr3BDataToBeFilled, SGSTPaid_df, creditLedgerDataToBeFilled, creditLedger_df)


    def startValidate():
        global path, fromDate, toDate, startingRow, gstr3BDataToBeFilled, creditLedgerDataToBeFilled

        isThereError = False
        errorName = []

        path = {'GSTR 3B': gstr3BPath_Var.get(),
                'Credit Ledger': creditLedgerPath_Var.get(),
                'GST Summary': gstSummaryPath_Var.get()}

        fromDate = fromDate_Var.get()
        toDate = toDate_Var.get()
        startingRow = int(startingRow_E.get())
        gstr3BDataToBeFilled = gstr3BPath_CBVar.get()
        creditLedgerDataToBeFilled = creditLedgerPath_CBVar.get()

        print(type(startingRow))
        print(startingRow)

        # for entry in path.keys():
        #     if path[entry] == '':
        #         isThereError = True
        #         errorName.append('All Fields Not Filled')
        #         break
        if path['GST Summary'] == '':
            isThereError = True
            errorName.append('GST Summary Path Not Given')
            gstSummaryPath_L.configure(fg='#fa1302', bg='#f57971')
        else:
            gstSummaryPath_L.configure(fg='#000000', bg='#F0F0F0')


        if path['GSTR 3B'] == '' and gstr3BDataToBeFilled:
            isThereError = True
            errorName.append('GSTR 3B Folder Path Not Given')
            gstr3BPath_L.configure(fg='#fa1302', bg='#f57971')
        else:
            gstr3BPath_L.configure(fg='#000000', bg='#F0F0F0')

        if path['Credit Ledger'] == '' and creditLedgerDataToBeFilled:
            isThereError = True
            errorName.append('Credit Ledger Folder Path Not Given')
            creditLedgerPath_L.configure(fg='#fa1302', bg='#f57971')
        else:
            creditLedgerPath_L.configure(fg='#000000', bg='#F0F0F0')

        if fromDate == '' or toDate == '':
            isThereError = True
            errorName.append('Date Not Filled')
            if fromDate == '':
                fromDate_L.configure(fg='#fa1302', bg='#f57971')
            else:
                fromDate_L.configure(fg='#000000', bg='#F0F0F0')
            if toDate == '':
                toDate_L.configure(fg='#fa1302', bg='#f57971')
            else:
                toDate_L.configure(fg='#000000', bg='#F0F0F0')

        if not (validateDateFormet(fromDate) and validateDateFormet(toDate)):
            isThereError = True
            errorName.append('Ether Date or Its Formate Invalid')
            fromDate_L.configure(fg='#fa1302', bg='#f57971')
            toDate_L.configure(fg='#fa1302', bg='#f57971')
        else:
            fromDate_L.configure(fg='#000000', bg='#F0F0F0')
            toDate_L.configure(fg='#000000', bg='#F0F0F0')

        if startingRow <= 0:
            isThereError = True
            errorName.append('Invalid Starting Row')
            startingRow_L.configure(fg='#fa1302', bg='#f57971')
        else:
            startingRow_L.configure(fg='#000000', bg='#F0F0F0')

        if isThereError:
            tkinter.messagebox.showwarning('Warning', errorName[0])
        else:
            print('OK!!!')
            # generateGSTSummary()


    def browseFolder(var, title):
        folderPath = filedialog.askdirectory(title=title)
        var.set(folderPath)


    def browseFile(var, title, fileType):
        filePath = filedialog.askopenfilename(title=title, filetypes=(("files type", fileType),))
        var.set(filePath)


    gstSummaryPath_L = Label(home, text='GST Summary Path')
    gstSummaryPath_L.grid(row=0, column=1, sticky=W)

    gstSummaryPath_Var = StringVar()
    gstSummaryPath_E = Entry(home, name='gstSummaryPathEntry', textvariable=gstSummaryPath_Var, width=55)
    gstSummaryPath_E.grid(row=0, column=2, columnspan=2, sticky=W, padx=5, pady=5)

    gstSummaryPath_BB = Button(home, name='browseGSTSummaryPath', text='Browse',
                               command=lambda var=gstSummaryPath_Var, title='Select GST Summary File', fileType="*.xlsx": browseFile(var, title, fileType))
    gstSummaryPath_BB.grid(row=0, column=4)



    gstr3BPath_CBVar = BooleanVar()
    gstr3BPath_CBVar.set(True)
    gstr3BPath_CB = Checkbutton(home, name='gstr3BPathCheckBox', variable=gstr3BPath_CBVar, offvalue=False, onvalue=True)
    gstr3BPath_CB.grid(row=1, column=0)

    gstr3BPath_L = Label(home, text='GSTR 3B Folder Path', anchor=W)
    gstr3BPath_L.grid(row=1, column=1, sticky=W)

    gstr3BPath_Var = StringVar()
    gstr3BPath_E = Entry(home, name='gstr3BPathEntry', textvariable=gstr3BPath_Var, width=55)
    gstr3BPath_E.grid(row=1, column=2, columnspan=2, sticky=W, padx=5, pady=5)

    gstr3BPath_BB = Button(home, name='browseGSTR3BPath', text='Browse',
                           command=lambda var=gstr3BPath_Var, title='Select GSTR 3B Folder': browseFolder(var, title))
    gstr3BPath_BB.grid(row=1, column=4)



    creditLedgerPath_CBVar = BooleanVar()
    creditLedgerPath_CBVar.set(True)
    creditLedgerPath_CB = Checkbutton(home, name='creditLedgerPathCheckBox', variable=creditLedgerPath_CBVar, offvalue=False, onvalue=True)
    creditLedgerPath_CB.grid(row=2, column=0)

    creditLedgerPath_L = Label(home, text='Credit Ledger Path')
    creditLedgerPath_L.grid(row=2, column=1, sticky=W)

    creditLedgerPath_Var = StringVar()
    creditLedgerPath_E = Entry(home, name='creditLedgerPathEntry', textvariable=creditLedgerPath_Var, width=55)
    creditLedgerPath_E.grid(row=2, column=2, columnspan=2, sticky=W, padx=5, pady=5)

    creditLedgerPath_BB = Button(home, name='browseCreditLedgerPath', text='Browse',
                                 command=lambda var=creditLedgerPath_Var, title='Select Credit Ledger Folder': browseFolder(var, title))
    creditLedgerPath_BB.grid(row=2, column=4)



    fromDate_L = Label(home, text='From:')
    fromDate_L.grid(row=3, column=0, columnspan=2, sticky=E)
    fromDate_Var = StringVar()
    fromDate_E = Entry(home, name='fromDate', textvariable=fromDate_Var)
    fromDate_E.grid(row=3, column=2, sticky=W, padx=5, pady=5)

    FromDateFormate_L = Label(home, text='e.g. :DD/MM/YYYY')
    FromDateFormate_L.grid(row=3, column=3, sticky=W, padx=10)


    toDate_L = Label(home, text='To:')
    toDate_L.grid(row=4, column=0, columnspan=2, sticky=E)
    toDate_Var = StringVar()
    toDate_E = Entry(home, name='toDate', textvariable=toDate_Var)
    toDate_E.grid(row=4, column=2, sticky=W, padx=5, pady=5)

    toDateFormate_L = Label(home, text='e.g. :DD/MM/YYYY')
    toDateFormate_L.grid(row=4, column=3, sticky=W, padx=10)



    startingRow_L = Label(home, text='Starting Row')
    startingRow_L.grid(row=6, column=0, columnspan=2, sticky=E)

    startingRow_Var = IntVar()
    startingRow_E = Entry(home, name='startingRow', textvariable=startingRow_Var, width=5)
    startingRow_E.grid(row=6, column=2, padx=5, sticky=W)



    generate_B = Button(home, name='generateSGSTClaimSummary', text='Generate SGST Claim Summary', command=startValidate)
    generate_B.grid(columnspan=4, padx=5, pady=5)

    home.mainloop()