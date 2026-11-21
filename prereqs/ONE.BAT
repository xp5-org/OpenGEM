@echo off
echo === %1 >> BUILD.LOG
wcc -bt=dos -ms -zq -d__PACIFIC__ -dfar=__far -dnear=__near -i=. -i=GEMINC %1 >> BUILD.LOG
