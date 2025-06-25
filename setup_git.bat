@echo off
REM Git commands untuk push ke repository tanpa file sensitif
REM File yang dikecualikan: .streamlit/, spotify_data.csv, dan lainnya (lihat .gitignore)

echo 🚀 Starting Git Setup for Celerates_Moodify...
echo.

REM 0. Check if large files exist and warn user
if exist "spotify_data.csv" (
    echo ⚠️ WARNING: spotify_data.csv detected ^(large file^)
    echo This file will be excluded from git repository
    echo.
)

REM 1. Buat README.md jika belum ada
if not exist "README.md" (
    echo # Celerates_Moodify >> README.md
    echo ✅ README.md created
) else (
    echo ✅ README.md already exists
)

REM 2. Initialize git repository
git init
echo ✅ Git repository initialized

REM 3. Add .gitignore first (KRITICAL - harus sebelum git add .)
git add .gitignore
echo ✅ .gitignore added first

REM 4. Verify .gitignore is working
echo.
echo 📋 Checking which files will be tracked...
git add --dry-run .
echo.

REM 5. Ask user to confirm before proceeding
echo ⚠️ IMPORTANT: Make sure spotify_data.csv is NOT listed above!
echo Press any key to continue, or Ctrl+C to abort...
pause >nul

REM 6. Add all files (excluding those in .gitignore)
git add .
echo ✅ All files added (excluding large/sensitive files)

REM 7. Show final status before commit
echo.
echo 📋 Final git status before commit:
git status --short
echo.

REM 8. Check for large files in staging area
echo � Checking for large files in staging area...
for /f "tokens=*" %%i in ('git ls-files --stage') do (
    for /f "tokens=2" %%j in ("%%i") do (
        if %%j GTR 10000000 (
            echo ⚠️ Large file detected: %%i
            echo This may cause push to fail!
        )
    )
)
echo.

REM 9. Commit
git commit -m "first commit: Moodify AI - Enhanced Indonesian Music Recommendation System"
echo ✅ First commit created

REM 10. Set main branch
git branch -M main
echo ✅ Branch set to main

REM 11. Add remote origin
git remote add origin https://github.com/masuden0000/Celerates_Moodify.git
echo ✅ Remote origin added

REM 12. Push to repository
echo.
echo 🚀 Pushing to GitHub repository...
git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo ✅ Successfully pushed to GitHub repository
    echo.
    echo 🎉 Git setup completed successfully!
) else (
    echo ❌ Push failed! Check the error message above.
    echo.
    echo 💡 Common solutions:
    echo    1. Large files detected - check .gitignore
    echo    2. Network connection issues
    echo    3. Repository access permissions
)

echo.
echo 📂 Files excluded from repository:
echo    - .streamlit/ folder
echo    - spotify_data.csv
echo    - __pycache__/ folders  
echo    - .env files
echo    - Other temporary files
echo.
echo 🔗 Repository URL: https://github.com/masuden0000/Celerates_Moodify
echo.
pause
