#Written by Siddarth Sreeram
#Background information/data acquired from:
#https://www.kaggle.com/datasets/tjkyner/global-seawater-oxygen18-levels
#Tested on Python 3.8

#import all modules
from turtle import color
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon
import csv
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import numpy as np
import matplotlib as mpl
import math
from tkinter import simpledialog
import scipy as spi
from sklearn.metrics import r2_score

#define variables and lists used throughout program
i = 0  #i is used for iterating through the csv
shapefile = "ne_110m_admin_0_countries.shp"  #shapefile is used to establish the .shp file as a variable
data = gpd.read_file(
    shapefile
)  #data is used to establish shapefile as a geopandas-friendly map
df = pd.read_csv(
    "gso18.csv")  #df is used to establish the csv as a pandas dataframe
d18OList = []  #creates list
yearList = []  #creates list
monthList = []  #creates list
saltList = []  #creates list
latList = []  #creates list
longList = []  #creates list
userListYear = []  #creates list
userListd18O = []  #creates list
tempListLong = []  #creates list
tempListLat = []  #creates list

#loop to make the dataframe column into a string with values suitable for colors
i = 0  #defines variable used for while loops
#while loop that establishes the dataframe values in lists
while i < len(df.index):
    d18OList.append(float(df["d18O"][i]))
    yearList.append(float(df["Year"][i]))
    monthList.append(float(df["Month"][i]))
    yearList[i] = float(yearList[i] + (monthList[i] / 12))
    i = i + 1
i = 0
#while loop that establishes the dataframe values in lists
while i < len(df.index):
    saltList.append(float(df["Salinity"][i]))
    latList.append(float(df["Latitude"][i]))
    longList.append(float(df["Longitude"][i]))
    i = i + 1
i = 0


#functions that allows for a user input of a latitude/longitude pair to find the nearest similar values in the data set
def nearestpoint(longitude, latitude):
    i = 0
    longitude = float(longitude)
    latitude = float(latitude)
    currentDist = 0
    minDist = 9999999999
    while i < (df.shape[0]):
        currentDist = (((float(df["Longitude"][i]) - longitude)**2) +
                       (float(df["Latitude"][i]) - latitude)**2)**0.5
        if currentDist < minDist:
            tempListLong.append(float(df["Longitude"][i]))
            tempListLat.append(float(df["Latitude"][i]))
            minDist = currentDist
        i = i + 1


def heatmapGraph():
    with plt.style.context(('dark_background')):
        df = pd.read_csv("gso18.csv")
        data.plot()  #graphs data
        plt.scatter(df.Longitude, df.Latitude, s=3, c=d18OList,
                    cmap='Reds')  #plots the points using colorlist
        plt.colorbar(orientation="horizontal",
                     fraction=0.07,
                     anchor=(1.0, 0.0))  #adds the colorbar at the bottom
        plt.title("Oxygen-18 Concentrations Plotted on a Map")  #adds title
        plt.xlabel("Latitude")  #adds x-axis label
        plt.ylabel("Longitude")  #adds y-axis label
        wm = plt.get_current_fig_manager()
        wm.window.state('zoomed')
        plt.show(block=True)


#code for Salinity button
def salinityGraph():
    with plt.style.context(('dark_background')):
        plt.scatter(saltList, d18OList, s=3, cmap='Greens')
        plt.xlim(0, 50)
        plt.title("Oxygen-18 Concentration vs Salinity")  #adds title
        plt.xlabel("Salinity")  #adds x-axis label
        plt.ylabel("Oxygen-18 Concentration")  #adds y-axis label
        a, b = np.polyfit(np.array(saltList), np.array(d18OList), 1)
        plt.plot(np.array(saltList), a*(np.array(saltList))+b, color='purple', linestyle='--', linewidth=2)
        slope, intercept, r_value, p_value, std_err = spi.stats.linregress(np.array(saltList), np.array(d18OList))
        plt.text(40, -0.88, 'y = ' + '{:.2f}'.format(b) + ' + {:.2f}'.format(a) + 'x' + "\n $R^2$="+str(float(r_value)**2), size=14, color='white')
        wm = plt.get_current_fig_manager()
        wm.window.state('zoomed')
        plt.show(block=True)


#code for Location button
def userLocation():
    nearPoint = []
    with plt.style.context(('dark_background')):
        root1 = tk.Tk()
        root1.withdraw()
        root1.wm_attributes("-topmost", 1)
        user_Lat = simpledialog.askstring(
            title="Latitude", prompt="Enter the latitude of your location:")
        user_Long = simpledialog.askstring(
            title="Longitude", prompt="Enter the longitude of your location:")
        nearPoint = nearestpoint(user_Long, user_Lat)
        df = pd.read_csv("gso18.csv")
        i = 0
        userListYear = []
        userListd18O = []
        while i < len(df.index):
            if (df["Longitude"][i]
                    == tempListLong[-1]) and (df["Latitude"][i]
                                              == tempListLat[-1]):
                userListYear.append(
                    float(df["Year"][i]) + float((df["Month"][i]) / 12))
                userListd18O.append(float(df["d18O"][i]))
            i = i + 1
        plt.scatter(userListYear, userListd18O, s=3, cmap='Greens')
        plt.xlim(1964, 2009)
        plt.title("Time vs Oxygen-18 Concentration in a Particular Area"
                  )  #adds title
        plt.xlabel("Time (Year)")  #adds x-axis label
        plt.ylabel(
            "Oxygen-18 Concentration in a Particular Area")  #adds y-axis label
        wm = plt.get_current_fig_manager()
        wm.window.state('zoomed')
        plt.show(block=True)


#code for the primary GUI panel
root = Tk(className='Global Seawater Oxygen-18 Concentrations')
root.geometry("400x200")
root.configure(bg='black')
btn1 = Button(root, text='Heatmap', bd='10', command=heatmapGraph)
btn1.pack(side='top')
btn2 = Button(root, text='Salinity', bd='10', command=salinityGraph)
btn2.pack(side='left')
btn3 = Button(root, text='Location', bd='10', command=userLocation)
btn3.pack(side='right')
#code for the main graph on the central GUI
with plt.style.context(('dark_background')):
    figure1 = plt.Figure(figsize=(100, 0.5), dpi=200)
    data1 = {'Year': yearList, 'Oxygen-18 Conc.': d18OList}
    df1 = DataFrame(data1, columns=['Year', 'Oxygen-18 Conc.'])
    ax1 = figure1.add_subplot(111)
    ax1.scatter(df1['Year'], df1['Oxygen-18 Conc.'], color='g')
    coef1 = np.polyfit(yearList, d18OList, 1)
    poly1d_fn = np.poly1d(coef1)
    scatter1 = FigureCanvasTkAgg(figure1, root)
    scatter1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
    ax1.set_xlabel('Time (Year)')
    ax1.set_ylabel('Oxygen-18 Concentration')
    ax1.set_title('Oxygen-18 Concentration vs. Time')
    #ax1.plot(yearList,d18OList, 'o', yearList, poly1d_fn(yearList), '-m', label="Line of Best Fit")
    ax1.plot(yearList, d18OList, 'o')
    ax1.plot(yearList, poly1d_fn(yearList), '-m', label="Line of Best Fit")
    ax1.legend(loc="upper left")
root.mainloop()
