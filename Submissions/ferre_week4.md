Ty   8/27   Assignment 4

---------
## Can you believe that it is already week 4?

### I guess it doesn't matter if you believe it or not ... kind of like science.

*no advanced math was used ... but some overly fancy footwork was employed*

The flow for each day of the year is compared to the flow on the same day in the most recent year for the previous 21 complete years.  These are used to find a likelihood measure to describe how much each year resembles the previous year.  These likelihoods are then used to weight the future flow of each previous year to project the daily flow during the prediction period. The daily flows are averaged to get projected weekly flows.

Histograms showing:

the flow distributions for the best matching year compared to the most recent 12 months.

![before](best.jpg)


the flow distributions for the worst matching year compared to the most recent 12 months.

![before](worst2.jpg)

Based on this approach, I get the following predicted daily flow for the 365 days following 8/22/20:

![before](projection.jpg)

The last data that I considered was 8/21/2020.  Despite knowing in my bones that these values are too high ... my projections are:

- 8/22 -  77
- 8/30 - 75
- 9/06 - 67
- 9/13 - 66
- 9/20 - 101
- 9/27 - 95
- 10/4 - 87
- 10/11 - 101
- 10/18 - 108
- 10/25 - 118
- 11/1 - 127
- 11/8 - 134
- 11/15 - 167
- 11/22 - 212
- 11/29 - 221
- 12/6 - 350


# Answers to your questions
The variables flow, year, month, and day are so well named that their definitions are obvious ... good coding practices!

They are all Lists, which I converted to ndarrays as needed
 - day, month and year are lists of integers
 - flow is a list of floats
 - they are all 1D, with length 11573

My estimated flow NEXT WEEK is 101.

All years
 - September days =  944
 - Times exceeded =  579
 - % exceeded     =  61

Before 2001
 - September days =  360
 - Times exceeded =  289
 - % exceeded     =  80

After 2009
 - September days =  314
 - Times exceeded =  171
 - % exceeded     =  54


### Progress towards personal fulfillment

- Maybe give EXTRA-polation a try ... given that we are in a megadrought
- World remains undominated ... by me ... leave it to the 1%
- Losing hope for emojis
