oi = ['input', 'output']
eli_ineli = ['eligible', 'nonEligible']
in_out_guj = ['withinState', 'outsideState']
col_within = ['qtn', 'basicPrice', 'SGST', 'CGST']
col_outside = ['qtn', 'basicPrice', 'IGST']

column = []

for in_out in oi:
    for e_ine in eli_ineli:
        # print(f"'{in_out}_{e_ine}': []")
        for ig_og in in_out_guj:
            col = col_outside
            if ig_og == 'withinState':
                col = col_within
            for c in col:
                print(f"\'{ig_og}_{c}\': [],")
                column.append(f'{ig_og}_{c}')

print(column)
