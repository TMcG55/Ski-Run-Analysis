import gpxpy
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D 
import os
import numpy as np
import random


class Strava:
    def findRadius(self,xCords,yCords):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(xCords,yCords,linestyle = '-',linewidth=2)
        centreX=[]
        centreY=[]
        n = len(xCoords)
        for count in range(0,n-3):
            a=count
            b=count+1
            c=count+2
            d=count+3


            Mac = (yCords[c]-yCords[a])/(xCords[c]-xCords[a])
            Mbd = (yCords[d]-yCords[b])/(xCords[d]-xCords[b])
            Mbr = -1/((yCords[c]-yCords[a])/(xCords[c]-xCords[a]))
            Mcr = -1/((yCords[d]-yCords[b])/(xCords[d]-xCords[b]))

            Cac = yCords[a]-Mac*xCords[a]
            Cbd = yCords[b]-Mbd*xCords[b]
            Cbr = yCords[b]-Mbr*xCords[b]
            Ccr = yCords[c]-Mcr*xCords[c]

            simEqA = [[1,-Mbr],[1,-Mcr]]
            simEqY =[[Cbr],[Ccr]]

            res = np.linalg.inv(simEqA).dot(simEqY)


            xGuess = (Ccr-Cbr)/(Mbr-Mcr)
            yGuess = (Mcr*Cbr-Mbr*Cbr)/(Mcr-Mbr)
            
            centreX.append(res[1])
            centreY.append(res[0])


            xSample = np.arange(-15,15,0.1)
            ySample = []
            Yac = []
            Ybd = []
            Ybr = []
            Ycr = []
            
            for x in xSample:
                #ySample.append(np.sqrt(25-x**2)) 
                Yac.append(Mac*x+Cac)
                Ybd.append(Mbd*x+Cbd)
                Ybr.append(Mbr*x+Cbr)
                Ycr.append(Mcr*x+Ccr)
            
        
            #ax.plot(xSample,ySample,linewidth=1,linestyle = '--')
            # ax.plot(xSample,Ybr,linewidth=1,linestyle = '--')
            # ax.plot(xSample,Ycr,linewidth=1,linestyle = '--')
            # ax.plot(xSample,Yac,linewidth=1,linestyle = ':')
            # ax.plot(xSample,Ybd,linewidth=1,linestyle = ':')
            ax.plot(res[1],res[0],marker = 'x',color = 'r')

        xTotal = 0
        yTotal = 0
        for i in range(len(centreX)):
            xTotal = xTotal+centreX[i]
            yTotal = yTotal+centreY[i]
        avgX = xTotal/len(centreX)
        avgY = yTotal/len(centreX)
        ax.plot(np.pi/2,0,marker = 'o',color = 'g')
        ax.plot(avgX,avgY,marker = 'o',color = 'b')
        # ax.set_xlim(-5,10)
        # ax.set_ylim(-5,10)
        plt.show()
    
        return [centreX,centreY]
    
    def findTurn(self, data):
        turnLat = []
        turnLong = []
        turn = [[],[]]
        length = len(data['long'])

        for i in range(0,length-3):
            area = 0.5 * abs(data['long'][i] * (data['lat'][i+1]  - data['lat'][i+2]) + data['long'][i+1]  * (data['lat'][i+2] - data['lat'][i]) + data['long'][i+1]  * (data['lat'][i] - data['lat'][i+1]))
            if area >= 10e-10:
                turnLat.append(data['lat'][i])
                turnLong.append(data['long'][i])
        turn = {
            'lat':turnLat,
            'long':turnLong
        }
        turn = pd.DataFrame(turn)
        return turn
    
    def importData(self):

        folder_path = r'D:\Tom\05_Programming\04_StravaProject'
        file_extension = '.gpx'  # Specify the file extension you're looking for

        # Get a list of all files in the folder
        all_files = os.listdir(folder_path)

        # Filter files with the specified file extension
        filtered_files = [file for file in all_files if file.endswith(file_extension)]

        allData = []

        for file in filtered_files:
            # Parse GPX file
            with open(file) as gpx_file:
                gpx = gpxpy.parse(gpx_file)

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

        return df

    def plotData(self,data,turn):
        #data = data[1100:1300]
        fig = plt.figure()
        ax_3d = fig.add_subplot(121, projection='3d')
        # Adding labels to the ax_3des
        # ax_3d.set_ylabel('Latitude (NS)')
        # ax_3d.set_xlabel('Longitude (EW)')
        # ax_3d.set_zlabel('Elevation')

        # #ax_3d.set_zlim(0, 100)

        # # Setting plot title
        # plt.title('3D Line Plot')

        
        # windowLow = 500
        # windowHigh = 1500
       
        #ax_3d.plot(data['long'][windowLow:windowHigh], data['lat'][windowLow:windowHigh], data['elev'][windowLow:windowHigh],linewidth=1,marker='x', markersize=8)
        

        # 2D plot
        ax_2d = fig.add_subplot(122)
        ax_2d.set_ylabel('Latitude (NS)')
        ax_2d.set_xlabel('Longitude (EW)')
        plt.title('2D Line Plot')
        ax_2d.plot(data['long'], data['lat'], linewidth=1, marker='o', markersize=8)
        ax_2d.plot(turn['long'],turn['lat'], linewidth=0, marker='x', markersize=8,color = 'r')
        # Display the plot
        plt.tight_layout()
        plt.show()
            

            
        print('pause')



test = Strava()
#xCoords = np.arange(0,10,0.25)
xCoords = []
j=0
while j<np.pi:
    diff = round(random.uniform(0,0.1), 3)
    j = j+diff
    if j>np.pi:
        break
    xCoords.append(j)
yCords = []
for x in xCoords:
    # yCords.append(np.sqrt(25-x**2))
    yCords.append(np.sin(x))

# test.findRadius(xCoords,yCords)
dataSet = test.importData()
turn = test.findTurn(dataSet)
test.plotData(dataSet, turn)



