#include all the import 
import traceback
import os, sys
import time
import exceptions
import skimsquery
from numpy import *

#class to define the database connection along with other functions
class SkimsProcessor(object):
    """
    This is the class for extending the C code to access the graph
    and get the travel times.

    Input: 
    """

    def __init__(self, offset, nodes):
        self.offset = offset
        self.nodes = nodes
        #print self.offset, self.nodes
        #print 'Testing extension'

        #Starting graph creation
        if self.nodes == 0:
            #get the nodes and edges
            nodes, edges = self.get_graph_nodes()
        else:
            nodes = self.nodes
            edges = self.nodes * self.nodes
        
        #initialize the graph
        skimsquery.initialize_array(nodes)


    def create_carray(self, num):
        """
        This method is used to create the origin and destination carrays.
        
        Input: Origin and destination numpy arrays
        
        Output: Origin and destination carrays
        """
        #print 'testing carray creation'
        p = skimsquery.new_intArray(num)
        skimsquery.create_array(p, num)
        skimsquery.print_array(p, num)
        return p
        
    
    def create_graph(self):
        """
        This method is used to create the network graph
        
        Input:
        None
        
        Output:
        Entire network Graph is created
        """
        
        #assign all values to the graph
        skimsquery.set_array(self.offset)
        

        
    def get_graph_nodes(self):
        """
        This method get the nodes and edges
        
        Input:
        None
        
        Output:
        Nodes and edges
        """
        #call get nodes to read file and get the nodes
        self.nodes = skimsquery.get_nodes()
        self.edges = self.nodes*self.nodes
        
        #return the nodes and edges
        return self.nodes, self.edges
        
        
    def numpy_to_carray(self, numpy_arr, arr_len, data_type):
        """
        This method converts the numpy array to a carray
        
        Input:
        Numpy array, array length and data type (to differentiate between float and int)
        
        Output:
        Carray
        """
        #check the datatype
        if data_type == 1:
            #create a new carray
            new_carr = skimsquery.new_floatArray(arr_len)
            i = 0
        
            #run a loop to assign the values in the numpy array to the carray
            for each in numpy_arr:
                skimsquery.floatArray_setitem(new_carr, i, float(each))
                i = i + 1
        else:
            #create a new carray
            new_carr = skimsquery.new_intArray(arr_len)
            i = 0
        
            #run a loop to assign the values in the numpy array to the carray
            for each in numpy_arr:
                skimsquery.intArray_setitem(new_carr, i, int(each))
                i = i + 1
        
        #return the carray        
        return new_carr

        
    def carray_to_numpy(self, carray, arr_len, data_type):
        """
        This method converts carray to numpy
        
        Input:
        Carray, array length and data type (to differentiate between float and int)
        
        Output:
        Numpy Array
        """
        #create a dummy array of length arr_len
        numpy_arr = zeros(arr_len)
        
        #check for datatype
        if data_type == 1:
            #run a loop to assign the values in the carray to the numpy array
            for i in range(arr_len):
                numpy_arr[i] = skimsquery.floatArray_getitem(carray,i)
        else:
            #run a loop to assign the values in the carray to the numpy array
            for i in range(arr_len):
                numpy_arr[i] = skimsquery.intArray_getitem(carray,i)
        
        #return the numpy array
        return numpy_arr
        
    
    def get_travel_times(self, origin, destination):
        """
        This method is used to get the travel times
        
        Input:
        Origin and destination arrays
        
        Output:
        Returns an array with travel times
        """         

	# Printing vertices
	#print 'origin - ', origin
	#print 'destination - ', destination


        #get the array length and initialize the tt array
        arr_len = origin.size
        tt = zeros(arr_len)
        
        #convert the arrays to carrays
        org_arr = self.numpy_to_carray(origin, arr_len, 0)
        dest_arr = self.numpy_to_carray(destination, arr_len, 0)
        tt_arr = self.numpy_to_carray(tt, arr_len, 1)
        
        #start retrieving travel times
        skimsquery.get_tt(org_arr, dest_arr, tt_arr, arr_len, self.offset)
        
        #conversion from carray to numpy
        new_tt = self.carray_to_numpy(tt_arr, arr_len, 1)

        #deleting all the carrays
        self.delete_carray(org_arr, 0)
        self.delete_carray(dest_arr, 0)
        self.delete_carray(tt_arr, 1)
        
        #return the travel times numpy array
	#print 'tt', new_tt
        return new_tt
        
   
    def create_location_array(self, arr_len):
        """
        This method initializes the location array and the temporary location 
        array. It also sets the arrays to zero
        
        Input:
        Array length
        
        Output:
        Loctions array and temp locations array are initialized and set to zero
        """
        #Starting location array initialization
        skimsquery.initialize_location_array(arr_len)
        
        #set the locations graph to zero
        skimsquery.set_location_array_to_zero(arr_len)
        
        #set the temp locations array to zero
        skimsquery.set_temp_location_array()
    
    
    def get_location_choices(self, origin, destination, tt, num_of_locations, land_use):
        """
        This method gets the locations choices. it internally calls 
        the generate random locations method.
        
        Input:
        Origin, Destination, Trave times and number of locations
        
        Output:
        Location array
        """
        #get the array length and length for location array
        arr_len = origin.size
        loc_len = arr_len * num_of_locations
        land_use_len = land_use.size
        
        #check if the landuse array is of length 1
        if land_use_len == 1:
            #check if the data is zero
            if land_use[0] == 0:
                #no land use information present, set land use length to nodes
                land_use_len = self.nodes
        
        #print 'land use length is %s'%land_use_len
        #initialize locations array to zero
        locations = zeros(loc_len)
        
        #convert the arrays to carrays
        org_arr = self.numpy_to_carray(origin, arr_len, 0)
        dest_arr = self.numpy_to_carray(destination, arr_len, 0)
        tt_arr = self.numpy_to_carray(tt, arr_len, 1)
        loc_arr = self.numpy_to_carray(locations, loc_len, 0)
        land_use_arr = self.numpy_to_carray(land_use, land_use_len, 0)
               
        #Starting location choices computation
        skimsquery.get_location_choices(org_arr, dest_arr, tt_arr, loc_arr, arr_len, self.offset, num_of_locations, land_use_arr, land_use_len)
        
        #Conversion from carray to numpy
        new_loc = self.carray_to_numpy(loc_arr, loc_len, 0)

        #change the dimensions of the new_loc numpy array
        new_loc.shape = (arr_len, num_of_locations)

        #deleting all the carrays
        self.delete_carray(org_arr, 0)
        self.delete_carray(dest_arr, 0)
        self.delete_carray(tt_arr, 1)
        self.delete_carray(loc_arr, 0)
        
        #deleting locations graph
        self.delete_location(arr_len)

        #return the locations numpy array
        return new_loc
            
        
    def delete_carray(self, carray, data_type):
        """
        This method is used to delete the carrays
        
        Input:
        Carray and datatype
        
        Output:
        Carrays deleted
        """
        #check for the datatype and delete the respective carray
        if data_type == 1:
            skimsquery.delete_floatArray(carray)
        else:
            skimsquery.delete_intArray(carray)
        
        
    def delete_graph(self):
        """
        This method is used the delete the dynamic arrays created 
        in the C program
        
        Input:
        None
        
        Output:
        Dynamic Arrays deleted
        """
        #delete the network graph created in the C program
        skimsquery.delete_array()
        
    
    def delete_location(self, arr_len):
        """
        This method deletes the locations array in the C program
        
        Input:
        Array length
        
        Output:
        Dynamic array deleted
        """
        #delete the locations array created in the C program
        skimsquery.delete_location_array(arr_len)
        
        
    def set_string(self, file_path, flag):
        """
        This method is used to assign the file names
        
        Input:
        File name (file path) and flag (to differentiate if the file is graph or node file)
        
        Output:
        File names in the C program are set
        """
        #check for the flag and assign file name
        skimsquery.set_file(file_path, 1, flag)
        
        #print the file name
        #skimsquery.print_string()


    def __del__(self):
        #check if object is deleted
    	print 'object is deleted'


