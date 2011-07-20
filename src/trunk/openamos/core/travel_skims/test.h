#include<stdio.h>
#include<stdlib.h>
#include<conio.h>
#include<time.h>
#include<malloc.h>
#include<string.h>


char *input_file_name;
char *output_file_name;
char *temp_file_name_1;
char *temp_file_name_2;
char *temp_file_name_3;


void create_new_file(int interval, int number_intervals, char *file1, char *file2, char *file3)
{
	int i, j;
	int travel_time, test_interval;
	int fin_tt;
	int no_of_intervals = 0;
	int file_flag = 0;
	int loop_counter = 0;
	float temp1, temp2, temp3, temp4, temp5;
	int temp_tt;
	char *mystring;
	char *tt_temp;
	int length = 1;
	FILE *ip_file, *tp_file_1, *tp_file_2;

	//set the file names
	length = strlen(file1) + 20;
    
	input_file_name = (char *)malloc(length*sizeof(char));
    temp_file_name_1 = (char *)malloc(length*sizeof(char));
	temp_file_name_2 = (char *)malloc(length*sizeof(char));
    
	input_file_name = file1;
	temp_file_name_1 = file2;
	temp_file_name_2 = file3;

	//open the files 
	ip_file = fopen(input_file_name, "r");
	
	test_interval = interval;
	no_of_intervals = number_intervals;

	//initialize mystring and temp string
	tt_temp = (char *)malloc(10*sizeof(char));
	mystring = (char *)malloc(10*sizeof(char));
	
	if(ip_file != NULL)
	{
		//now open the files for writing
		for(i = 0; i < no_of_intervals; i++)
		{
			//keep reading the file
			if(i == 0)
			{
				//first interval. read from input file only
				file_flag = 0;
				tp_file_2 = fopen(temp_file_name_2, "w");
				if(tp_file_2 != NULL)
				{
					for(j = 0; j < test_interval; j++)
					{
						fscanf(ip_file, "%f;%f;%d;%f;%f;%f", &temp1, &temp2, &travel_time, &temp3, &temp4, &temp5);
						tt_temp = itoa(travel_time, tt_temp, 10);
						fputs(tt_temp, tp_file_2);
						fputs("\n", tp_file_2);
					}
				}
				fclose(tp_file_2);
			}
			else if(i == 1)
			{
				//even intervals. open the respective file
				file_flag = 1;
				tp_file_1 = fopen(temp_file_name_1, "w");
				tp_file_2 = fopen(temp_file_name_2, "r");
				if(tp_file_2 != NULL && tp_file_1 !=NULL)
				{
					for(j = 0; j < test_interval * i; j++)
					{
						fscanf(ip_file, "%f;%f;%d;%f;%f;%f", &temp1, &temp2, &travel_time, &temp3, &temp4, &temp5);
						fgets (mystring , 10 , tp_file_2);
						tt_temp = itoa(travel_time, tt_temp, 10);
						fputs(mystring, tp_file_1);
						fputs(tt_temp, tp_file_1);
						fputs("\n", tp_file_1);
					}
				}
				fclose(tp_file_1);
				fclose(tp_file_2);
			}
			else if(i % 2 == 0)
			{
				//even intervals. open the respective file
				file_flag = 0;
				tp_file_1 = fopen(temp_file_name_1, "r");
				tp_file_2 = fopen(temp_file_name_2, "w");
				if(tp_file_2 != NULL && tp_file_1 !=NULL)
				{
					for(j = 1; j <= test_interval * i; j++)
					{
						fgets (mystring , 10 , tp_file_1);
						fputs(mystring, tp_file_2);
						//fputs("\n", tp_file_2);
						if(j % i == 0)
						{
							fscanf(ip_file, "%f;%f;%d;%f;%f;%f", &temp1, &temp2, &travel_time, &temp3, &temp4, &temp5);
							tt_temp = itoa(travel_time, tt_temp, 10);
							fputs(tt_temp, tp_file_2);
							fputs("\n", tp_file_2);
						}	
					}
				}
				fclose(tp_file_1);
				fclose(tp_file_2);
			}
			else if(i % 2 != 0 && i != 1)
			{
				//odd intervals
				file_flag = 1;
				tp_file_1 = fopen(temp_file_name_1, "w");
				tp_file_2 = fopen(temp_file_name_2, "r");
				if(tp_file_2 != NULL && tp_file_1 !=NULL)
				{
					for(j = 1; j <= test_interval * i; j++)
					{
						fgets (mystring , 10 , tp_file_2);
						fputs(mystring, tp_file_1);
						//fputs("\n", tp_file_1);
						if(j % i == 0)
						{
							fscanf(ip_file, "%f;%f;%d;%f;%f;%f", &temp1, &temp2, &travel_time, &temp3, &temp4, &temp5);
							tt_temp = itoa(travel_time, tt_temp, 10);
							fputs(tt_temp, tp_file_1);
							fputs("\n", tp_file_1);
						}	
					}
				}
				fclose(tp_file_1);
				fclose(tp_file_2);
			}
		}
	}
	fclose(ip_file);
		
	//at the end of for loop determine which file was read last 
	//and write all results to the other file
	if(file_flag)
	{
		printf("Last write was on file %s\n", temp_file_name_1);
		//open the file that was last written to
		tp_file_1 = fopen(temp_file_name_1, "r");
		tp_file_2 = fopen(temp_file_name_2, "w");
		printf("reading from file %s and writing to file %s \n", temp_file_name_1, temp_file_name_2);
		//write to file 2
		if(tp_file_2 != NULL && tp_file_1 !=NULL)
		{
			for(i = 0; i < test_interval; i++)
			{
				for(j = 0; j < no_of_intervals; j++)
				{
					fscanf(tp_file_1, "%d", &fin_tt);
					tt_temp = itoa(fin_tt, tt_temp, 10);
					fputs(tt_temp, tp_file_2);
					fputs("\t", tp_file_2);
				}
				fputs("\n", tp_file_2);
			}
		}
		fclose(tp_file_1);
		fclose(tp_file_2);
	}
	else
	{
		printf("Last write was on file %s\n", temp_file_name_2);
		//open the file that was last written to
		tp_file_2 = fopen(temp_file_name_2, "r");
		tp_file_1 = fopen(temp_file_name_1, "w");
		printf("reading from file %s and writing to file %s \n", temp_file_name_2, temp_file_name_1);
		//write to file 2
		if(tp_file_2 != NULL && tp_file_1 !=NULL)
		{
			for(i = 0; i < test_interval; i++)
			{
				for(j = 0; j < no_of_intervals; j++)
				{
					fscanf(tp_file_2, "%d", &fin_tt);
					tt_temp = itoa(fin_tt, tt_temp, 10);
					fputs(tt_temp, tp_file_1);
					fputs("\t", tp_file_1);
				}
				fputs("\n", tp_file_1);
			}
		}
		fclose(tp_file_1);
		fclose(tp_file_2);
	}

	//free the strings 
	//free(tt_temp);
	//free(mystring);

}


