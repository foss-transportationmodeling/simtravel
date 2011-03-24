import time

from numpy import unique, int64, int32, float32, float64, load
from numpy.ma import zeros, masked_equal, ones
from openamos.core.data_array import DataArray

class DB(object):
    def __init__(self):
    
        # TODO: where do we get the table definitions and relationships from
        # for now this is static



	self.tableCols = {'travel_skims':['origin', 'destination', 'tt'], 
			  'locations':['locationid', 'population', 'public_employment', 'retail_employment',
				       'office_employment', 'industrial_employment', 'other_employment', 
				       'public_employment_ind', 'retail_employment_ind', 'office_employment_ind',
				       'industrial_employment_ind', 'other_employment_ind', 'total_area', 
				       'residential_population', 'single_family_dwelling', 'institutional_population',
				       'multi_family_dwelling'],
			  'households_vehicles_count_r':['houseid', 'vehcount'],
			  'vehicles_r':['houseid', 'vehid', 'vehtype'],
			  'schedule_r':['houseid', 'personid', 'scheduleid', 'activitytype', 'locationid', 'starttime',
					'endtime', 'duration', 'dependentpersonid'],
  			  'schedule_ltrec_r':['houseid', 'personid', 'scheduleid', 'activitytype', 'locationid', 'starttime',
					'endtime', 'duration', 'dependentpersonid'],
			  'schedule_cleanfixedactivityschedule_r':['houseid', 'personid', 'scheduleid', 'activitytype', 'locationid', 'starttime',
					'endtime', 'duration', 'dependentpersonid'],
			  'schedule_childreninctravelrec_r':['houseid', 'personid', 'scheduleid', 'activitytype', 'locationid', 'starttime',
					'endtime', 'duration', 'dependentpersonid'],
			  'schedule_conflictrec_r':['houseid', 'personid', 'scheduleid', 'activitytype', 'locationid', 'starttime',
					'endtime', 'duration', 'dependentpersonid'],
			  'schedule_inctravelrec_r':['houseid', 'personid', 'scheduleid', 'activitytype', 'locationid', 'starttime',
					'endtime', 'duration', 'dependentpersonid'],
			  'schedule_dailyallocrec_r':['houseid', 'personid', 'scheduleid', 'activitytype', 'locationid', 'starttime',
					'endtime', 'duration', 'dependentpersonid'],
			  'schedule_final_r':['houseid', 'personid', 'scheduleid', 'activitytype', 'locationid', 'starttime',
					'endtime', 'duration', 'dependentpersonid'],

			  'trips_r':['houseid', 'personid', 'vehid', 'tripmode', 'fromzone', 'tozone', 'starttime', 'endtime', 'trippurpose'],
			  'trips_to_malta_r':['tripid', 'houseid', 'personid', 'vehid', 'tripmode', 'fromzone', 'tozone', 'starttime', 'endtime', 'trippurpose'],
			  'trips_arrival_from_malta_r':['tripid', 'arrivaltime'],
			  'workers_r':['houseid', 'personid', 'episodes'], 
			  'child_dependency_r':['houseid', 'personid', 'dependency'],
			  'daily_school_status_r':['houseid', 'personid', 'schdailystatus'],
			  'daily_work_satus_r':['houseid', 'personid', 'wrkdailystatus']}



	self.colDef = {'houseid':int64, 'personid':int32, 'dependency':int32, 'schdailystatus':int32,
			'wrkdailystatus':int32, 'episodes':int32, 'tripid':int32, 'vehid':int32, 
			'tripmode':int32, 'fromzone':int32, 'tozone':int32, 'starttime':int32,
			'endtime':int32, 'origin':int32, 'destination':int32, 'tt':float32, 'locationid':int32,
			'trippurpose':int32, 'arrivaltime':int32, 
			'population':int32, 'public_employment':int32, 'retail_employment':int32, 
			'office_employment':int32, 'industrial_employment':int32, 'other_employment':int32, 
			'public_employment_ind':int32, 'retail_employment_ind':int32, 
			'office_employment_ind':int32, 'industrial_employment_ind':int32, 'other_employment_ind':int32, 
			'total_area':float32, 'residential_population':int32, 'single_family_dwelling':int32, 
			'institutional_population':int32, 'multi_family_dwelling':int32, 'vehcount':int32, 
			'vehtype':int32, 'scheduleid':int32, 'activitytype':int32, 'duration':int32, 
			'dependentpersonid':int32}

	

    def tableColTypes(self, tableName):
	colTypes = {}
	for col in self.tableCols[tableName]:
	    colTypes[col] = self.colDef[col]
	return colTypes


    def returnTypeConversion(self, tableName):
        colDtypes = self.tableColTypes(tableName)

        uniqColDtypes = list(set(colDtypes.values()))

        for i in uniqColDtypes:
            if i in [int32, int64]:
                convType = "int"
            if i in [float32, float64]:
                convType = "float"
                return convType
        return convType


    def returnCols(self, tableName):
	return self.tableCols[tableName]

    def returnColId(self, tableName, colName):
	return self.tableCols[tableName].index(colName)

    def returnTable(self, tableName, id_var, colNames, fileLoc):
	
	data = load('%s/%s.npy' %(fileLoc, tableName))

	colId = self.returnColId(tableName, id_var)
	idVarColumn = data[:,colId]
	
	uniqueIds = unique(idVarColumn.astype(int))

	table = zeros((max(uniqueIds) + 1, len(colNames)))

	#print data.shape
	#print len(uniqueIds)

        for i in range(len(colNames)):
	    print i
	    table[uniqueIds, i] = data[:,i]
	
	#print table
	return DataArray(table, colNames), uniqueIds



    def returnTableAsMatrix(self, tableName, originColName, destinationColName, 
			    skimColName, fileLoc, fillValue=9999):
        
	data = load('%s/%s.npy' %(fileLoc, tableName))

        origin = data[:,0].astype(int)
        destination = data[:,1].astype(int)
        skims = data[:,2]

	#print origin[:5]

        # Initialize matrix
        skimsMatrix = ones((max(origin)+1, max(destination)+1)) * fillValue

        # Populate matrix
        skimsMatrix[origin, destination] = skims
	#skimsMatrix = masked_equal(skimsMatrix, 9999)
        
        return masked_equal(skimsMatrix, 9999), unique(origin)

    
if __name__ == '__main__':
    db = DB('w')
    db.create()
    table = db.returnTableReference('households_r')
