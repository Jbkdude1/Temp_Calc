import pandas as pd
from datetime import date
import xlrd
data = pd.read_excel('Daily_Temps.xlsx', 'DailyTemps')
numDays = pd.Series([31,28,31,30,31,30,31,31,30,31,30,31])

def get_avg(d, m): #Given integers d(day) and m(month), calculates the average min and max temp for said day from 2010-2019
    min_avg = 0
    max_avg = 0
    index = 0
    while index < len(data.index):
        if(data.iloc[index, 1] == m):   #if index is in month m
            min_avg += data.iloc[index + d - 1, 6]
            max_avg += data.iloc[index + d - 1, 5]
            while index < len(data.index) and data.iloc[index, 1] == m:
                index = index + 1   #iterate past current month to not repeat data
        index = index + 1
    min_avg /= 10
    max_avg /= 10
    return pd.Series({'min':min_avg, 'max':max_avg})    #return series index 0 = min temp, 1 = max temp

day = date.today().day
month = date.today().month
min_temps = pd.Series(0, index=['-6','-5','-4','-3','-2','-1','0','1','2','3','4','5','6','7'])#empty series to fill with temp data
max_temps = pd.Series(0, index=['-6','-5','-4','-3','-2','-1','0','1','2','3','4','5','6','7'])
curday = day
curmonth = month
for i in range(7):  #iterate from day 0 to day -6
    averages = get_avg(curday, curmonth)
    min_temps.iloc[6 - i] = averages.iloc[0]
    max_temps.iloc[6 - i] = averages.iloc[1]
    curday -= 1
    if(curday == 0):    #if day or month has gone below accepted value, loop to max accepted value ie. month 1(jan) becomes month 12(dec)
        if(curmonth == 0):
            curmonth = 13
        curmonth -= 1
        curday = numDays.iloc[curmonth - 1]
curday = day
curmonth = month
for i in range(8):  #iterate from day 0 to day 7
    averages = get_avg(curday, curmonth)
    min_temps.iloc[6 + i] = averages.iloc[0]
    max_temps.iloc[6 + i] = averages.iloc[1]
    curday += 1
    if(curday > numDays.iloc[curmonth - 1]):
        if(curmonth == 12):
            curmonth = 0
        curmonth += 1
        curday = numDays.iloc[curmonth - 1]
sum_x = 91
sum_sqrx = 819
min_sum_y = 0
min_sum_xy = 0
max_sum_y = 0
max_sum_xy = 0
for item in range(14):
    min_sum_y += min_temps.iloc[item]
    min_sum_xy += (item * min_temps.iloc[item])
    max_sum_y += max_temps.iloc[item]
    max_sum_xy += (item * max_temps.iloc[item])
min_a = ((min_sum_y * sum_sqrx) - (sum_x * min_sum_xy)) / ((14 * sum_sqrx) - (sum_x**2))
min_b = ((14 * min_sum_xy) - (sum_x * min_sum_y)) / ((14 * sum_sqrx) - (sum_x**2))
max_a = ((max_sum_y * sum_sqrx) - (sum_x * max_sum_xy)) / ((14 * sum_sqrx) - (sum_x**2))
max_b = ((14 * max_sum_xy) - (sum_x * max_sum_y)) / ((14 * sum_sqrx) - (sum_x**2))
print("Predicted temperatures for {}/{} based on temperature data from 2010-2019".format(str(month), str(day + 1)))
print("Temperature high: {0:.1f} deg. F".format((max_b * 15) + max_a))
print("Temperature low: {0:.1f} deg. F".format((min_b * 15) + min_a))