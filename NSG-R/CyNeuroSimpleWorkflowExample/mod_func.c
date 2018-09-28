#include <stdio.h>
#include "hocdec.h"
#define IMPORT extern __declspec(dllimport)
IMPORT int nrnmpi_myid, nrn_nobanner_;

extern void _kdr_reg();
extern void _leak_reg();
extern void _na_reg();

modl_reg(){
	//nrn_mswindll_stdio(stdin, stdout, stderr);
    if (!nrn_nobanner_) if (nrnmpi_myid < 1) {
	fprintf(stderr, "Additional mechanisms from files\n");

fprintf(stderr," kdr.mod");
fprintf(stderr," leak.mod");
fprintf(stderr," na.mod");
fprintf(stderr, "\n");
    }
_kdr_reg();
_leak_reg();
_na_reg();
}
