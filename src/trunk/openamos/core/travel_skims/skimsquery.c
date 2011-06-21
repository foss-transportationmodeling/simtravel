/* File: arrayex.c */
#include<stdio.h>
#include<stdlib.h>
#include<malloc.h>
#include<math.h>
#include<string.h>
#include "skimsquery.h"

#define MAX 100

//declare the files
char *node_file_name;
char *graph_file_name;
char *locations_file = "locations.txt";

//dynamic array
float **org_graph;
int **location_choices;

//initialize edges and nodes
int nodes;
int edges;
int start, end;
float tt;
int rows;
int columns;
int no_of_locations;

//array
int temp_locations[MAX];


/* Sample functions */
/*********************************************/
void print_array(int a[], int n)
{
    int i;    
    for(i = 0; i < n; i++)
    {
        printf("[%d] = %d \n", i, a[i]);
    }
    printf("\n");
}


void create_array(int a[], int n)
{
    int i, count;
    count = 0;
    for(i = 0; i < n; i++)
    {
        a[i] = count;
        count++;
    }
}
/*********************************************/


/* String Functions */
/*********************************************/
void set_file(char *s, int length, int flag){
   //if flag is 1 then nodes of the graph were not provided
   //set the file name to the node_file_name(function needs to be called twice)
   //if flag is 0 nodes are already known 
   //set the file name to the graph_file_name
   if(flag == 1)
   {
        node_file_name = (char *)malloc(length*sizeof(char));
        node_file_name = s;
        //printf("C-->node file name --> %s\n", node_file_name);
   }
   else
   {
        graph_file_name = (char *)malloc(length*sizeof(char));
        graph_file_name = s;
        //printf("C-->graph_file name --> %s\n", graph_file_name);
   }
}


void print_string()
{
    //printf("C--> printing the file names\n");
    //printf("C--> node file name:  %s\n", node_file_name);
    //printf("C--> graph file name:  %s\n", graph_file_name);
}
/*********************************************/


/*File functions */
/*********************************************/
/*
This function writes all the locations to the file
*/
void write_locations(int index)
{
    //write all locations to a temp file 
    FILE *fp = NULL;
    int i, j, k;
    //printf("C--> Write to file\n");
    
    //if index is 0 then its the first entry. create a new file
    if(index > 0)
    {
        fp = fopen(locations_file, "a");
    }
    //else open the file in append mode
    else
    {
        fp = fopen(locations_file, "w");
    }
    //file open error return error message
    if(fp == NULL)
    {
        printf("C--> Error opening file ", locations_file);
        printf("\n");
    }
    //else write all locations to file
    else
    {
        fprintf(fp, "For location id: %d\n", index);
        for(i = 0; i < MAX; i++)
        {
            fprintf(fp, "%d\n", temp_locations[i]);
        }
        fclose(fp);
    }
}
/*********************************************/


/* Main functions */
/*********************************************/
/*
This function reads the file and finds the total number 
of nodes and edges and saves them in the respective variables.
*/
int get_nodes()
{
    //open the file
    //printf("C--> Opening the file\n");
    //printf("C--> Node File: %s\n", node_file_name);
    FILE *file = fopen(node_file_name, "r");
    
    //process till end of file
    if( node_file_name != NULL )
    {
        //find the nodes and edges
        //printf("C--> Reading from the file\n");
        fscanf(file, "%d, %d", &nodes, &edges);
        //printf("C--> Nodes are: %d\n", nodes);
        //printf("C--> Edges are: %d\n", edges);
        
        //close the file
        //printf("C--> Closing the file\n");
        fclose(file);
        
        //return the nodes
        return nodes;
    }
    else
    {
        //error if file is null
        //printf("C--> Error reading the file.\n");
        perror(node_file_name);
        return 0;
    }
}


