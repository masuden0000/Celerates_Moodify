@echo off
REM Script untuk cleanup git repository dan mengatasi masalah file besar

echo 🔧 Git Repository Cleanup Script
echo ================================
echo.

echo 📋 What this script will do:
echo 1. Remove current git repository
echo 2. Reinitialize clean repository
echo 3. Ensure large files are excluded
echo 4. Setup fresh repository for push
echo.

echo ⚠️ WARNING: This will remove all git history!
echo Press any key to continue, or close this window to cancel...
pause >nul

echo.
echo 🗑️ Removing existing git repository...
if exist ".git" (
    rmdir /s /q ".git"
    echo ✅ Git repository removed
) else (
    echo ℹ️ No git repository found
)

echo.
echo 🔍 Checking for large files that should be excluded...
if exist "spotify_data.csv" (
    echo ⚠️ Found: spotify_data.csv ^(167MB - will be excluded^)
)
if exist ".streamlit" (
    echo ⚠️ Found: .streamlit folder ^(contains secrets - will be excluded^)
)

echo.
echo 📝 Ensuring .gitignore is properly configured...
if exist ".gitignore" (
    echo ✅ .gitignore exists
) else (
    echo ❌ .gitignore missing! Creating one...
    (
        echo # Large files
        echo spotify_data.csv
        echo *.csv
        echo.
        echo # Streamlit
        echo .streamlit/
        echo *.streamlit
        echo.
        echo # Python
        echo __pycache__/
        echo *.py[cod]
        echo.
        echo # Environment
        echo .env
        echo .venv
        echo venv/
    ) > .gitignore
    echo ✅ Basic .gitignore created
)

echo.
echo 🚀 Ready to run clean git setup!
echo Run setup_git.bat to proceed with clean repository setup.
echo.
pause
