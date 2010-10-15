#main class. this class will be used to define the database connection.
#it will create/drop database, schema and tables
 

#include all the import 
import sys
import os
import exceptions
import time
import sqlalchemy
import psycopg2 as dbapi2
import numpy as na
from cursor_database_connection import DataBaseConnection
from psycopg2 import extensions
from sqlalchemy.types import Integer, SmallInteger, \
			     Numeric, Float, \
			     VARCHAR, String, CLOB, Text,\
			     Boolean, DateTime
from numpy import array, ma
from database_configuration import DataBaseConfiguration
from openamos.core.data_array import DataArray

class QueryBrowser(object):
    #initialize the class 

    def __init__(self,dbconfig):
        
        if not isinstance(dbconfig, DataBaseConfiguration):
            raise DatabaseConfigurationError, """The dbconfig input is not a valid """\
                """DataBaseConfiguration object."""

        self.protocol = dbconfig.protocol
        self.user_name = dbconfig.user_name
        self.password = dbconfig.password
        self.host_name = dbconfig.host_name
        self.database_name = dbconfig.database_name
        self.database_config_object = dbconfig
        self.dbcon_obj = DataBaseConnection(dbconfig)
        #print self.dbcon_obj

    ########## methods for select query  ##########
    #select all rows from the table
    def select_all_from_table(self, table_name, cols=None):
        """
        This method is used to fetch all rows from the table specified.

        Input:
        Class name corresponding to the table

        Output:
        Returns all the rows in the table
        """
	colsStr = ""
	if cols == None:
            colsStr = "*"
	else:
	    for i in cols:
		colsStr += "%s," %(i)
	    colsStr = colsStr[:-1]


        #check if table exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        if tab_flag:
            #print 'Table %s exists.'%table_name
            try:    
                self.dbcon_obj.cursor.execute("SELECT %s FROM %s" %(colsStr, table_name))
                result = self.dbcon_obj.cursor.fetchall()
                cols_list = self.dbcon_obj.get_column_list(table_name)
                
                data = self.createResultArray(result, cols_list)

                #return data, cols_list ##changes made here
                return data
            except Exception, e:
                print 'Error while retreiving the data from the table'
                print e
        else:
            print 'Table %s does not exist.'%table_name
    
  
    #select rows based on a selection criteria
    def fetch_selected_rows(self, table_name, column_name, value):
        """
        This method is used to fetch selected rows fom the table in the database.

        Input:
        Database configuration object, class name and selection criteria.

        Output:
        Returns the rows that satisfy the selection criteria
        """
        fin_flag = None
        #check if table exists and then if columns exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        if tab_flag:
            #check for columns
            get_cols = self.dbcon_obj.get_column_list(table_name)
            if column_name in get_cols:
                fin_flag = True
            else:
                fin_flag = False
        else:
            print 'Table %s does not exist.'%table_name
            
        if fin_flag:
            try:
                self.dbcon_obj.cursor.execute("SELECT * FROM %s where %s = '%s'"%(table_name, column_name, value))
                data = self.dbcon_obj.cursor.fetchall()
    
                row_list = []
                counter = 0
                for each in data:
                    counter = counter + 1
                    row_list.append(each)

                if counter == 0:
                    print 'No rows selected.\n'           
                print 'Select query successful.\n'
                return self.dbcon_obj.cursor, row_list
            except Exception, e:
                print 'Error retrieving the information. Query failed.\n'
                print e
        else:
            print 'Column %s does not belong to the table %s'%(column_name, table_name)
            return None    


    def select_join(self, db_dict, column_names, table_names, max_dict=None, 
                    spatialConst_list=None, analysisInterval=None, subsample=None):
        """
        This method is used to select the join of tables and display them.
        
        Input:
        Database configuration object, table names, columns and values.
        
        Output:
        Displays the rows based on the join and the selection criterion.
        """
        #db_dict = {'households': ['urb', 'numchild', 'inclt35k', 'ownhome', 'one', 'drvrcnt', 'houseid'], 
        #           'vehicles_r': ['vehtype', 'vehid'], 
        #           'households_r': ['numvehs']}
        #columns_names = ['houseid']
        #table_names = ['households', 'households_r', 'vehicles_r']
        #max_dict = {'vehicles_r':['vehid']}
        
        # Prism Query or or just a Travel Time Query with Vertices
        # ADD APPROPRIATE JOIN/?INNER JOINS


        #print 'Database Dictionary of Table and Columns - ', db_dict
        #print 'Column Names', column_names
        #raw_input()

        #initialize the variables
        final_list = []
        table_list = []
        class_list = []
        cols_list = []
        tabs_list = []
        #col_name = column_name
        final_col_list = db_dict.values()
        table_list = db_dict.keys()

        table_flag = None
        all_tables = table_list + table_names

        #check if the tables exist in the database.
        for each_tab in all_tables:
            table_flag = self.dbcon_obj.check_if_table_exists(each_tab)
            if table_flag:
                pass
            else:
                print 'Table %s does not exist in the database. Exiting the funtion.'%each_tab
                return 0
        
        #similarly check if the table in the list exists
        num_tab = len(list(set(table_list) & set(table_names)))
        if num_tab <= len(table_list):
            #print 'Tables exist'
            pass
        else:
            #print 'Tables do not exists'
            return None
        
        #check for the columns passed in the dictionary
	tables = db_dict.keys()
	tables.sort()
        for i in tables:
            clist = self.dbcon_obj.get_column_list(i.lower())
            list1 = db_dict[i]
            chk_list = len(list(set(list1) & set(clist)))
            if chk_list == len(list1):
	        cols = db_dict[i]
	        cols.sort()
                for j in cols:
                    #print '\tColumn - ', j
                    new_str = i.lower() + '.' + j.lower()
                    final_list.append(new_str)                    
                cols_list = cols_list + cols
                #print cols_list, 'initial list without spatial const'
            else:
                print ('Column passed in the dictionary does not exist in the table - ')
                print 'Column List in the Table - ', clist
                print 'Actual List of Columns requested from table - ', list1
                
                return None
        #print 'final_list is %s'%final_list
        

                
        #print 'FINAL LIST', final_list
        #print 'TABLE LIST', table_list

        # Generating the left join statements
        mainTable = table_names[0]
        #print 'mainTable ----> ', mainTable

        primCols = []
        for i in column_names:
            primCols += column_names[i]
        primCols = list(set(primCols))

        joinStrList = []
        for table in table_list:
            if table == mainTable:
                continue
            joinCondition = ''
            for col in column_names[table]:
                joinCondition = (joinCondition 
                                 + ' %s.%s=%s.%s ' %(mainTable, col, 
                                                     table, col) 
                                 + 'and')
                
            joinCondition = joinCondition[:-3]
            joinStr = ' left join %s on (%s)' %(table, joinCondition)
            joinStrList.append(joinStr)

        #print 'JOIN STRING LIST', joinStrList

        #check the max flag
        
        if max_dict is not None:
            max_flag = 1
            max_table = max_dict.keys()
            max_column = max_dict.values()[0][0]
            #print max_column, max_table
            #for each in max_dict.values():
            #    max_column = each[0]
        else:
            max_flag = 0

        # Index of the table containing the max dict var
        # as it stands only querying for one count variable is 
        # provided
        #print max_dict
        if max_dict is not None:
            maxTable = max_dict.keys()[0]
            maxColumn = max_dict.values()[0][0]
            index = table_list.index(maxTable)
            #print 'INDEX--->', index
        
            #remove the count column from the col list
            countVarStr = '%s.%s' %(maxTable, maxColumn)
            final_list.remove(countVarStr)
            final_list.append('temp.%s'%maxColumn)
            cols_list.remove(maxColumn)
            cols_list.append(maxColumn)

            #print 'NEW FINAL LIST -->', final_list

            # left join for the count variable
            joinStr = ''


            #grouping string
            grpStr = ''
            joinCondition=''

            #print 'column_names of max TABLE ----->', column_names
            for i in column_names[maxTable]:
                #print 'createing join string for column name - ', i
                grpStr = grpStr + '%s,' %(i)
                joinCondition = (joinCondition 
                                 + ' temp.%s=%s.%s ' %(i, 
                                                       mainTable, i) 
                                 + 'and')
            grpStr = grpStr[:-1]
            joinCondition = joinCondition[:-3]
            
        #combine left join along with the count variable/max condition
            mJoinStr = joinStrList.pop(index-1)
            mJoinStrIncMaxConditionVar = (mJoinStr[:-1] + 
                                          'and %s.%s=temp.%s)' 
                                          %(maxTable, maxColumn, maxColumn))
            
            joinStrList.append(""" left join (select %s, max(%s) as %s from """
                               """%s group by %s) as temp on (%s) """ %(grpStr, maxColumn, 
                                                                        maxColumn,maxTable, grpStr,
                                                                        joinCondition)
                               + mJoinStrIncMaxConditionVar)
            #print 'LEFT JOIN MAX COL LIST--->', joinStrList
	"""        
        # separate all the columns from the lists
        new_keys = db_dict.keys()
        for i in new_keys:
	    cols = db_dict[i]
	    cols.sort()
            cols_list = cols_list + cols
        """    


        # Spatial TSP identification
        if spatialConst_list is not None:
            for i in spatialConst_list:
                if i.countChoices is not None:
                    # substring for the inner join
                    stTable = i.startConstraint.table
                    #stLocationField = 'st_' + i.startConstraint.locationField
                    stLocationCol = 'stl.%s' %i.startConstraint.locationField
                    #stTimeField = 'st_'+ i.startConstraint.timeField
                    stTimeCol = 'st.%s' %i.startConstraint.timeField

                    enTable = i.endConstraint.table
                    #enLocationField = 'en_' + i.endConstraint.locationField
                    enLocationCol = 'enl.%s' %i.endConstraint.locationField
                    #enTimeField = 'en_' + i.endConstraint.timeField                    
                    enTimeCol = 'en.%s' %i.endConstraint.timeField

                    timeCols = [stTimeCol, enTimeCol]

                    table_list.append(stTable)
                    

                    # left join for end location
                    
                    # time cols are part of sptime
                    timeColsNewNames = []
                    for j in timeCols:
                        timeColsNewNames.append(j.replace('.', '_'))
                        
                    timeColsStr = ''
                    for j in range(len(timeCols)):
                        # minimum of the time cols gives the first prism
                        timeColsStr += 'min(%s) %s,' %(timeCols[j], timeColsNewNames[j])

                    timeColsStr = timeColsStr[:-1]

                    spGrpNewNameStr = ''
                    spGrpStr = ''
                    for j in column_names[stTable]:
                        spGrpNewNameStr += 'st.%s %s,' %(j, j)
                        spGrpStr += 'st.%s,' %(j)
                    spGrpNewNameStr = spGrpNewNameStr[:-1]
                    spGrpStr = spGrpStr[:-1]

                    spInnerJoinCondition = ''
                    for j in column_names[stTable]:
                        spInnerJoinCondition += ' %s.%s = %s.%s and' %('st', j, 'en', j)
                    spInnerJoinCondition = spInnerJoinCondition[:-3]
                        
                    spJoinCondition = ''
                    for j in column_names[stTable]:
                        spJoinCondition += ' %s.%s = %s.%s and' %('sptime', j, mainTable, j)
                    spJoinCondition = spJoinCondition[:-3]

                    # Left join condition for prism start location
                    stLocJoinCondition = ''
                    stLocCondCols = column_names[stTable] 
                    for j in stLocCondCols:
                        stLocJoinCondition += ' %s.%s = %s.%s and' %('stl', j, mainTable, j)
                    stLocJoinCondition += ' sptime.st_%s = %s.%s' %(i.startConstraint.timeField,
                                                               'stl', i.startConstraint.timeField)

                    final_list.append('stl.%s as st_%s' %(i.startConstraint.locationField,
                                                          i.startConstraint.locationField))
                    cols_list.append('st_%s' %i.startConstraint.locationField)
                    #stLocJoinCondition = stLocJoinCondition[:-3]

                    # Left join condition for prism end location
                    enLocJoinCondition = ''
                    enLocCondCols = column_names[stTable] 
                    for j in enLocCondCols:
                        enLocJoinCondition += ' %s.%s = %s.%s and' %('enl', j, mainTable, j)
                    enLocJoinCondition += ' sptime.en_%s = %s.%s' %(i.endConstraint.timeField,
                                                               'enl', i.endConstraint.timeField)
                    final_list.append('enl.%s as en_%s' %(i.endConstraint.locationField, 
                                                       i.endConstraint.locationField))
                    cols_list.append('en_%s' %i.endConstraint.locationField)
                    #enLocJoinCondition = enLocJoinCondition[:-3]

                    
                    # TSP consistency check
                    # nextepisode_starttime > lastepisode_endtime
                    #consistencyStr = '%s < %s' %(stTimeCol, endTimeCol)
                    

                    analysisPeriodStr = ('%s=%s and %s>%s' 
                                         %(stTimeCol, analysisInterval,
                                           enTimeCol, analysisInterval))
        
                    spatialJoinStr = (""" join (select %s, %s """\
                                          """from %s as %s """\
                                          """inner join %s as %s """\
                                          """on ( %s and %s) group by"""\
                                          """ %s) """\
                                          """as sptime on (%s)"""
                                      % (spGrpNewNameStr, timeColsStr, 
                                         stTable, 'st', 
                                         enTable, 'en',
                                         spInnerJoinCondition, analysisPeriodStr,
                                         spGrpStr,
                                         spJoinCondition))
                    #print 'SPATIAL JOIN'
                    #print spatialJoinStr
                    # left join for start location

                    stLocJoinStr = (""" left join %s %s on """\
                                        """(%s) """ 
                                    %(stTable, 'stl', stLocJoinCondition))


                    enLocJoinStr = (""" left join %s %s on """\
                                        """(%s) """ 
                                    %(enTable, 'enl', enLocJoinCondition))

        
                    joinStrList.append(spatialJoinStr)
                    joinStrList.append(stLocJoinStr)
                    joinStrList.append(enLocJoinStr)
                    
                    cols_list += timeColsNewNames
                    

                    for i in timeColsNewNames:
                        final_list.append('sptime.%s' %(i))
                    # Only one time-space prism can be retrieved within a component
                    # there cannot be two TSP's in the same component
                    break
                                         

        # Generating the col list
        colStr = ''
        for i in final_list:
            colStr = colStr + '%s,' %(i)
        colStr = colStr[:-1]
        
        # Build the SQL string
        allJoinStr = ''
        for i in joinStrList:
            allJoinStr = allJoinStr + '%s' %i
            

        sql_string = 'select %s from %s %s' %(colStr, mainTable, allJoinStr)
        print 'SQL string for query - ', sql_string
        #print cols_list
        
        try:
            self.dbcon_obj.cursor.execute(sql_string)
            result = self.dbcon_obj.cursor.fetchall()
            data = self.createResultArray(result, cols_list)

            # Sort with respect to primary columns
            data.sort(primCols)

            return data
        except Exception, e:
            print e
            print 'Error retrieving the information. Query failed.'
        


    def createResultArray(self, result, cols_list, fillValue=0):
        t = time.time()


        # Create list of records
        #data = [i[:] for i in result]
        #print '\tLooping through results took - %.4f' %(time.time()-t), len(data)

        # Converting the none values returned into a zero value
        # using the ma library in numpy
        # - retrieve mask for None
        # - then assign the fillValue to those columns
        data = array(result)
        mask = ma.masked_equal(data, None).mask

        if mask.any():
            data[mask] = fillValue

        #Sorting the array by primary cols identifying the agent as 
        # postgres seems to return queries without any order
            
        
        # Convert it back to a regular array to enable all the other processing
        print '\t - Size of the data set that was retrieved - ', data.shape
        print '\t - Records were processed after query in %.4f' %(time.time()-t)

        return DataArray(data, cols_list)

    ########## methods for select query end ##########
    
    
    ########## methods for delete query  ##########    
    #delete rows based on a deletion criteria
    def delete_selected_rows(self, table_name, column_name, value):
        """
        This method is used to delete selected rows fom the table in the database.

        Input:
        Database configuration object, table name and selection criteria

        Output:
        Deletes the rows that satisfy the selection criteria
        """
        fin_flag = None
        #check if table exists and then if columns exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        if tab_flag:
            #check for columns
            get_cols = self.dbcon_obj.get_column_list(table_name)
            if column_name in get_cols:
                fin_flag = True
            else:
                fin_flag = False
        else:
            print 'Table %s does not exist.'%table_name
            
        if fin_flag:
            try:
                self.dbcon_obj.cursor.execute("delete FROM %s where %s = '%s'"%(table_name, column_name, value))
                self.dbcon_obj.connection.commit()
                print 'Delete successful'
            except Exception, e:
                print e
                print 'Error deleting the information. Query failed.'
        else:
             'Column %s does not belong to the table %s. Could not delete rows.'%(column_name, table_name)


    #delete all rows i.e. empty table
    def delete_all(self, table_name):
        """
        This method is used to delete all rows from the table.

        Input:
        Database configuration object, table name

        Output:
        Deletes all rows in the table
        """
        #check if table exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        if tab_flag:
            #print 'Table %s exists.'%table_name
            try:
                self.dbcon_obj.cursor.execute("delete FROM %s "%table_name)
                self.dbcon_obj.connection.commit()
                print '\t - Delete all records successful.'
            except Exception, e:
                print e
                print '\t - Error retrieving the information. Query failed.'
        else:
            print '\t - Table %s does not exist.'%table_name
            
    ########## methods for delete query end ##########


    ########## methods for insert query     ##########
    #insert values in the table
    def insert_into_table(self, arr, cols_list, table_name, keyCols, chunkSize=100000):
        """
        self, arr, cols_list, table_name, keyCols, chunkSize=None):
        This method is used to insert rows into the table.

        Input:
        Database configuration object, table name, data array

        Output:
        Inserts all the rows from data array in the table
        """
        
        table_name = table_name.lower()

        # Delete index before inserting
        index_cols = self.delete_index(table_name)


        #check if table exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        tab_flag = True

        if tab_flag:
            #print 'Table %s exists.'%table_name
            try:
                
                ti = time.time()
                #arr_str = [tuple(each) for each in arr]
                #arr_str = str(arr_str)[1:-1]
                #Generate the column list
                cols_listStr = ""
                for i in cols_list:
                    cols_listStr += "%s," %i
                cols_listStr = cols_listStr[0:-1]
                cols_listStr = "(%s)" %cols_listStr
                
                #Divide the data into chunks
                last = 0
                lastRow = len(arr)
                nChunks = int(lastRow/chunkSize)
                for i in range(nChunks):
                    last = (i+1)*chunkSize
                    arrSub = arr[i*chunkSize:last]
                    self.insert_nrows(table_name, cols_listStr, arrSub)
                
                #Insert last ODD chunk
                arrSub = arr[nChunks*chunkSize:]
                self.insert_nrows(table_name, cols_listStr, arrSub)
                    
                #result = self.dbcon_obj.cursor.execute(insert_stmt)
                self.dbcon_obj.connection.commit()
                print '\t\tTime after insert query %.4f' %(time.time()-ti)
            except Exception, e:
                print e
        else:
           print 'Table %s does not exist.'##%table_name 
        self.create_index(table_name, keyCols)

    def copy_into_table(self, arr, cols_list, table_name, keyCols, loc):
        """
        self, arr, cols_list, table_name, keyCols, chunkSize=None):
        This method is used to insert rows into the table.

        Input:
        Database configuration object, table name, data array

        Output:
        Inserts all the rows from data array in the table
        """
        
        table_name = table_name.lower()

        # Delete index before inserting
        index_cols = self.delete_index(table_name)


        self.file_write(arr, loc)
        
        #check if table exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        tab_flag = True

        cols_listStr = ""
        for i in cols_list:
            cols_listStr += "%s,"%i
        cols_listStr = "(%s)" %cols_listStr[:-1]

        if tab_flag:
            #print 'Table %s exists.'%table_name
            try:
                ti = time.time()
                insert_stmt = ("""copy %s %s from '%s/tempData.csv' """
                               """ delimiters ','""" %(table_name, cols_listStr, loc))
                                                                       
                print insert_stmt
                result = self.dbcon_obj.cursor.execute(insert_stmt)
                self.dbcon_obj.connection.commit()
                print 'Time after insert query - %.4f' %(time.time() - ti)
                #print '\t\tTime to insert - %.4f' %(time.time()-ti)
            except Exception, e:
                print e
        else:
           print 'Table %s does not exist.'##%table_name 
        self.create_index(table_name, keyCols)
        
        
    def insert_nrows(self, table_name, cols_listStr, arr):
        arr_str = [tuple(each) for each in arr]
        arr_str = str(arr_str)[1:-1]
        try:
            insert_stmt = "insert into %s %s values %s"%(table_name, cols_listStr, arr_str)
            result = self.dbcon_obj.cursor.execute(insert_stmt)
            self.dbcon_obj.connection.commit()
        except Exception, e:
            print '\t    Error while inserting data in the table'
            print e

    ########## methods for delete query end ##########



    ########## methods for creating and deleting index##########
    #create an index
    def create_index(self, table_name, col_list):
        """
        This method creates an index on the table
        
        Input:
        Database configuration object, table name and column list
        
        Output:
        Index created on the table with the specified columns
        """
        fin_flag = None
        #check if table exists and then if columns exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        if tab_flag:
            #check for columns
            get_cols = self.dbcon_obj.get_column_list(table_name)
            num_tab = len(list(set(get_cols) & set(col_list)))
            if num_tab <= len(get_cols):
                fin_flag = True
            else:
                fin_flag = False
        else:
            print 'Table %s does not exist.'%table_name

        if fin_flag:
            index_stmt = ''
            columns = ''
            count = 0
            index_name = table_name + '_index'

            for i in col_list:
                if count < (len(col_list)-1):
                    columns = columns + i + ', '
                    count = count + 1
                else:
                    columns = columns + i
            index_stmt = 'create index %s on %s (%s)'%(index_name, table_name, columns)
            try:
                self.dbcon_obj.cursor.execute(index_stmt)
                self.dbcon_obj.connection.commit()
                print '\t\tIndex %s created'%index_name
            except Exception, e:
                print 'Error while creating an index'
                print e
                self.dbcon_obj.connection.rollback()

    #delete an index
    def delete_index(self, table_name):
        """
        This method deletes an index on the table
        
        Input:
        Database configuration object and table name
        
        Output:
        Index on the table is deleted
        """
        #check if table exists and then if columns exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        if tab_flag:
            index_name = table_name + '_index'
            try:
                self.dbcon_obj.cursor.execute("drop index %s"%index_name)
                self.dbcon_obj.connection.commit()
                print '\t\tIndex %s deleted'%index_name
            except Exception, e:
                print 'Error while deleting an index'
                print e
                self.dbcon_obj.connection.rollback()
    ########## methods for creating and deleting index##########

    ########### file function #################
    def file_write(self, data_arr, loc):
        """
        This method write the resultset to a file.
        
        Input:
        Data array or resultset and the column list
        
        Output:
        File created with all data written in it.
        """
        #open the file
        ti = time.time()
        print 'opening a file'
        myfile = open('%s/tempData.csv' %loc, 'w')
        
        #enter the columns in the file
        #myfile.write(str(cols_list)[1:-1])
        #myfile.write('\n')
        
        #data_arr = na.zeros(7).reshape(1,7)
        #loop through the array and write to file
        for each in data_arr:
            each = list(each)
            myfile.write(str(each)[1:-1])
            myfile.write('\n')
        myfile.close()
        print '\t\tTime to write to file - %.4f' %(time.time()-ti)
    ########### file function ends ############
    
    ###########################################
    #new code for copy file
    #file to get datatype
    def column_data_type(self, res, temp_arr):
        """
        Input:
        resultset and data array object
        """
        temp_cols = temp_arr.varnames
        print temp_cols
        write_file_str = ""
        write_file_str = self.get_column_data_type(temp_cols)
        print write_file_str
        
        print 'write file start ----------->', time.time()
        try:
            file_fp = open('/home/namrata/Documents/DBclasses/dbapi/temp1.csv', 'w')
            print 'file opened'
            data_arr_len = len(temp_arr.data)
            myfile.write(str(temp_cols)[1:-1])
            myfile.write('\n')
        
            for each in temp_arr.data:
                each = list(each)
                each = str(each)[1:-1]
                parts = each.split(', ')
                count = len(parts)
                ctr = 0
                #write_str = "'%s,%s,%s,%s'%(int(float(parts[0])), long(float(parts[1])), float(parts[2]), int(float(parts[3])))"
                #print write_str
                #file_fp.write('%s,%s,%s,%s\n'%(int(float(parts[0])), long(float(parts[1])), float(parts[2]), int(float(parts[3]))))
                file_fp.write(eval(write_file_str))
                file_fp.write('\n')                    
        except Exception, e:
            print e
        file_fp.close()
        print 'write file end ----------->', time.time()
        
        print '\ninsert data'
        
        try:
            insert_stmt = "copy abc from '/home/namrata/Documents/DBclasses/dbapi/temp1.csv' with delimiter as ',' csv header"
            #print insert_stmt
            print 'time before insert query ------>', time.time()
            result = self.dbcon_obj.cursor.execute(insert_stmt)
            self.dbcon_obj.connection.commit()
            print 'time after insert query ------>', time.time()
        except Exception, e:
            print e
        print '\n'
        
    
    def get_column_data_type(self, temp_arr):
        """
        Input:
        resultset and data array object
        """
        data_type_arr = []
        data_type_stmt = "select column_name, data_type  from information_schema.columns where table_schema = 'public'"
        try:
            self.dbcon_obj.cursor.execute(data_type_stmt)
            result = self.dbcon_obj.cursor.fetchall()
            
            columns = [cl[0] for cl in result]
            data_type = [dt[1] for dt in result]
            print columns
            for each in temp_arr:
                for col, dat in zip(columns, data_type):
                    if each == col:
                        data_type_arr.append(dat)
                        break
        except Exception, e:
            print e
        print 'data_type_arr is ------>', data_type_arr
        final_data_types = self.define_mapping(data_type_arr)
        print 'final data types are ------->', final_data_types
        
        #create string for file 
        file_str = ""
        type_iden_str = " '"
        #create string for the type identifier
        for each in range(len(temp_arr)):
            type_iden_str = type_iden_str + "%s\t"
        type_iden_str = type_iden_str[1:-1]
        type_iden_str = type_iden_str + "'%"
        
        #create string for 
        data_type_str = "("
        count = 0
        for each in final_data_types:
            if count == (len(final_data_types)-1):
                data_type_str = data_type_str + each + "(float(parts["+ str(count) + "])))"
            else:
                data_type_str = data_type_str + each + "(float(parts["+ str(count) + "])), "
                count = count + 1
        
        final_str = type_iden_str + data_type_str
        return final_str
    
    
    def define_mapping(self, data_type_list):
        new_data_types = []
        
        for each in data_type_list:
            if each == 'integer':
                new_data_types.append('int')
            elif each == 'real':
                new_data_types.append('float')
            elif each == 'bigint':
                new_data_types.append('long')
            elif each == 'character varying':
                new_data_types.append('str')
            elif each == 'double precision':
                new_data_types.append('float')

        return new_data_types
    ###########################################################



