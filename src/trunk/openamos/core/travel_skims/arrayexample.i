/* File: arrayex.i */

%module arrayexample

%include "carrays.i"
%array_functions(float, floatArray);

void print_array(float a[], int n);
void create_array(float a[], int n);

int get_nodes();
void initialize_array(int nodes);
void set_array(int offset);
void get_tt(float org[], float dest[], float tt[], int arr_len, int offset );
void delete_array();

void print_tt_array(float org[], float dest[], int len);
void print_org_array(int offset);

