import tkinter.messagebox
from tkinter import *
from tkinter import ttk, filedialog
import datetime

home = Tk()
fromDate = ''
toDate = ''
percentageOfIGST = 0


def browseFolder(var):
    folderPath = filedialog.askdirectory()
    var.set(folderPath)

def browseFile(var):
    filePath = filedialog.askopenfilename()
    var.set(filePath)


templetPath_L = Label(home, text='Templet Path')
templetPath_L.grid(row=0, column=0, sticky=W)

templetPath_Var = StringVar()

templetPath_E = Entry(home, name='templetPathEntry', textvariable=templetPath_Var, width=55)
templetPath_E.grid(row=0, column=1, sticky=W, columnspan=2, padx=5, pady=5)

templetPath_BB = Button(home, name='browseTempletPath', text='Browse', command=lambda var=templetPath_Var: browseFile(var))
templetPath_BB.grid(row=0, column=3)

gstr3BPath_L = Label(home, text='GSTR 3B Folder Path', anchor=W)
gstr3BPath_L.grid(row=1, column=0, sticky=W)

gstr3BPath_Var = StringVar()

gstr3BPath_E = Entry(home, name='gstr3BPathEntry', textvariable=gstr3BPath_Var, width=55)
gstr3BPath_E.grid(row=1, column=1, sticky=W, columnspan=2, padx=5, pady=5)

gstr3BPath_BB = Button(home, name='browseGSTR3BPath', text='Browse', command=lambda var=gstr3BPath_Var: browseFolder(var))
gstr3BPath_BB.grid(row=1, column=3)



gstSummaryPath_L = Label(home, text='GST Summary Path')
gstSummaryPath_L.grid(row=2, column=0, sticky=W)

gstSummaryPath_Var = StringVar()

gstSummaryPath_E = Entry(home, name='gstSummaryPathEntry', textvariable=gstSummaryPath_Var, width=55)
gstSummaryPath_E.grid(row=2, column=1, sticky=W, columnspan=2, padx=5, pady=5)

gstSummaryPath_BB = Button(home, name='browseGSTSummaryPath', text='Browse', command=lambda var=gstSummaryPath_Var: browseFile(var))
gstSummaryPath_BB.grid(row=2, column=3)



creditLedgerPath_L = Label(home, text='Credit Ledger Path')
creditLedgerPath_L.grid(row=3, column=0, sticky=W)

creditLedgerPath_Var = StringVar()

creditLedgerPath_E = Entry(home, name='creditLedgerPathEntry', textvariable=creditLedgerPath_Var, width=55)
creditLedgerPath_E.grid(row=3, column=1, sticky=W, columnspan=2, padx=5, pady=5)

creditLedgerPath_BB = Button(home, name='browseCreditLedgerPath', text='Browse', command=lambda var=creditLedgerPath_Var: browseFolder(var))
creditLedgerPath_BB.grid(row=3, column=3)





fromDate_L = Label(home, text='From:')
fromDate_L.grid(row=4, column=0, sticky=E)
fromDate_Var = StringVar()
fromDate_E = Entry(home, name='fromDate', textvariable=fromDate_Var)
fromDate_E.grid(row=4, column=1, sticky=W, padx=5, pady=5)

FromDateFormate_L = Label(home, text='e.g. :DD/MM/YYYY')
FromDateFormate_L.grid(row=4, column=2, sticky=W, padx=10)

toDate_L = Label(home, text='To:')
toDate_L.grid(row=5, column=0, sticky=E)
toDate_Var = StringVar()
toDate_E = Entry(home, name='toDate', textvariable=toDate_Var)
toDate_E.grid(row=5, column=1, sticky=W, padx=5, pady=5)

toDateFormate_L = Label(home, text='e.g. :DD/MM/YYYY')
toDateFormate_L.grid(row=5, column=2, sticky=W, padx=10)

def done():
    while True:
        print('Done')



precetageIGST_L = Label(home, text='IGST(%)')
precetageIGST_L.grid(row=6, column=0, sticky=E)

precetageIGST_Var = IntVar()
precetageIGST_E = Entry(home, name='percentageOfIGST', textvariable=precetageIGST_Var, width=5)
precetageIGST_E.grid(row=6, column=1, padx=5, sticky=W)


def validateDateFormet(date):
    format = "%d/%m/%Y"
    res = True

    # using try-except to check for truth value
    try:
        res = bool(datetime.datetime.strptime(date, format))
    except ValueError:
        res = False
    return res


def generateClaims():
    global path, fromDate, toDate, percentageOfIGST

    isThereError = False
    errorName = []

    path = {'GSTR 3B': gstr3BPath_Var.get(),
            'Cash and Credit Ledger': creditLedgerPath_Var.get(),
            'Templet': templetPath_Var.get(),
            'GST Summary': gstSummaryPath_Var.get()}

    fromDate = fromDate_Var.get()
    toDate = toDate_Var.get()
    percentageOfIGST = precetageIGST_Var.get()

    for entry in path.keys():
        if path[entry] == '':
            isThereError = True
            errorName.append('All Fields Not Filled')
            break

    if fromDate == '' or toDate == '':
        isThereError = True
        errorName.append('Date Not Filled')

    if not (validateDateFormet(fromDate) and validateDateFormet(toDate)):
        isThereError = True
        errorName.append('Ether Date or Its Formate Invalid')

    if percentageOfIGST <= 0 or percentageOfIGST > 100:
        isThereError = True
        errorName.append('Invalid IGST')

    if isThereError:
        tkinter.messagebox.showwarning('Warning', errorName[0])
    else:
        done()


generate_B = Button(home, name='generateSGSTClaims', text='Generate SGST Claims', command=generateClaims)
generate_B.grid(columnspan=4, padx=5, pady=5)


home.mainloop()