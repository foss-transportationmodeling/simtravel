import tables as t
import time

from numpy import unique
from numpy.ma import zeros, masked_values, ones
from openamos.core.run.dataset_table_layouts import *

class DB(object):
    def __init__(self, fileLoc, mode='w'):
        self.fileh = t.openFile("%s/amosdb.h5" %(fileLoc), mode=mode)

    """
        self.groupDict = {'households_r':'households',
                          'vehicles_r':'households',
                          'person_r':'persons',
                          'tsp_r':'persons',
                          'scehulde_r':'persons',
                          'trips_r':'persons'}

        # TODO: where do we get the table definitions and relationships from
        # for now this is static
        self.tableDefDict = {'households_r':['houseid, numvehs'],
                             'vehicles_r':['houseid', 'vehid', 'vehtype'],
                             'person_r':['persons'],
                             'tsp_r':'persons',
                             'scehulde_r':'persons',
                             'trips_r':'persons'}
    """    
    def create(self, tableName=None):
        # TODO: create output/input tables everytime?

        # Output Tables - Creating groups
        output_grp = self.fileh.createGroup(self.fileh.root, "output_grp")
        # Input Tables - Creating groups
        input_grp = self.fileh.createGroup(self.fileh.root, "input_grp")

        # Output Tables - Creating the table
        self.fileh.createTable(output_grp, "vehicles_r", Vehicles_R)
        self.fileh.createTable(output_grp, "households_r", Households_R)
        self.fileh.createTable(output_grp, "tsp_r", Tsp_R)
        self.fileh.createTable(output_grp, "schedule_r", Schedule_R)
        self.fileh.createTable(output_grp, "persons_r", Persons_R)
        #Input Tables - Creatign the table
        self.fileh.createTable(input_grp, "travel_skims", Travel_Skims)
        self.fileh.createTable(input_grp, "households", Households)
        self.fileh.createTable(input_grp, "persons", Persons)


    def close(self):
        self.fileh.close()
        
    def returnGroup(self, tableName):
        if tableName[-2:] == "_r":
            return 'output'
        else:
            return 'input'


    def returnTableReference(self, tableName):
        tableName = tableName.lower()
        grp = self.returnGroup(tableName)
        loc = '/%s_grp' %(grp)
        return self.fileh.getNode(loc, name=tableName)

    def createTableFromDatabase(self, tableName, queryBrowser):
        t = time.time()
        data = queryBrowser.select_all_from_table(tableName)
        print 'Time taken to retrieve records %.4f' %(time.time()-t)

        cols = data.varnames
        colIndices = range(data.cols)
        
        tableRef = self.returnTableReference(tableName)
        tableRow = tableRef.row


        for i in data.data:
            for j in colIndices:
                if i[j] is not None:
                    tableRow[cols[j]] = i[j]
            tableRow.append()
        tableRef.flush()
        print 'Time taken to write to hdf5 format %.4f' %(time.time()-t)
        

    def returnTableAsMatrix(self, tableName, originColName, destinationColName, skimColName, fillValue=9999):
        tableRef = self.returnTableReference(tableName)
        
        origin = tableRef.col(originColName)
        destination = tableRef.col(destinationColName)
        skims = tableRef.col(skimColName)

        # Initialize matrix
        skimsMatrix = ones((max(origin)+1, max(destination)+1)) * fillValue
        #skimsMatrix.fill(fillValue)

        # Populate matrix
        skimsMatrix[origin, destination] = skims
        #skimsMatrix = masked_values(skimsMatrix, 0)
        
        return skimsMatrix, unique(origin)


    
if __name__ == '__main__':
    db = DB('w')
    db.create()
    table = db.returnTableReference('households_r')
