import openpyxl, os, datetime, pandas
from dateutil.relativedelta import relativedelta


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

    return claimPeriod_list


def startSummaryExcelEntry(summaryPath, startingRow, fromDate, toDate, gstr3BDataToBeFilled, SGSTPaid_df, creditLedgerDataToBeFilled, creditLedger_df):

    dataCol = {
        'Claim Period': 'B',
        'SGST Paid': 'E',
        'sgst as per Credit Ledger': 'T'
    }
    claimPeriodList = getClaimPeriodList(fromDate, toDate)

    wb = openpyxl.load_workbook(summaryPath)
    sheet1 = wb['Sheet1']

    rowCount = 1
    row = startingRow

    for date in claimPeriodList:
        sheet1[f"{dataCol['Claim Period']}{row}"] = date
        # print(f"{date} in {dataCol['Claim Period']}{row}")

        date = datetime.datetime.strptime(date, '%b-%y')
        date = date.strftime('%d/%m/%Y')

        if gstr3BDataToBeFilled:
            sheet1[f"{dataCol['SGST Paid']}{row}"] = SGSTPaid_df.loc[date, 'SGST Paid']

        if creditLedgerDataToBeFilled:
            sheet1[f"{dataCol['sgst as per Credit Ledger']}{row}"] = creditLedger_df.loc[date, 'SGST']


        if rowCount == 3:
            row += 2
            rowCount = 1
        else:
            row += 1
            rowCount += 1

    savePath = summaryPath.split('/')
    savePath.pop(-1)
    savePath = r''.join(f'{p}\\' for p in savePath)

    os.chdir(savePath)
    wb.save('GST CLAIM SUMMARY (trial).xlsx')



if __name__ == '__main__':
    from creditLedgerDataCollection import getCreditLedgerData
    from SGSTPaid import getSGSTPaid

    startingRow = 8
    path = r"C:\Users\Lenovo1\Desktop\test\GST CLAIM SUMMARY.xlsx"

    formDate = '01/04/2021'
    toDate = '01/03/2022'

    gstr3BDataToBeFilled = True
    SGSTPaid_df = getSGSTPaid(r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\Atulya Polypack\2021-2022\Atulya Polypack 3B')
    creditLedgerDataToBeFilled = True
    creditLedger_df = getCreditLedgerData(r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\Atulya Polypack\2021-2022\Atulya Polypack cash & credit Ledger')

    startSummaryExcelEntry(path, startingRow, formDate, toDate, gstr3BDataToBeFilled, SGSTPaid_df, creditLedgerDataToBeFilled, creditLedger_df)


