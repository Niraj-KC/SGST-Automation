import tkinter.messagebox
from tkinter import *
from tkinter import ttk, filedialog
import datetime

path = {}
fromDate = ''
toDate = ''
percentageOfIGST = 0


def browseFolder(var, title):
    folderPath = filedialog.askdirectory(title=title)
    var.set(folderPath)

def browseFile(var, title, fileType):
    filePath = filedialog.askopenfilename(title=title, filetypes=(("file type", fileType),))
    var.set(filePath)


def validateDateFormet(date):
        format = "%d/%m/%Y"
        res = True

        try:
            res = bool(datetime.datetime.strptime(date, format))
        except ValueError:
            res = False
        return res



if __name__ == '__main__':
    import os
    import excelEntry, GSTR3BDataCollection, gstSummaryDataCollection, creditLedgerDataCollection
    import datetime
    from dateutil.relativedelta import relativedelta

    startingRow = 0
    fromDate = ''
    toDate = ''
    gstr3BDataToBeFilled = False
    gstr3B_df = ''
    gstSummaryDataToBeFilled = False
    gstSummary_df = ''
    creditLedgerDataToBeFilled = False
    creditLedger_df = ''

    def getClaimPeriodList(fromDate, toDate):
        claimPeriod_list = []

        toDate = toDate.split('/')
        toDate[0] = '01'
        toDate = toDate[0] + '/' + toDate[1] + '/' + toDate[2]

        fromDate = datetime.datetime.strptime(fromDate, '%d/%m/%Y')
        toDate = datetime.datetime.strptime(toDate, '%d/%m/%Y')

        iterDate = fromDate

        while iterDate != toDate:
            claimPeriod_list.append(iterDate.strftime('%d/%m/%Y'))
            iterDate = iterDate + relativedelta(months=1)
        claimPeriod_list.append(iterDate.strftime('%d/%m/%Y'))

        claimPeriod_list_temp = []
        for idx in range(0, len(claimPeriod_list), 3):
            claimPeriod_list_temp.append([claimPeriod_list[idx], claimPeriod_list[idx + 1], claimPeriod_list[idx + 2]])

        return claimPeriod_list_temp


    def generateExcell(cp):
        excelEntry.excellEntery(cp, path['Templet'], gstr3BDataToBeFilled, gstr3B_df, gstSummaryDataToBeFilled, gstSummary_df, creditLedgerDataToBeFilled, creditLedger_df, display_F, False, 'polypack')

    def generateSGSTClaims(fromDate, toDate):
        global gstr3B_df, gstSummary_df, creditLedger_df, gstSummaryDataToBeFilled, creditLedgerDataToBeFilled, gstr3BDataToBeFilled

        if gstr3BDataToBeFilled:
            gstr3B_df = GSTR3BDataCollection.collectGSTR3BData(percentageOfIGST, path['GSTR 3B'])
        if gstSummaryDataToBeFilled:

            Label(display_F, text='Collecting GST Summary Data').pack()

            gstSummary_df = gstSummaryDataCollection.getGSTSummaryData(path['GST Summary'])
        if creditLedgerDataToBeFilled:
            creditLedger_df = creditLedgerDataCollection.getCreditLedgerData(path['Cash and Credit Ledger'])

        claimPeriod_list = getClaimPeriodList(fromDate, toDate)
        print(claimPeriod_list)
        for claimPeriod in claimPeriod_list:
            listOf31daysMonth = ['01', '03', '05', '07', '08', '10', '12']
            lm = claimPeriod[-1].split('/')
            if lm[1] in listOf31daysMonth:
                lm[0] = '31'
            else:
                lm[0] = '30'

            lm = lm[0] + '/' + lm[1] + '/' + lm[2]

            claimPeriodStr = f'{claimPeriod[0].replace("/", ".")} to {lm.replace("/", ".")}'

            Label(display_F, text=claimPeriodStr).pack()

            generateExcell(claimPeriod)


    home = Tk()

    templetPath_L = Label(home, text='Templet Path')
    templetPath_L.grid(row=0, column=0+1, sticky=W)

    templetPath_Var = StringVar()

    templetPath_E = Entry(home, name='templetPathEntry', textvariable=templetPath_Var, width=55)
    templetPath_E.grid(row=0, column=1+1, sticky=W, columnspan=2, padx=5, pady=5)

    templetPath_BB = Button(home, name='browseTempletPath', text='Browse',
                            command=lambda var=templetPath_Var, title='Select Templet File For Application Form and Annexure-A',fileType="*.xlsx": browseFile(var, title, fileType))
    templetPath_BB.grid(row=0, column=3+1)


    gstr3BPath_CBVar = BooleanVar()
    gstr3BPath_CBVar.set(True)
    gstr3BPath_CB = Checkbutton(home, name='gstr3BPathCheckBox', variable=gstr3BPath_CBVar, offvalue=False, onvalue=True)
    gstr3BPath_CB.select()
    gstr3BPath_CB.grid(row=1, column=0)

    gstr3BPath_L = Label(home, text='GSTR 3B Folder Path', anchor=W)
    gstr3BPath_L.grid(row=1, column=0+1, sticky=W)

    gstr3BPath_Var = StringVar()
    gstr3BPath_E = Entry(home, name='gstr3BPathEntry', textvariable=gstr3BPath_Var, width=55)
    gstr3BPath_E.grid(row=1, column=1+1, sticky=W, columnspan=2, padx=5, pady=5)

    gstr3BPath_BB = Button(home, name='browseGSTR3BPath', text='Browse',
                           command=lambda var=gstr3BPath_Var, title='Select GSTR 3B Folder': browseFolder(var, title))
    gstr3BPath_BB.grid(row=1, column=3+1)



    gstSummatyPath_CBVar = BooleanVar()
    gstSummatyPath_CBVar.set(True)
    gstSummatyPath_CB = Checkbutton(home, name='gstSummatyPathCheckBox', variable=gstSummatyPath_CBVar, offvalue=False, onvalue=True)
    gstSummatyPath_CB.select()
    gstSummatyPath_CB.grid(row=2, column=0)

    gstSummaryPath_L = Label(home, text='GST Summary Path')
    gstSummaryPath_L.grid(row=2, column=0+1, sticky=W)

    gstSummaryPath_Var = StringVar()

    gstSummaryPath_E = Entry(home, name='gstSummaryPathEntry', textvariable=gstSummaryPath_Var, width=55)
    gstSummaryPath_E.grid(row=2, column=1+1, sticky=W, columnspan=2, padx=5, pady=5)

    gstSummaryPath_BB = Button(home, name='browseGSTSummaryPath', text='Browse',
                               command=lambda var=gstSummaryPath_Var, title='Select GST Summary File', fileType="*.xlsx": browseFile(var, title, fileType))
    gstSummaryPath_BB.grid(row=2, column=3+1)

    #
    # gstSummaryDataCollection_LF = LabelFrame(home, name='gstr3BDataCollection_LF', text='GST Summary Column NAME For:')
    # gstSummaryDataCollection_LF.grid(row=3, column=1, columnspan=4)
    #
    # ITCAdded_L = Label(gstSummaryDataCollection_LF, text='ITC Added During Mounth Column:')
    # ITCAdded_L.grid(row=0, column=0)
    #
    # ITCAdded_VarE = StringVar()
    # ITCAdded_VarE.set('ITC added during the month')
    # ITCAdded_E = Entry(gstSummaryDataCollection_LF, name='iTCAdded', textvariable=ITCAdded_VarE, width=50)
    # ITCAdded_E.grid(row=0, column=1)
    #
    # ITCAdjusted_L = Label(gstSummaryDataCollection_LF, text='ITC Adjusted During Month Column:')
    # ITCAdjusted_L.grid(row=1, column=0)
    #
    # ITCAdjusted_VarE = StringVar()
    # ITCAdjusted_VarE.set('ITC adjusted during the QTR')
    # ITCAdjusted_E = Entry(gstSummaryDataCollection_LF, name='iTCAdjusted', textvariable=ITCAdjusted_VarE, width=50)
    # ITCAdjusted_E.grid(row=1, column=1)
    #
    #
    # openingPlusInputBal_L = Label(gstSummaryDataCollection_LF, text='Opening + Input Balance:')
    # openingPlusInputBal_L.grid(row=2, column=0)
    #
    # openingPlusInputBal_VarE = StringVar()
    # openingPlusInputBal_VarE.set('Opening Bal + input')
    # openingPlusInputBal_E = Entry(gstSummaryDataCollection_LF, name='openingPlusInputBal', textvariable=openingPlusInputBal_VarE, width=50)
    # openingPlusInputBal_E.grid(row=2, column=1)

    creditLedgerPath_CBVar = BooleanVar()
    creditLedgerPath_CBVar.set(True)
    creditLedgerPath_CB = Checkbutton(home, name='creditLedgerPathCheckBox', variable=creditLedgerPath_CBVar, offvalue=False, onvalue=True)
    creditLedgerPath_CB.select()
    creditLedgerPath_CB.grid(row=4, column=0)

    creditLedgerPath_L = Label(home, text='Credit Ledger Path')
    creditLedgerPath_L.grid(row=4, column=0+1, sticky=W)

    creditLedgerPath_Var = StringVar()

    creditLedgerPath_E = Entry(home, name='creditLedgerPathEntry', textvariable=creditLedgerPath_Var, width=55)
    creditLedgerPath_E.grid(row=4, column=1+1, sticky=W, columnspan=2, padx=5, pady=5)

    creditLedgerPath_BB = Button(home, name='browseCreditLedgerPath', text='Browse',
                                 command=lambda var=creditLedgerPath_Var, title='Select Credit Ledger Folder': browseFolder(var, title))
    creditLedgerPath_BB.grid(row=4, column=3+1)



    fromDate_L = Label(home, text='From:')
    fromDate_L.grid(row=5, column=0+1, sticky=E)
    fromDate_Var = StringVar()
    fromDate_E = Entry(home, name='fromDate', textvariable=fromDate_Var)
    fromDate_E.grid(row=5, column=1+1, sticky=W, padx=5, pady=5)

    FromDateFormate_L = Label(home, text='e.g. :DD/MM/YYYY')
    FromDateFormate_L.grid(row=5, column=2+1, sticky=W, padx=10)


    toDate_L = Label(home, text='To:')
    toDate_L.grid(row=6, column=0+1, sticky=E)
    toDate_Var = StringVar()
    toDate_E = Entry(home, name='toDate', textvariable=toDate_Var)
    toDate_E.grid(row=6, column=1+1, sticky=W, padx=5, pady=5)

    toDateFormate_L = Label(home, text='e.g. :DD/MM/YYYY')
    toDateFormate_L.grid(row=6, column=2+1, sticky=W, padx=10)



    precetageIGST_L = Label(home, text='IGST(%)')
    precetageIGST_L.grid(row=7, column=0, columnspan=2, sticky=E)

    precetageIGST_Var = IntVar()
    precetageIGST_E = Entry(home, name='percentageOfIGST', textvariable=precetageIGST_Var, width=5)
    precetageIGST_E.grid(row=7, column=2, padx=5, sticky=W)

    #--------------------test data-------------------------
    # templetPath_Var.set(r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\venus polypack ind\test\temp.xlsx')
    # gstr3BPath_Var.set(r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\venus polypack ind\0
    # .gstSummaryPath_Var.set(r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\venus polypack ind\GST CLAIM SUMMARY -2020-21.xlsx')
    # creditLedgerPath_Var.set(r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\venus polypack ind\Venus polypack Cash & Credit Ledger')
    #
    # fromDate_Var.set('01/07/2021')
    # toDate_Var.set('01/06/2022')
    # precetageIGST_Var.set(18)
    #--------------------------------------------------------
    def generateClaims():
        global path, fromDate, toDate, percentageOfIGST, gstSummaryDataToBeFilled, gstr3BDataToBeFilled, creditLedgerDataToBeFilled

        isThereError = False
        errorName = []

        path = {'GSTR 3B': gstr3BPath_Var.get(),
                'Cash and Credit Ledger': creditLedgerPath_Var.get(),
                'Templet': templetPath_Var.get(),
                'GST Summary': gstSummaryPath_Var.get()}
        fromDate = fromDate_Var.get()
        toDate = toDate_Var.get()
        gstr3BDataToBeFilled = gstr3BPath_CBVar.get()
        creditLedgerDataToBeFilled = creditLedgerPath_CBVar.get()

        gstSummaryDataToBeFilled = gstSummatyPath_CBVar.get()

        labelsAndCb = {
            'GSTR 3B': [gstr3BPath_L, gstr3BDataToBeFilled],
            'Cash and Credit Ledger': [creditLedgerPath_L, creditLedgerDataToBeFilled],
            'Templet': [templetPath_L, True],
            'GST Summary': [gstSummaryPath_L, gstSummaryDataToBeFilled]
        }
        try:
            percentageOfIGST = precetageIGST_Var.get()
        except tkinter.TclError:
            percentageOfIGST = 0

        for entry in path.keys():
            if path[entry] == '' and labelsAndCb[entry][1]:
                isThereError = True
                errorName.append('All Fields Not Filled')
                labelsAndCb[entry][0].configure(fg='#fa1302', bg='#f57971')
            else:
                labelsAndCb[entry][0].configure(fg='#000000', bg='#F0F0F0')

        # if gstSummaryDataToBeFilled:
        #     if ITCAddedCol == '':
        #         isThereError = True
        #         errorName.append('ITC Added Column not given')
        #         ITCAdded_L.configure(fg='#fa1302', bg='#f57971')
        #     else:
        #         ITCAdded_L.configure(fg='#000000', bg='#F0F0F0')
        #
        #     if ITCAdjustedCol == '':
        #         isThereError = True
        #         errorName.append('ITC Audjusted Column not given')
        #         ITCAdjusted_L.configure(fg='#fa1302', bg='#f57971')
        #     else:
        #         ITCAdjusted_L.configure(fg='#000000', bg='#F0F0F0')
        #
        #     if openingBalPlusInputCol == '':
        #         isThereError = True
        #         errorName.append('opening Balance + input column name not given')
        #         openingPlusInputBal_L.configure(fg='#fa1302', bg='#f57971')
        #     else:
        #         openingPlusInputBal_L.configure(fg='#000000', bg='#F0F0F0')

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

        if (percentageOfIGST <= 0 or percentageOfIGST > 100) and gstr3BDataToBeFilled:
            isThereError = True
            errorName.append('Invalid IGST Rate')
            precetageIGST_L.configure(fg='#fa1302', bg='#f57971')
        else:
            precetageIGST_L.configure(fg='#000000', bg='#F0F0F0')

        if isThereError:
            tkinter.messagebox.showwarning('Warning', errorName[0])
        else:
            generateSGSTClaims(fromDate, toDate)


    generate_B = Button(home, name='generateSGSTClaims', text='Generate SGST Claims', command=generateClaims)
    generate_B.grid(row=8, columnspan=4, padx=5, pady=5)

    display_F = LabelFrame(home, text='Claims')
    display_F.grid(column=1, padx=5)


    home.mainloop()