/*
This function initializes the dynamic array/graph.
It allocates memory to the array/graph based on the number of nodes.
*/
void initialize_array(int nodes_temp)
{
    int x;
    nodes = nodes_temp;
    //printf("C--> Nodes are %d\n", nodes);
    edges = nodes * nodes;
    //printf("C--> Initializing the graph\n");
    
    //initialize the 2D array to the size of the number of nodes
    org_graph = (float **)malloc(nodes*sizeof(float *));
    //org_graph = malloc(nodes * sizeof(float *));
        
    //create all the nodes
    for(x = 0; x < nodes; x++)
    {
        org_graph[x] = (float *)malloc(nodes*sizeof(float));
        //org_graph[x] = malloc(nodes * sizeof(float));
    }
    //printf("C--> Graph created\n");
}


/*
This function reads the origin, destination and tt from a file.
It then sets the array/graph elements to tt read from the file.
*/
void set_array(int offset)
{
    int i;

    //open the file to read data
    //printf("C--> Opening the file\n");
    //printf("C--> Graph File: %s\n", graph_file_name);
    FILE *file = fopen(graph_file_name, "r");

    //process till end of file
    if( graph_file_name != NULL )
    {
        //read the file and initialize the edges 
        for(i = 0; i < edges; i++)
        {
            //read the origin, destination and tt and save it
            fscanf(file, "%d, %d, %f", &start, &end, &tt);
            
            //set the value of tt to the graph
            org_graph[start-offset][end-offset] = tt;
            
            //test
            //printf("%d %d %f ", start, end, org_graph[start-offset][end-offset]);
        }
        
        //close the file
        //printf("C--> Closing the file\n");
        fclose(file);
    }
    else
    {
        //error if file is null
        //printf("C--> Error reading the file.\n");
        perror(graph_file_name);
    }
    //printf("C--> Graph created with new values\n");
}


/*
This function is used to get the travel times from the graph.
Input: two array of same size that have the origins and destinations
Output: array with all the travel times.
*/
void get_tt(int org[], int dest[], float tt[], int arr_len, int offset )
{
    //local variables
    int i;
    int st, en;
    int count;
    float temp;
    
    //printf("C--> Get the travel times\n");
    count = 0;

    //get the travel times using the origin and destination
    for ( i = 0; i < arr_len; i++ )
    {
        st = org[i];
        en = dest[i];
        
        //if origin or destination are zero the location is invalid. set travel time to 0
        if (st == 0 || en == 0) 
        {
            tt[i] = 0;
        }
        else
        {
            temp = org_graph[st-offset][en-offset];
            tt[i] = temp;
        }
    }
    //printf("C--> Travel times retrieved\n");
}


/*
This function is used to delete the original graph 
and travel times array and free memory.
*/

void delete_array()
{
    int i;
    
    //delete all the rows
    for ( i = 0; i < nodes; i++ )
    {
        free(org_graph[i]);
    }
    
    //delete the pointer to the array
    free(org_graph);  
        
    //set the pointer to NULL to avoid any memory access
    org_graph = NULL;
    
    //printf("C--> Array deleted\n");
}

/*********************************************/


/* Print functions */
/*********************************************/
/* Print the travel times array */
void print_tt_array(int org[], int dest[], float tt[], int len)
{
    int i;

    for(i = 0; i < len; i++)
    {
        printf("%d %d %g\n", org[i], dest[i], tt[i]);
    }
}


/* Print the original graph */
void print_org_array(int offset)
{
    int i, j;    
    for(i = 0; i < 10; i++)
    {
        for(j = 0; j < 10; j++)
        {
            printf("C--> org_graph[%d][%d] = %g\n", (i+offset), (j+offset), org_graph[i][j]);
        }
    }
}
/*********************************************/


/* Location choices functions */
/*********************************************/
/*
This function initializes the location choices dynamic array
It allocates memory to the array based on the number of nodes.
*/
void initialize_location_array(int arr_len)
{
    int x;
    rows = arr_len;
    //printf("C--> Initializing locations graph\n");
    
    //initialize the 2D array to the size of the number of nodes
    location_choices = (int **)malloc(rows*sizeof(int *));

    //create all the nodes
    for(x = 0; x < rows; x++)
    {
        location_choices[x] = (int *)malloc(nodes*sizeof(int));
    }
    //printf("C--> Locations graph created\n");
}