#unit test to test the code
import unittest

#define a class for testing
class TestMainClass(unittest.TestCase):
    #only initialize objects here
    def setUp(self):
        self.protocol = 'postgres'		
        self.user_name = 'postgres'
        self.password = '1234'
        self.host_name = 'localhost'
        self.database_name = 'postgres'

    
    def testMainClass(self):
        abc = DataBaseConfiguration(self.protocol, self.user_name, self.password, self.host_name, self.database_name)
        newobject = QueryBrowser(abc)

        """ create a connection to the database """
        newobject.dbcon_obj.new_connection()
        
        table_name = 'temp_table1'
        column_name = 'role_id'
        value = '1'
        abc = None
        defg = None
        #abc = newobject.fetch_selected_rows(table_name, column_name, value)
        #print abc
        #newobject.fetch_selected_rows(table_name, column_name, value)
        
        #newobject.delete_selected_rows(table_name, column_name, value)

        #newobject.delete_all(table_name)
        
        col_list = ['grad', 'role_id']
        #newobject.create_index(table_name, col_list)
        
        #newobject.delete_index(table_name)

        #data_arr = [('aa','aa','1'),('bb','bb','1')]
        #newobject.insert_into_table(data_arr, table_name)
        
        DB_DICT = {'households': ['htaz', 'numchild', 'inclt35k', 'hhsize'], 
                 'persons': ['male', 'schstatus', 'one', 'houseid', 'personid'], 
                 'schedule_r': ['scheduleid', 'activitytype']}
        COLUMN_NAMES = {'households': ['houseid'], 
                      'schedule_r': ['personid', 'houseid']}
        TABLE_NAMES = ['persons', 'households', 'schedule_r', 'abcd']
        MAX_DICT = {'schedule_r': ['scheduleid']}

        #print DB_DICT, COLUMN_NAMES, TABLE_NAMES, MAX_DICT
        
        #newobject.select_join(DB_DICT, COLUMN_NAMES, TABLE_NAMES, MAX_DICT)
        print '\n-----------------> select all from table'
        res, temp, columns = newobject.select_all_from_table(table_name)
        print '\n-----------------> write data to file'
        newobject.file_write(temp, columns)
        print '\n-----------------> insert into table'
        #newobject.insert_into_table()
        """ close the connection to the database """
        newobject.dbcon_obj.close_connection()


if __name__ == '__main__':
    unittest.main()
