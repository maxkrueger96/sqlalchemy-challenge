# sqlalchemy-challenge
Repo for SQL Alchemy HW

# Analysis

It appears as though the temperatures recorded by the most active station is normally distributed, with a slight negative skew. These traits make sense to me given both the Central Limit Theorem and the warmer weather in Hawaii. As for the average precipitation levels on the islands from 2016 to 2017, the year average is quite low compared to some of the peaks in the graph. The sample mean is roughly 0.17, whereas there are several peaks reaching 1.0 and beyond, like around late September in 2016 and late February in 2017. Given the number of clear outliers, it seems to me that rainfall in Hawaii must be, on average, hard to predict as it behaves with no clear pattern. By doing IQR testing, I found 30 outliers above Q3 + 1.5 * IQR = 0.47, ranging from 0.48 to 2.38, and none below Q1 - 1.5 * IQR, which is negative. These 30 outliers have a mean of 0.97, so like the box plot shows, the peaks tend to hover around 1.0.


