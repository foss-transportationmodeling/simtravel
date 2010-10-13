



class TravelSkimsPeriodDBInfo(object):
    def __init__(self, tableName, origin_var, destination_var, 	
                 skims_var, intervalStart, intervalEnd, targetTableName=None):
        self.tableName = tableName
        self.origin_var = origin_var
        self.destination_var = destination_var
        self.skims_var = skims_var
        self.intervalStart = intervalStart
        self.intervalEnd = intervalEnd
        self.targetTableName = targetTableName


    def __repr__(self):
        return ("""Table name - %s, Target table name - %s, """\
                    """origin variable - %s, destination variable - %s, """\
                    """skims variable - %s, interval start - %s, """\
                    """interval end - %s""" %(self.tableName, self.targetTableName,
                                              self.origin_var, self.destination_var,
                                              self.skims_var, self.intervalStart,
                                              self.intervalEnd))

class TravelSkimsInfo(object):
    def __init__(self, referenceTableName, indb_flag=True):
        self.referenceTable = referenceTableName
        if indb_flag == None:
            indb_flag = False
            
        self.indb_flag = indb_flag
        self.table_lookup = {}
        self.tableDBInfoList = []
        self.tableNamesList = []

    def add_tableLookup(self, intervalStart, intervalEnd, tableName):
        self.table_lookup[(intervalStart, intervalEnd)] = tableName
        print 'tablename - %s, start - %s, end - %s' %(tableName, intervalStart,
                                                       intervalEnd)
        
    def add_tableInfoToList(self, tableName, origin_var, destination_var,
                            skims_var, intervalStart, intervalEnd, targetTableName):
        if tableName not in self.tableNamesList:
            dbInfoObject = TravelSkimsPeriodDBInfo(tableName, origin_var,
                                                   destination_var, 
                                                   skims_var,
                                                   intervalStart,
                                                   intervalEnd)
            print dbInfoObject
            self.tableDBInfoList.append(dbInfoObject)
            self.tableNamesList.append(tableName)
        self.add_tableLookup(intervalStart, intervalEnd, tableName)


    def lookup_table(self, period):
        period_boundaries = self.table_lookup.keys()
        period_boundaries.sort()
        

        for boundary in period_boundaries:
            if period >= boundary[0] and period <= boundary[1]:
                return self.table_lookup[boundary]

        return None


            
                 
