from tkinter import *
from Resource.TKinterLabelEntry import LabelEntry
from Resource import Validate
import datetime
from dateutil.relativedelta import relativedelta









if __name__ == '__main__':

    root = Tk()

    templetPath_Element = LabelEntry(root, name='templetPath', text='           SGST Claim Templet Path  :', row=0, column=0, lableWidth=27, browseButton=True, browsingType='File', title='Select SGST Claim Audit Format Templet', fileType='*.xlsx')
    gstr3bPath_Element = LabelEntry(root, name='gstr3bPath', text='GSTR-3B Folder Path   :', row=2, column=0, lableWidth=23, checkButton=True, browseButton=True, browsingType='Directory', title='Select GSTR-3B Folder')
    summaryPath_Element = LabelEntry(root, name='summaryPath', text='GST Summary Path    :', row=3, column=0, lableWidth=23, checkButton=True, browseButton=True, browsingType='File', title='Select GST Summary File', fileType='*.xlsx')
    creditLedgerPath_Element = LabelEntry(root, name='creditLedgerPath', text='Credit Ledger Folder Path :', row=4, column=0, lableWidth=23, checkButton=True, browseButton=True, browsingType='Directory', title='Select Credit Ledger Folder')

    fromDate_Element = LabelEntry(root, name='fromDate', text='From :', row=5, column=0, entryWidth=13)
    toDate_Element = LabelEntry(root, name='toDate', text='To   :', row=6, column=0, entryWidth=13)

    #---Date Format lable-------------------
    fdf_L = Label(root, text='e.g. :dd/mm/yyyy')
    fdf_L.grid(row=5, column=2, sticky=E)
    tdf_L = Label(root, text='e.g. :dd/mm/yyyy')
    tdf_L.grid(row=6, column=2, sticky=E)

    igstRate_Element = LabelEntry(root, name='IGSTRate', text='IGST Rate  :', row=7, column=0, entryWidth=10)
    igstRate_Element.entry_var.set(0)

    exportInqury_var = BooleanVar()
    exportInqury_Element = Checkbutton(root, variable=exportInqury_var, text='Export data row?', onvalue=True, offvalue=False)
    exportInqury_Element.grid(row=8, column=0, rowspan=2)
    exportInqury_var.set(False)

    industryType_var = Variable()
    industryType1_RB = Radiobutton(root, text='Polypack', variable=industryType_var, value='polypack')
    industryType1_RB.grid(row=8, column=1, sticky=W)

    industryType2_RB = Radiobutton(root, text='Cotton Gening', variable=industryType_var, value='geneing')
    industryType2_RB.grid(row=9, column=1, sticky=W)

    industryType_var.set(None)

    def validateFileds():
        global templetPath, gstr3bPath, summaryPath, creditLedgerPath, igstRate, fromDate, toDate, gstr3bDataToBeFilled, summaryDataToBeFilled, creditLedgerDataToBeFilled, industryType, exportInqury
        isThereError = False
        templetPath = templetPath_Element.entry_var.get()

        gstr3bPath = gstr3bPath_Element.entry_var.get()
        summaryPath = summaryPath_Element.entry_var.get()
        creditLedgerPath = creditLedgerPath_Element.entry_var.get()

        summaryDataToBeFilled = summaryPath_Element.checkButton_var.get()
        gstr3bDataToBeFilled = gstr3bPath_Element.checkButton_var.get()
        creditLedgerDataToBeFilled = creditLedgerPath_Element.checkButton_var.get()

        igstRate = igstRate_Element.entry_var.get()
        exportInqury = exportInqury_var.get()
        industryType = industryType_var.get()


        if not Validate.path(templetPath):
            templetPath_Element.indicatError()
            isThereError = True
        else:
            templetPath_Element.noError()


        if gstr3bDataToBeFilled:
            if not Validate.path(gstr3bPath):
                gstr3bPath_Element.indicatError()
                isThereError = True
            else:
                gstr3bPath_Element.noError()

            if not Validate.tax(float(igstRate)):
                global igstError_L
                igstRate_Element.indicatError()
                isThereError = True
                igstError_L = Label(root, text='IGST Can\'t be 0')
                igstError_L.grid(row=7, column=1, sticky=E)
                igstError_L.configure(bg='#f8c0c0', fg='#fa1302')
            else:
                igstRate_Element.noError()
                try:
                    igstError_L.destroy()
                except:
                    pass

        else:
            gstr3bPath_Element.noError()
            igstRate_Element.noError()
            try:
                igstError_L.destroy()
            except:
                pass


        if summaryDataToBeFilled:
            if not Validate.path(summaryPath):
                summaryPath_Element.indicatError()
                isThereError = True
            else:
                summaryPath_Element.noError()

            print(industryType)
            if industryType == 'None':
                print('=====')
                global industryTypeError_L
                industryType1_RB.configure(fg='#fa1302', bg='#f8c0c0')
                industryType2_RB.configure(fg='#fa1302', bg='#f8c0c0')
                industryTypeError_L = Label(root, text='Select Industry Type')
                industryTypeError_L.grid(row=8, column=2, rowspan=2)
                industryTypeError_L.configure(fg='#fa1302', bg='#f8c0c0')
                isThereError = True

            else:
                industryType1_RB.configure(fg='#000000', bg='#f0f0f0')
                industryType2_RB.configure(fg='#000000', bg='#f0f0f0')

                try:
                    industryTypeError_L.destroy()
                except:
                    pass



        else:
            summaryPath_Element.noError()
            industryType1_RB.configure(fg='#000000', bg='#f0f0f0')
            industryType2_RB.configure(fg='#000000', bg='#f0f0f0')

            try:
                industryTypeError_L.destroy()
            except:
                pass

        if creditLedgerDataToBeFilled:
            if not Validate.path(creditLedgerPath):
                creditLedgerPath_Element.indicatError()
                isThereError = True
            else:
                creditLedgerPath_Element.noError()
        else:
            creditLedgerPath_Element.noError()


        fromDate = fromDate_Element.entry_var.get()
        toDate = toDate_Element.entry_var.get()

        if not Validate.dateFormat(fromDate, '%d/%m/%Y'):
            fromDate_Element.indicatError()
            fdf_L.configure(fg='#fa1302', bg='#f8c0c0')
            isThereError = True
        else:
            fromDate_Element.noError()
            fdf_L.configure(fg='#000000', bg='#f0f0f0')

        if not Validate.dateFormat(toDate, '%d/%m/%Y'):
            toDate_Element.indicatError()
            tdf_L.configure(fg='#fa1302', bg='#f8c0c0')
            isThereError = True
        else:
            toDate_Element.noError()
            tdf_L.configure(fg='#000000', bg='#f0f0f0')
        if Validate.dateFormat(fromDate, '%d/%m/%Y') and Validate.dateFormat(toDate, '%d/%m/%Y'):
            global error_L
            if not Validate.dateRange(fromDate, toDate):
                fromDate_Element.indicatError()
                toDate_Element.indicatError()
                error_L = Label(root, text='Date Range Invalid')
                error_L.grid(row=5, column=1, rowspan=2, sticky=E)
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


    def getData():
        global gstr3b_df, gstSummary_df, creditLedger_df
        if gstr3bDataToBeFilled:
            from GSTR3BDataCollection import getGSTR3BData
            gstr3b_df = getGSTR3BData(gstr3bPath, float(igstRate))
            Label(display_F, text='Collecting GSTR3B Data')
        else:
            gstr3b_df = None

        if summaryDataToBeFilled:
            from SummaryDataCollection import getGSTSummaryData
            gstSummary_df = getGSTSummaryData(summaryPath)
            Label(display_F, text='Collecting GST Summary Data')

        else:
            gstSummary_df = None

        if creditLedgerDataToBeFilled:
            from creditLedgerDataCollection import getCreditLedgerData
            creditLedger_df = getCreditLedgerData(creditLedgerPath)
            Label(display_F, text='Collecting Credit Ledger Data')

        else:
            creditLedger_df = None

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

    def getClaimPeriodStr(claimPeriod):
        listOf31daysMonth = ['01', '03', '05', '07', '08', '10', '12']
        lm = claimPeriod[-1].split('/')
        if lm[1] in listOf31daysMonth:
            lm[0] = '31'
        else:
            lm[0] = '30'

        lm = lm[0] + '/' + lm[1] + '/' + lm[2]

        claimPeriodStr = f'{claimPeriod[0].replace("/", ".")} to {lm.replace("/", ".")}'
        return claimPeriodStr

    def generateSGSTClaims():
        global templetPath, gstr3bPath, summaryPath, creditLedgerPath, igstRate, fromDate, toDate, gstr3bDataToBeFilled, summaryDataToBeFilled, creditLedgerDataToBeFilled, industryType, exportInqury

        if not validateFileds():
            print('START')
            from ExcelEntry import startExcellEntry
            getData()
            claimPeriod_list = getClaimPeriodList(fromDate, toDate)
            print(claimPeriod_list)
            for claimPeriod in claimPeriod_list:

                startExcellEntry(claimPeriod, templetPath, gstr3bDataToBeFilled, gstr3b_df, summaryDataToBeFilled, gstSummary_df,
                    creditLedgerDataToBeFilled, creditLedger_df, display_F, exportInqury, industryType)
                Label(display_F, text=getClaimPeriodStr(claimPeriod))


        else:
            print('Error')


    Button(root, text='Generate SGST Claims', command=generateSGSTClaims).grid(columnspan=4)

    display_F = LabelFrame(root)
    display_F.grid(columnspan=4)


    templetPath_Element.entry_var.set(r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\Golden Cotton\SGST Claims\New folder\GST Claim (templet).xlsx')
    gstr3bPath_Element.entry_var.set(r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\Golden Cotton\Jan-21 to Jul-22\GSTR 3B')
    summaryPath_Element.entry_var.set(r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\Golden Cotton\GST CLAIM SUMMARY.xlsx')
    creditLedgerPath_Element.entry_var.set(r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\Golden Cotton\Jan-21 to Jul-22\Cash & Cedit Ledger')
    fromDate_Element.entry_var.set('01/01/2021')
    toDate_Element.entry_var.set('30/06/2022')
    igstRate_Element.entry_var.set(5)

    industryType2_RB.select()
    exportInqury_var.set(False)



    root.mainloop()
