/* File: arrayex.i */

%module extending

%include "carrays.i"
%array_functions(float, floatArray);
%array_functions(int, intArray);
%include "cstring.i"
%cstring_bounded_mutable(char *path, 1024);
%newobject set_file;

void set_file(char *s, int length, int flag);
void print_string();

void print_array(int a[], int n);
void create_array(int a[], int n);

void write_locations(int index);

int get_nodes();
void initialize_array(int nodes);
void set_array(int offset);
void get_tt(int org[], int dest[], float tt[], int arr_len, int offset );
void delete_array();

void print_tt_array(int org[], int dest[], float tt[], int len);
void print_org_array(int offset);

void initialize_location_array(int arr_len);
void set_location_array_to_zero(int arr_len);
void set_temp_location_array();
void print_location_array(int arr_len);
void generate_random_locations(int loc_length, int no_of_loc, int index);
void get_location_choices(int origin[], int destination[], float travel_time[], int locations[], int arr_len, int offset, int no_of_locations);
void delete_location_array(int arr_len);

