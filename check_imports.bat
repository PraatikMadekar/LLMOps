@echo off
echo ========================================
echo Checking for langchain.schema imports
echo ========================================
echo.

cd /d "C:\Users\MIRACLE\Desktop\LLMOps"

echo Searching for old imports...
echo.

findstr /S /N /C:"from langchain.schema" *.py multi_doc_chat\*.py tests\*.py 2>nul

if errorlevel 1 (
    echo.
    echo ========================================
    echo SUCCESS! No old imports found.
    echo All imports have been updated.
    echo ========================================
) else (
    echo.
    echo ========================================
    echo WARNING! Old imports still exist.
    echo Please review the files listed above.
    echo ========================================
)

echo.
echo Checking for new imports...
echo.

findstr /S /N /C:"from langchain_core.documents import Document" *.py multi_doc_chat\*.py tests\*.py 2>nul

echo.
echo ========================================
echo Check complete!
echo ========================================
pause
