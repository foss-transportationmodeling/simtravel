



class TravelSkimsPeriodDBInfo(object):
    def __init__(self, tableName, origin_var, destination_var, 	
                 skims_var, intervalStart, intervalEnd,
		 import_flag=None, file_location=None, delimiter=None):
        self.tableName = tableName
        self.origin_var = origin_var
        self.destination_var = destination_var
        self.skims_var = skims_var
        self.intervalStart = intervalStart
        self.intervalEnd = intervalEnd
	self.importFlag = import_flag
	self.fileLocation = file_location
	self.delimiter = delimiter

    def __repr__(self):
        return ("""\tTravel skims table that will be cached - %s """\
                    """\n\t\tOrigin variable - %s, Destination variable - %s, """\
                    """Skims variable - %s, Interval start - %s, """\
                    """Interval end - %s""" %(self.tableName, 
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
        print '\tSkims table name - %s applies for interval starting at %s and ending at %s' %(tableName, intervalStart,
                                                              intervalEnd)
        
    def add_tableInfoToList(self, tableName, origin_var, destination_var,
                            skims_var, intervalStart, intervalEnd, targetTableName,
			    import_flag=None, file_location=None, delimiter=None):
        if tableName not in self.tableNamesList:
            dbInfoObject = TravelSkimsPeriodDBInfo(tableName, origin_var,
                                                   destination_var, 
                                                   skims_var,
                                                   intervalStart,
                                                   intervalEnd,
						   import_flag,
						   file_location,
						   delimiter)
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


            
                 
