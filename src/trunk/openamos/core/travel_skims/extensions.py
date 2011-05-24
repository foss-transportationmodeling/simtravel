#include all the import 
import traceback
import os, sys
import time
import exceptions
import arrayexample
from numpy import *

#class to define the database connection along with other functions
class Extensions(object):
    """
    This is the class for extending the C code to access the graph
    and get the travel times.

    Input: 
    """

    def __init__(self, offset, nodes):
        self.offset = offset
        self.nodes = nodes
        print self.offset, self.nodes
        print 'Testing extension'


    def create_carray(self, num):
        """
        This method is used to create the origin and destination carrays.
        
        Input: Origin and destination numpy arrays
        
        Output: Origin and destination carrays
        """
        print 'testing carray creation'
        p = arrayexample.new_intArray(num)
        arrayexample.create_array(p, num)
        arrayexample.print_array(p, num)
        return p
        
    
    def create_graph(self):
        """
        This method is used to create the network graph
        
        Input:
        
        
        Output:
        Entire network Graph is created
        """
        print 'Starting graph creation'
        t1 = time.time()
        if self.nodes == 0:
            #get the nodes and edges
            nodes, edges = self.get_graph_nodes()
        else:
            nodes = self.nodes
            edges = self.nodes * self.nodes
        
        #initialize the graph
        arrayexample.initialize_array(nodes)
        
        #assign all values to the graph
        arrayexample.set_array(self.offset)
        t2 = time.time()
        print '\t\tTime taken %s'%(t2-t1)
        
        return nodes, edges

        
    def get_graph_nodes(self):
        """
        This method get the nodes and edges
        
        Input:
        None
        
        Output:
        Nodes and edges
        """
        self.nodes = arrayexample.get_nodes()
        self.edges = self.nodes*self.nodes
        return self.nodes, self.edges
        
        
    def numpy_to_carray(self, numpy_arr, arr_len, data_type):
        """
        This method converts the numpy array to a carray
        
        Input:
        Numpy array, array length and data type (to differentiate between float and int)
        
        Output:
        Carray
        """
        if data_type == 1:
            new_carr = arrayexample.new_floatArray(arr_len)
            i = 0

            for each in numpy_arr:
                arrayexample.floatArray_setitem(new_carr, i, float(each))
                i = i + 1
        else:
            new_carr = arrayexample.new_intArray(arr_len)
            i = 0
            
            for each in numpy_arr:
                arrayexample.intArray_setitem(new_carr, i, int(each))
                i = i + 1
                
        return new_carr

        
    def carray_to_numpy(self, carray, arr_len, data_type):
        """
        This method converts carray to numpy
        
        Input:
        Carray, array length and data type (to differentiate between float and int)
        
        Output:
        Numpy Array
        """
        numpy_arr = zeros(arr_len)
        if data_type == 1:
            for i in range(arr_len):
                numpy_arr[i] = arrayexample.floatArray_getitem(carray,i)
                #numpy_arr[i]
        else:
            for i in range(arr_len):
                numpy_arr[i] = arrayexample.intArray_getitem(carray,i)
                
        return numpy_arr
        
    
    def get_travel_times(self, origin, destination):
        """
        This method is used to get the travel times
        
        Input:
        Origin and destination arrays and array length
        
        Output:
        Returns an array with travel times
        """         
        arr_len = origin.size
        tt = zeros(arr_len)
        
        #convert the arrays to carrays
        print 'starting conversion from numpy to carray'
        t1 = time.time()
        org_arr = self.numpy_to_carray(origin, arr_len, 0)
        dest_arr = self.numpy_to_carray(destination, arr_len, 0)
        tt_arr = self.numpy_to_carray(tt, arr_len, 1)
        t2 = time.time()
        print '\t\t\tTime taken %s'%(t2-t1)
        
        print 'Starting travel times computation'
        t1 = time.time()
        arrayexample.get_tt(org_arr, dest_arr, tt_arr, arr_len, self.offset)
        t2 = time.time()
        print '\t\tTime taken %s'%(t2-t1)
        
        print 'deleting all the carrays'
        t1 = time.time()
        self.delete_carray(org_arr, 0)
        self.delete_carray(dest_arr, 0)
        t2 = time.time()
        print '\t\tTime taken %s'%(t2-t1)
        
        print 'Starting conversion from carray to numpy'
        t1 = time.time()
        new_tt = self.carray_to_numpy(tt_arr, arr_len, 1)
        t2 = time.time()
        print '\t\tTime taken %s'%(t2-t1)
        
        print 'Numpy array obtained. delete carray'
        self.delete_carray(tt_arr, 1)
        
        #return the numpy array
        return new_tt
        
   
    def create_location_array(self, arr_len):
        """
        This method initializes the location array and the temporary location 
        array. It also sets the arrays to zero
        
        Input:
        
        Output:
        """
        print 'Starting location array initialization'
        t1 = time.time()
        arrayexample.initialize_location_array(arr_len)
        arrayexample.set_location_array_to_zero(arr_len)
        arrayexample.set_temp_location_array()
        t2 = time.time()
        print '\t\tTime taken %s'%(t2-t1)
    
    
    def get_location_choices(self, origin, destination, tt, num_of_locations):
        """
        This method gets the locations choices. it internally calls 
        the generate random locations method.
        
        Input:
        Origin, Destination, Trave times and Locations array, array length and offset
        
        Output:
        Location array
        """
        arr_len = origin.size
        loc_len = arr_len * num_of_locations
        
        locations = zeros(loc_len)
        
        #convert the arrays to carrays
        print 'starting conversion from numpy to carray'
        t1 = time.time()
        org_arr = self.numpy_to_carray(origin, arr_len, 0)
        dest_arr = self.numpy_to_carray(destination, arr_len, 0)
        tt_arr = self.numpy_to_carray(tt, arr_len, 1)
        loc_arr = self.numpy_to_carray(locations, loc_len, 0)
        t2 = time.time()
        print '\t\t\tTime taken %s'%(t2-t1)
               
        print 'Starting location choices computation'
        t1 = time.time()
        arrayexample.get_location_choices(org_arr, dest_arr, tt_arr, loc_arr, arr_len, self.offset, num_of_locations)
        t2 = time.time()
        print '\t\tTime taken %s'%(t2-t1)
        
        print 'deleting all the carrays'
        t1 = time.time()
        self.delete_carray(org_arr, 0)
        self.delete_carray(dest_arr, 0)
        self.delete_carray(tt_arr, 1)
        t2 = time.time()
        print '\t\tTime taken %s'%(t2-t1)

        print 'deleting graph'
        t1 = time.time()
        self.delete_location()
        t2 = time.time()
        print '\t\tTime taken %s'%(t2-t1)
        
        print 'Starting conversion from carray to numpy'
        t1 = time.time()
        new_loc = self.carray_to_numpy(loc_arr, loc_len, 0)
        t2 = time.time()
        print '\t\tTime taken %s'%(t2-t1)
        
        #before returning the location choices delete the locations carray
        print 'deleting all the carrays'
        t1 = time.time()
        self.delete_carray(loc_arr, 0)
        t2 = time.time()
        print '\t\tTime taken %s'%(t2-t1)
        
        #change the dimensions of the new_loc numpy array
        new_loc.shape = (arr_len, num_of_locations)
        #return the locations numpy array
        return new_loc
            
        
    def delete_carray(self, carray, data_type):
        """
        This method is used to delete the carrays
        
        Input:
        Origin, destination and travel time carrays
        
        Output:
        Carrays deleted
        """
        if data_type == 1:
            arrayexample.delete_floatArray(carray)
        else:
            arrayexample.delete_intArray(carray)
        print 'Carray deleted.'
        
        
    def delete_graph(self):
        """
        This method is used the delete the dynamic arrays created 
        in the C program
        
        Input:
        None
        
        Output:
        Dynamic Arrays deleted
        """
        arrayexample.delete_array()
        print 'Dynamic arrays deleted'
        
    
    def delete_location(self):
        """
        This method deletes the locations array in the C program
        
        Input:
        None
        
        Output:
        Dynamic array deleted
        """
        arrayexample.delete_location_array()
        print 'Dynamic location array deleted'
        
        
    def set_string(self, file_path, flag):
        """
        This method is used to assign the file names
        """
        arrayexample.set_file(file_path, 1, flag)
        arrayexample.print_string()



