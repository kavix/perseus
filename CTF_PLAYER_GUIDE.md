# Perseus - CTF Challenge Setup Guide

## 📱 Challenge Information

**Challenge Name:** Perseus  
**Category:** Mobile / Android Forensics  
**Difficulty:** Medium  
**Points:** TBD  
**Author:** kavix  
**Event:** MEDUSA 2.0  

---

## 📋 Prerequisites & Requirements

### Required Tools

#### 1. **Android Debug Bridge (ADB)**
- **Purpose:** Interact with Android device/emulator
- **Installation:**
  - **macOS:** `brew install android-platform-tools`
  - **Linux (Debian/Ubuntu):** `sudo apt-get install android-tools-adb android-tools-fastboot`
  - **Linux (Arch):** `sudo pacman -S android-tools`
  - **Windows:** Download from [Android SDK Platform Tools](https://developer.android.com/tools/releases/platform-tools)
- **Verify Installation:**
  ```bash
  adb --version
  # Should show: Android Debug Bridge version 1.0.41 or higher
  ```

#### 2. **Android Device or Emulator**
- **Minimum Requirements:**
  - **Android Version: 5.0 (Lollipop) or higher (API Level 21+)** ⚠️ REQUIRED
  - Recommended: **Android 9.0 (Pie)** or higher (API Level 28+)
  - Architecture: ARM, ARM64, or x86_64
  - Storage: At least 200MB free space
  - RAM: 2GB minimum, 4GB recommended

- **Option A: Physical Android Device**
  - Enable USB Debugging:
    1. Go to `Settings` → `About Phone`
    2. Tap `Build Number` 7 times to enable Developer Options
    3. Go to `Settings` → `Developer Options`
    4. Enable `USB Debugging`
  - Connect via USB and authorize the computer

- **Option B: Android Emulator**
  - **Android Studio Emulator (Recommended):**
    - Download: [Android Studio](https://developer.android.com/studio)
    - Create AVD: Tools → AVD Manager → Create Virtual Device
    - Recommended: Pixel 5, API 33 (Android 13), x86_64
  
  - **Genymotion:**
    - Download: [Genymotion](https://www.genymotion.com/)
    - Free for personal use
  
  - **Other:** NOX, BlueStacks, LDPlayer (may require additional configuration)

#### 3. **SQLite Tools**
- **Purpose:** Analyze database files
- **Installation:**
  - **macOS:** `brew install sqlite3` (usually pre-installed)
  - **Linux:** `sudo apt-get install sqlite3`
  - **Windows:** Download from [SQLite Downloads](https://www.sqlite.org/download.html)
- **Verify:**
  ```bash
  sqlite3 --version
  ```

#### 4. **Base64 Decoder**
- **Purpose:** Decode encoded strings
- **Built-in on macOS/Linux:**
  ```bash
  echo "encoded_string" | base64 -d
  ```
- **Windows:** Use online tools or install `certutil`

#### 5. **Python 3** (Optional but Recommended)
- **Purpose:** Custom decryption scripts
- **Version:** 3.7 or higher
- **Verify:**
  ```bash
  python3 --version
  ```

---

### Optional Advanced Tools

#### For APK Analysis:
1. **apktool** - Decompile/rebuild APKs
   ```bash
   # macOS
   brew install apktool
   
   # Linux
   sudo apt-get install apktool
   ```

2. **jadx** - Dex to Java decompiler
   ```bash
   # macOS
   brew install jadx
   
   # Or download from: https://github.com/skylot/jadx/releases
   ```

3. **Frida** - Dynamic instrumentation (Advanced)
   ```bash
   pip3 install frida-tools
   ```

4. **Android Backup Extractor** - Extract .ab backup files
   - Download: [ABE on GitHub](https://github.com/nelenkov/android-backup-extractor)
   - Requires Java JRE

---

## 🚀 Getting Started

### Step 1: Verify ADB Connection

```bash
# Start ADB server
adb start-server

# List connected devices
adb devices

# Expected output:
# List of devices attached
# emulator-5554   device
# or
# <device_id>     device
```

**Troubleshooting:**
- If no devices shown, check USB cable/debugging enabled
- If "unauthorized", accept the prompt on your device
- If emulator not detected, ensure it's fully booted

### Step 2: Install the APK

```bash
# Install the provided APK
adb install perseus.apk

# If you get "INSTALL_FAILED_ALREADY_EXISTS":
adb install -r perseus.apk

# For multiple devices, specify device:
adb -s <device_id> install perseus.apk
```

**Verify Installation:**
```bash
adb shell pm list packages | grep perseus
# Should output: package:com.example.perseus
```

### Step 3: Launch the Application

```bash
# Method 1: Launch via ADB
adb shell am start -n com.example.perseus/.MainActivity

# Method 2: Manually open the app on your device
# Look for the "MEDUSA CTF" app icon
```

**Important:** You MUST launch the app at least once and attempt to login before the database files are created!

### Step 4: Explore the Filesystem

```bash
# Connect to device shell
adb shell

# Navigate to app's external storage
cd /storage/emulated/0/Android/data/com.example.perseus

# List contents
ls -la

# Exit shell
exit
```

---

## 📁 What You'll Find

### Application Details
- **Package Name:** `com.example.perseus`
- **Minimum Android Version:** 5.0 Lollipop (API Level 21) ⚠️
- **Target SDK:** 34 (Android 14)
- **Compile SDK:** 34
- **APK Size:** ~20-25 MB (release build)
- **Permissions Required:** READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

### Data Locations
The app stores data in multiple locations:

1. **External Storage** (Accessible without root)
   - Path: `/storage/emulated/0/Android/data/com.example.perseus/`
   - Contains: Application files, databases, cached data

2. **Internal Storage** (Requires root or special access)
   - Path: `/data/data/com.example.perseus/`
   - Contains: SharedPreferences, internal databases

---

## 🔍 Challenge Objectives

### Primary Goal
Find and extract the flag from the application.

### What You Need to Do
1. ✅ Install and run the application
2. ✅ Explore the app's file structure
3. ✅ Locate hidden data
4. ✅ Extract and analyze databases
5. ✅ Decrypt the flag
6. ✅ Submit in format: `MEDUSA{...}`

---

## 💡 Hints System

Hints will be available on the CTF platform with decreasing point values:
- **Hint 1:** Free - General direction
- **Hint 2:** -25 points - Specific location type
- **Hint 3:** -50 points - Tool suggestions
- **Hint 4:** -100 points - Exact path

---

## 📚 Helpful Commands Reference

### ADB Basics
```bash
# List all installed packages
adb shell pm list packages

# Get app info
adb shell dumpsys package com.example.perseus

# Pull files from device
adb pull /path/on/device /path/on/computer

# Push files to device
adb push /path/on/computer /path/on/device

# View app's storage locations
adb shell run-as com.example.perseus pwd
# Note: This only works on debug builds!

# Create backup (for SharedPreferences extraction)
adb backup -noapk com.example.perseus
```

### SQLite Basics
```bash
# Open database
sqlite3 database.db

# List tables
.tables

# Show table schema
.schema table_name

# Query data
SELECT * FROM table_name;

# Exit
.quit
```

### File Operations
```bash
# Find files
find /path -name "*.db"
find /path -type f -name "config*"

# Search in files
grep -r "pattern" /path

# View file contents
cat filename
head -n 20 filename
tail -n 20 filename
```

---

## ⚠️ Important Notes

### DO:
- ✅ Explore the filesystem thoroughly
- ✅ Check both internal and external storage
- ✅ Analyze database files
- ✅ Look for encoded/encrypted data
- ✅ Use SQLite tools for database analysis
- ✅ Read the app's source code if you decompile it

### DON'T:
- ❌ Try to brute force the flag
- ❌ Assume the database is in the APK assets (it's created at runtime)
- ❌ Skip launching the app (files are created on first run)
- ❌ Only check `/data/data/` (you may not have access)
- ❌ Overlook hidden directories or misleading folder names

---

## 🆘 Troubleshooting

### Problem: "adb: device unauthorized"
**Solution:** Check your device for authorization popup, unlock screen

### Problem: "Installation failed: INSTALL_FAILED_INSUFFICIENT_STORAGE"
**Solution:** Free up space on device, need at least 200MB

### Problem: "adb: device offline"
**Solution:**
```bash
adb kill-server
adb start-server
adb devices
```

### Problem: Can't find database files
**Solution:** 
1. Launch the app
2. Try to login (enter any username/password)
3. Files are created on first login attempt
4. Check `/storage/emulated/0/Android/data/com.example.perseus/files`

### Problem: Permission denied when accessing files
**Solution:**
- Use `adb pull` to copy files to your computer
- For external storage, no root needed
- For `/data/data/`, you need root or backup method

### Problem: Emulator won't start
**Solution:**
- Check virtualization is enabled in BIOS
- Try x86_64 images instead of ARM
- Allocate more RAM to emulator (4GB recommended)

---

## 📖 Learning Resources

### Android Forensics
- [Android Developer Docs - ADB](https://developer.android.com/tools/adb)
- [Android App Storage](https://developer.android.com/training/data-storage)
- [Mobile Security Framework (MobSF)](https://github.com/MobSF/Mobile-Security-Framework-MobSF)

### CTF Resources
- [Android Security Awesome List](https://github.com/ashishb/android-security-awesome)
- [OWASP Mobile Security Testing Guide](https://owasp.org/www-project-mobile-security-testing-guide/)

### Tools Documentation
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [apktool Documentation](https://apktool.org/docs/the-basics/)
- [Frida Documentation](https://frida.re/docs/home/)

---

## 🏆 Scoring

- **Base Points:** TBD
- **Hint Penalties:** As described above
- **First Blood Bonus:** TBD
- **Time Bonus:** TBD

---

## 📞 Support

If you encounter technical issues (not related to solving the challenge):
- Contact CTF admins on Discord/Slack
- Check the FAQ section on the CTF platform
- Report bugs to challenge author

**Note:** Hints about the solution should be requested through the official hint system, not via direct messages.

---

## ✅ Pre-Challenge Checklist

Before starting the challenge, ensure:

- [ ] ADB is installed and working (`adb --version`)
- [ ] Android device/emulator is connected (`adb devices`)
- [ ] SQLite3 is installed (`sqlite3 --version`)
- [ ] You can install APKs (`adb install --help`)
- [ ] You have basic command-line knowledge
- [ ] You understand Android file structure basics
- [ ] You have a text editor for analyzing files
- [ ] You have Python 3 installed (optional)

---

## 🎯 Expected Time

- **Beginner:** 2-4 hours
- **Intermediate:** 1-2 hours  
- **Advanced:** 30-60 minutes

Good luck, and may Perseus guide your way! 🏛️

---

**Challenge Author:** kavix  
**Contact:** [Your Contact Info]  
**Last Updated:** November 13, 2025
