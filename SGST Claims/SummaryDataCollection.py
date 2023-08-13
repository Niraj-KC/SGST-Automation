import pandas as pd

def getGSTSummaryData(path):
    gstSummary_df = pd.read_excel(path, engine="openpyxl", skiprows=4)
    gstSummary_df.fillna('', inplace=True)
    gstSummary_df.drop(
        gstSummary_df[(gstSummary_df['Claim Period '] == 'TOTAL') | (gstSummary_df['Claim Period '] == '')].index,
        axis=0, inplace=True)

    print(gstSummary_df.columns.tolist())
    gstSummary_df.columns = [col.strip() for col in gstSummary_df.columns.tolist()]

    gstSummary_df['Claim Period'] = pd.to_datetime(gstSummary_df['Claim Period']).dt.strftime('%d/%m/%Y')
    gstSummary_df.drop(columns='Sr No.:', inplace=True)
    gstSummary_df.index = gstSummary_df['Claim Period']
    gstSummary_df.drop(columns='Claim Period', inplace=True)
    # print(gstSummary_df.columns)#
    # print(gstSummary_df['ITC adjuste during the QTR'])

    return gstSummary_df


if __name__ == '__main__':
    path = r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\Golden Cotton\GST CLAIM SUMMARY.xlsx'
    df = getGSTSummaryData(path)
    print(type(df.iloc[5]['Eligible SGST input']))