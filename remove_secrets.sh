#!/bin/bash
# Script to remove fix_project.py from git history and add to gitignore

echo "Removing fix_project.py from git tracking..."
git rm --cached fix_project.py

echo "Adding to .gitignore..."
echo "" >> .gitignore
echo "# Temporary fix scripts with secrets" >> .gitignore
echo "fix_project.py" >> .gitignore

echo "Committing changes..."
git add .gitignore
git commit -m "Remove fix_project.py and add to gitignore (contains secrets)"

echo "Done! Now you can push safely."
echo ""
echo "Run: git push origin master"
