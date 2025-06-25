#!/bin/bash

# Git commands untuk push ke repository tanpa file sensitif
# File yang dikecualikan: .streamlit/, spotify_data.csv, dan lainnya (lihat .gitignore)

echo "🚀 Starting Git Setup for Celerates_Moodify..."

# 1. Buat README.md
echo "# Celerates_Moodify" >> README.md
echo "✅ README.md created"

# 2. Initialize git repository
git init
echo "✅ Git repository initialized"

# 3. Add .gitignore first (penting agar file yang dikecualikan tidak ter-add)
git add .gitignore
echo "✅ .gitignore added"

# 4. Add semua file KECUALI yang ada di .gitignore
git add .
echo "✅ All files added (excluding .streamlit/ and spotify_data.csv)"

# 5. Check status untuk memastikan file yang benar ter-add
echo "📋 Checking git status..."
git status

# 6. Commit
git commit -m "first commit: Moodify AI - Enhanced Indonesian Music Recommendation System"
echo "✅ First commit created"

# 7. Set main branch
git branch -M main
echo "✅ Branch set to main"

# 8. Add remote origin
git remote add origin https://github.com/masuden0000/Celerates_Moodify.git
echo "✅ Remote origin added"

# 9. Push to repository
git push -u origin main
echo "✅ Pushed to GitHub repository"

echo "🎉 Git setup completed successfully!"
echo ""
echo "📂 Files excluded from repository:"
echo "   - .streamlit/ folder"
echo "   - spotify_data.csv"
echo "   - __pycache__/ folders"
echo "   - .env files"
echo "   - Other temporary files"
echo ""
echo "🔗 Repository URL: https://github.com/masuden0000/Celerates_Moodify"
