import pandas as pd
from datetime import date
import xlrd
data = pd.read_excel('Daily_Temps.xlsx', 'DailyTemps')
numDays = pd.Series([31,28,31,30,31,30,31,31,30,31,30,31])

def get_avg(d, m): #Given integers d(day) and m(month), calculates the average min and max temp, as well as humidity for said day from 2010-2019
    min_avg = 0
    max_avg = 0
    hum_avg = 0
    index = 0
    while index < len(data.index):
        if(data.iloc[index, 1] == m):   #if index is in month m, add days total to total sum
            min_avg += data.iloc[index + d - 1, 6]
            max_avg += data.iloc[index + d - 1, 5]
            hum_avg += data.iloc[index + d - 1, 7]
            while index < len(data.index) and data.iloc[index, 1] == m:
                index = index + 1   #iterate past current month to not repeat data
        index = index + 1
    min_avg /= 10
    max_avg /= 10
    hum_avg /= 10
    return pd.Series({'min':min_avg, 'max':max_avg, 'hum':hum_avg})    #return series index 0 = min temp, 1 = max temp, 2 = humidity

inp = input("Enter '1' to input a date. Enter any other key to use today's date.\n")    #takes user input to determine what date to use
if(inp == '1'):
    month = input("Enter the month in number format (january = 1, etc.)\n")
    day = input("Enter the day\n")
    month = int(month)
    day = int(day)
else:
    print("Using today's date.")        #if user doesn't input, uses today's date
    day = date.today().day
    month = date.today().month

min_temps = pd.Series(0, index=['-6','-5','-4','-3','-2','-1','0','1','2','3','4','5','6','7'])#empty series to fill with data
max_temps = pd.Series(0, index=['-6','-5','-4','-3','-2','-1','0','1','2','3','4','5','6','7'])
humidity = pd.Series(0, index=['-6','-5','-4','-3','-2','-1','0','1','2','3','4','5','6','7'])
curday = day
curmonth = month
for i in range(7):  #iterate from day 0 to day -6, filling series with average data
    averages = get_avg(curday, curmonth)
    min_temps.iloc[6 - i] = averages.iloc[0]
    max_temps.iloc[6 - i] = averages.iloc[1]
    humidity.iloc[6 - i] = averages.iloc[2]
    curday -= 1
    if(curday == 0):    #if day or month has gone below accepted value, loop to max accepted value ie. month 1(jan) becomes month 12(dec)
        if(curmonth == 0):  # and day 1 becomes final day of previous month
            curmonth = 13
        curmonth -= 1
        curday = numDays.iloc[curmonth - 1]
curday = day
curmonth = month
for i in range(8):  #iterate from day 0 to day 7, filling series with average data
    averages = get_avg(curday, curmonth)
    min_temps.iloc[6 + i] = averages.iloc[0]
    max_temps.iloc[6 + i] = averages.iloc[1]
    humidity.iloc[6 + i] = averages.iloc[2]
    curday += 1
    if(curday > numDays.iloc[curmonth - 1]):    #same as previous loop but reversed ie. month 12(dec) becomes month 1(jan)
        if(curmonth == 12):                     # and final day of month becomes day 1 of next month
            curmonth = 0
        curmonth += 1
        curday = 1

sum_x = 91          #x is constant
sum_sqrx = 819  
min_sum_y = 0
min_sum_xy = 0
max_sum_y = 0
max_sum_xy = 0
hum_sum_y = 0
hum_sum_xy = 0
for item in range(14):      #used for linear regression algorithm
    min_sum_y += min_temps.iloc[item]
    min_sum_xy += (item * min_temps.iloc[item])
    max_sum_y += max_temps.iloc[item]
    max_sum_xy += (item * max_temps.iloc[item])
    hum_sum_y += humidity.iloc[item]
    hum_sum_xy += (item * humidity.iloc[item])      #perform linear regression on data points
min_a = ((min_sum_y * sum_sqrx) - (sum_x * min_sum_xy)) / ((14 * sum_sqrx) - (sum_x**2))
min_b = ((14 * min_sum_xy) - (sum_x * min_sum_y)) / ((14 * sum_sqrx) - (sum_x**2))
max_a = ((max_sum_y * sum_sqrx) - (sum_x * max_sum_xy)) / ((14 * sum_sqrx) - (sum_x**2))
max_b = ((14 * max_sum_xy) - (sum_x * max_sum_y)) / ((14 * sum_sqrx) - (sum_x**2))
hum_a = ((hum_sum_y * sum_sqrx) - (sum_x * hum_sum_xy)) / ((14 * sum_sqrx) - (sum_x**2))
hum_b = ((14 * hum_sum_xy) - (sum_x * hum_sum_y)) / ((14 * sum_sqrx) - (sum_x**2))

var_min = 0
var_max = 0
var_hum = 0
for x in range(14):         #calculate average variance from actual values: used to determine prediction range
    var_min += ((min_temps.iloc[x] - ((min_b * x) + min_a))**2)
    var_max += ((max_temps.iloc[x] - ((max_b * x) + max_a))**2)
    var_hum += ((humidity.iloc[x] - ((hum_b * x) + hum_a))**2)
var_min /= 12
var_max /= 12
var_hum /= 12

print("\nRegression formulas used:")
print("high: {0:.1f}x + {1:.1f}, variance: {2:.1f}".format(max_b, max_a, var_max))
print("low: {0:.1f}x + {1:.1f}, variance: {2:.1f}".format(min_b, min_a, var_min))
print("humidity: {0:.1f}x + {1:.1f}, variance: {2:.1f}".format(hum_b, hum_a, var_hum))

print("\nPredicted values for the week after {}/{} based on data from 2010-2019".format(str(month), str(day)))
curday = day
curmonth = month
for p in range(7):
    curday += 1         #iterates for next 7 days
    if(curday > numDays.iloc[curmonth - 1]):
        if(curmonth == 12):
            curmonth = 0
        curmonth += 1
        curday = 1                                           #outputs next 7 days predictions based on regression analysis
    print("{}/{}: ".format(str(curmonth), str(curday)))     #range uses regression formula +/- average variance
    print("\thigh: {0:.1f}-{1:.1f} deg. F\tlow: {2:.1f}-{3:.1f} deg. F".format((max_b * (p + 7)) + max_a - var_max, (max_b * (p + 7)) + max_a + var_max, (min_b * (p + 7)) + min_a - var_min, (min_b * (p + 7)) + min_a + var_min))
    print('\thumidity: {0:.1f}-{1:.1f}%'.format(((hum_b * (p + 7)) + hum_a) - var_hum, ((hum_b * (p + 7)) + hum_a) + var_hum))