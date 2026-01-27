@echo off
echo ========================================
echo Fixing Git Push Issue (Removing Secrets)
echo ========================================
echo.

cd /d "C:\Users\MIRACLE\Desktop\LLMOps"

echo [Step 1] Removing fix_project.py from git tracking...
git rm --cached fix_project.py
if errorlevel 1 (
    echo File already removed or not tracked
)

echo.
echo [Step 2] Staging .gitignore changes...
git add .gitignore
git add .gitIgnore

echo.
echo [Step 3] Committing changes...
git commit -m "Remove fix_project.py from tracking (contains secrets) and update .gitignore"

echo.
echo ========================================
echo Done! Now you can safely push.
echo ========================================
echo.
echo Run: git push origin master
echo.
pause
