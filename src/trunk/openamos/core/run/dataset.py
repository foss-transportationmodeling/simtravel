import tables as t
import time

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
        #Input Tables - Creatign the table
        self.fileh.createTable(input_grp, "travel_skims", Travel_Skims)
        self.fileh.createTable(input_grp, "households", Households)
        self.fileh.createTable(input_grp, "persons", Persons)

        
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
        query_gen, cols = queryBrowser.select_all_from_table(tableName)
        print 'Time taken to retrieve records %.4f' %(time.time()-t)

        tableRef = self.returnTableReference(tableName)
        
        tableRow = tableRef.row

        indices = range(len(cols))

        for i in query_gen:
            for j in indices:
                if i[j] is not None:
                    tableRow[cols[j]] = i[j]
            tableRow.append()
        tableRef.flush()
        print 'Time taken to write to hdf5 format %.4f' %(time.time()-t)
        

    def createNetowrkArray(self, tableName):
        tableRef = self.returnTableReference(tableName)

        tableRow = tableRef.row


    def close(self):
        fileh.close()
    
if __name__ == '__main__':
    db = DB('w')
    db.create()
    table = db.returnTableReference('households_r')
