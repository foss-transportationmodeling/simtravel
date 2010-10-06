#main class. this class will be used to define the database connection.
#it will create/drop database, schema and tables
 

#include all the import 
import sys
import os
import exceptions
import time
import sqlalchemy
import psycopg2 as dbapi2
from database_connection import DataBaseConnection
from psycopg2 import extensions
from sqlalchemy.types import Integer, SmallInteger, \
			     Numeric, Float, \
			     VARCHAR, String, CLOB, Text,\
			     Boolean, DateTime


class MainClass(object):
    #initialize the class 
    def __init__(self, protocol = None, user_name = None,
                    password = None, host_name = None, 
                    database_name = None, engine = None, 
                    connection = None, result = None):

        self.protocol = protocol
        self.user_name = user_name
        self.password = password
        self.host_name = host_name
        self.database_name = database_name
        self.connection = None
        self.result = None
        self.cursor = None
        dbcon_obj = DataBaseConnection(self.protocol, self.user_name, self.password, self.host_name, self.database_name)
        self.dbcon_obj = dbcon_obj
        print self.dbcon_obj
    
    
    ########## methods for select query  ##########
    #select all rows from the table
    def select_all_from_table(self, table_name):
        """
        This method is used to fetch all rows from the table specified.

        Input:
        Class name corresponding to the table

        Output:
        Returns all the rows in the table
        """
        #check if table exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        if tab_flag:
            print 'Table %s exists.'%table_name
            try:    
                self.dbcon_obj.cursor.execute("SELECT * FROM %s"%table_name)
                tables = self.dbcon_obj.cursor.fetchall()
                tbs = [tb for tb in tables]
                return self.dbcon_obj.cursor, tbs
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


        print 'Database Dictionary of Table and Columns - ', db_dict
        print 'Column Names', column_names
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
        for i in db_dict.keys():
            clist = self.dbcon_obj.get_column_list(i.lower())
            list1 = db_dict[i]
            #print 'table--', i
            #print 'clist', clist
            #print 'list1', list1
            chk_list = len(list(set(list1) & set(clist)))
            if chk_list == len(list1):
                for j in db_dict[i]:
                    #print '\tColumn - ', j
                    new_str = i.lower() + '.' + j.lower()
                    final_list.append(new_str)                    
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
        print '\n\nSQL string for query - \n', sql_string
        
        try:
            result = self.dbcon_obj.cursor.execute(sql_string)
                        
            resultArray = self.createResultArray(result)

            # Returns the query as a DataArray object
            data = DataArray(resultArray, cols_list)

            data.sort(primCols)
        
            return data
        except Exception, e:
            print e
            print 'Error retrieving the information. Query failed.'
        

    def createResultArray(self, result, fillValue=0):
        t = time.time()

        # Create list of records
        data = [i[:] for i in result]
        print '\tLooping through results took - %.4f' %(time.time()-t), len(data)

        # Converting the none values returned into a zero value
        # using the ma library in numpy
        # - retrieve mask for None
        # - then assign the fillValue to those columns
        data = array(data)
        mask = ma.masked_equal(data, None).mask

        if mask.any():
            data[mask] = fillValue

        #Sorting the array by primary cols identifying the agent as 
        # postgres seems to return queries without any order
            
        
        # Convert it back to a regular array to enable all the other processing
        print '\tSize of the data set that was retrieved - ', data.shape
        print '\tRecords were processed after query in %.4f' %(time.time()-t)

        return data

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
            print 'Column %s does not belong to the table %s. Could not delete rows.'%(column_name, table_name)


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
            print 'Table %s exists.'%table_name
            try:
                self.dbcon_obj.cursor.execute("delete FROM %s "%table_name)
                self.dbcon_obj.connection.commit()
                print 'Delete all records successful.'
            except Exception, e:
                print e
                print 'Error retrieving the information. Query failed.'
        else:
            print 'Table %s does not exist.'%table_name
            
    ########## methods for delete query end ##########


    ########## methods for insert query     ##########
    #insert values in the table
    def insert_into_table(self, data_arr, table_name):
        """
        This method is used to insert rows into the table.

        Input:
        Database configuration object, table name, data array

        Output:
        Inserts all the rows from data array in the table
        """
        #check if table exists
        tab_flag = self.dbcon_obj.check_if_table_exists(table_name)
        if tab_flag:
            print 'Table %s exists.'%table_name
            try:
                print 'time before insert query ', time.time()
                arr_str = [tuple(each) for each in data_arr]
                arr_str = str(arr_str)[1:-1]
                insert_stmt = "insert into %s values %s"%(table_name, arr_str)
                #insert_stmt = "copy school from '/home/namrata/Documents/DBclasses/myfile.csv' with delimiter as ',' csv header"
                result = self.dbcon_obj.cursor.execute(insert_stmt)
                self.dbcon_obj.connection.commit()
                print 'time after insert query ', time.time()
            except Exception, e:
                print e
        else:
           print 'Table %s does not exist.'%table_name 
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
            print index_stmt
            try:
                self.dbcon_obj.cursor.execute(index_stmt)
                self.dbcon_obj.connection.commit()
                print 'Index %s created'%index_name
            except Exception, e:
                print 'Error while creating an index'
                print e


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
                print 'Index %s deleted'%index_name
            except Exception, e:
                print 'Error while creating an index'
                print e
        
    ########## methods for creating and deleting index##########



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
        newobject = MainClass(self.protocol, self.user_name, self.password, self.host_name, self.database_name)

        """ create a connection to the database """
        newobject.dbcon_obj.new_connection()
        
        table_name = 'asu'
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

        """ close the connection to the database """
        newobject.dbcon_obj.close_connection()


if __name__ == '__main__':
    unittest.main()
