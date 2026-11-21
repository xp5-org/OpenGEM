@echo off
set WATCOM=C:\WATCOM
set PATH=%WATCOM%\BINW;%WATCOM%\BINB;%PATH%
set INCLUDE=%WATCOM%\H
if exist BUILD.LOG del BUILD.LOG
echo === library >> BUILD.LOG
set WCC=-bt=dos -ml -zq -dLARGE_MODEL -d__PACIFIC__ -dfar=__far -dnear=__near -dFP_CONSTRUCT=MK_FP -i=. -i=..\GEMINC
cd LIBSRC
for %%f in (*.c) do call ..\ONEL.BAT %%f
wasm -zq -fo=PPDLDRAW.OBJ ..\PPDLDRAW.ASM >> ..\BUILD.LOG
if exist LIB.RSP del LIB.RSP
for %%f in (*.obj) do echo +%%f >> LIB.RSP
wlib -q -b -n PPDGEM-L.LIB @LIB.RSP >> ..\BUILD.LOG
cd ..
set WCC=-bt=dos -ml -zq -dLARGE_MODEL -d__PACIFIC__ -dfar=__far -dnear=__near -i=. -i=GEMINC
echo === desktop >> BUILD.LOG
wasm -zq -fo=DESKOSIF.OBJ DESKOSIF.ASM >> BUILD.LOG
for %%f in (*.c) do call ONED.BAT %%f
echo === link >> BUILD.LOG
wlink @LINK.LNK >> BUILD.LOG
echo done > DONE.TXT
