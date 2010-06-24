"""
Template to generate the database schema: v1
TODO: have to include the relationship between database.
"""

#import the necessary modules
from elixir import *

#define metadata and connect to the database
metadata.bind = "postgres://postgres:1234@localhost/template"
metadata.bind.echo = True

#start define the classes
#Vehicle class
class Vehicle(Entity):
    using_options(tablename='vehicle')
    Vehicle_ID = Field(Integer, primary_key = True)
    Person_ID = Field(Integer)
    Body_Type = Field(UnicodeText)
    Fuel_Type = Field(UnicodeText)
    Vintage = Field(UnicodeText)
    Mileage = Field(UnicodeText)
    Capacity = Field(UnicodeText)


#TSP class
class TSP(Entity):
    using_options(tablename='tsp')
    TSP_ID = Field(Integer, primary_key = True)
    Start_Location = Field(Integer)
    End_Location = Field(Integer)
    Start_Time = Field(Integer)
    End_Time = Field(Integer)
    DO_ID = Field(Integer)


#person schedule class
class Person_Schedule(Entity):
    using_options(tablename='person_schedule')
    PS_ID = Field(Integer, primary_key = True)
    Person_ID = Field(Integer)
    Schedule_ID = Field(Integer)

    
#link class
class Link(Entity):
    using_options(tablename='link')
    Link_ID = Field(Integer, primary_key = True)
    Oppurtinities_by_Activity_Type = Field(UnicodeText)
    X_Coordinates = Field(Integer)
    Y_Coordinates = Field(Integer)
    
    
#destination opportunities class
class Destination_Opportunities(Entity):
    using_options(tablename='destination_opportunities')
    DO_ID = Field(Integer, primary_key = True)
    TSP_ID = Field(Integer)
    Link_ID = Field(Integer)


#trip class
class Trip(Entity):
    using_options(tablename='trip')
    Trip_ID = Field(Integer, primary_key = True)
    Start_Time = Field(Integer)
    End_Time = Field(Integer)
    Vehicle_ID = Field(Integer)
    PT_ID = Field(Integer)
    Start_Location = Field(Integer)
    Mode = Field(UnicodeText)
    Fare = Field(Integer)
    Travel_Times = Field(Integer)
    
    
#link od class
class Link_OD(Entity):
    using_options(tablename='link_od')
    Link_OD_ID = Field(Integer, primary_key = True)
    TOD = Field(Integer)
    Mode = Field(UnicodeText)
    Travel_Time = Field(Integer)
    Cost = Field(Integer)
    Average_Speed = Field(Integer)
    Distance = Field(Integer)
    

#household class
class Household(Entity):
    using_options(tablename='household')
    Household_ID = Field(Integer, primary_key = True)
    adults = Field(Integer)
    age_of_head = Field(Integer)
    autos = Field(Integer)
    building_id = Field(Integer)
    homestaz = Field(Integer)
    household_size = Field(Integer)
    income = Field(Integer)
    nfulltime = Field(Integer)
    nparttime = Field(Integer)
    persons = Field(Integer)
    race_id = Field(Integer)
    test = Field(Integer)
    tract_id = Field(Integer)
    zone_id = Field(Integer)


#person trip class
class Person_Trip(Entity):
    using_options(tablename='person_trip')
    PT_ID = Field(Integer, primary_key = True)
    Trip_ID = Field(Integer)
    Person_ID = Field(Integer)


#schedule class
class Schedule(Entity):
    using_options(tablename='schedule')
    Schedule_ID = Field(Integer, primary_key = True)
    Type_of_Activity = Field(UnicodeText)
    Start_Time = Field(Integer)
    End_Time = Field(Integer)
    Destination = Field(Integer)
    Duration = Field(Integer)


#person class
class Person(Entity):
    using_options(tablename='person')
    Person_ID = Field(Integer, primary_key = True)
    Age = Field(Integer)
    Gender = Field(UnicodeText)
    School_Status = Field(UnicodeText)
    Worker_Status = Field(UnicodeText)
    Driver_Status = Field(UnicodeText)
    Number_of_jobs = Field(Integer)
    Work_Location = Field(Integer)
    School_Location = Field(Integer)
    Pre_School_Location = Field(Integer)
    Earliest_Start_Time_of_Morning_Prism = Field(Integer)
    Latest_End_Time_of_Evening_Prism = Field(Integer)
    PS_ID = Field(Integer)
    Household_ID = Field(Integer)
    Vehicle_ID = Field(Integer)


#create all the tables and commit the changes to the database
setup_all()
create_all()

session.commit()

#end of schema generator template
