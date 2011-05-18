/* File: arrayex.c */
#include<stdio.h>
#include<stdlib.h>
#include<malloc.h>
#include<math.h>
#include<string.h>


//declare the files
static const char file_name_1[] = "temp_data_copy.csv";
static const char file_name_2[] = "skim1.dat";
char *node_file_name;
char *graph_file_name;

//dynamic array
float **org_graph;

//initialize edges and nodes
int nodes;
int edges;
int start, end;
float tt;

/* Sample functions */
/*********************************************/
void print_array(float a[], int n)
{
    int i;    
    for(i = 0; i < n; i++)
    {
        printf("[%d] = %g \n", i, a[i]);
    }
}


void create_array(float a[], int n)
{
    int j;
    for(j = 0; j < n; j++)
    {
        a[j] = j;
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
        //printf("node file name --> %s\n", node_file_name);
   }
   else
   {
        graph_file_name = (char *)malloc(length*sizeof(char));
        graph_file_name = s;
        //printf("graph_file name --> %s\n", graph_file_name);
   }
}


void print_string()
{
    printf("printing the file names\n");
    printf("node file name:  %s\n", node_file_name);
    printf("graph file name:  %s\n", graph_file_name);
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
    printf("C--> Opening the file\n");
    printf("C--> Node File: %s\n", node_file_name);
    FILE *file = fopen(node_file_name, "r");
    
    //process till end of file
    if( node_file_name != NULL )
    {
        //find the nodes and edges
        printf("C--> Reading from the file\n");
        fscanf(file, "%d, %d", &nodes, &edges);
        printf("C--> Nodes are: %d\n", nodes);
        printf("C--> Edges are: %d\n", edges);
        
        //close the file
        printf("C--> Closing the file\n");
        fclose(file);
        
        return nodes;
    }
    else
    {
        //error if file is null
        printf("C--> Error reading the file.\n");
        perror(node_file_name);
        return 0;
    }
}


/*
This function initializes the dynamic array/graph.
It allocates memory to the array/graph based on the number of nodes.
*/
void initialize_array(int nodes)
{
    int x;
    printf("C--> Nodes are %d\n", nodes);
    edges = nodes * nodes;
    printf("C--> Initializing the graph\n");
    //initialize the 2D array to the size of the number of nodes
    org_graph = (float *)malloc(nodes*sizeof(float));
    //org_graph = malloc(nodes * sizeof(float *));
        
    //create all the nodes
    for(x = 0; x < nodes; x++)
    {
        org_graph[x] = (float *)malloc(nodes*sizeof(float));
        //org_graph[x] = malloc(nodes * sizeof(float));
    }
    printf("C--> Graph created\n");
}


/*
This function reads the origin, destination and tt from a file.
It then sets the array/graph elements to tt read from the file.
*/
void set_array(int offset)
{
    int i;

    //open the file to read data
    printf("C--> Opening the file\n");
    printf("C--> Graph File: %s\n", graph_file_name);
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
        printf("C--> Closing the file\n");
        fclose(file);
    }
    else
    {
        //error if file is null
        printf("Error reading the file.\n");
        perror(graph_file_name);
    }
    printf("C--> Graph created with new values\n");
}


/*
This function is used to get the travel times from the graph.
Input: two array of same size that have the origins and destinations
Output: array with all the travel times.
*/
void get_tt(float org[], float dest[], float tt[], int arr_len, int offset )
{
    //local variables
    int i;
    int st, en;
    int count;
    float temp;
    
    printf("C--> Get the travel times\n");
    count = 0;

    //get the travel times using the origin and destination
    for ( i = 0; i < arr_len; i++ )
    {
        st = org[i];
        en = dest[i];
        //printf("C--> i is %d st is %d en is %d node1 is %d node2 is %d\n", i, st, en, (st-offset), (en-offset));
        temp = org_graph[st-offset][en-offset];
        //printf("C--> temp: %f\n", temp);
        tt[i] = temp;
        //printf("C--> org: %g dest: %g tt: %g\n", org[i], dest[i], tt[i]);
        /*if ( count%10 == 0 )
        {
            printf("%f ", temp);
        }
        count++;*/
    }
    printf("C--> Travel times retrieved\n");
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
    
    printf("C--> Array deleted\n");
}

/*********************************************/


/* Print functions */
/*********************************************/
/* Print the travel times array */
void print_tt_array(float org[], float dest[], float tt[], int len)
{
    int i;

    for(i = 0; i < len; i++)
    {
        printf("%g %g %g\n", org[i], dest[i], tt[i]);
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





