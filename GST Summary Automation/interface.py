from tkinter import *
# from summarycalculation import calculate
root = Tk()
root.geometry('1500x500')

#
# sheetDisplay = Frame(root, width=1500, height=500)
# sheetDisplay.grid()

canvas = Canvas(root)
canvas.pack(fill='both', expand='yes')

scroll = Scrollbar(canvas, orient='horizontal', command=canvas.xview)
scroll.pack(side=BOTTOM, fill='x')
canvas.config(xscrollcommand=scroll.set)

canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))


sheet = Frame(canvas)
canvas.create_window((0,0), window=sheet, anchor='nw')

class SummaryRow:
    def __init__(self, master):
        self.master = master

        self.frame = Frame(self.master)
        self.frame.grid(columnspan=17)

        self.addCells()

    def calculate(self, var):
        pass

    def addCells(self):
        self.month_var = IntVar()
        self.month_var.trace('w', lambda name, index, mode, sv=self.month_var: self.calculate(sv))
        self.month_E = Entry(self.frame, textvariable=self.month_var)
        self.month_E.grid(row=0, column=0)

        self.openingBal_var = IntVar()
        self.openingBal_var.trace('w', lambda name, index, mode, sv=self.openingBal_var: self.calculate(sv))
        self.openingBal_E = Entry(self.frame, textvariable=self.openingBal_var)
        self.openingBal_E.grid(row=0, column=1)

        self.eligibleSGSTInput_var = IntVar()
        self.eligibleSGSTInput_var.trace('w',
                                         lambda name, index, mode, sv=self.eligibleSGSTInput_var: self.calculate(sv))
        self.eligibleSGSTInput_E = Entry(self.frame, textvariable=self.eligibleSGSTInput_var)
        self.eligibleSGSTInput_E.grid(row=0, column=2)

        self.SGSTPaid_var = IntVar()
        self.SGSTPaid_var.trace('w', lambda name, index, mode, sv=self.SGSTPaid_var: self.calculate(sv))
        self.SGSTPaid_E = Entry(self.frame, textvariable=self.SGSTPaid_var)
        self.SGSTPaid_E.grid(row=0, column=3)

        self.totalEligibleITC_var = IntVar()
        self.totalEligibleITC_var.trace('w', lambda name, index, mode, sv=self.totalEligibleITC_var: self.calculate(sv))
        self.totalEligibleITC_E = Entry(self.frame, textvariable=self.totalEligibleITC_var)
        self.totalEligibleITC_E.grid(row=0, column=4)

        self.eligibleSGSTadjustedAgainstEligibleGoods_var = IntVar()
        self.eligibleSGSTadjustedAgainstEligibleGoods_var.trace('w', lambda name, index, mode,
                                                                            sv=self.eligibleSGSTadjustedAgainstEligibleGoods_var: self.calculate(
            sv))
        self.eligibleSGSTadjustedAgainstEligibleGoods_E = Entry(self.frame,
                                                                textvariable=self.eligibleSGSTadjustedAgainstEligibleGoods_var)
        self.eligibleSGSTadjustedAgainstEligibleGoods_E.grid(row=0, column=5)

        self.eligibleSGSTadjustedAgainst_Non_EligibleGoods_var = IntVar()
        self.eligibleSGSTadjustedAgainst_Non_EligibleGoods_var.trace('w', lambda name, index, mode,
                                                                                 sv=self.eligibleSGSTadjustedAgainst_Non_EligibleGoods_var: self.calculate(
            sv))
        self.eligibleSGSTadjustedAgainst_Non_EligibleGoods_E = Entry(self.frame,
                                                                     textvariable=self.eligibleSGSTadjustedAgainst_Non_EligibleGoods_var)
        self.eligibleSGSTadjustedAgainst_Non_EligibleGoods_E.grid(row=0, column=6)

        self.balanceEligibleSGST_var = IntVar()
        self.balanceEligibleSGST_var.trace('w',
                                           lambda name, index, mode, sv=self.balanceEligibleSGST_var: self.calculate(
                                               sv))
        self.balanceEligibleSGST_E = Entry(self.frame, textvariable=self.balanceEligibleSGST_var)
        self.balanceEligibleSGST_E.grid(row=0, column=7)

        self.openingBal_RMC_var = IntVar()
        self.openingBal_RMC_var.trace('w', lambda name, index, mode, sv=self.openingBal_RMC_var: self.calculate(sv))
        self.openingBal_RMC_E = Entry(self.frame, textvariable=self.openingBal_RMC_var)
        self.openingBal_RMC_E.grid(row=0, column=8)

        self.RCM_EligibleSGSTInput_var = IntVar()
        self.RCM_EligibleSGSTInput_var.trace('w', lambda name, index, mode,
                                                         sv=self.RCM_EligibleSGSTInput_var: self.calculate(sv))
        self.RCM_EligibleSGSTInput_E = Entry(self.frame, textvariable=self.RCM_EligibleSGSTInput_var)
        self.RCM_EligibleSGSTInput_E.grid(row=0, column=9)

        self.RMC_SGSTUtilisedagnistEligiblegoods_var = IntVar()
        self.RMC_SGSTUtilisedagnistEligiblegoods_var.trace('w', lambda name, index, mode,
                                                                       sv=self.RMC_SGSTUtilisedagnistEligiblegoods_var: self.calculate(
            sv))
        self.RMC_SGSTUtilisedagnistEligiblegoods_E = Entry(self.frame,
                                                           textvariable=self.RMC_SGSTUtilisedagnistEligiblegoods_var)
        self.RMC_SGSTUtilisedagnistEligiblegoods_E.grid(row=0, column=10)

        self.RMC_eligibleSGSTadjustedAgainst_Non_EligibleGoods_var = IntVar()
        self.RMC_eligibleSGSTadjustedAgainst_Non_EligibleGoods_var.trace('w', lambda name, index, mode,
                                                                                     sv=self.RMC_eligibleSGSTadjustedAgainst_Non_EligibleGoods_var: self.calculate(
            sv))
        self.RMC_eligibleSGSTadjustedAgainst_Non_EligibleGoods_E = Entry(self.frame,
                                                                         textvariable=self.RMC_eligibleSGSTadjustedAgainst_Non_EligibleGoods_var)
        self.RMC_eligibleSGSTadjustedAgainst_Non_EligibleGoods_E.grid(row=0, column=11)

        self.balanceSGST_RMC_var = IntVar()
        self.balanceSGST_RMC_var.trace('w', lambda name, index, mode, sv=self.balanceSGST_RMC_var: self.calculate(sv))
        self.balanceSGST_RMC_E = Entry(self.frame, textvariable=self.balanceSGST_RMC_var)
        self.balanceSGST_RMC_E.grid(row=0, column=12)

        self.SGSTClaims_var = IntVar()
        self.SGSTClaims_var.trace('w', lambda name, index, mode, sv=self.SGSTClaims_var: self.calculate(sv))
        self.SGSTClaims_E = Entry(self.frame, textvariable=self.SGSTClaims_var)
        self.SGSTClaims_E.grid(row=0, column=13)

        self.totalSGSTBal_var = IntVar()
        self.totalSGSTBal_var.trace('w', lambda name, index, mode, sv=self.totalSGSTBal_var: self.calculate(sv))
        self.totalSGSTBal_E = Entry(self.frame, textvariable=self.totalSGSTBal_var)
        self.totalSGSTBal_E.grid(row=0, column=14)

        self.SGStAsPerCreditLedger_var = IntVar()
        self.SGStAsPerCreditLedger_var.trace('w', lambda name, index, mode,
                                                         sv=self.SGStAsPerCreditLedger_var: self.calculate(sv))
        self.SGStAsPerCreditLedger_E = Entry(self.frame, textvariable=self.SGStAsPerCreditLedger_var)
        self.SGStAsPerCreditLedger_E.grid(row=0, column=15)

        self.diff_var = IntVar()
        self.diff_var.trace('w', lambda name, index, mode, sv=self.diff_var: self.calculate(sv))
        self.diff_E = Entry(self.frame, textvariable=self.diff_var)
        self.diff_E.grid(row=0, column=16)

col_header = ['month', 'openingBal', 'eligibleSGSTInput', 'SGSTPaid', 'totalEligibleITC', 'eligibleSGSTadjustedAgainstEligibleGoods',
     'eligibleSGSTadjustedAgainst_Non_EligibleGoods', 'balanceEligibleSGST',
     'openingBal_RMC', 'RCM_EligibleSGSTInput', 'RMC_SGSTUtilisedagnistEligiblegoods', 'RMC_eligibleSGSTadjustedAgainst_Non_EligibleGoods', 'balanceSGST_RMC',
     'SGSTClaims', 'totalSGSTBal', 'SGStAsPerCreditLedger', 'diff']

col = 0
for heading in col_header:
    Label(sheet, text=heading).grid(row=0, column=col)
    col+=1

SummaryRow(sheet)
SummaryRow(sheet)







root.mainloop()