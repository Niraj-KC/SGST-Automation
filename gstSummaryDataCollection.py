import os
import pandas as pd


def getGSTSummaryData(path):


    gstSummary_df = pd.read_excel(path, engine="openpyxl", skiprows=4)
    gstSummary_df.fillna('', inplace=True)
    gstSummary_df.drop(gstSummary_df[(gstSummary_df['Claim Period '] == 'TOTAL') | (gstSummary_df['Claim Period '] == '')].index, axis=0, inplace=True)
    gstSummary_df['Claim Period '] = pd.to_datetime(gstSummary_df['Claim Period ']).dt.strftime('%d/%m/%Y')

    # print(gstSummary_df.columns)#
    # print(gstSummary_df['ITC adjuste during the QTR'])

    return gstSummary_df
# print(list(gstSummary_df.keys()))


#to get data
# print(gstSummary_df.iloc[gstSummary_df[(gstSummary_df['Claim Period '] == '01/03/21')].index].get('Opening Bal SGST ').values)
# print(gstSummary_df['Claim Period '])


if __name__ == '__main__':

    # cp = gstSummary_df['Claim Period '].to_dict()
    # ob = gstSummary_df['Opening Bal SGST '].to_dict()
    # cp = [cp[k] for k in cp.keys()]
    # ob = [ob[k] for k in ob.keys()]
    #
    # df = dict(zip(cp, ob))
    # gstSummary_df.index = cp
    # print(gstSummary_df)
    #
    # print(type(gstSummary_df.loc['01/07/2021', 'Opening Bal SGST ']))
    def toFloat(value):
        return float('{:.2f}'.format(float(value)))

    path = r'C:\Users\Lenovo1\Desktop\NIraj Office\SGST\venus polypack ind\GST CLAIM SUMMARY -2020-21.xlsx'
    gstSummary_df = getGSTSummaryData(path)
    print(gstSummary_df.columns)
    gstSummary_idx = gstSummary_df[(gstSummary_df['Claim Period '] == '01/07/2021')].index
    print(gstSummary_idx)
    ee = gstSummary_df.loc[gstSummary_idx, 'Eligible SGST Adjusted againnst in eligible goods']
    ene = gstSummary_df.loc[gstSummary_idx, 'Eligible SGST Adjusted againnst in Non eligible goods']
    ree = gstSummary_df.loc[gstSummary_idx, 'RCM SGST Utilised in eligible goods']
    rene = gstSummary_df.loc[gstSummary_idx, 'RCM SGST Utilised in non eligible goods']

    print(ee)
    print(ene)
    print(ree)
    print(rene)

    data =  toFloat(gstSummary_df.loc[gstSummary_idx, 'Eligible SGST Adjusted againnst in eligible goods']) \
    + toFloat(gstSummary_df.loc[gstSummary_idx, 'Eligible SGST Adjusted againnst in Non eligible goods']) \
    + toFloat(gstSummary_df.loc[gstSummary_idx, 'RCM SGST Utilised in eligible goods']) \
    + toFloat(gstSummary_df.loc[gstSummary_idx, 'RCM SGST Utilised in non eligible goods'])

    print(gstSummary_df.columns)

    d = gstSummary_df[['Eligible SGST Adjusted againnst in eligible goods',
       'Eligible SGST Adjusted againnst in Non eligible goods',
       'RCM SGST Utilised in eligible goods',
       'RCM SGST Utilised in non eligible goods']].sum(axis='columns')

    print(d.loc[gstSummary_idx])
