import numpy as np
import matplotlib.cm as cm
import  matplotlib.pyplot as plt
from matplotlib.colors import Normalize

"""

n = 100000
x = np.random.standard_normal(n)
y = 2.0 + 3.0 * x + 4.0 * np.random.standard_normal(n)
xmin = x.min()
xmax = x.max()
ymin = y.min()
ymax = y.max()

plt.subplots_adjust(hspace=0.5)
plt.subplot(121)
plt.hexbin(x,y, cmap=cm.jet)
plt.axis([xmin, xmax, ymin, ymax])
plt.title("Skim Difference Heat Map")
cb = plt.colorbar()
cb.set_label('TT Diff')


plt.subplot(122)
plt.scatter(x,y, cmap=cm.jet)
plt.axis([xmin, xmax, ymin, ymax])
plt.title("Scatter Plot")

plt.show()
"""

import shutil
import time
import csv
import os
from numpy import array, average, zeros


class PlotHeatMap(object):
    def __init__(self, locNew='/home/karthik/simtravel/test/mag_zone_dynamic/skimOutput/dynamic/',
		       locOld='/home/karthik/simtravel/test/mag_zone_dynamic/skimOutput/dynamic/skims_first_iter/',
		       nodes=1996, timeIntervalList=-99):
	self.nodes = nodes
	if timeIntervalList == -99:
	    self.timeIntervalList = range(24)
	else:
	    self.timeIntervalList = timeIntervalList
	self.locNew = locNew
	self.locOld = locOld
	
	
    def createHeatMapForSkims(self):
	plt.subplots_adjust(hspace=0.1)

	subPlotNum = 120
	for timeInt in self.timeIntervalList:
		
	    subPlotNum += 1
	    plt.subplot(subPlotNum)

	    t_old = self.load_file(self.locOld + 'skim%d.dat'%timeInt)

	    t_new = self.load_file(self.locNew + 'skim%d.dat'%timeInt)

	    t_old_min = t_old[:,-1].min()
	    t_old_max = t_old[:,-1].max()
	    t_old_max = 150

	    t_new_min = t_new[:,-1].min()
	    t_new_max = t_new[:,-1].max()
	    t_new_max = 100

	    print 'old', t_old[:5,-1]
	    print 'new', t_new[:5,-1]

	    plt.hexbin(t_old[:,-1],t_new[:,-1], cmap=cm.jet, bins=100)
	    plt.axis([t_old_min, t_old_max, t_new_min, t_new_max])

	    plt.title("Skims Old(X) Vs New(Y) - %d" %timeInt)

	    cb = plt.colorbar()
	    cb.set_label('OD Count')


	plt.show()

    def createHeatMapForXY(self, xName, xLoc, yName, yLoc):
	plt.subplots_adjust(hspace=0.1)

	subPlotNum = 111
		
	plt.subplot(subPlotNum)

	x = self.load_file(xLoc)

	y = self.load_file(yLoc)

	x_min = x[:,-1].min()
	x_max = x[:,-1].max()

	y_min = y[:,-1].min()
	y_max = y[:,-1].max()

	print 'First 5 x values - ', x[:5,-1]
	print 'First 5 y values - ', y[:5,-1]

	plt.hexbin(x[:,-1],y[:,-1], cmap=cm.jet, bins=100)
	plt.axis([x_min, x_max, y_min, y_max])

	plt.title("%s(Y) Vs %s(X)" %(yName, xName))

	cb = plt.colorbar()
	cb.set_label('Count')

	plt.show()

    def load_file(self, filePath, delimiterChar=","):
	f = csv.reader(open(filePath, 'r'), delimiter=delimiterChar)
	
	arr = []
	k=0
	for i in f:
	    arr.append(i)
	    k+= 1
	    #if k > 100000:
	    #	break
	arr = array(arr, float)

	return arr

    def calculate_deviation(self):
	dev = []
	for timeInt in self.timeIntervalList:
	    t_old = self.load_file(self.locOld + 'skim%d.dat'%timeInt)

	    t_new = self.load_file(self.locNew + 'skim%d.dat'%timeInt)
		
            dev.append((np.abs(t_old[:,-1] - t_new[:,-1])).sum())

	    print dev

	print dev


