# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 10:46:21 2019

@author: 16327143仲逊
"""

annual_salary=float(input('Enter your starting annual salary:' ))
total_cost=1000000
portion_down_payment=0.25
need_pay=portion_down_payment*total_cost

def calculate_36month_after(portion_saved,monthly_salary):
    """
    计算36个月后的存款
    """
    r=0.04
    month=1
    current_savings=0.0
    semi_annual_raise=0.07
    
    for month in range(1,37):
        current_savings+=(current_savings*r/12)
        current_savings+=(monthly_salary*portion_saved)
        if(month%6==0):
            monthly_salary*=(1+semi_annual_raise)
            
    return current_savings

def calculate_saving_rate(annual_salary):
    """
    计算最佳存款率
    """
    monthly_salary=annual_salary/12
    left,right=0,10000
    steps=0
    #若每个月剩下100%都无法满足题意，返回非法值
    if(calculate_36month_after(1,monthly_salary)<need_pay):
        return -1,-1
    #二分查找
    while left<right:
        steps+=1
        mid=left+(right-left)//2
        if(calculate_36month_after(mid/10000,monthly_salary)<need_pay):
            left=mid+1
        else:    
            right=mid
    #返回存款率和二分查找次数  
    return left/10000,steps
            
        
Best_savings_rate,steps=calculate_saving_rate(annual_salary)
if(steps==-1):
    print("It is not possible to pay the down payment in three years.")
else:        
    print('Best_savings_rate:',Best_savings_rate)
    print('Steps in bisection search:',steps)