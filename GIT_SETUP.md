# Git Setup Guide

## 🎯 Tujuan
Setup git repository untuk Celerates_Moodify dengan mengecualikan file-file sensitif dan tidak perlu.

## 📂 File yang DIKECUALIKAN dari Repository

### ❌ **File Sensitif:**
- `.streamlit/` folder (berisi secrets dan config)
- `spotify_data.csv` (dataset besar)
- `.env` files (API keys)
- `secrets.toml` (Streamlit secrets)

### ❌ **File Temporary:**
- `__pycache__/` folders
- `*.pyc` files
- `*.log` files
- `tmp/` dan `temp/` folders

### ❌ **IDE & OS Files:**
- `.vscode/` folder
- `.idea/` folder
- `.DS_Store` (macOS)
- `Thumbs.db` (Windows)

## 🚀 Cara Menjalankan

### Option 1: Windows Batch File
```bash
# Double-click atau run di command prompt
setup_git.bat
```

### Option 2: Bash Script (Git Bash/Linux/Mac)
```bash
# Make executable
chmod +x setup_git.sh

# Run script
./setup_git.sh
```

### Option 3: Manual Commands
```bash
# 1. Create README
echo "# Celerates_Moodify" >> README.md

# 2. Initialize git
git init

# 3. Add .gitignore first (PENTING!)
git add .gitignore

# 4. Add all files (yang tidak dikecualikan)
git add .

# 5. Check status
git status

# 6. Commit
git commit -m "first commit: Moodify AI - Enhanced Indonesian Music Recommendation System"

# 7. Set branch
git branch -M main

# 8. Add remote
git remote add origin https://github.com/masuden0000/Celerates_Moodify.git

# 9. Push
git push -u origin main
```

## ⚠️ **PENTING: Urutan Eksekusi**

1. **WAJIB** add `.gitignore` SEBELUM `git add .`
2. Cek `git status` untuk memastikan file yang benar ter-add
3. File `.streamlit/` dan `spotify_data.csv` TIDAK boleh muncul di status

## ✅ **Verifikasi Berhasil**

Setelah setup, cek bahwa file-file ini **TIDAK ADA** di repository GitHub:
- ❌ `.streamlit/secrets.toml`
- ❌ `spotify_data.csv`
- ❌ `__pycache__/` folders
- ❌ `.env` files

## 🔗 **Repository URL**
https://github.com/masuden0000/Celerates_Moodify

## 📋 **File yang AKAN DI-UPLOAD ke GitHub**

### ✅ **Core Application:**
- `app.py`
- `src/` folder (semua module)
- `requirements*.txt`
- `README.md`

### ✅ **Documentation:**
- `SETUP.md`
- `ENHANCED_FEATURES_LOG.md`
- `FIX_LOG.md`

### ✅ **Configuration:**
- `.gitignore`
- `setup_git.sh` & `setup_git.bat`

### ✅ **Tests:**
- `test_*.py` files

## 🛠️ **Troubleshooting**

### Jika file sensitif sudah ter-commit:
```bash
# Remove from git but keep local file
git rm --cached .streamlit/secrets.toml
git rm --cached spotify_data.csv

# Commit the removal
git commit -m "Remove sensitive files"

# Push changes
git push
```

### Jika repository sudah ada:
```bash
# Remove existing remote
git remote remove origin

# Add correct remote
git remote add origin https://github.com/masuden0000/Celerates_Moodify.git

# Force push
git push -u origin main --force
```

## 💡 **Tips**

1. **Selalu cek** `git status` sebelum commit
2. **Review** `.gitignore` untuk file baru yang perlu dikecualikan
3. **Backup** file sensitif secara terpisah
4. **Update** README.md dengan informasi setup yang lengkap
