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

# Make a numpy array of this data
flow_data = data[['year', 'month','day', 'flow']].to_numpy()

# Getting rid of the pandas dataframe since we wont be using it this week
del(data)

# %%
# Starter Code
# Count the number of values with flow > 600 and month ==7
flow_count = np.sum((flow_data[:,3] > 600) & (flow_data[:,1]==7))

# Calculate the average flow for these same criteria 
flow_mean = np.mean(flow_data[(flow_data[:,3] > 600) & (flow_data[:,1]==7),3])

print("Flow meets this critera", flow_count, " times")
print('And has an average value of', flow_mean, "when this is true")

# Make a histogram of data
# Use the linspace  funciton to create a set  of evenly spaced bins
mybins = np.linspace(0, 1000, num=15)
# another example using the max flow to set the upper limit for the bins
#mybins = np.linspace(0, np.max(flow_data[:,3]), num=15) 
#Plotting the histogram
plt.hist(flow_data[:,3], bins = mybins)
plt.title('Streamflow')
plt.xlabel('Flow [cfs]')
plt.ylabel('Count')

# Get the quantiles of flow
# Two different approaches ---  you should get the same answer
# just using the flow column
flow_quants1 = np.quantile(flow_data[:,3], q=[0,0.1, 0.5, 0.9])
print('Method one flow quantiles:', flow_quants1)
# Or computing on a colum by column basis 
flow_quants2 = np.quantile(flow_data, q=[0,0.1, 0.5, 0.9], axis=0)
# and then just printing out the values for the flow column
print('Method two flow quantiles:', flow_quants2[:,3])

# %%
# Ty's code - week 4
# define prediction window
startpred_year = 2020
startpred_months=[8,8,9,9,9,9,10,10,10,10,11,11,11,11,11,12]
startpred_days=[22,30,6,13,20,27,4,11,18,25,1,8,15,22,29,6]
pred_window=7

# remove too-recent data
lastdataday=datefn(2020, 8, 21)

elday=np.zeros((np.shape(flow_data)[0]))
for i in np.arange(np.shape(flow_data)[0]):
        tempvar=datefn(int(flow_data[i,0]), int(flow_data[i,1]), int(flow_data[i,2]))-lastdataday
        elday[i]=tempvar.days

flowdata_calc=flow_data.copy()

for i in np.arange(3):
        if i==0:
                gooddate=np.where((flowdata_calc[:,0]<=2020) & (flowdata_calc[:,1]==9))
        elif i==1:
                gooddate=np.where((flowdata_calc[:,0]<2001) & (flowdata_calc[:,1]==9))
                findyears=flowdata_calc[0,:]<2001
        else:
                gooddate=np.where((flowdata_calc[:,0]>2000) & (flowdata_calc[:,1]==9))
        print('September days = ', np.sum(flowdata_calc[:,1]==9))
        print('Times exceeded = ', np.sum(flowdata_calc[gooddate,3]>101))
        print('% exceeded     = ', int(np.sum(flowdata_calc[gooddate,3]>101)/np.sum(flowdata_calc[:,1]==9)*100))
        print()

# find DOY of each observation
doy=np.zeros((np.shape(flowdata_calc)[0]))
for i in np.arange(np.shape(flowdata_calc)[0]):
        tempvar=datefn(int(flow_data[i,0]), int(flow_data[i,1]), int(flow_data[i,2]))-datefn(int(flow_data[i,0]), 1, 1)
        doy[i]=tempvar.days

# remove last doy for leap years ... crude, but wth
flowdata_calc=np.delete(flowdata_calc,np.where(doy==365),axis=0)

remainder=np.shape(flowdata_calc)[0]%365    # cut down to whole years looking backward from last data date
flowdata_calc=flowdata_calc[remainder:,:]
flowcalc_vector=flowdata_calc[:,3].copy()

flowcalc_vector=np.reshape(flowcalc_vector,(-1,365))
flowcalc_thisyear=flowcalc_vector[-1,:]
flowdiff=np.abs(flowcalc_vector-flowcalc_thisyear)
flowdiff=np.delete(flowdiff,-1,axis=0)
# flowdiff[flowdiff>100]=100
flowdiff=(flowdiff+.1)**-2
# flowdiff=1/flowdiff

normfactor=np.sum((flowdiff),axis=0)
L=flowdiff/normfactor

Lbyyear=np.sum(L,axis=1)
matchingyear=np.where(Lbyyear==np.max(Lbyyear))
worstmatchingyear=np.where(Lbyyear==np.min(Lbyyear))

Lw_flow=np.sum(L*flowcalc_vector[:-1,:],axis=0)

remainder=np.shape(Lw_flow)[0]%7    # cut down to whole years looking backward from last data date
weekly_flow=np.round(np.mean(np.reshape(Lw_flow[remainder:],(-1,7)),axis=1))
print('weekly flows starting 8/22:', weekly_flow)

fig = plt.figure()
ax = plt.subplot(111)
ax.plot(np.arange(np.shape(Lw_flow)[0]),Lw_flow,'.b')
plt.xlabel('Days from last observation')
plt.ylabel('Flow')
fig.savefig('projection.jpg')

fig = plt.figure()
ax = plt.subplot(111)
ax.hist(np.log10(flowcalc_vector[-1,:]), normed=1, alpha = 0.5, label='past year')
tempvar=np.reshape(flowcalc_vector,(-1,1))
ax.hist(np.log10(tempvar), normed=1, alpha = 0.5, label='all years')
plt.ylabel('Normed Frequency')
plt.xlabel('log10 Flow')
ax.legend()
fig.savefig('ave.jpg')

fig = plt.figure()
ax = plt.subplot(111)
ax.hist(np.log10(flowcalc_vector[-1,:]), normed=1, alpha = 0.5, label='past year')
flowcalc_vector_matchingyear=np.squeeze(flowcalc_vector[matchingyear,-365:])
ax.hist(np.log10(flowcalc_vector_matchingyear), normed=1, alpha = 0.5, label='best match year')
plt.ylabel('Normed Frequency')
plt.xlabel('log10 Flow')
ax.legend()
fig.savefig('best.jpg')

fig = plt.figure()
ax = plt.subplot(111)
ax.hist(np.log10(flowcalc_vector[-1,:]), normed=1, alpha = 0.5, label='past year')
flowcalc_vector_matchingyear=np.squeeze(flowcalc_vector[worstmatchingyear,-365:])
ax.hist(np.log10(flowcalc_vector_matchingyear), normed=1, alpha = 0.5, label='worst match year')
plt.ylabel('Normed Frequency')
plt.xlabel('log10 Flow')
ax.legend()
fig.savefig('worst2.jpg')



# %%
