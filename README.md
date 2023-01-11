# Climate DB Analysis - Surf's Up!
Using SQLAlchemy ORM queries, Pandas, and Matplotlib to perform basic climate analysis and data exploration of a climate database

![surfs-up.png](Images/surfs-up.png)
- - -
## Project Structure:
### All project code can be found in the [Project_Files](Project_Files/) folder:  
**Part 1:** Climate Analysis and Exploration: [climate_info.ipynb](Project_Files/climate_info.ipynb)  
**Part 2:** Design Your Climate App: [app.py](Project_Files/app.py)  
### **Bonus: Other Recommended Analyses** 
**Temperature Analysis Part 1:** [bonus_temp_analysis_1.ipynb](Project_Files/bonus_temp_analysis_1.ipynb)  
**Temperature Analysis Part 2:** [bonus_temp_analysis_2.ipynb](Project_Files/bonus_temp_analysis_2.ipynb)

The Resources folder contains the original sqlite and csv files used for the project, & Images folder contains images used for this README file.

- - -
## Scenario

Congratulations! You've decided to treat yourself to a long holiday vacation in Honolulu, Hawaii! To help with your trip planning, you need to do some climate analysis on the area. The following sections outline the steps you must take to accomplish this task.

## Part 1: Climate Analysis and Exploration

In this section, you’ll use Python and SQLAlchemy to perform basic climate analysis and data exploration of your climate database. Complete the following tasks by using SQLAlchemy ORM queries, Pandas, and Matplotlib.

### Precipitation Analysis

To perform an analysis of precipitation in the area, do the following:

* Using the most recent date in the dataset, retrieve the previous 12 months of precipitation data.

* Plot the results by using the DataFrame `plot` method, as shown in the following image:

  ![precipitation](Images/precipitation.png)

* Use Pandas to print the summary statistics for the precipitation data.

### Station Analysis

To perform an analysis of stations in the area, do the following:

* Design a query to find the most active stations.

* Using the most active station id, calculate the lowest, highest, and average temperatures.

* Query the previous 12 months of temperature observation data for this station.

* Plot the results as a histogram with `bins=12`, as shown in the following image:

    ![station-histogram](Images/station-histogram.png)

- - -

## Part 2: Design Your Climate App

Now that you have completed your initial analysis, you’ll design a Flask API based on the queries that you have just developed.

Use Flask to create your routes, as follows:

* `/`

    * Homepage.

    * List all available routes.

* `/api/v1.0/precipitation`

    * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.

    * Return the JSON representation of your dictionary.

* `/api/v1.0/stations`

    * Return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`

    * Query the dates and temperature observations of the most active station for the previous year of data.

    * Return a JSON list of temperature observations (TOBS) for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`

    * Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range.

    * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than or equal to the start date.

    * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates from the start date through the end date (inclusive).
- - -
## Bonus: Other Recommended Analyses

### Temperature Analysis 1

Conduct an analysis to answer the following question: Hawaii is reputed to enjoy mild weather all year round. Is there a meaningful difference between the temperatures in, for example, June and December?

* Identify the average temperature in June at all stations across all available years in the dataset. Do the same for the temperature in December.

* Use the t-test to determine whether the difference in means, if any, is statistically significant. Will you use a paired t-test or an unpaired t-test? Why?
- - -
### Temperature Analysis 2

You want to take a trip from August 1 to August 7 of this year, but you are worried that the weather will be less than ideal. Using historical data in the dataset, find out what the temperature has previously been for this timeframe.

* Use the `calc_temps` function to calculate the minimum, average, and maximum temperatures for your trip using the matching dates from a previous year (for example, use "2017-08-01").

* Plot the minimum, average, and maximum temperature from your previous query as a bar chart, as captured in the following steps and image:

    ![temperature](Images/temperature.png)

#### Daily Rainfall Average

Now that you have an idea of the temperature, let’s find out what the rainfall has been. You don't want to visit if it rains the whole time! Complete the following steps:

* Calculate the rainfall per weather station using the previous year's matching dates.

* Sort this in descending order by precipitation amount, and list the station, name, latitude, longitude, and elevation.

#### Daily Temperature Normals

Calculate the daily normals for the duration of your trip. Normals are the averages for the minimum, average, and maximum temperatures.

* Use Pandas to plot an area plot (`stacked=False`) for the daily normals, as shown in the following image:

  ![daily-normals](Images/daily-normals.png)

- - -
## References

Menne, M.J., I. Durre, R.S. Vose, B.E. Gleason, and T.G. Houston, 2012: An overview of the Global Historical Climatology Network-Daily Database. Journal of Atmospheric and Oceanic Technology, 29, 897-910, [https://doi.org/10.1175/JTECH-D-11-00103.1](https://doi.org/10.1175/JTECH-D-11-00103.1)

- - -

© 2022 edX Boot Camps LLC. Confidential and Proprietary. All Rights Reserved.
