# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 01:44:26 2019

@author: 16327143仲逊
"""

portion_down_payment = 0.25     #首付所需比例
current_savings=0.0             #当前存款
r = 0.04                        #每月理财收益

annual_salary=float(input('Enter your starting annual salary:' ))
portion_saved=float(input('Enter the percent of your salary to save, as a decimal: '))
total_cost=float(input('Enter the cost of your dream home: '))
semi_annual_raise=float(input('Enter the semiannual raise, as a decimal:'))
need_pay=portion_down_payment*total_cost
month=1
monthly_salary=annual_salary/12
while(True):
    current_savings+=(current_savings*r/12)
    current_savings+=(monthly_salary*portion_saved)
    if(month%6==0):
        monthly_salary*=(1+semi_annual_raise)
    if(need_pay>current_savings):
        month+=1
    else:
        break
        
print('Number of months: ',month)