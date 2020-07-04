# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 17:32:56 2020

@author: pulkit
"""

#Import statements, make sure to install Hurst module
import numpy as np
import math
import os
import pandas as pd
import hurst
from scipy import stats
from math import log,sqrt
from scipy import stats
from statsmodels.tsa.stattools import adfuller as adf1
import matplotlib.pyplot as plt
plt.style.use('ggplot')

def MeanReversionSpeed(data):  
    x=data[0:len(data)-1]
    y=data[1:len(data)]
    x=np.array(x)
    y=np.array(y)
    slope, intercept, r_value, p_value, std_siperr = stats.linregress(x,y)
    Sx=sum(x)
    Sy=sum(y)
    Sxx=np.dot(x,x)
    Syy=np.dot(y,y)
    Sxy=np.dot(x,y)
    a=slope
    b=intercept
    n=len(x)
    sd=sqrt(((n*Syy)-(Sy*Sy)-(a*((n*Sxy)-(Sx*Sy))))/(n*(n-2)))
    delta=1
    try:
        lamda=-(log(a)/delta)
    except:
        return 10

    return round(lamda,3)

plt.style.use('ggplot')


#Set your path directory
path="C:\\Users\\pulki\\OneDrive\Documents\\Algo Trading\\Data North America\\NYSE\\"
files=os.listdir(path)


#load data for stocks and statistics
data=pd.read_csv(path+"USA.csv")
statistics=pd.read_csv(path+"Statistics.csv")
statistics.dropna(inplace=True)

#Groupby sectors
sectors_list=list(set(statistics.Sector))
groups={}
for i in sectors_list:
    groups[i]=statistics[statistics.Sector == i]
    groups[i].index=groups[i]["Stock"]
    groups[i]=groups[i].drop(["Stock"],axis=1)


#Filter 2 based on Beta and Market Cap
pairsFilter1={}

for group in groups.keys():
    bins=groups[group]
    temp=[]
    print (group)
    for i in range(len(bins)):
        for j in range(i+1,len(bins)):            
            beta1= bins.iloc[i].Beta
            beta2= bins.iloc[j].Beta
            marketCap1= bins.iloc[i].Marketcap
            marketCap2= bins.iloc[j].Marketcap
            betaDiff=abs(100*((beta1-beta2)/(beta1)))
            mcDiff=abs(100*((marketCap1-marketCap2)/(marketCap1)))
            if betaDiff < 10 and mcDiff<10:
                temp.append([bins.index[i],bins.index[j]])
                
    pairsFilter1[group]=temp
    
    
#Filter 3 based on Statistics
pairsFilter2={}
hurstThreshold=0.35
correlationThreshold=0.9
for pairs in pairsFilter1.keys():
    bins=pairsFilter1[pairs]
    temp=[]
    for stock in (bins):       
        s1=data[stock[0]]
        s2=data[stock[1]]
        if (any([math.isnan(x) for x in s1])) or (any([math.isnan(x) for x in s2])):
            continue
        else:
            spread=s1/s2
            ad1=adf1(list(spread),maxlag=4)
            adff=round(ad1[1],3)
            hurst1= round(hurst.compute_Hc(spread)[0],3)
            ms= MeanReversionSpeed(spread)
            corr=np.corrcoef(s1,s2)[0][1]
            if hurst1<hurstThreshold and corr>correlationThreshold:
                temp.append(stock)
                
            
    pairsFilter2[pairs]=temp
    
    
