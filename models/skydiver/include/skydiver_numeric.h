/*************************************************************************
PURPOSE: ( Skydiver Numeric Model )
**************************************************************************/

#ifndef SKYDIVER_NUMERIC_H
#define SKYDIVER_NUMERIC_H

#include "skydiver.h"

#ifdef __cplusplus
extern "C" {
#endif
int skydiver_integ(SKYDIVER*) ;
int skydiver_update(SKYDIVER*) ;
// double skydiver_impact(SKYDIVER*) ;
#ifdef __cplusplus
}
#endif
#endif