@echo off
cls
chcp 65001 >nul
rem ---------------------------------
set lib-package-name=battlebotslib

rem Suppression de l'ancienne version
echo - Suppression des anciennes versions
del /Q battlebotslib.zip 2> nul

rem Partie lib client
rem -----------------
rem Création du dossier de package temporaire
set tmp_lib=_tmp_lib
rmdir /S /Q %tmp_lib% 2> nul
mkdir %tmp_lib%

rem Recopie de la lib client
echo - Recopie de la lib client
robocopy /E dist %tmp_lib% > nul

rem Zip du package lib client
echo - Zip du package lib client
cd %tmp_lib%
..\7za.exe a -tzip -r ..\%lib-package-name% * > nul
cd ..

rem Suppression du dossier temporaire
echo - Suppression du dossier temporaire %tmp_lib%
rmdir /S /Q %tmp_lib% 2> nul

pause
