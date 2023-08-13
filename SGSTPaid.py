import pdfplumber, datetime
import pandas as pd
import os, re

#Payment of tax
def printList(list):
    for item in list:
        print(item)


def getSGSTPaid(path):

    lastQtr = ['January', 'February', 'March']

    gstr3bData = {'Claim Period': [],
                  'SGST Paid': []
                  }
    # 'Total taxable value': [],
    # 'IGST taxable value': [],
    # 'IGST': [],
    # 'SGST taxable value': [],
    # 'SGST': [],

    def getFloate(strRawVale):
        return re.findall("\d+\.\d+", strRawVale)[0]

    def toFloat(StrValue):
        return float('{:.2f}'.format(float(StrValue)))

    def isReqTable(table):
        isReqTableVar = False
        for row in table:
            for item in row:
                if item == '(A) Other than reverse charge':
                    isReqTableVar = True
                    break
        return isReqTableVar

    def getDate(month, year):

        if month in lastQtr:
            year = '20' + year.split('-')[1]
        else:
            year = year.split('-')[0]

        date = f'01/{month}/{year}'
        date = datetime.datetime.strptime(date, '%d/%B/%Y')
        date = date.strftime('%d/%m/%Y')

        return date

    os.chdir(path)

    pdfList = []
    for pdfFile in os.listdir():
        if 'pdf' in pdfFile.split('.'):
            pdfList.append(pdfFile)

    for pdfFile in pdfList:
        print(pdfFile)
        with pdfplumber.open(pdfFile) as pdf:
            date = ''
            pages = pdf.pages

            for page in pages:
                # print(page.page_number)
                content = page.extract_text()
                if page.page_number == 1:
                    table = page.extract_tables()[0]
                    date = getDate(table[1][1], table[0][1])

                if 'Payment of tax' in content:
                    # print(page.page_number)
                    tables = page.extract_tables()

                    for table in tables:
                        # print(table)
                        if isReqTable(table):
                            idx = [str(row[0].replace('\n', '')).lower() if row[0]!= None else None for row in table]
                            # printList(idx)
                            # print(len(idx))
                            col = ['description', 'total tax', 'tax paid through itc', None, None, None, 'tax/cess paid in cash', 'interest paid in cash', 'late fee paid in cash']


                            db = pd.DataFrame(table)
                            db.drop(0, inplace=True)
                            # print(db)
                            for x in range(7, 12):
                                # print(x)
                                db.drop(x, inplace=True)
                                idx[x] = '!'

                            for t in range(0, idx.count('!')):
                                idx.remove('!')

                            idx.pop(0)


                            db.columns = col
                            db.index = idx

                            # print('\n---------------------------')
                            # print(db.index)
                            # print(db.columns)
                            # print(db.loc['state/ut tax', 'tax/cess paid in cash'])
                            #
                            # print(db)

                            gstr3bData['Claim Period'].append(date)
                            gstr3bData['SGST Paid'].append(db.loc['state/ut tax', 'tax/cess paid in cash'])

    SGSTPaid_df = pd.DataFrame(gstr3bData)
    SGSTPaid_df.index = gstr3bData['Claim Period']

    print(SGSTPaid_df)
    return SGSTPaid_df

if __name__ == '__main__':

    # gst3bFolder_path = r'C:\Users\Lenovo1\Desktop\Niraj Office (old)\Lex Polytex Ind\GSTR-3B' #path['GSTR 3B']
    gst3bFolder_path = r'C:\Users\Lenovo1\Desktop\test'
    getSGSTPaid(gst3bFolder_path)