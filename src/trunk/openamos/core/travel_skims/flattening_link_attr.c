#include "flattening_link_attr.h"

int main()
{

    int interval, number_intervals;
    char *linkAttList_fileName, *tempFile1, *tempFile2, *linkFlatten_fileName;

    linkAttList_fileName = "output_gui_LinkStats_0.dat";
    tempFile1 = "tmpLinkAttrFile1.dat";
    tempFile2 = "tmpLinkAttrFile2.dat";
    linkFlatten_fileName = "input_HTDSP_tdcost_MAG_24hr_new.dat";
    interval = 20522;
    number_intervals = 4;

    flatten_link_attributes(interval, number_intervals, linkAttList_fileName, tempFile1, tempFile2, linkFlatten_fileName);
}

