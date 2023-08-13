import openpyxl, os, datetime, pandas
from tkinter import Label


def startExcellEntry(claimPeriod, templetPath, gstr3BDataToBeFilled, gst3B_df, gstSummaryDataToBeFilled, gstSummary_df,
                    creditLedgerDataToBeFilled, creditLedger_df, frame, exportRow, industryType):
    templetFolder = ''.join(
        [f'{f}/' for f in templetPath.replace('\\', '/').split('/')[:-1]])
    os.chdir(templetFolder)

    print(claimPeriod)


    if exportRow:
        noOfRowToAdd = 1
    else:
        noOfRowToAdd = 0

    def toFloat(value):
        return float('{:.2f}'.format(float(value)))

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

    def startEntry(month):

        if gstr3BDataToBeFilled:
            # IGST Taxable value
            sheet2[f'{cp_sdCol[month][0]}{6 + noOfRowToAdd}'] = gst3B_df.loc[month, 'IGST taxable value']
            # IGST
            sheet2[f'{cp_sdCol[month][1]}{6 + noOfRowToAdd}'] = gst3B_df.loc[month, 'IGST']

            # SGST Taxable value
            sheet2[f'{cp_sdCol[month][2]}{6 + noOfRowToAdd}'] = gst3B_df.loc[month, 'SGST taxable value']
            # SGST
            sheet2[f'{cp_sdCol[month][3]}{6 + noOfRowToAdd}'] = gst3B_df.loc[month, 'SGST']

        if gstSummaryDataToBeFilled:
            # print('SUMMARY FILLING')

            # opening Balance + Input
            openingBalPlusInput = gstSummary_df.loc[month, 'Opening Bal SGST'] + gstSummary_df.loc[month, 'Eligible SGST input']

            # All other RMC utilized
            if industryType == 'polypack':
                sheet2[f'{cp_sdCol[month][3]}{8 + noOfRowToAdd}'] = min(gstSummary_df.loc[month, 'Eligible SGST Adjusted againnst in eligible goods'],
                                                                        openingBalPlusInput)
            elif industryType == 'geneing':
                sheet2[f'{cp_sdCol[month][3]}{8 + noOfRowToAdd}'] = gstSummary_df.loc[month, 'Eligible SGST Adjusted againnst in eligible goods']

            # ITC added during the month
            ITCAdded = gstSummary_df[['Eligible SGST input', 'SGST Paid', 'Eligible SGST RCM  input']].sum(axis='columns')
            sheet2[f'{cp_sdCol[month][3]}{12 + noOfRowToAdd}'] = toFloat(ITCAdded.loc[month])

            # ITC adjuste during the QTR
            ITCAdjusted = gstSummary_df[['Eligible SGST Adjusted againnst in eligible goods',
                                         'Eligible SGST Adjusted againnst in Non eligible goods',
                                         'RCM SGST Utilised in eligible goods',
                                         'RCM SGST Utilised in non eligible goods']].sum(axis='columns')

            sheet2[f'{cp_sdCol[month][3]}{14 + noOfRowToAdd}'] = toFloat(ITCAdjusted.loc[month])

        # if SGST Paid o/p > actual
        # sheet2[f'{cp_sdCol[cp][3]}12'] = df.iloc[df[(df['Claim Period '] == cp)].index].get('ITC added during the month ').values[0]

    # print(gstSummary_df.keys)
    print(claimPeriod[0])

    if gstSummaryDataToBeFilled:
        openingBal = gstSummary_df[['Opening Bal SGST', 'Opening Bal SGST RCM']].sum(axis='columns')
        sheet2[f'E{11 + noOfRowToAdd}'] = toFloat(openingBal.loc[claimPeriod[0]])

    if gstr3BDataToBeFilled or gstSummaryDataToBeFilled:
        for cp in claimPeriod:
            print(cp)
            startEntry(cp)

    if creditLedgerDataToBeFilled:
        try:
            creditLedger_idx = claimPeriod[-1]
            sheet2[f'Q{23 + noOfRowToAdd}'] = creditLedger_df.loc[creditLedger_idx, 'IGST']
            sheet2[f'Q{24 + noOfRowToAdd}'] = creditLedger_df.loc[creditLedger_idx, 'CGST']
            sheet2[f'Q{25 + noOfRowToAdd}'] = creditLedger_df.loc[creditLedger_idx, 'SGST']
        except:
            sheet2[f'Q{23 + noOfRowToAdd}'] = 0
            sheet2[f'Q{24 + noOfRowToAdd}'] = 0
            sheet2[f'Q{25 + noOfRowToAdd}'] = 0

    wb.save(f'GST Claim {claimPeriodStr}.xlsx')
    Label(frame, text=f'GST Claim {claimPeriodStr}.xlsx')

    print('Saved')