/*
This function is used to the set values of all the nodes in 
the location choices array to 0.
*/
void set_location_array_to_zero(int arr_len)
{
    int i, j;
    //printf("C--> Setting locations graph to 0\n");
    
    //set the rows to 0
    for(i = 0; i < arr_len; i++)
    {
        //set the columns in each row to 0
        for(j = 0; j < nodes; j++)
        {
            location_choices[i][j] = 0;
        }
    }    
}


/*
This function is used to the set values of all the nodes in 
the temp location choices array to 0.
*/
void set_temp_location_array()
{
    int x;
    //printf("C--> Setting temp locations array to 0\n");
    
    //set all elements in temp locations array to 0
    for(x = 0; x < MAX; x++)
    {
        temp_locations[x] = 0;
    }

}


/*
This function prints the locations array.
*/
void print_location_array(int arr_len)
{
    int i, j;
    
    //for(i = 700; i < 1000; i++)
    for(i = 0; i < arr_len; i++)
    {
        //for(j = 1000; j < 1500; j++)
        for(j = 0; j < nodes; j++)
        {
            if(location_choices[i][j] == 1)
            {
                printf("%d ", location_choices[i][j]);
            }
        }
        printf("\n");
    }
}


/*
This function is used to generate random locations from 
and save them in the temp locations array
*/
void generate_random_locations(int loc_length, int no_of_loc, int index)
{
    int i, j, limit, random_num, count;
    i = 0;
    count = 0;

    //number of locations obtained are more than number of locations required
    if(loc_length > no_of_loc)
    {
        //run a loop till no of locations required         //for(i = 0; i < no_of_loc; i++)
        while(temp_locations[no_of_loc-1] == 0)
        {
            //generate a random number based on no of locations obtained
            random_num = rand();
            limit = random_num % nodes;
            
            //need to check for repeat random numbers
            if (location_choices[index][limit] == 1)
            {   
                location_choices[index][limit] = 0;
                temp_locations[count] = limit + 1;
                count++;
            }
        }
    }
    //number of locations obtained and required are the same
    else if(loc_length == no_of_loc)
    {
        for(i = 0; i < nodes; i++)
        {
            if(location_choices[index][i] == 1)
            {
                temp_locations[count] = i + 1;
                count++;
            }
            if(count == no_of_loc)
            {
                break;
            }
        }
    }
    //number of locations obtained are less than number locations required
    else
    {
        for(i = 0; i < nodes; i++)
        {
            if(location_choices[index][i] == 1)
            {
                temp_locations[count] = i + 1;
                count++;
            }
            if(count == loc_length)
            {
                break;
            }
        }        
    }
}


