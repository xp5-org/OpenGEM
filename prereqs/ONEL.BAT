@echo off
echo === %1 >> ..\BUILD.LOG
wcc %1 >> ..\BUILD.LOG
