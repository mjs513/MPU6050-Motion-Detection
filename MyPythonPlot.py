import pyqtgraph as pg
import serial
import string
from math import *
from time import time

ax =0.
ay = 0.
az = 0.
zm = 0
Xneg = 0.
Xpos = 0.

pg.mkQApp()

# Create remote process with a plot window
import pyqtgraph.multiprocess as mp
proc = mp.QtProcess()
rpg = proc._import('pyqtgraph')

plotwin = rpg.plot()
plotwin.win.resize(800,450)

curve = plotwin.plot(pen='y')
curve1 = plotwin.plot(pen='r')
curve2 = plotwin.plot(pen='g')
curve3 = plotwin.plot(pen='w')
curve4 = plotwin.plot(pen='b')

plotwin.addLegend()
style = pg.PlotDataItem(pen='w')
plotwin.plotItem.legend.addItem(1, "ax - yellow")
plotwin.plotItem.legend.addItem(1, "Xneg - red   ")
plotwin.plotItem.legend.addItem(1, "Xpos - green ")
#plotwin.plotItem.legend.addItem(1, "zm - zero motion")
#plotwin.setXRange(0,50)

# create an empty list in the remote process
data_x = proc.transfer([0]*50)
data_y = proc.transfer([0]*50)
data1_y = proc.transfer([0]*50)
data2_y = proc.transfer([0]*50)
data3_y = proc.transfer([0]*50)
data4_y = proc.transfer([0]*50)


# Send new data to the remote process and plot it
# We use the special argument _callSync='off' because we do
# not want to wait for a return value.
#data_y.extend([1,5,2,4,3], _callSync='off')
#curve.setData(y=data_y, _callSync='off')

#data1_y.extend([5,6,7,3], _callSync='off')
#data1_x.extend([-1,-2,3,5],_callSync='off')
#curve1.setData(y=data1_y, _callSync='off')
#for x in range(0,50):
#    data1_x.extend([x-38],_callSync='off')
#    data1_y.extend([x], _callSync='off')
#    curve1.setData(x=data1_x, y=data1_y, _callSync='off')


#ser = serial.Serial(port='COM4',baudrate=38400, timeout=1)
#f = open("Serial"+str(time())+".txt", 'w')
# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(port='COM4',baudrate=38400, timeout = 1)

i = 0

while 1:
    i = i + 1
    line = ser.readline()
    #line = line.replace("!ANG:","")   # Delete "!ANG:"
    #print line
    #f.write(line)                     # Write to the output log file
    words = string.split(line,",")     # Fields split
    if len(words) > 5:
        try:
            ax = float(words[1])
            ay = float(words[2])
            az = float(words[3])
            Xneg = float(words[8])
            Xpos = float(words[9])                  
            zm = int(words[7])
            #print ax
        except:
            print "Invalid line"
            pass
          
    data_y.extend([ax], _callSync='off')
    curve.setData(y=data_y, _callSync='off', name='ax') 
    data1_y.extend([Xneg], _callSync='off')
    curve1.setData(y=data1_y, _callSync='off', name='ay')
    data2_y.extend([Xpos], _callSync='off')
    curve2.setData(y=data2_y, _callSync='off', name='az')
    #data3_y.extend([zm], _callSync='off')
    #curve3.setData(y=data3_y, _callSync='off', name='zm')

ser.close
