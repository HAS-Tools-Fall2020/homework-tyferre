# Start code for assignment 3
# this code sets up the lists you will need for your homework
# and provides some examples of operations that will be helpful to you

# %%
# Import the modules we will use
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date as datefn
from datetime import timedelta
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

# %%
# ** MODIFY **
# Set the file name and path to where you have stored the data
filename = 'streamflow_week4.txt'
filepath = os.path.join('data\week_4', filename)
filepath = filename
print(os.getcwd())
print(filepath)

# %%
# DON'T change this part -- this creates the lists you 
# should use for the rest of the assignment
# no need to worry about how this is being done now we will cover
# this in later sections. 

#Read the data into a pandas dataframe
data=pd.read_table(filepath, sep = '\t', skiprows=30,
        names=['agency_cd', 'site_no', 'datetime', 'flow', 'code']
        )

# Expand the dates to year month day
data[["year", "month", "day"]] =data["datetime"].str.split("-", expand=True)
data['year'] = data['year'].astype(int)
data['month'] = data['month'].astype(int)
data['day'] = data['day'].astype(int)

#make lists of the data
flow = data.flow.values.tolist()
date = data.datetime.values.tolist()
year = data.year.values.tolist()
month = data.month.values.tolist()
day = data.day.values.tolist()

# Getting rid of the pandas dataframe since we wont be using it this week
del(data)

# %%
# Here is some starter code to illustrate some things you might like to do
# Modify this however you would like to do your homework. 
# From here on out you should use only the lists created in the last block:
# flow, date, yaer, month and day

# Calculating some basic properites
print(min(flow))
print(max(flow))
print(np.mean(flow))
print(np.std(flow))

# Making and empty list that I will use to store
# index values I'm interested in
ilist = []

# Loop over the length of the flow list
# and adding the index value to the ilist
# if it meets some criteria that I specify
for i in range(len(flow)):
        if flow [i] > 198 and month[i] == 9:
                ilist.append(i)

# see how many times the criteria was met by checking the length
# of the index list that was generated
print(len(ilist))

# Alternatively I could have  written the for loop I used 
# above to  create ilist like this
ilist2 = [i for i in range(len(flow)) if flow[i] > 198 and month[i]==9 and year[i]>=2010]
ilist3 = [i for i in range(len(flow)) if flow[i] > 0 and month[i]==9 and year[i]>=2010]

print('exceeding days ', len(ilist2))
print('fraction exceeding ', len(ilist2)/len(ilist3))

# Grabbing out the data that met the criteria
# This  subset of data is just the elements identified 
# in the ilist
subset = [flow[j] for j in ilist]



# %%
# Ty's code - week 4

recentweeks2exclude=0

months2consider=24
months2extend=2
weeks2consider=months2consider*4
weeks2extend=months2extend*4

flowbyday=flow.copy()
# remove peak flows
cutoff_quantile=0.8
flowbyday[flowbyday>np.quantile(flowbyday,cutoff_quantile)]=float("Nan")

if recentweeks2exclude>0:
        flowbyday=flowbyday[:-7*recentweeks2exclude]
remainder=np.shape(flowbyday)[0]%28    # cut down to whole multiple of 28 day months
flowbyday=flowbyday[remainder:]

for i in np.arange(1,len(flowbyday)):
        if np.isnan(flowbyday[i])>0:
                flowbyday[i]=flowbyday[i-1]

if len(flowbyday)>28*months2consider:
        flowbyday=flowbyday[-months2consider*28:]
        flowbyweek= flowbyday.reshape(-1, 7)
        flowweekave= np.mean(flowbyweek,axis=1)

        flowbymonth= flowbyday.reshape(-1, 28)
        flowmonthave= np.mean(flowbymonth,axis=1)

else:
        print('you requested too many months of data - for shame!')
        die

# tried spline ... not good
from scipy.interpolate import InterpolatedUnivariateSpline
order = 2

