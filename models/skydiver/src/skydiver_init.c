/******************************* TRICK HEADER ****************************
PURPOSE: (Set the initial data values)
*************************************************************************/

/* Model Include files */
#include <math.h>
#include "../include/skydiver.h"

/* default data job */
int skydiver_default_data(SKYDIVER* S) {

    S->g = 9.81;
    S->Rho = 1.225;
    S->S = 1.0;
    S->Cd = 0.43;
    S->m = 85.0;
    return 0 ;
}

/* initialization job */
int skydiver_init(SKYDIVER* S) {
   
    S->vel0 = 0.0;
    S->pos0 = 3000.0 ;

    S->vel = S->vel0 ; 
    S->pos = S->pos0 ;
    S->Fd = 0.0;
    return 0 ; 
}