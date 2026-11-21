

#include "ppdgem.h"
#include "ppdd0.h"



	WORD
dos_sdta(ldta)	/* set the Disk Transfer Address ( DTA ) */
	LPVOID		ldta;
{
	return dos_lpvoid(0x1a00, ldta);
}
