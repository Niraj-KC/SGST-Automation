import pdfplumber, datetime
import pandas as pd
import os, re

def getGSTR1Data(path):
    os.chdir(path)
    gstr1Data = {
        'month': [],
        'basicPrice': [],
        'IGST': [],
        'SGST': [],
        'CGST': [],
    }
    def getFloate(strRawVale):
        return re.findall("\d+\.\d+", strRawVale)[0]

    def toFloat(StrValue):
        if '\n' in StrValue:
            return float('{:.2f}'.format(float(StrValue.split('\n')[-1].replace(',', ''))))
        else:
            return float('{:.2f}'.format(float(StrValue.replace(',', ''))))

    def getDate(month, year):
        lastQtr = ['January', 'February', 'March']

        if month in lastQtr:
            year = '20' + year.split('-')[1]
        else:
            year = year.split('-')[0]

        date = f'01/{month}/{year}'
        date = datetime.datetime.strptime(date, '%d/%B/%Y')
        date = date.strftime('%b-%y')

        return date


    pdfList = []
    for pdfFile in os.listdir():
        if 'pdf' in pdfFile.split('.'):
            pdfList.append(pdfFile)

    for pdfFile in pdfList:
        print(pdfFile)
        with pdfplumber.open(pdfFile) as pdf:
            page = pdf.pages[0]

            tables = page.extract_tables()

            month = tables[0][1][1].split('(')[0]
            year = tables[0][0][1]
            date = getDate(month, year)
            gstr1Data['month'].append(date)
            reqTable = tables[2]
            if reqTable[0][0] == 'Description':
                print('New Format')
                reqTable = [row for row in reqTable if row[0] != '']

                for idx, reqRow in enumerate(reqTable):
                    if '4A' in reqRow[0]:
                        reqRow = reqTable[idx+1]
                        print(reqRow)
                        gstr1Data['basicPrice'].append(toFloat(reqRow[3]))
                        gstr1Data['IGST'].append(toFloat(reqRow[4]))
                        gstr1Data['SGST'].append(toFloat(reqRow[6]))
                        gstr1Data['CGST'].append(toFloat(reqRow[5]))

                        break # in code

            else:
                print('old format')
                reqRow = reqTable[1]
                gstr1Data['basicPrice'].append(toFloat(reqRow[2]))
                gstr1Data['IGST'].append(toFloat(reqRow[3]))
                gstr1Data['SGST'].append(toFloat(reqRow[5]))
                gstr1Data['CGST'].append(toFloat(reqRow[4]))

    gstr1_df = pd.DataFrame(gstr1Data)
    gstr1_df.index = gstr1Data['month']
    gstr1_df.drop('month', axis=1, inplace=True)

    return gstr1_df








if __name__ == '__main__':
    path = r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\Silk woven sack\GSTR 1'

    df = getGSTR1Data(path)
    print(df)