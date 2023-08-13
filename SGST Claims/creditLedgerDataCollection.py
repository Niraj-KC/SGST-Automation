import os, datetime, pdfplumber
import pandas as pd

def getCreditLedgerData(path):
    os.chdir(path)

    creditLedgerData = {'Claim Period': [],
                        'IGST': [],
                        'CGST': [],
                        'SGST': []}

    temp = {}
    tempDataCollection = {}

    creditLedgerFiles = []
    for file in os.listdir():
        if 'CreditLedger' in file:
            creditLedgerFiles.append(file)

    for pdfFile in creditLedgerFiles:
        with pdfplumber.open(pdfFile) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                print(pdfFile)
                # print(page.page_number)
                for table in tables:
                    for row in table:
                        try:
                            if row[3] != None:
                                cp = datetime.datetime.strptime(row[3], '%b-%y')
                                cp = cp.strftime('%d/%m/%Y')
                                # if row[5] == 'Debit':
                                #     temp[cp] = [row[11], row[12], row[13]]
                                # print(row[5])
                                tempDataCollection[cp] = {}
                                tempDataCollection[cp][row[5]] = [row[11], row[12], row[13]]

                            else:
                                pass
                        except ValueError or TypeError:
                            pass
    for month in tempDataCollection.keys():
        try:
            reqData = tempDataCollection[month]['Debit']
        except KeyError:
            reqData = tempDataCollection[month]['Credit']
        temp[month] = reqData

    for key in temp.keys():
        creditLedgerData['Claim Period'].append(key)
        creditLedgerData['IGST'].append(temp[key][0])
        creditLedgerData['CGST'].append(temp[key][1])
        creditLedgerData['SGST'].append(temp[key][2])

    def convertStrListToFloatList(StrList):
        conList = []
        for strNum in StrList:
            if type(strNum) == str:
                print('String')
                #------ Remove Comma --------------
                strNum = strNum.replace(',', '')
                floNum = float('{:.2f}'.format(float(strNum)))
                conList.append(floNum)
            else:
                # print('not String')
                raise ValueError(f'StrList Element must be String got {type(strNum)} : {strNum}')

        return conList

    creditLedgerData['IGST'] = convertStrListToFloatList(creditLedgerData['IGST'])
    creditLedgerData['CGST'] = convertStrListToFloatList(creditLedgerData['CGST'])
    creditLedgerData['SGST'] = convertStrListToFloatList(creditLedgerData['SGST'])


    creditLedger_df = pd.DataFrame(creditLedgerData)
    creditLedger_df.index = creditLedgerData['Claim Period']
    creditLedger_df.drop(columns='Claim Period', inplace=True)

    return creditLedger_df


if __name__ == '__main__':
    path = r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\Golden Cotton\Jul-17 to Dec-20\Credit Ledger'
    df = getCreditLedgerData(path)
    print(df)