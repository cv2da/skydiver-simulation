/*************************************************************************
PURPOSE: (Represent the state and initial conditions of a skydiver)
**************************************************************************/
#ifndef SKYDIVER_H
#define SKYDIVER_H
#include "trick/regula_falsi.h"

typedef struct {

    double vel0 ;    /* *i m Init velocity of skydiver */
    double pos0 ;    /* *i m Init position of skydiver */
    double g;        /* *i m/s2 Init gravity */
    double Rho;      /* *i kg/m3 Init air density */
    double S;        /* *i m2 Init surface area */
    double Cd;       /* *i -- Init coeff of drag */
    double m;        /* *i kg Init mass of the skydiver */

    double acc ;     /* m/s2 z-acceleration  */
    double vel ;     /* m/s z-velocity */
    double pos ;     /* m z-position */
    double Fd;      /* N drag force */

    REGULA_FALSI rf;

} SKYDIVER ;

#ifdef __cplusplus
extern "C" {
#endif
    int skydiver_default_data(SKYDIVER*) ;
    int skydiver_init(SKYDIVER*) ;
    int skydiver_shutdown(SKYDIVER*) ;
#ifdef __cplusplus
}
#endif

#endif