daily_spline = InterpolatedUnivariateSpline(np.arange(weeks2consider*7), flowbyday, k=order)
flowdaily_spline = daily_spline(np.arange((weeks2consider+weeks2extend)*7))
weekly_spline = InterpolatedUnivariateSpline(np.arange(weeks2consider), flowweekave, k=order)
flowweekly_spline = weekly_spline(np.arange((weeks2consider+weeks2extend)))
monthly_spline = InterpolatedUnivariateSpline(np.arange(int(weeks2consider/4)), flowmonthave, k=order)
flowmonthly_spline = monthly_spline(np.arange((int(weeks2consider+weeks2extend)/4)))


plt.figure()
plt.plot(np.arange(weeks2consider*7),flowbyday, '*y',label='daily')
plt.plot((np.arange(weeks2consider)+.5)*7,flowweekave, '*b',label='weekly')
plt.plot((np.arange(months2consider)+.5)*28,flowmonthave, '*r',label='monthly')
plt.xlabel('days')
plt.ylabel('average flow')
plt.legend()
plt.show()

plt.figure()
plt.plot((np.arange(weeks2consider)+.5)*7,flowweekave, '*b',label='calculated')
plt.plot((np.arange(weeks2consider+weeks2extend)+.5)*7,flowweekly_spline, '-b',label='spline')
plt.legend()
plt.xlabel('days')
plt.ylabel('average flow')
plt.show()







tryflow=flow.copy()
lastdataday=datefn(2020, 8, 21)
np.intersect1(np.where(year>=lastdataday.year), np.where(month>=lastdataday.month)) and np.where(day>=lastdataday.day)


# %%
# define prediction window
startpred_year = 2020
startpred_months=[8,8,9,9,9,9,10,10,10,10,11,11,11,11,11,12]
startpred_days=[22,30,6,13,20,27,4,11,18,25,1,8,15,22,29,6]
pred_window=7

# remove too-recent data
lastdataday=datefn(2020, 8, 21)

elday=np.zeros((np.shape(year)[0]))
for i in np.arange(np.shape(year)[0]):
        tempvar=datefn(year[i], month[i], day[i])-lastdataday
        elday[i]=tempvar.days
flow=np.delete(flow,np.where(elday>0))
year=np.delete(year,np.where(elday>0))
month=np.delete(month,np.where(elday>0))
day=np.delete(day,np.where(elday>0))

# find DOY of each observation
doy=np.zeros((np.shape(year)[0]))
for i in np.arange(np.shape(year)[0]):
        tempvar=datefn(year[i], month[i], day[i])-datefn(year[i], 1, 1)
        doy[i]=tempvar.days

# find mean and median flow for each DOY
flowarr=np.array(flow)
uniquedoy=np.unique(doy)
meanflow_doy=np.zeros((np.shape(uniquedoy)[0]))
medianflow_doy=np.zeros((np.shape(uniquedoy)[0]))
for i in np.arange(np.shape(uniquedoy)[0]):
        meanflow_doy[i]=np.mean(flowarr[np.where(doy==i)])
        medianflow_doy[i]=np.median(flowarr[np.where(doy==i)])

# find DOY of the start day of each prediction window
startpred_doy=np.zeros((np.shape(startpred_months)[0]))
for ij in np.arange(np.shape(startpred_months)[0]):
        startpred_month=startpred_months[ij]
        startpred_day=startpred_days[ij]
        tempvar=datefn(startpred_year, startpred_month, startpred_day)-datefn(startpred_year, 1, 1)
        startpred_doy[ij] = tempvar.days

# find median value of median value for days in prediction window
holdpreds=np.zeros((np.shape(startpred_months)[0]))
for ij in np.arange(np.shape(startpred_months)[0]):
        holdpreds[ij]=np.median(medianflow_doy[int(startpred_doy[ij]):int(startpred_doy[ij])+pred_window])

# visualize predictions and bases
plt.plot(doy,np.log10(flow),'.b',label='data')
plt.plot(uniquedoy,np.log10(meanflow_doy),'r',label='mean_doy')
plt.plot(uniquedoy,np.log10(medianflow_doy),'g',label='median_doy')
plt.plot(startpred_doy,np.log10(holdpreds),'.y',label='predictions')
plt.legend()
plt.ylabel('log10 flow')
plt.xlabel('DOY')
plt.show()

print(holdpreds)

# %%
