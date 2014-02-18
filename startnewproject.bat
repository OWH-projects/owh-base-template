:: for Windows users, a batch file to quickly start a new Data Omaha project

cd git
@echo off
set /p name="Name your project: " %=%
git clone https://github.com/OWH-projects/owh-base-template %name%
%SystemRoot%\explorer.exe "C:\Users\Winchester\Desktop\git\%name%"