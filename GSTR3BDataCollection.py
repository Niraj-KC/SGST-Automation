import pdfplumber, datetime
import pandas as pd
import os, re


def collectGSTR3BData(IGST, path):

    lastQtr = ['January', 'February', 'March']

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
        return float('{:.2f}'.format(float(StrValue)))

    os.chdir(path)

    pdfList = []
    for pdfFile in os.listdir():
        if 'pdf' in pdfFile.split('.'):
            pdfList.append(pdfFile)

    for pdfFile in pdfList:

        with pdfplumber.open(pdfFile) as pdf:
            page = pdf.pages[0]
            tables = page.extract_tables()

        # print(tables[0])
        # print(tables[2][0])


        gstr3b_df = pd.DataFrame(tables[2])

        # col = tables[2][0]
        # col[2] = 'Integrated \nTax'
        gstr3b_df.columns = ['Nature of Supplies', 'Total Taxable value', 'Integrated Tax', 'Central Tax', 'State/UT Tax', 'Cess']
        gstr3b_df.drop(0, inplace=True)

        idx = [removeEnter(row[0]) for row in tables[2]]
        idx.pop(0)

        gstr3b_df.index = idx

        # print(gstr3b_df.index)
        # print(gstr3b_df.columns)

        year = tables[0][0][1]
        month = tables[0][1][1]

        if month in lastQtr:
            year = '20'+year.split('-')[1]
        else:
            year = year.split('-')[0]

        date = f'01/{month}/{year}'
        date = datetime.datetime.strptime(date, '%d/%B/%Y')
        date = date.strftime('%d/%m/%Y')

        # print(gstr3b_df.keys())
        # print(gstr3b_df.iloc[gstr3b_df[(gstr3b_df['Nature of Supplies'] == gstr3b_df['Nature of Supplies'].to_dict()[1])].index].get('Total taxable \nvalue').values)
        # print(gstr3b_df['Nature of Supplies'].to_dict())
        #'Integrated \nTax'
        igstTV = toFloat(toFloat(getFloate(gstr3b_df.loc['(a) Outward taxable supplies (other than zero rated, nil rated and exempted)', 'Integrated Tax']))/IGST*100)
        sgstTV = toFloat(toFloat(getFloate(gstr3b_df.loc['(a) Outward taxable supplies (other than zero rated, nil rated and exempted)', 'Total Taxable value']))) - igstTV

        gstr3bData['Claim Period'].append(date)
        gstr3bData['Total taxable value'].append(toFloat(float(gstr3b_df.loc['(a) Outward taxable supplies (other than zero rated, nil rated and exempted)', 'Total Taxable value'])))
        gstr3bData['IGST taxable value'].append(igstTV)
        gstr3bData['IGST'].append(toFloat(float(getFloate(gstr3b_df.loc['(a) Outward taxable supplies (other than zero rated, nil rated and exempted)', 'Integrated Tax']))))
        gstr3bData['SGST taxable value'].append(sgstTV)
        gstr3bData['SGST'].append(toFloat(float(gstr3b_df.loc['(a) Outward taxable supplies (other than zero rated, nil rated and exempted)', 'State/UT Tax'])))


        print(pdfFile)

        # break
    #
    # for key in gstr3bData.keys():
    #     print(gstr3bData[key])
    #     print(len(gstr3bData[key]))


    gstr3b_df = pd.DataFrame(gstr3bData)

    return gstr3b_df

if __name__ == '__main__':
    from main import path

    # -------------INPUT--------------------

    gst3bFolder_path = r'C:\Users\Lenovo1\Desktop\Niraj Office (old)\Lex Polytex Ind\GSTR-3B' #path['GSTR 3B']
    percentageOfIGST = 18

    # -------------------------------------------------------------

    print(collectGSTR3BData(percentageOfIGST, gst3bFolder_path).iloc[36])

