import pandas as pd
import pdfplumber
import os, datetime
def getAnnexureBData(filePaths):

    annexureB_dict = {
        'month': [],
        'input_eligible_withinState_qtn': [],
        'input_eligible_withinState_basicPrice': [],
        'input_eligible_withinState_IGST': [],
        'input_eligible_outsideState_qtn': [],
        'input_eligible_outsideState_basicPrice': [],
        'input_eligible_outsideState_IGST': [],
        'input_nonEligible_withinState_qtn': [],
        'input_nonEligible_withinState_basicPrice': [],
        'input_nonEligible_withinState_IGST': [],
        'input_nonEligible_outsideState_qtn': [],
        'input_nonEligible_outsideState_basicPrice': [],
        'input_nonEligible_outsideState_IGST': [],
        'output_eligible_withinState_qtn': [],
        'output_eligible_withinState_basicPrice': [],
        'output_eligible_withinState_IGST': [],
        'output_eligible_outsideState_qtn': [],
        'output_eligible_outsideState_basicPrice': [],
        'output_eligible_outsideState_IGST': [],
        'output_nonEligible_withinState_qtn': [],
        'output_nonEligible_withinState_basicPrice': [],
        'output_nonEligible_withinState_IGST': [],
        'output_nonEligible_outsideState_qtn': [],
        'output_nonEligible_outsideState_basicPrice': [],
        'output_nonEligible_outsideState_IGST': []
    }

    def removeEnter(string):
        if type(string) == str:
            return string.replace('\n', '')
        else:
            return string

    def addDataFrame(df: pd.DataFrame, other: pd.DataFrame):
        df_dict = df.to_dict()
        other_dict = other.to_dict()

        for col in df_dict.keys():
            for row in df_dict[col].keys():
                try:
                    data_df = float(df_dict[col][row])
                    data_other = float(other_dict[col][row])
                except:
                    print('ERROR IN addDataFrame')
                    data_df = df_dict[col][row]
                    data_other = other_dict[col][row]
                    print(data_df)
                    print(data_other)


                df_dict[col][row] = data_df + data_other

        return pd.DataFrame(df_dict)

    for fileKey in filePaths.keys():
        main_df = pd.DataFrame()
        for fileNum, filePath in enumerate(filePaths[fileKey]):
            sub_df = pd.DataFrame()
            with pdfplumber.open(filePath) as pdf:
                for page in pdf.pages:
                    print(page.page_number)
                    tables = page.extract_tables()
                    for table in tables:
                        for rowNum, row in enumerate(table):
                            table[rowNum][1] = removeEnter(row[1])
                            # print(row)

                        col = ['Sr. No.', 'Month', 'withinState_qtn', 'withinState_basicPrice', 'withinState_SGST', 'withinState_CGST', 'withinState_total', 'outsideState_qtn', 'outsideState_basicPrice', 'outsideState_IGST', 'outsideState_total']


                        index = [removeEnter(row[1]) for row in table]

                        # table.pop(0)
                        # table.pop(0)

                        df = pd.DataFrame(table, columns=col, index=index)
                        df.drop(columns='Sr. No.', inplace=True)
                        df.drop(columns='Month', inplace=True)
                        df.drop('Month', inplace=True)
                        if page.page_number == 1:
                            sub_df = df.copy()
                        else:
                            sub_df = pd.concat([sub_df, df])

                        # print(df.to_dict())

                    # break
            print(sub_df.to_dict())
            if fileNum == 0:
                main_df = sub_df.copy()
            else:
                main_df = addDataFrame(main_df, sub_df)

        print(main_df)
        break


if __name__ == '__main__':
    filePaths = {'input_eligible': ['C:/Users/Lenovo1/Desktop/test/New folder/in_eli_1.pdf', 'C:/Users/Lenovo1/Desktop/test/New folder/in_eli_2.pdf', 'C:/Users/Lenovo1/Desktop/test/New folder/in_eli_3.pdf'], 'input_nonEligible': ['C:/Users/Lenovo1/Desktop/test/New folder/in_noneli_1.pdf'], 'output_eligible': ['C:/Users/Lenovo1/Desktop/test/New folder/out_eli_1.pdf'], 'output_nonEligible': ['C:/Users/Lenovo1/Desktop/test/New folder/out_noeli_1.pdf', 'C:/Users/Lenovo1/Desktop/test/New folder/out_noeli_2.pdf', 'C:/Users/Lenovo1/Desktop/test/New folder/out_noeli_3.pdf']}

    getAnnexureBData(filePaths)
    print("done")