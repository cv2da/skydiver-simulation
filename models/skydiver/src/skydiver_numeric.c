/*********************************************************************
  PURPOSE: ( Trick numeric )
*********************************************************************/
#include <stddef.h>
#include <stdio.h>
#include "trick/integrator_c_intf.h"
#include "../include/skydiver_numeric.h"

int skydiver_update(SKYDIVER* S) {
    S->Fd = 0.5 * S->Cd * S->Rho * S->S * S->vel * S->vel; // drag force
    S->acc = (S->Fd / S->m) - S->g; // Newton's 2nd law
    return(0);
}

int skydiver_integ(SKYDIVER* S) {
    int ipass;
    double now = get_integ_time();  // Get current simulation time
    static double next_print = 0.0;  // Time for next print

    load_state(
        &S->pos ,
        &S->vel ,
        NULL);

    load_deriv(
        &S->vel ,
        &S->acc ,
        NULL);

    ipass = integrate();

    unload_state(
        &S->pos ,
        &S->vel ,
        NULL );

    // Print only when we've reached or passed the next print time
    if (now >= next_print) {
        fprintf(stderr, "Time = %.9f, Pos = %.9f\n", now, S->pos);
        next_print = now + 1.0;  // Set next print time to 1 second later
    }

    return(ipass);
}