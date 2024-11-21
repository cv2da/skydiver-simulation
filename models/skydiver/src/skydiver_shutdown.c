/************************************************************************
PURPOSE: (Print the final skydiver state.)
*************************************************************************/
#include <stdio.h>
#include "../include/skydiver.h"
#include "trick/exec_proto.h"

int skydiver_shutdown(SKYDIVER* S) {
    double t = exec_get_sim_time();
    printf( "========================================\n");
    printf( "      Skydiver State at Shutdown     \n");
    printf( "t = %g\n", t);
    printf( "pos = [%.9f]\n", S->pos);
    printf( "vel = [%.9f]\n", S->vel);
    printf( "========================================\n");
    return 0 ;
}