Temp_calc by Spencer Eaves and Jaymon Kendall

This program uses weather data for the Salt Lake City are from 2010 - 2019 in order 
to predict a daily minimum and maximum temperature, as well as humidity.
	Source for historical data: Salt Lake City International Airport

The program contains four parts:
-It first prompts the user whether to use a specific date or today's date
	Press '1' and then enter to enter a custom date
		Enter a month in the form of a number between 1-12, with 1 being January, etc.
		Enter the day to predict the next week from ie. entering '1' will begin the prediction at day 2
	Press anything other than '1' and then enter to use today's date
-Next it calculates a linear regression formula for the maximum and minimum temperatures, as well as humidity
	By comparing said formula to known data points, it calculates an average variance for the regression formula
	It then outputs the formulas used for each prediction, as well as their variance
-Next it uses each of the regression formulas to create a prediction for the next 7 days, and outputs the data
	The range of data is created using the predicted number +/- the calculated average variance
-If a custom date was not selected, the program will finally output prediction data from openweathermap.org
	This is done in order to compare our predicted data with data from a professional source

This program requires python be installed, as well as several python modules
A quick method to get the required resources for running the program is by using Anaconda

1. Navigate to anaconda.com/products/individual
2. Download and install the proper version for your computer
3. After installation is complete, open the newly installed program Anaconda Prompt
4. Navigate to the dirctory that Temp_calc.py and Daily_Temps.xlsx are located
	If the program is in Downloads, enter the following command:
	cd C:\users\<username>\Downloads\Temp_calc
5. Run the file by typing the following command
	python Temp_calc.py