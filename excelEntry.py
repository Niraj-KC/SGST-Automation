import openpyxl, os, datetime, pandas
from tkinter import Label
def excellEntery(claimPeriod, templetPath, gstr3BDataToBeFilled, gst3B_df, gstSummaryDataToBeFilled, gstSummary_df, creditLedgerDataToBeFilled, creditLedger_df, frame, exportRow, indutryType):
    templetFolder = ''.join([f'{f}/' for f in templetPath.replace('\\', '/').split('/')[:-1]])   # TODO remove replae after test runs
    os.chdir(templetFolder)

    print(claimPeriod)


    if exportRow:
        noOfRowToAdd = 1
    else:
        noOfRowToAdd = 0

    def toFloat(value):
        if type(value) == str:
            return float('{:.2f}'.format(float(value.replace(',', ''))))
        elif type(value) == int:
            return float('{:.2f}'.format(float(value)))
        elif type(value) == float:
            return value
        else:
            try:
                return float('{:.2f}'.format(float(value[0].replace(',', ''))))
            except AttributeError:
                return float('{:.2f}'.format(float(value[0])))


    def getClaimPeriodStr(claimPreiod):
        listOf31daysMonth = ['01', '03', '05', '07', '08', '10', '12']
        lm = claimPeriod[-1].split('/')
        if lm[1] in listOf31daysMonth:
            lm[0] = '31'
        else:
            lm[0] = '30'

        lm = lm[0] + '/' + lm[1] + '/' + lm[2]

        claimPeriodStr = f'{claimPeriod[0].replace("/", ".")} to {lm.replace("/", ".")}'
        return claimPeriodStr

    claimPeriodStr = getClaimPeriodStr(claimPeriod)

    if f'GST Claim {claimPeriodStr}.xlsx' in os.listdir():
        wb = openpyxl.load_workbook(f'GST Claim {claimPeriodStr}.xlsx')
    else:
        wb = openpyxl.load_workbook(templetPath)

        sheet1 = wb['DataSheet1']
        sheet1['B11'] = claimPeriodStr
    row = 14
    for month in claimPeriod:
        sheet1 = wb['DataSheet1']
        month = datetime.datetime.strptime(month, '%d/%m/%Y')
        sheet1[f'A{row}'] = month
        row += 1

    sheet2 = wb['DataSheet2']

    summaryDataCol = [['B', 'C', 'D', 'E'], ['H', 'I', 'J', 'K'], ['N', 'O', 'P', 'Q']]
    cp_sdCol = dict(zip(claimPeriod, summaryDataCol))
    # print(gstSummary_df.keys())



    def startEntry(cp):

        if gstr3BDataToBeFilled:
            gst3B_idx = gst3B_df[(gst3B_df['Claim Period'] == cp)].index
            #IGST Taxable value
            sheet2[f'{cp_sdCol[cp][0]}{6+noOfRowToAdd}'] = toFloat(gst3B_df.loc[gst3B_idx, 'IGST taxable value'])

            #IGST
            sheet2[f'{cp_sdCol[cp][1]}{6+noOfRowToAdd}'] = toFloat(gst3B_df.loc[gst3B_idx, 'IGST'])

            #SGST Taxable value
            sheet2[f'{cp_sdCol[cp][2]}{6+noOfRowToAdd}'] = toFloat(gst3B_df.loc[gst3B_idx, 'SGST taxable value'])

            #SGST
            sheet2[f'{cp_sdCol[cp][3]}{6+noOfRowToAdd}'] = toFloat(gst3B_df.loc[gst3B_idx, 'SGST'])

        if gstSummaryDataToBeFilled: # TODO fix Summary Error
            print('SUMMARY FILLING')
            gstSummary_idx = gstSummary_df[(gstSummary_df['Claim Period '] == cp)].index

            #opening Balance + Input
            openingBalPlusInput = toFloat(gstSummary_df.loc[gstSummary_idx, 'Opening Bal SGST ']) + toFloat(gstSummary_df.loc[gstSummary_idx, 'Eligible SGST input '])

            #All other RMC utilized
            if indutryType == 'polypack':
                sheet2[f'{cp_sdCol[cp][3]}{8+noOfRowToAdd}'] = toFloat(min(gstSummary_df.loc[gstSummary_idx, 'Eligible SGST Adjusted againnst in eligible goods'],
                                                    openingBalPlusInput))
            elif indutryType == 'geneing':
                sheet2[f'{cp_sdCol[cp][3]}{8 + noOfRowToAdd}'] = gstSummary_df.loc[gstSummary_idx, 'Eligible SGST Adjusted againnst in eligible goods']


            #ITC added during the month
            ITCAdded = gstSummary_df[['Eligible SGST input ', 'SGST Paid ', 'Eligible SGST RCM  input ']].sum(axis='columns')
            sheet2[f'{cp_sdCol[cp][3]}{12+noOfRowToAdd}'] = toFloat(ITCAdded.loc[gstSummary_idx])


            #ITC adjuste during the QTR
            ITCAdjusted = gstSummary_df[['Eligible SGST Adjusted againnst in eligible goods',
       'Eligible SGST Adjusted againnst in Non eligible goods',
       'RCM SGST Utilised in eligible goods',
       'RCM SGST Utilised in non eligible goods']].sum(axis='columns')

            sheet2[f'{cp_sdCol[cp][3]}{14+noOfRowToAdd}'] = toFloat(ITCAdjusted.loc[gstSummary_idx])


        # if SGST Paid o/p > actual
        # sheet2[f'{cp_sdCol[cp][3]}12'] = df.iloc[df[(df['Claim Period '] == cp)].index].get('ITC added during the month ').values[0]

    # print(gstSummary_df.keys)
    print(claimPeriod[0])

    if gstSummaryDataToBeFilled:
        cp = gstSummary_df['Claim Period '].to_dict()
        ob = gstSummary_df['Opening Bal SGST '].to_dict()
        cp = [cp[k] for k in cp.keys()]
        ob = [ob[k] for k in ob.keys()]

        df = dict(zip(cp, ob))
        sheet2[f'E{11+noOfRowToAdd}'] = toFloat(df[claimPeriod[0]])

    if gstr3BDataToBeFilled or gstSummaryDataToBeFilled:
        for cp in claimPeriod:
            print(cp)
            startEntry(cp)

    if creditLedgerDataToBeFilled:
        try:
            creditLedger_idx = creditLedger_df[(creditLedger_df['Claim Period'] == claimPeriod[-1])].index
            sheet2[f'Q{23+noOfRowToAdd}'] = toFloat(creditLedger_df.loc[creditLedger_idx, 'IGST'])
            sheet2[f'Q{24+noOfRowToAdd}'] = toFloat(creditLedger_df.loc[creditLedger_idx, 'CGST'])
            sheet2[f'Q{25+noOfRowToAdd}'] = toFloat(creditLedger_df.loc[creditLedger_idx, 'SGST'])
        except IndexError:
            sheet2[f'Q{23+noOfRowToAdd}'] = 0
            sheet2[f'Q{24+noOfRowToAdd}'] = 0
            sheet2[f'Q{25+noOfRowToAdd}'] = 0



    wb.save(f'GST Claim {claimPeriodStr}.xlsx')
    Label(frame, text=f'GST Claim {claimPeriodStr}.xlsx')
    
    print('Saved')

if __name__ == '__main__':
    # from main import folderPath, gst3B_df, gstSummary_df
    from  gstSummaryDataCollection import gstSummary_df
    from  GSTR3BDataCollection import collectGSTR3BData, gst3bFolder_path
    claimPeriod = ['01/04/2021', '01/05/2021', '01/06/2021']

    gst3B_df = collectGSTR3BData(18, gst3bFolder_path)
    templetPath =  r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\Natural Technofab\2021-2022'

    excellEntery(['01/01/2022', '01/02/2022', '01/03/2022'], templetPath,'templet.xlsx', gst3B_df, gstSummary_df)