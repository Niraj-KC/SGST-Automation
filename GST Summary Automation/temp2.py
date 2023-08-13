l = ['month', 'openingBal', 'eligibleSGSTInput', 'SGSTPaid', 'totalEligibleITC', 'eligibleSGSTadjustedAgainstEligibleGoods',
     'eligibleSGSTadjustedAgainst_Non_EligibleGoods', 'balanceEligibleSGST',
     'openingBal_RMC', 'RCM_EligibleSGSTInput', 'RMC_SGSTUtilisedagnistEligiblegoods', 'RMC_eligibleSGSTadjustedAgainst_Non_EligibleGoods', 'balanceSGST_RMC',
     'SGSTClaims', 'totalSGSTBal', 'SGStAsPerCreditLedger', 'diff']

col = 0
for item in l:
    print(f"self.{item}_var = IntVar() \n"
          f"self.{item}_var.trace('w', lambda name, index, mode, sv=self.{item}_var: self.calculate(sv)) \n"
          f"self.{item}_E = Entry(self.frame, textvariable=self.{item}_var) \n"
          f"self.{item}_E.grid(row=0, column={col}) \n")
    col+=1