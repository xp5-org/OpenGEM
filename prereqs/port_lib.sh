#!/bin/sh
# Prepare the Pacific C GEM bindings library sources for OpenWatcom.
# usage: port_lib.sh <libwork dir> ; the dir holds a throwaway copy only.
set -e
D=${1:?dir}
cd "$D"
for f in *.C *.H GEMINC/*.H; do tr -d '\032' < "$f" > "$f.t" && mv "$f.t" "$f"; done
sed -i -E 's/typedef FAR +([A-Za-z_0-9]+) +\*([A-Za-z_0-9]+)/typedef \1 FAR *\2/' GEMINC/MACHINE.H
# register far void *p  ->  void far *p
sed -i -E 's/register far void \*/void far */' PPDVDI.C
# Pacific returns AX from functions that fall off the end; make it explicit
sed -i -E 's/^(\s*)(dos_lpvoid\([^;]*\);)/\1return \2/' PPDD003.C PPDD007.C
sed -i -E 's/^(\s*)__DOS\(\);\s*$/\1return __DOS();/' PPDD002.C PPDD028.C
sed -i -E 's/^(\s*\*pavail = .*;)\s*$/\1\n\treturn DOS_AX;/' PPDD019.C
sed -i -E 's/^(\s*DOS_ERR = DR\.x\.cflag;)\s*$/\1\n\treturn DR.x.ax;/' PPDD000.C
# PPDHOOK (INT 0xEF hook for desk accessories) is Pacific asm: not built
rm -f PPDHOOK.C
sed -i -E "s/VOID +dos_lpvoid/WORD dos_lpvoid/" PPDD0.H
sed -i -E '/^\s*VOID\s*$/{N;s/VOID(\s*\r?\ndos_lpvoid)/WORD\1/}' PPDD002.C
sed -i "1i #include <dos.h>" PPDD013.C PPDD026.C
