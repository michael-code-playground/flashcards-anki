@echo off
cd /d %USERPROFILE%\Downloads
for %%F in (takeout*.zip) do (
    tar.exe -xf "%%F" )

copy "C:\Users\michael\Downloads\Takeout\Chrome\*.json" "C:\Users\michael\Desktop\PROJECTS\work-offloaders\"
