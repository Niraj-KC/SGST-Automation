import openpyxl, os, datetime
from dateutil.relativedelta import relativedelta

import pandas as pd

def startAuditFormatEntry(templetPath, claimPeriod, gstr1DataToBeFilled, gstr1_df, gstr3BDataToBeFilled, gstr3b_df):
    templetFolder = ''.join(
        [f'{f}/' for f in templetPath.replace('\\', '/').split('/')[:-1]])  # TODO remove replace after test runs
    os.chdir(templetFolder)

    def getClaimPeriodStr(claimPeriod):
        listOf31daysMonth = ['01', '03', '05', '07', '08', '10', '12']
        cp_t = []
        for month in claimPeriod:
            date = datetime.datetime.strptime(month, '%b-%y')
            date = datetime.datetime.strftime(date, '%d/%m/%Y')
            cp_t.append(date)
        claimPeriod = cp_t
        lm = claimPeriod[-1].split('/')
        if lm[1] in listOf31daysMonth:
            lm[0] = '31'
        else:
            lm[0] = '30'

        lm = lm[0] + '/' + lm[1] + '/' + lm[2]

        claimPeriodStr = f'From Date {claimPeriod[0].replace("/", ".")} to {lm.replace("/", ".")}'
        return claimPeriodStr

    def getFilename(claimPeriod):
        return f'SGST Claim {claimPeriod[0]} to {claimPeriod[2]}.xlsx'

    fileName = getFilename(claimPeriod)
    if fileName in os.listdir():
        wb = openpyxl.load_workbook(fileName)
    else:
        wb = openpyxl.load_workbook(templetPath)

    sheet1 = wb['Output']
    if gstr3BDataToBeFilled:
        sheet2 = wb['Input']

    claimPeriodStr = getClaimPeriodStr(claimPeriod)
    sheet1['A2'] = claimPeriodStr

    sheet1['A11'], sheet1['A12'], sheet1['A13'] = claimPeriod
    def fillMonthData(month, gstr1_Row, gstr3B_Row_output, gstr3B_Row_input_reverseCharges, gstr3B_Row_input_itc):
        if gstr1DataToBeFilled:
            #----- GSTR1 Data in Output Sheet ---------------
            sheet1[f'P{gstr1_Row}'] = gstr1_df.loc[month, 'basicPrice']
            sheet1[f'Q{gstr1_Row}'] = gstr1_df.loc[month, 'CGST']
            sheet1[f'R{gstr1_Row}'] = gstr1_df.loc[month, 'SGST']
            sheet1[f'S{gstr1_Row}'] = gstr1_df.loc[month, 'IGST']

        if gstr3BDataToBeFilled:
            #------- GSTR-3B Data in Output Sheet ------------
            sheet1[f'P{gstr3B_Row_output}'] = gstr3b_df.loc[month, 'outBasicPrice']
            sheet1[f'Q{gstr3B_Row_output}'] = gstr3b_df.loc[month, 'outCGST']
            sheet1[f'R{gstr3B_Row_output}'] = gstr3b_df.loc[month, 'outSGST']
            sheet1[f'S{gstr3B_Row_output}'] = gstr3b_df.loc[month, 'outIGST']

            #-------- GSTR-3B Data in Input Sheet ------------------
            #--------- Revers Charge Data --------------------
            sheet2[f'Q{gstr3B_Row_input_reverseCharges}'] = gstr3b_df.loc[month, 'reCGST']
            sheet2[f'R{gstr3B_Row_input_reverseCharges}'] = gstr3b_df.loc[month, 'reSGST']
            sheet2[f'S{gstr3B_Row_input_reverseCharges}'] = gstr3b_df.loc[month, 'reIGST']
            #-------- ITC Data in Input Sheet----------------
            sheet2[f'Q{gstr3B_Row_input_itc}'] = gstr3b_df.loc[month, 'itcCGST']
            sheet2[f'R{gstr3B_Row_input_itc}'] = gstr3b_df.loc[month, 'itcSGST']
            sheet2[f'S{gstr3B_Row_input_itc}'] = gstr3b_df.loc[month, 'itcIGST']


    if gstr3BDataToBeFilled and gstr1DataToBeFilled:
        gstr1_startingRow = 22
        gstr3B_startingRow_output = 33

        gstr3B_startingRow_input_reverseCharges = 33
        gstr3B_startingRow_input_itc = 53

        for month in claimPeriod:
            try:
                fillMonthData(month, gstr1_startingRow, gstr3B_startingRow_output, gstr3B_startingRow_input_reverseCharges, gstr3B_startingRow_input_itc)
            except KeyError:
                print(f'data missing For {month}')

            gstr1_startingRow += 1
            gstr3B_startingRow_output += 1
            gstr3B_startingRow_input_reverseCharges += 1
            gstr3B_startingRow_input_itc += 1

    wb.save(fileName)
    print(fileName)






if __name__ == '__main__':
    from GSTR3BDataCollection import getGSTR3BData
    from GSTR1DataCollection import getGSTR1Data

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


    path = r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\venus polypack ind\Audit Format\SGST Claim (Audit Format templet).xlsx'

    fromDate = '01/07/2021'
    toDate = '30/06/2022'

    cp = getClaimPeriodList(fromDate, toDate)

    gstr1_df = getGSTR1Data(r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\venus polypack ind\GSTR 1')
    gstr3b_df = getGSTR3BData(r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\venus polypack ind\Venus polypack 3B_')

    for m in cp:
        startAuditFormatEntry(path, m, True, gstr1_df, True, gstr3b_df)