
from IPython import get_ipython

from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

import numpy as np
import pandas as pd
from pandas.plotting import table
import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

db = "sqlite:///Database/hawaii.sqlite"
engine = create_engine(db)

Base = automap_base()
Base.prepare(engine, reflect = True)
Base.classes.keys()

Station = Base.classes.station
Measurement = Base.classes.measurement

session = Session(engine)
dates = session.query(Measurement.date)
session.close()
dates_des = dates.order_by(Measurement.date.desc())
last_date = dates_des.first().date
prev_year = last_date.replace("2017", "2016")
prev_year_dt = dt.datetime.strptime(prev_year, "%Y-%m-%d")

session = Session(engine)
p_scores = session.query(Measurement.date, func.round(func.avg(Measurement.prcp),4)).            filter(Measurement.date >= prev_year_dt - dt.timedelta(days=1)).            order_by(Measurement.date).            group_by(Measurement.date)
session.close()

p_df = pd.read_sql_query(p_scores.statement,engine)
p_df.set_index("date",inplace=True)
p_df.rename(columns={"round_1":"avg_prcp"},inplace=True)
p_df.sort_values("date")
p_df.head(5).style

noidx_dt = p_df.index.values
plt_df = pd.DataFrame({'Dates': noidx_dt, 'Precipitation': p_df['avg_prcp']})
plt_df['Dates'] = pd.to_datetime(plt_df['Dates'])

months =[]
for x in plt_df['Dates']:
    if x.day == 23:
            months.append(f'{x.date()}')

def save_prcp():
        ax = plt_df.plot.bar(
                x = 'Dates',y= 'Precipitation',
                title="Average Percipitation in Hawaii during Aug. 2016 through Aug. 2017",
                facecolor="xkcd:cerulean",edgecolor='k',use_index=False,
                xlim=(plt_df['Dates'].iloc[0],plt_df['Dates'].iloc[-1]),width=3,figsize=(13,13)
        )
        ax.set_xticks([plt_df.index.get_loc(m) for m in months])
        ax.xaxis.set_ticklabels(months)
        ax.spines["top"].set_color('xkcd:blue green')
        ax.spines["bottom"].set_color('xkcd:blue green')
        ax.spines["left"].set_color('xkcd:blue green')
        ax.spines["right"].set_color('xkcd:blue green')
        ax.figure.set_facecolor(color='xkcd:light sea green')
        ax.figure.tight_layout()
        plt.hlines(y=p_df.mean(),xmin =ax.get_xticks()[0] ,xmax=ax.get_xticks()[-1],linewidths=1.25,linestyles='dashed',label='Mean Precip.',colors='red')
        plt.subplots_adjust(top=.5)
        ax.autoscale(tight=False)
        ax.legend()
        ax.figure.set_frameon(True)
        for label in ax.get_xticklabels():
                label.set_rotation(50)
                label.set_horizontalalignment('right')
        return plt.savefig('Images/precipitation.png', bbox_inches = 'tight',facecolor='xkcd:light sea green')

def save_describe():
        fig, ax = plt.subplots(frameon=False,figsize=(5,3)) # no visible frame
        ax.xaxis.set_visible(False)  # hide the x axis
        ax.yaxis.set_visible(False)  # hide the y axis
        tab = table(ax, p_df.describe(),loc='center')  # where df is your data frame
        tab.scale(1,1.5)
        plt.tight_layout()
        return plt.savefig('Images/prcp_describe.png', bbox_inches = 'tight')

session = Session(engine)
stations = session.query(Station.station)
session.close()

station_num = stations.count()

session = Session(engine)
station_measure = session.query(Measurement.station, Station.name,func.count(Measurement.date)).                group_by(Station.name).                order_by(func.count(Measurement.date).desc()).                join(Station, Station.station == Measurement.station)
session.close()
station_meas = station_measure.all()


session = Session(engine)
station_temp = session.query(Measurement.station, func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).                group_by(Measurement.station).                filter(Measurement.station == station_meas[0][0])
session.close()

session = Session(engine)
year_temps = session.query(Measurement.station, Measurement.date, Measurement.tobs).            filter(Measurement.date >= prev_year_dt - dt.timedelta(days=1)).            filter_by(station= station_meas[0][0])
session.close()

temp_df= pd.read_sql_query(year_temps.statement,engine)

def save_hist():
        fig, (ax1,ax2,ax3) = plt.subplots(1,3,figsize=(20,10))
        ax1.hist(temp_df['tobs'],bins = 7,density=True, label = "Density Histogram\n(bins = 7)",color="xkcd:yellow tan")
        dense1 = gaussian_kde(temp_df['tobs'],bw_method=.75)
        x = np.linspace(60,83,200)
        ax1.plot(x,dense1(x),label="Kernel Density Estimation\n(bandwidth = 0.75)",color="xkcd:hot purple")

        ax2.hist(temp_df['tobs'],density=True, label = "Density Histogram\n(auto-bins)",color="xkcd:faded orange")
        dense2 = gaussian_kde(temp_df['tobs'])
        ax2.plot(x,dense2(x),label="Kernel Density Estimation\n(Default bandwidth)",color="xkcd:vivid blue")

        ax3.hist(temp_df['tobs'],bins=12,density=True, label = "Density Histogram\n(bins = 12)",color="xkcd:dusty red")
        dense3 = gaussian_kde(temp_df['tobs'],bw_method=0.2)
        ax3.plot(x,dense3(x),label="Kernel Density Estimation\n(bandwidth = 0.2)",color="xkcd:electric green")

        ax2.set_title(f"\nThree Density Histograms with Different Bin Sizes\n\nfor the Temperature Measured by Station {station_meas[0][0]} in 2016 and 2017\n",fontsize = 30,color='xkcd:eggplant purple')

        xl = "Temp (F)"
        yl = "Gaussian Density"

        for ax in [ax1,ax2,ax3]:
                for pos in ['top','bottom','left','right']:
                        getattr(ax,'spines')[pos].set_color('xkcd:grass green')
                        getattr(ax,'set_xlabel')(xl)
                        getattr(ax,'set_ylabel')(yl)
                        getattr(ax,'legend')(loc='upper left')
                        getattr(ax,'set_facecolor')(color='xkcd:light grey')
                        
        ax.figure.set_facecolor(color='xkcd:duck egg blue')

        plt.tight_layout()
        plt.subplots_adjust(top=1.75)
        plt.subplots_adjust(bottom=1)

        return plt.savefig('Images/temperature.png', bbox_inches = 'tight',facecolor='xkcd:duck egg blue')


