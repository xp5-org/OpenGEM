#!/bin/sh
# Pacific C -> OpenWatcom source fixups for the FreeGEM desktop. Usage: port_desktop.sh <desk_run dir>
# Everything is applied to the throwaway copy; the SDK tree is never edited.
set -e
D="$1"; cd "$D"
# 1. old DOS ^Z end-of-file markers
for f in *.C *.H GEMINC/*.H; do tr -d '\032' < "$f" > "$f.tmp" && mv "$f.tmp" "$f"; done
# 2. Watcom wants the far qualifier after the type: "typedef FAR VOID *P" -> "typedef VOID FAR *P"
sed -i -E 's/typedef FAR +([A-Za-z_0-9]+) +\*([A-Za-z_0-9]+)/typedef \1 FAR *\2/' GEMINC/MACHINE.H
# 3. Watcom's string.h now has its own strlcpy/strlcat with other prototypes
sed -i -E 's/\bstrl(cpy|cat)\b/dsk_strl\1/g' *.C *.H
# 4. Pacific "#asm" blocks. INT3.C -> Watcom inline asm; MAIN.C's only asm is the unused freemem()
cat > INT3.C <<'EOT'
void debugbreak(void)
{
	_asm { int 3 }
}
unsigned getcs(void);
#pragma aux getcs = "mov ax,cs" value [ax];
EOT
n=$(grep -n '^#asm' MAIN.C | head -1 | cut -d: -f1)
[ -n "$n" ] && head -n $((n-1)) MAIN.C > MAIN.tmp && mv MAIN.tmp MAIN.C
# 5. version string in the resource (same length, offsets unchanged)
python3 "$(dirname "$0")/patch_version.py" DESKTOP.RSC
