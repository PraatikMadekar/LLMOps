#!/bin/bash
# Complete fix for git secrets issue

echo "========================================"
echo "Complete Fix for Git Secrets Issue"
echo "========================================"
echo ""

cd ~/Desktop/LLMOps

# Step 1: Make sure fix_project.py is not tracked
echo "[Step 1] Ensuring fix_project.py is not tracked..."
git rm --cached fix_project.py 2>/dev/null || echo "File already removed from tracking"

# Step 2: Delete the file completely
echo "[Step 2] Deleting fix_project.py..."
rm -f fix_project.py

# Step 3: Update .gitignore
echo "[Step 3] Updating .gitignore..."
if ! grep -q "fix_project.py" .gitignore; then
    echo "fix_project.py" >> .gitignore
fi

# Step 4: Stage all changes
echo "[Step 4] Staging changes..."
git add .gitignore
git add -u

# Step 5: Amend the last commit to remove the secrets
echo "[Step 5] Amending last commit to remove secrets..."
git commit --amend -m "Setup project files and configurations (secrets removed)"

echo ""
echo "========================================"
echo "Now force push to overwrite remote"
echo "========================================"
echo ""
echo "Run this command:"
echo "git push origin master --force"
echo ""
echo "IMPORTANT: This will rewrite history on GitHub!"
echo "Only do this if you're the only one working on the repo."
echo ""
