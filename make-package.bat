@echo off
cls
chcp 65001 >nul
rem ---------------------------------
set lib-package-name=battlebotslib-python
set doc-package-name=battlebotslib-python-doc

rem Suppression de l'ancienne version
echo - Suppression des anciennes versions
del /Q %lib-package-name%.zip 2> nul
del /Q %doc-package-name%.zip 2> nul

rem Build de la lib
rem ---------------
del /Q dist\*.whl 2> nul
venv\Scripts\python setup.py bdist_wheel

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


rem Partie documentation
rem --------------------
rem Création du dossier de package temporaire
set tmp_doc=_tmp_doc
rmdir /S /Q %tmp_doc% 2> nul
mkdir %tmp_doc%

rem Recopie de la doc
echo - Recopie de la documentation
robocopy /E docs %tmp_doc% > nul
robocopy /E example %tmp_doc%\example > nul

rem Suppression des fichiers inutiles
echo - Suppression des fichiers inutiles
del /Q %tmp_doc%\*.md 2> nul
del /Q %tmp_doc%\*.bak 2> nul
del /Q %tmp_doc%\client\*.md 2> nul
del /Q %tmp_doc%\client\*.bak 2> nul
del /Q %tmp_doc%\tech\*.md 2> nul
del /Q %tmp_doc%\tech\*.bak 2> nul
del /Q %tmp_doc%\style\*.bak 2> nul
rmdir /S /Q %tmp_doc%\example\.idea 2> nul
rmdir /S /Q %tmp_doc%\example\venv 2> nul
rmdir /S /Q %tmp_doc%\example\__pycache__ 2> nul

rem Zip du package documentation
echo - Zip du package documentation
cd %tmp_doc%
..\7za.exe a -tzip -r ..\%doc-package-name% * > nul
cd ..

rmdir /S /Q %tmp_doc% 2> nul


pause
