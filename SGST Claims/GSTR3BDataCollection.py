import os, re, pdfplumber, datetime
import pandas as pd

def getGSTR3BData(path, IGSTrate):
    os.chdir(path)
    gstr3bData = {'Claim Period': [],
                  'Total taxable value': [],
                  'IGST taxable value': [],
                  'IGST': [],
                  'SGST taxable value': [],
                  'SGST': [],
                  }

    def getFloate(strRawVale):
        return re.findall("\d+\.\d+", strRawVale)[0]

    def removeEnter(str):
        return re.sub(" \n", " ", str)


    def toFloat(StrValue):
        if '\n' in StrValue:
            return float('{:.2f}'.format(float(StrValue.split('\n')[-1])))
        else:
            return float('{:.2f}'.format(float(StrValue)))

    def getDate(month, year):
        lastQtr = ['January', 'February', 'March']

        if month in lastQtr:
            year = '20' + year.split('-')[1]
        else:
            year = year.split('-')[0]

        date = f'01/{month}/{year}'
        date = datetime.datetime.strptime(date, '%d/%B/%Y')
        date = date.strftime('%d/%m/%Y')

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
            table = tables[0]
            date = getDate(table[1][1], table[0][1])

            output_df = pd.DataFrame(tables[2])

            output_df.columns = ['Nature of Supplies', 'Total Taxable value', 'Integrated Tax',
                                 'Central Tax', 'State/UT Tax', 'Cess']

            output_df.drop(0, inplace=True)

            idx = [row[0] for row in tables[2]]
            idx.pop(0)
            idx = [removeEnter(i) for i in idx]

            output_df.index = idx

            # print(output_df.columns)
            # print(output_df.index)

            totalTaxableValue = toFloat((output_df.loc[
                '(a) Outward taxable supplies (other than zero rated, nil rated and exempted)', 'Total Taxable value']))

            IGST = toFloat((getFloate(output_df.loc[
                '(a) Outward taxable supplies (other than zero rated, nil rated and exempted)', 'Integrated Tax'])))

            SGST = toFloat((output_df.loc[
                '(a) Outward taxable supplies (other than zero rated, nil rated and exempted)', 'State/UT Tax']))

            IGSTTaxableValue = toFloat(str(IGST*100/IGSTrate))
            SGSTTaxableValue = totalTaxableValue-IGSTTaxableValue


            gstr3bData['Claim Period'].append(date)
            gstr3bData['Total taxable value'].append(totalTaxableValue)
            gstr3bData['IGST taxable value'].append(IGSTTaxableValue)
            gstr3bData['IGST'].append(IGST)
            gstr3bData['SGST taxable value'].append(SGSTTaxableValue)
            gstr3bData['SGST'].append(SGST)

    gstr3b_df = pd.DataFrame(gstr3bData)
    gstr3b_df.index = gstr3bData['Claim Period']
    gstr3b_df.drop(columns='Claim Period', inplace=True)
    return gstr3b_df



if __name__ == '__main__':
    path = r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\Golden Cotton\GSTR-3B'
    df = getGSTR3BData(path, 5)
    print(df.iloc[3])