/*
This function is used to get the location choices for set of 
origin destination pairs
*/
void get_location_choices(int origin[], int destination[], float travel_time[], int locations[], int arr_len, int offset, int no_of_locations, int land_use_array[], int land_use_length)
{
    int i, j, k;
    int org, dest;
    float tt, temp_tt;
    int count, counter;
    int final_count, loop_counter;
    int length;
    int land_use_var;
    counter = 0;
    final_count = 0;
    loop_counter = 0;
    //printf("C--> inside location choices\n");
    
    //check if land use data is present
    if(land_use_length == nodes)
    {
        //land use data not present. loop over all the nodes
        //i --> rows in origin/dest j --> all nodes k --> final location choices
        //run a loop on the number of origin-destination pairs for every pair look for nodes that are accessible
        //printf("C--> No land use data\n");
        for(i = 0; i < arr_len; i++)
        {
            //set the origin, destination and travel time to local variable
            count = 0;
            org = origin[i];
            dest = destination[i];
            tt = travel_time[i];
            if( org == 0 || dest == 0)
            {
                //invalid origin or destination. set all the locations to zero. copy the locations into location choices
	            //printf("C--> Origin or destination are zeros - %d\n", i);
                for(k = 0; k < no_of_locations; k++)
                {
                    if(i == 0)
                    {
                        locations[k] = 0;
                    }
                    else
                    {
                        counter = i * no_of_locations + k;
                        locations[counter] = 0;
                    }
                }
            }
            else
            {
                //run a loop over all the nodes to get the locations accessible
                for(j = 0; j < nodes; j++)
                {
                    temp_tt = org_graph[org-offset][j] + org_graph[j][dest-offset];

                    //check if the travel time is less than travel time of OD pair
                    if(temp_tt <= tt)
                    {
                        //save the node to temp locations
                        location_choices[i][j] = 1;
                        
                        //printf("C--> org: %d dest: %d tt:%f count of nodes: %d j: %d temp_tt: %f\n", org, dest, tt, nodes, j, temp_tt);
    
                        //count will help determine the length of temp_locations
                        count++;
                    }
                }
    
                //generate randome locations
                generate_random_locations(count, no_of_locations, i);
        
                //copy the locations into location choices
                for(k = 0; k < no_of_locations; k++)
                {
                    if(i == 0)
                    {
                        locations[k] = temp_locations[k];
                    }
                    else
                    {
                        counter = i * no_of_locations + k;
                        locations[counter] = temp_locations[k];
                    }
                }
        
                //write all the locations to the file
                write_locations(i);
                
                //after copying the locations, reset temp locations
                set_temp_location_array();
            }
        }
    }
    else
    {
        //land use data is present. loop over all the elements in the land use array
        //i --> rows in origin/dest j --> all nodes k --> final location choices
        //run a loop on the number of origin-destination pairs for every pair look for nodes that are accessible
        //printf("C--> Land use data present.\n");
        for(i = 0; i < arr_len; i++)
        {
            //set the origin, destination and travel time to local variable
            count = 0;
            org = origin[i];
            dest = destination[i];
            tt = travel_time[i];
            if( org == 0 || dest == 0)
            {
                //invalid origin or destination. set all the locations to zero. copy the locations into location choices
	            //printf("C--> Origin or destination are zeros - %d\n", i);
                for(k = 0; k < no_of_locations; k++)
                {
                    if(i == 0)
                    {
                        locations[k] = 0;
                    }
                    else
                    {
                        counter = i * no_of_locations + k;
                        locations[counter] = 0;
                    }
                }
            }
            else
            {
                //run a loop over all the nodes to get the locations accessible
                for(j = 0; j < land_use_length; j++)
                {
                    land_use_var = land_use_array[j];
                    temp_tt = org_graph[org-offset][land_use_var-1] + org_graph[land_use_var-1][dest-offset];

                    //check if the travel time is less than travel time of OD pair
                    if(temp_tt <= tt)
                    {
                        //save the node to temp locations
                        location_choices[i][land_use_var-1] = 1;
                        
                        //printf("C--> org: %d dest: %d tt:%f count of nodes: %d j: %d temp_tt: %f\n", org, dest, tt, nodes, j, temp_tt);
    
                        //count will help determine the length of temp_locations
                        count++;
                    }
                }
    
                //generate randome locations
                generate_random_locations(count, no_of_locations, i);
        
                //copy the locations into location choices
                for(k = 0; k < no_of_locations; k++)
                {
                    if(i == 0)
                    {
                        locations[k] = temp_locations[k];
                    }
                    else
                    {
                        counter = i * no_of_locations + k;
                        locations[counter] = temp_locations[k];
                    }
                }
        
                //write all the locations to the file
                //write_locations(i);
                
                //after copying the locations, reset temp locations
                set_temp_location_array();
            }
        }
    }
}


/*
This function is used to delete the location choices array 
and free memory.
*/
void delete_location_array(int arr_len)
{
    int i;
    //printf("C--> Starting to delete location array\n");    
    //printf("Nodes-%d\n", nodes);
    //delete all the rows
    for ( i = 0; i < arr_len; i++ )
    {
	//printf("Counter-%d\n", i);
        free(location_choices[i]);
    }
    
    //delete the pointer to the array
    free(location_choices);
    
    //set the pointer to NULL to avoid any memory access
    location_choices = NULL;
    //printf("C--> Location array deleted\n");
}
/*********************************************/




