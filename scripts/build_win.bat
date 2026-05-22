@echo off
setlocal

pip install pyinstaller

pyinstaller ^
  --onedir ^
  --name pyxis ^
  --collect-all llama_cpp ^
  --collect-all psutil ^
  --collect-all prompt_toolkit ^
  -y ^
  run.py

if exist build rmdir /s /q build
if exist pyxis.spec del pyxis.spec
if not exist dist\models mkdir dist\models
copy scripts\Run-Pyxis.bat dist\

echo.
echo Done. Distribute the dist\ folder:
echo   dist\Run-Pyxis.bat      -- double-click to open a cmd window
echo   dist\pyxis\pyxis.exe    -- run from terminal: pyxis\pyxis.exe
echo   dist\models\            -- drop .gguf files here
