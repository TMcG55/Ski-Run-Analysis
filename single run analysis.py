import gpxpy
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
import os
import numpy as np


class Strava:
    def findRadius(self,points=[[0,2,4,5],[5,4,2,0]]):
        yCoords = []
        for x in points[0]:
            yCoords.append(np.sqrt(25-x**2))
        xCords = points[0]
        Mac = (yCoords[2]-yCoords[0])/(xCords[2]-xCords[0])
        Mbd = (yCoords[3]-yCoords[1])/(xCords[3]-xCords[1])
        Mbr = -1/((yCoords[2]-yCoords[0])/(xCords[2]-xCords[0]))
        Mcr = -1/((yCoords[3]-yCoords[1])/(xCords[3]-xCords[1]))

        Cac = yCoords[0]-Mac*xCords[0]
        Cbd = yCoords[1]-Mbd*xCords[1]
        Cbr = yCoords[1]-Mbr*xCords[1]
        Ccr = yCoords[2]-Mcr*xCords[2]

        
        centreX = (Ccr-Cbr)/(Mbr-Mcr)
        centreY = Mbr*centreX+Cbr


        xSample = np.arange(0,5,0.001)
        ySample = []
        Yac = []
        Ybd = []
        Ybr = []
        Ycr = []
        
        for x in xSample:
            ySample.append(np.sqrt(25-x**2)) 
            Yac.append(Mac*x+Cac)
            Ybd.append(Mbd*x+Cbd)
            Ybr.append(Mbr*x+Cbr)
            Ycr.append(Mcr*x+Ccr)
            
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(xCords,yCoords,marker = 'x',linewidth=0)
        ax.plot(xSample,ySample,linewidth=1,linestyle = '--')
        ax.plot(xSample,Ybr,linewidth=1,linestyle = '-',label = 'br')
        ax.plot(xSample,Ycr,linewidth=1,linestyle = '-',label = 'cr')
        ax.plot(xSample,Yac,linewidth=1,linestyle = ':',label = 'ac')
        ax.plot(xSample,Ybd,linewidth=1,linestyle = ':',label = 'vd')
        ax.plot(centreX,centreY,marker = 'x',color = 'r')
        ax.set_xlim(-2,5)
        ax.set_ylim(-2,5)
        plt.show()
        print('centre guess:',centreX,centreY)
        input('press')
        return [centreX,centreY]
    

    def importData(self,):

        folder_path = r'D:\Tom\05_Programming\04 Strava project'
        file_extension = '.gpx'  # Specify the file extension you're looking for

        # Get a list of all files in the folder
        all_files = os.listdir(folder_path)

        # Filter files with the specified file extension
        filtered_files = [file for file in all_files if file.endswith(file_extension)]

        chosenFile = filtered_files[0]

        allData = []
        
        gpx = gpxpy.parse(open(chosenFile))

        lat = []
        long = []
        elev = []
        time = []

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    lat.append(point.latitude)
                    long.append(point.longitude)
                    elev.append(point.elevation)
                    time.append(point.time)

        # Creating a DataFrame from existing arrays
        data = {
            'lat': lat,
            'long': long,
            'elev': elev,
            'time': time,
        }

        df = pd.DataFrame(data)

        allData.append(df)

        return allData
    
    def plotData(self,data):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        # Adding labels to the axes
        ax.set_ylabel('Latitude (NS)')
        ax.set_xlabel('Longitude (EW)')
        ax.set_zlabel('Elevation')


        # Setting plot title
        plt.title('3D Line Plot')

        for sets in data:
            windowLow = 1100
            windowHigh = 1145
            # Plotting the 3D line
            ax.plot(sets['long'][windowLow:windowHigh], sets['lat'][windowLow:windowHigh], sets['elev'][windowLow:windowHigh],linewidth=1, markersize=8)

            # Display the plot
            plt.show()



test = Strava()
test.findRadius()
dataSet = test.importData()
test.plotData(dataSet)



