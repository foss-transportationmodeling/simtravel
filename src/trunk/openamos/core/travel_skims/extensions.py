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


    def create_carray(self):
        """
        This method is used to create the origin and destination carrays.
        
        Input: Origin and destination numpy arrays
        
        Output: Origin and destination carrays
        """
        print 'testing carray creation'
        p = arrayexample.new_floatArray(10)
        arrayexample.create_array(p, 10)
        arrayexample.print_array(p, 10)
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
        #get the nodes and edges
        nodes, edges = self.get_graph_nodes()
        
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
        
        
    def numpy_to_carray(self, numpy_arr, arr_len):
        """
        This method converts the numpy array to a carray
        
        Input:
        Numpy array
        
        Output:
        Carray
        """
        new_carr = arrayexample.new_floatArray(arr_len)
        i = 0

        for each in numpy_arr:
            arrayexample.floatArray_setitem(new_carr, i, float(each))
            i = i + 1

        return new_carr

        
    def carray_to_numpy(self, carray, arr_len):
        """
        This method converts carray to numpy
        
        Input:
        Carray
        
        Output:
        Numpy Array
        """
        numpy_arr = zeros(arr_len)

        for i in range(arr_len):
            numpy_arr[i] = arrayexample.floatArray_getitem(carray,i)
            numpy_arr[i]

        return numpy_arr
        
    
    def get_travel_times(self, origin, destination, tt, arr_len):
        """
        This method is used to get the travel times
        
        Input:
        Origin and destination arrays and array length
        
        Output:
        Returns an array with travel times
        """         
        #convert the arrays to carrays
        print 'starting conversion from numpy to carray'
        t1 = time.time()
        org_arr = self.numpy_to_carray(origin, arr_len)
        dest_arr = self.numpy_to_carray(destination, arr_len)
        tt_arr = self.numpy_to_carray(tt, arr_len)
        t2 = time.time()
        print '\t\tTime taken %s'%(t2-t1)
               
        print 'Starting travel times computation'
        t1 = time.time()
        arrayexample.get_tt(org_arr, dest_arr, tt_arr, arr_len, self.offset)
        t2 = time.time()
        print '\t\tTime taken %s'%(t2-t1)

        print 'deleting origin and destination carrays'
        t1 = time.time()
        self.delete_carray(org_arr)
        self.delete_carray(dest_arr)
        t2 = time.time()
        print '\t\tTime taken %s'%(t2-t1)

        print 'Starting conversion from carray to numpy'
        t1 = time.time()
        new_tt = self.carray_to_numpy(tt_arr, arr_len)
        t2 = time.time()
        print '\t\tTime taken %s'%(t2-t1)
        
        print 'Delete the tt carray'
        self.delete_carray(tt_arr)
        
        #return the numpy array
        return new_tt
        
        
    def delete_carray(self, carray):
        """
        This method is used to delete the carrays
        
        Input:
        Origin, destination and travel time carrays
        
        Output:
        Carrays deleted
        """
        arrayexample.delete_floatArray(carray)
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
        
    def set_string(self, file_path, flag):
        """
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
        
        node_path = "/home/namrata/Documents/swig/arr_sample/temp_data_copy.csv"
        graph_path = "/home/namrata/Documents/swig/arr_sample/skim1.dat"
        flag = 1
        ext_obj.set_string(node_path, flag)
        flag = 0
        ext_obj.set_string(graph_path, flag)

        n, e = ext_obj.create_graph()
        print 'n: %s e: %s'%(n, e)
        #arrayexample.print_org_array(self.offset)
        #for small sample
        """
        origin = array([1,2,3,4,5,6,7,8,9,10])
        destination = array([10,9,8,7,6,5,4,3,2,1])
        arr_len = origin.size
        tt = zeros(arr_len)
        
        origin = zeros(10)
        destination = zeros(10)
        arr_len = origin.size
        tt = zeros(arr_len)
        i = 0
        j = 10
        offset = 1
        for i in range(0,10):
            origin[i] = i + offset
            destination[i] = j
            j = j - 1
        """
        
        #for full data
        #create origin and destination arrays
        origin = zeros(10000)
        destination = zeros(10000)
        arr_len = origin.size
        tt = zeros(arr_len)
        print '\t\t\t', arr_len
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
        
        
        print 'travel times'
        print '\t\t\t\t', time.time()
        new_tt = ext_obj.get_travel_times(origin, destination, tt, arr_len)
        print '\t\t\t\t', time.time()
                
        print 'array size ', new_tt.size
        """
        #for each in new_tt:
        #    print each
        org = ext_obj.numpy_to_carray(origin, arr_len)
        dest = ext_obj.numpy_to_carray(destination, arr_len)
        tt_arr = ext_obj.numpy_to_carray(new_tt, arr_len)
        arrayexample.print_tt_array(org, dest, tt_arr, arr_len)
        """
        for i in range(0, 100):
            print new_tt[i]
        
        ext_obj.delete_graph()
        
        

if __name__ == '__main__':
    unittest.main()
        
