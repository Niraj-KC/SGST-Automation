import pandas as pd
import pdfplumber, os, datetime

def getCreditLedgerData(path):
    os.chdir(path)

    creditLedgerData = {'Claim Period': [],
                        'IGST': [],
                        'CGST': [],
                        'SGST': []}

    temp = {}
    tempDataCOllection = {}

    creditLedgerFiles = []
    for file in os.listdir():
        if 'CreditLedger' in file:
            creditLedgerFiles.append(file)

    for pdfFile in creditLedgerFiles:
        with pdfplumber.open(pdfFile) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                print(pdfFile)
                print(page.page_number)
                for table in tables:
                    for row in table:
                        try:
                            if row[3] != None:
                                cp = datetime.datetime.strptime(row[3], '%b-%y')
                                cp = cp.strftime('%d/%m/%Y')
                                # if row[5] == 'Debit':
                                #     temp[cp] = [row[11], row[12], row[13]]
                                print(row[5])
                                tempDataCOllection[cp] = {}
                                tempDataCOllection[cp][row[5]] = [row[11], row[12], row[13]]

                            else:
                                pass
                        except ValueError or TypeError:
                            pass
    for month in tempDataCOllection.keys():
        try:
            reqData = tempDataCOllection[month]['Debit']
        except KeyError:
            reqData = tempDataCOllection[month]['Credit']
        temp[month] = reqData

    for key in temp.keys():
        creditLedgerData['Claim Period'].append(key)
        creditLedgerData['IGST'].append(temp[key][0])
        creditLedgerData['CGST'].append(temp[key][1])
        creditLedgerData['SGST'].append(temp[key][2])

    creditLedger_df = pd.DataFrame(creditLedgerData)
    creditLedger_df.index = creditLedgerData['Claim Period']
    return creditLedger_df



if __name__ == '__main__':
    #from main import path
    path = r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\Atulya Polypack\2021-2022\Atulya Polypack cash & credit Ledger'
    creditLedger_df = getCreditLedgerData(path)

    print(creditLedger_df)
    print(creditLedger_df['Claim Period'])


