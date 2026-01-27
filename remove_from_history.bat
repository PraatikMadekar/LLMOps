@echo off
echo ========================================
echo Removing Secrets from Git History
echo ========================================
echo.
echo WARNING: This will rewrite git history!
echo Make sure you have a backup of your work.
echo.
pause

cd /d "C:\Users\MIRACLE\Desktop\LLMOps"

echo.
echo [Step 1] Removing fix_project.py from all commits...
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch fix_project.py" --prune-empty --tag-name-filter cat -- --all

echo.
echo [Step 2] Cleaning up refs...
rm -rf .git/refs/original/
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo.
echo [Step 3] Verifying removal...
git log --all --full-history -- fix_project.py

echo.
echo ========================================
echo History cleaned! Now force push.
echo ========================================
echo.
echo IMPORTANT: Force push will overwrite remote history.
echo If others are working on this repo, coordinate with them first!
echo.
echo Run: git push origin master --force
echo.
pause
