import pdfplumber, datetime
import pandas as pd
import os, re

def getGSTR3BData(path):
    os.chdir(path)
    gstr3bData = {
        'month': [],
        'outBasicPrice': [],
        'outIGST': [],
        'outSGST': [],
        'outCGST': [],
        'reIGST': [],
        'reSGST': [],
        'reCGST': [],
        'itcIGST': [],
        'itcSGST': [],
        'itcCGST': []
    }

    def getFloate(strRawVale):
        return re.findall("\d+\.\d+", strRawVale)[0]

    def removeEnter(str):
        return re.sub(" \n", " ", str)

    def removeRupeeSymbol(str):
        return re.sub(" \(₹\)", "", str)

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
        date = date.strftime('%b-%y')

        return date


    pdfList = []
    for pdfFile in os.listdir():
        if 'pdf' in pdfFile.split('.'):
            pdfList.append(pdfFile)

    for pdfFile in pdfList:
        print(pdfFile)
        with pdfplumber.open(pdfFile) as pdf:
            pages = pdf.pages

            for page in pages:

                if page.page_number == 1:
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
                    gstr3bData['month'].append(date)

                    gstr3bData['outBasicPrice'].append(toFloat((output_df.loc[
                                                                               '(a) Outward taxable supplies (other than zero rated, nil rated and exempted)', 'Total Taxable value'])))
                    gstr3bData['outIGST'].append(toFloat((getFloate(output_df.loc[
                                                                          '(a) Outward taxable supplies (other than zero rated, nil rated and exempted)', 'Integrated Tax']))))
                    gstr3bData['outSGST'].append(toFloat((output_df.loc[
                                                                '(a) Outward taxable supplies (other than zero rated, nil rated and exempted)', 'State/UT Tax'])))
                    gstr3bData['outCGST'].append(toFloat((output_df.loc[
                                                            '(a) Outward taxable supplies (other than zero rated, nil rated and exempted)', 'Central Tax'])))


                contant = page.extract_text()
                # print(contant)
                if 'Eligible ITC' in contant:
                    tables = page.extract_tables()
                    for idx, table in enumerate(tables):
                        if table[0][0] == 'Details' or table[0][0] == 'F\nDetails':
                            print('----------------------')
                            col = table[0]
                            col = [removeRupeeSymbol(removeEnter(i)).lower() for i in col]
                            col[0] = 'Details'
                            idx = [i[0] for i in table]
                            idx[0] = 'Details'
                            # print(idx)
                            itc_df = pd.DataFrame(table)
                            itc_df.columns = col

                            itc_df.index = idx
                            itc_df.drop('Details', inplace=True)
                            itc_df.drop('Details', axis=1, inplace=True)
                            # print(itc_df)
                            # print(itc_df.index)
                            # print(itc_df.columns)
                            try:
                                gstr3bData['reIGST'].append(toFloat((itc_df.loc['(3) Inward supplies liable to reverse charge (other than 1 & 2 above)', 'integrated tax'])))
                                gstr3bData['reSGST'].append(toFloat((itc_df.loc['(3) Inward supplies liable to reverse charge (other than 1 & 2 above)', 'state/ut tax'])))
                                gstr3bData['reCGST'].append(toFloat((itc_df.loc['(3) Inward supplies liable to reverse charge (other than 1 & 2 above)', 'central tax'])))

                                gstr3bData['itcIGST'].append(toFloat((itc_df.loc['C. Net ITC available (A-B)', 'integrated tax'])))
                                gstr3bData['itcSGST'].append(toFloat((itc_df.loc['C. Net ITC available (A-B)', 'state/ut tax'])))
                                gstr3bData['itcCGST'].append(toFloat((itc_df.loc['C. Net ITC available (A-B)', 'central tax'])))

                            except KeyError:
                                gstr3bData['reIGST'].append(toFloat((itc_df.loc[
                                    '(B) ITC Reversed', 'integrated tax'])))
                                gstr3bData['reSGST'].append(toFloat((itc_df.loc[
                                    '(B) ITC Reversed', 'state/ut tax'])))
                                gstr3bData['reCGST'].append(toFloat((itc_df.loc[
                                    '(B) ITC Reversed', 'central tax'])))

                                gstr3bData['itcIGST'].append(
                                    toFloat((itc_df.loc['(C) Net ITC Available (A) – (B)', 'integrated tax'])))
                                gstr3bData['itcSGST'].append(
                                    toFloat((itc_df.loc['(C) Net ITC Available (A) – (B)', 'state/ut tax'])))
                                gstr3bData['itcCGST'].append(
                                    toFloat((itc_df.loc['(C) Net ITC Available (A) – (B)', 'central tax'])))

                            # print(gstr3bData)

                            break       # included in code
                # break
        # break
    # print(gstr3bData)
    gstr3b_df = pd.DataFrame(gstr3bData)
    gstr3b_df.index = gstr3bData['month']
    gstr3b_df.drop('month', axis=1, inplace=True)
    return gstr3b_df


if __name__ == '__main__':

    path = r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\Silk woven sack\GSTR 3B Jul-17 to Dec-20\New folder'

    df = getGSTR3BData(path)
    print(df.iloc[0])
    # print(df.iloc[9])