@echo off
echo ========================================
echo Alternative Fix: Reset and Recommit
echo ========================================
echo.
echo This approach:
echo 1. Resets to before the secret commit
echo 2. Recreates the commit without secrets
echo.
echo WARNING: This will lose any unpushed commits!
echo Make sure you have everything saved.
echo.
pause

cd /d "C:\Users\MIRACLE\Desktop\LLMOps"

echo.
echo [Step 1] Creating backup of current state...
git branch backup-before-fix

echo.
echo [Step 2] Showing recent commits...
git log --oneline -5

echo.
echo Enter the commit hash BEFORE the one with secrets (from above):
set /p SAFE_COMMIT="Commit hash: "

echo.
echo [Step 3] Resetting to safe commit...
git reset --soft %SAFE_COMMIT%

echo.
echo [Step 4] Removing fix_project.py...
if exist fix_project.py (
    del /f fix_project.py
)
git rm --cached fix_project.py 2>nul

echo.
echo [Step 5] Updating .gitignore...
findstr /C:"fix_project.py" .gitignore >nul
if errorlevel 1 (
    echo fix_project.py >> .gitignore
)

echo.
echo [Step 6] Staging all changes...
git add .

echo.
echo [Step 7] Creating new clean commit...
git commit -m "Setup project configuration and dependencies (no secrets)"

echo.
echo ========================================
echo Done! Now force push
echo ========================================
echo.
echo Run: git push origin master --force
echo.
echo If something goes wrong, restore with:
echo     git reset --hard backup-before-fix
echo.
pause
