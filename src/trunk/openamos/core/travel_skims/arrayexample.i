/* File: arrayex.i */

%module arrayexample

%include "carrays.i"
%array_functions(float, floatArray);
%include "cstring.i"
%cstring_bounded_mutable(char *path, 1024);
%newobject set_file;

void set_file(char *s, int length, int flag);
void print_string();

void print_array(float a[], int n);
void create_array(float a[], int n);

int get_nodes();
void initialize_array(int nodes);
void set_array(int offset);
void get_tt(float org[], float dest[], float tt[], int arr_len, int offset );
void delete_array();

void print_tt_array(float org[], float dest[], float tt[], int len);
void print_org_array(int offset);