if __name__ == "__main__":
    #obj = PlotHeatMap(timeIntervalList=[0])
    #obj.createHeatMapForSkims()

    # Dist (X) Vs New Skims(Y)
    #obj.createHeatMapForXY('iter1', '/home/karthik/simtravel/test/mag_zone_dynamic/iteration_1/skim3.dat',
    #			   'iter2', '/home/karthik/simtravel/test/mag_zone_dynamic/iteration_2/skim3.dat')
    #obj.createHeatMapForXY('iter2', '/home/karthik/simtravel/test/mag_zone_dynamic/iteration_2/skim3.dat',
    # 			   'iter3', '/home/karthik/simtravel/test/mag_zone_dynamic/iteration_3/skim3.dat')
    #obj.createHeatMapForXY('iter3', '/home/karthik/simtravel/test/mag_zone_dynamic/iteration_3/skim3.dat',
    #			   'iter4', '/home/karthik/simtravel/test/mag_zone_dynamic/iteration_4/skim3.dat')


    obj12 = PlotHeatMap(locNew='/home/karthik/simtravel/test/mag_zone_dynamic/iteration_1/',
		       locOld='/home/karthik/simtravel/test/mag_zone_dynamic/skimOutput/dynamic/startSkims/')
	
    obj12.calculate_deviation()
	

    #obj.createHeatMapForXY('start', '/home/karthik/simtravel/test/mag_zone_dynamic/skimOutput/dynamic/startSkims/skim3.dat',
    #			   'iter1', '/home/karthik/simtravel/test/mag_zone_dynamic/iteration_1/skim3.dat')


    """
    # Seq Vs Dynamic
    obj.createHeatMapForXY('new_seq_int-4', '/home/karthik/simtravel/test/mag_zone_dynamic/iter1_5per_sequential/skim4.dat',
			   'new_dyn_int-4', '/home/karthik/simtravel/test/mag_zone_dynamic/iter1_5per_dynamic/skim4.dat')



    # Peak Skims (Int 0) New (X) Vs Off Peak (Int4) Skims New(Y)
    obj.createHeatMapForXY('new_skim_int-0', '/home/karthik/simtravel/test/mag_zone_dynamic/skimOutput/dynamic/skim0.dat',
			   'new_skim_int-4', '/home/karthik/simtravel/test/mag_zone_dynamic/skimOutput/dynamic/skim4.dat')

    # Peak Skims (Int 0) Old (X) Vs Off Peak (Int4) Skims OLd(Y)
    obj.createHeatMapForXY('old_skim_int-0', '/home/karthik/simtravel/test/mag_zone_dynamic/skimOutput/dynamic/skims_first_iter/skim0.dat',
			   'old_skim_int-4', '/home/karthik/simtravel/test/mag_zone_dynamic/skimOutput/dynamic/skims_first_iter/skim4.dat')



    # Dist (X) Vs New Skims(Y)
    obj.createHeatMapForXY('peak dist', '/home/karthik/simtravel/test/mag_zone_dynamic/skimOutput/skims4Step.csv',
			   'new_skim_int-0', '/home/karthik/simtravel/test/mag_zone_dynamic/skimOutput/dynamic/skim0.dat')

    # Dist (X) Vs Old Skims(Y)
    obj.createHeatMapForXY('peak dist', '/home/karthik/simtravel/test/mag_zone_dynamic/skimOutput/skims4Step.csv',
    			   '4step_skim_int-0', '/home/karthik/simtravel/test/mag_zone_dynamic/skimOutput/dynamic/skims_first_iter/skim0.dat')
    """
