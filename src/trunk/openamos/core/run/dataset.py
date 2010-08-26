import tables as t

class Vehicles_R(t.IsDescription):
    houseid = t.Int32Col()
    vehid = t.Int16Col()
    vehtype = t.Int16Col()


class Households_R(t.IsDescription):
    houseid = t.Int32Col()
    numvehs = t.Int16Col()

class Tsp_R(t.IsDescription):
    houseid = t.Int32Col()
    personid = t.Int16Col()
    daystart = t.Float32Col()
    dayend = t.Float32Col()
	

class DB(object):
    def __init__(self, mode):
        pass
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
    def create(self):
        self.fileh = t.openFile("/home/kkonduri/simtravel/test/amosdb.h5", mode="w")
        root = self.fileh.root

        vehicles_r_grp = self.fileh.createGroup(root, "vehicles_r_grp")
        households_r_grp = self.fileh.createGroup(root, "households_r_grp")
        tsp_r_grp = self.fileh.createGroup(root, "tsp_r_grp")


        vehicles_r = self.fileh.createTable(vehicles_r_grp, "vehicles_r", Vehicles_R)
        households_r = self.fileh.createTable(households_r_grp, "households_r", Households_R)
        tsp_r = self.fileh.createTable(tsp_r_grp, "tsp_r", Tsp_R)

        
    def returnTableReference(self, tableName):
        tableName = tableName.lower()
        loc = '/%s_grp' %(tableName)
        return self.fileh.getNode(loc, name=tableName)

    def close(self):
        fileh.close()
    
if __name__ == '__main__':
    db = DB('w')
    db.create()
    table = db.returnTableReference('households_r')
