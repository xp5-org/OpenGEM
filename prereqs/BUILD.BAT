@echo off
set WATCOM=C:\WATCOM
set PATH=%WATCOM%\BINW;%WATCOM%\BINB;%PATH%
set INCLUDE=%WATCOM%\H
if exist BUILD.LOG del BUILD.LOG
for %%f in (*.c) do call ONE.BAT %%f
echo === link >> BUILD.LOG
wcl -bt=dos -ms -zq -fe=DESKTOP.EXE *.obj >> BUILD.LOG
echo done > DONE.TXT