#unit test to test the code
import unittest

#define a class for testing
class TestSkimsProcessor(unittest.TestCase):
    def setUp(self):
        self.numarr = 'numarr'
        self.offset = 1
        self.nodes = 1995

    def testEx(self):
        ext_obj = SkimsProcessor(self.offset, self.nodes)
        
        origin = zeros(100)
        destination = zeros(100)
        arr_len = origin.size
        num_of_locations = 15        
        land_use = array([1010,548,656,445,356,490,1258,184,1647,1722,327,360,1786,187,680,685,604,511,608,1005,545,461,549,1750,347,501,506,444,1262,1723,1266,352,945,524,1773,643,599,50,651,644,195,1751,322,1265,614,550,989,1713,469,1294,273,1712,996,174,484,576,589,339,266])
                
        i = 0
        j = 100
        offset = 1

        # 1st thousand
        for i in range(0, 100):
            origin[i] = i+offset
            #destination[i] = j*2
            destination[i] = j
            j = j - 1
        print origin, destination 
        
        """
        To get travel times
        """
        
        #pass file paths to the C program
        #node_path = "/home/namrata/Documents/swig/arr_sample/temp_data_copy.csv"
        graph_path = "/home/karthik/simtravel/test/skimsInput/travel_skims_peak.dat"

        #flag = 1
        #ext_obj.set_string(node_path, flag)
        flag = 0
        ext_obj.set_string(graph_path, flag)
        
        #create the travel times graph
        print '\tcreating the graph'
        t1 = time.time()
        n, e = ext_obj.create_graph()
        print 'n: %s e: %s'%(n, e)
        t2 = time.time()
        print '\tTime taken to create the graph - %.4f'%(t2-t1)
        
        #print 'travel times'
        t1 = time.time()
        new_tt = ext_obj.get_travel_times(origin, destination)
        t2 = time.time()

        print '\tTime taken to retrieve travel times %.4f'%(t2-t1)
        #print new_tt
        #print new_tt.size
        
        """
        For location choices
        """
        
        #initialize the location array
        print '\tcreating location graph'
        t1 = time.time()
        ext_obj.create_location_array(arr_len)
        t2 = time.time()
        print '\tTime taken to create location array - %.4f'%(t2-t1)
        
        #get location choices
        #land_use = zeros(1)
        print '\tLocation choices'
        t1 = time.time()
        new_loc = ext_obj.get_location_choices(origin, destination, new_tt*25, num_of_locations, land_use)
        t2 = time.time()
        print '\tTime taken to retrieve location choices %.4f'%(t2-t1)
        
	print 'LOCS RETRIEVED', new_loc.shape,  new_loc[:5,:]

        #printing the location choices
        for each in range(num_of_locations):
            print new_loc[:5,each]
                
        #after all computations are done delete all the arrays in the C program
        print 'deleting graph'
        t1 = time.time()
        ext_obj.delete_graph()
        t2 = time.time()
        print '\tTime taken to delete graph %.4f'%(t2-t1)
        


        
if __name__ == '__main__':
    unittest.main()
        