#unit test to test the code
import unittest

#define a class for testing
class TestExtensions(unittest.TestCase):
    def setUp(self):
        self.numarr = 'numarr'
        self.offset = 1
        self.nodes = 0

    def testEx(self):
        ext_obj = Extensions(self.offset, self.nodes)
        
        origin = zeros(10000)
        destination = zeros(10000)
        arr_len = origin.size

        num_of_locations = 60        
        #loc_len = arr_len * num_of_locations
        
        i = 0
        j = 1000
        offset = 1

        # 1st thousand
        for i in range(0, 1000):
            origin[i] = i+offset
            destination[i] = j*2
            j = j - 1
          
        # 2nd thousand
        j = 1000
        for i in range(1000, 2000):
            origin[i] = i+offset
            destination[i] = j
            j = j -1
        
        #3rd thousand
        j = 2000
        for i in range(2000, 3000):
            origin[i] = i/10
            destination[i] = j
            j = j - 1
        
        # 4th thousand
        j = 1500
        for i in range(3000, 4000):
            origin[i] = i/10
            destination[i] = j
            j = j -1
            
        # 5th thousand
        j = 1200
        for i in range(4000, 5000):
            origin[i] = i/10
            destination[i] = j
            j = j - 1
        
        # 6th thousand
        j = 1800
        for i in range(5000, 6000):
            origin[i] = i/10
            destination[i] = j
            j = j -1

        # 7th thousand
        j = 1400
        for i in range(6000, 7000):
            origin[i] = i/10
            destination[i] = j
            j = j -1
            
        # 8th thousand
        j = 1700
        for i in range(7000, 8000):
            origin[i] = i/10
            destination[i] = j
            j = j -1

        # 9th thousand
        j = 1300
        for i in range(8000, 9000):
            origin[i] = i/10
            destination[i] = j
            j = j -1
            
        # 10th thousand
        j = 1600
        for i in range(9000, 10000):
            origin[i] = i/10
            destination[i] = j
            j = j -1
        
        #origin destination arrays created
        
        """
        To get travel times
        """
        #pass file paths to the C program
        node_path = "/home/namrata/Documents/swig/arr_sample/temp_data_copy.csv"
        graph_path = "/home/namrata/Documents/swig/arr_sample/skim1.dat"

        flag = 1
        ext_obj.set_string(node_path, flag)
        flag = 0
        ext_obj.set_string(graph_path, flag)
        
        #create the travel times graph
        print 'creating the graph'
        t1 = time.time()
        n, e = ext_obj.create_graph()
        print 'n: %s e: %s'%(n, e)
        t2 = time.time()
        print '\t\t\tTime taken %s'%(t2-t1)
        
        #origin destination arrays created. get travel times
        print 'travel times'
        print '\t\t\t\t', time.time()
        new_tt = ext_obj.get_travel_times(origin, destination)
        print '\t\t\t\t', time.time()
        
        #the numpy array new_tt has the travel times.
        
        
        """
        For location choices
        """
        #initialize the location array
        print 'creating location graph'
        t1 = time.time()
        ext_obj.create_location_array(arr_len)
        t2 = time.time()
        print '\t\t\t\t', time.time()
        
        #get location choices
        print 'location choices'
        t1 = time.time()
        new_loc = ext_obj.get_location_choices(origin, destination, new_tt, num_of_locations)
        t2 = time.time()
        print '\t\t\t\t', time.time()
        
        #the numpy array new_loc has all the location choices
        
        #after all computations are done delete all the arrays in the C program
        print 'deleting graph'
        t1 = time.time()
        ext_obj.delete_graph()
        t2 = time.time()
        print '\t\tTime taken %s'%(t2-t1)
        
        print 'tt array is new_tt'
        print new_tt.size
        print new_tt[100]
        
        print 'location choices is new_loc'
        print new_loc.size
        print new_loc.ndim
        print new_loc[4][5]

        
        
if __name__ == '__main__':
    unittest.main()
        
