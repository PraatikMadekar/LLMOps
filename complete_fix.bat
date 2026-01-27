@echo off
echo ========================================
echo Complete Fix for Git Secrets Issue
echo ========================================
echo.
echo This will:
echo 1. Remove fix_project.py from tracking
echo 2. Delete the file
echo 3. Amend the last commit
echo 4. Prepare for force push
echo.
pause

cd /d "C:\Users\MIRACLE\Desktop\LLMOps"

echo.
echo [Step 1] Removing fix_project.py from git tracking...
git rm --cached fix_project.py 2>nul
if errorlevel 1 (
    echo File already removed or not tracked
)

echo.
echo [Step 2] Deleting fix_project.py from disk...
if exist fix_project.py (
    del /f fix_project.py
    echo File deleted
) else (
    echo File already deleted
)

echo.
echo [Step 3] Ensuring .gitignore has fix_project.py...
findstr /C:"fix_project.py" .gitignore >nul
if errorlevel 1 (
    echo fix_project.py >> .gitignore
    echo Added to .gitignore
) else (
    echo Already in .gitignore
)

echo.
echo [Step 4] Staging changes...
git add .gitignore
git add -u

echo.
echo [Step 5] Amending last commit to remove secrets...
git commit --amend -m "Setup project with proper configuration and dependencies"

echo.
echo ========================================
echo SUCCESS! Now you need to force push
echo ========================================
echo.
echo Run this command next:
echo     git push origin master --force
echo.
echo WARNING: Force push will overwrite remote history!
echo Only proceed if you're the only one working on this repo.
echo.
echo After force push:
echo 1. Rotate your API keys (get new ones)
echo 2. Update your .env file with new keys
echo.
pause
