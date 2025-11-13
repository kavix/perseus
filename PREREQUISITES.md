# Perseus CTF Challenge - Prerequisites & Setup Guide

## 📢 Read This BEFORE the Competition!

This document contains all the tools, requirements, and setup instructions you need to complete the **Perseus Android Challenge**. Please set up everything in advance to avoid losing time during the competition.

---

## 🎯 Challenge Information

- **Challenge Name:** Perseus
- **Category:** Mobile Security / Android Forensics
- **Difficulty:** Medium
- **Platform:** Android
- **Type:** APK Analysis & Reverse Engineering

---

## 📱 Device Requirements

### Minimum Requirements

#### Android Device Specifications
- **Minimum Android Version:** Android 5.0 Lollipop (API 21) ⚠️ **CRITICAL**
- **Recommended Version:** Android 9.0 Pie (API 28) or higher
- **Architecture:** ARM, ARM64, x86, or x86_64
- **Storage:** At least 500MB free space
- **RAM:** 2GB minimum, 4GB recommended

#### Computer Specifications
- **OS:** Windows 10/11, macOS 10.14+, or Linux (Ubuntu 20.04+)
- **Storage:** 5GB free space for tools
- **RAM:** 4GB minimum, 8GB recommended (if using emulator)
- **Internet:** Required for initial setup

---

## 🛠️ Required Tools Checklist

### Essential Tools (Must Have)

#### 1. Android Debug Bridge (ADB)
**Purpose:** Communicate with Android devices/emulators

**Installation:**

**macOS:**
```bash
brew install android-platform-tools
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt-get update
sudo apt-get install android-tools-adb android-tools-fastboot
```

**Linux (Arch):**
```bash
sudo pacman -S android-tools
```

**Windows:**
1. Download [Android SDK Platform Tools](https://developer.android.com/tools/releases/platform-tools)
2. Extract to `C:\platform-tools\`
3. Add to PATH: System Properties → Environment Variables → Path → Add `C:\platform-tools`

**Verify Installation:**
```bash
adb --version
# Expected: Android Debug Bridge version 1.0.41 or higher
```

---

#### 2. SQLite3
**Purpose:** Analyze database files

**Installation:**

**macOS:**
```bash
brew install sqlite3
# Usually pre-installed
```

**Linux:**
```bash
sudo apt-get install sqlite3
```

**Windows:**
1. Download from [SQLite Downloads](https://www.sqlite.org/download.html)
2. Extract `sqlite3.exe` to `C:\sqlite\`
3. Add to PATH

**Verify Installation:**
```bash
sqlite3 --version
# Expected: 3.x.x or higher
```

---

#### 3. Python 3
**Purpose:** Run decryption scripts, automation

**Installation:**

**macOS:**
```bash
brew install python3
```

**Linux:**
```bash
sudo apt-get install python3 python3-pip
```

**Windows:**
1. Download from [python.org](https://www.python.org/downloads/)
2. **Important:** Check "Add Python to PATH" during installation

**Verify Installation:**
```bash
python3 --version
# Expected: Python 3.7 or higher

pip3 --version
```

---

#### 4. Java Development Kit (JDK)
**Purpose:** Required for keytool, jarsigner, and Java-based tools

**Installation:**

**macOS:**
```bash
brew install openjdk@11
```

**Linux:**
```bash
sudo apt-get install openjdk-11-jdk
```

**Windows:**
Download from [Oracle](https://www.oracle.com/java/technologies/downloads/) or [Adoptium](https://adoptium.net/)

**Verify Installation:**
```bash
java -version
javac -version
keytool
# Should show usage information
```

---

### Recommended Tools (Highly Useful)

#### 5. apktool
**Purpose:** Decompile and rebuild APK files

**Installation:**

**macOS:**
```bash
brew install apktool
```

**Linux:**
```bash
sudo apt-get install apktool

# Or manual installation:
wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool
wget https://bitbucket.org/iBotPeaches/apktool/downloads/apktool_2.9.3.jar
chmod +x apktool
sudo mv apktool apktool_2.9.3.jar /usr/local/bin/
```

**Windows:**
1. Download `apktool.bat` and `apktool.jar` from [apktool.org](https://apktool.org/)
2. Place in `C:\apktool\`
3. Add to PATH

**Verify Installation:**
```bash
apktool --version
# Expected: 2.7.0 or higher
```

---

#### 6. jadx (Dex to Java Decompiler)
**Purpose:** Convert Android bytecode to readable Java code

**Installation:**

**macOS:**
```bash
brew install jadx
```

**Linux:**
```bash
# Download latest release
wget https://github.com/skylot/jadx/releases/download/v1.4.7/jadx-1.4.7.zip
unzip jadx-1.4.7.zip -d jadx
sudo mv jadx /opt/
sudo ln -s /opt/jadx/bin/jadx /usr/local/bin/jadx
sudo ln -s /opt/jadx/bin/jadx-gui /usr/local/bin/jadx-gui
```

**Windows:**
1. Download from [jadx releases](https://github.com/skylot/jadx/releases)
2. Extract to `C:\jadx\`
3. Add `C:\jadx\bin` to PATH

**Verify Installation:**
```bash
jadx --version
# or
jadx-gui
```

---

#### 7. apksigner (Android SDK Build Tools)
**Purpose:** Sign and verify APK signatures

**Installation:**

Comes with Android SDK Build Tools. Two options:

**Option A: Install via Android Studio**
1. Install [Android Studio](https://developer.android.com/studio)
2. Tools → SDK Manager → SDK Tools → Android SDK Build-Tools
3. Add to PATH: `~/Library/Android/sdk/build-tools/34.0.0/` (macOS/Linux)

**Option B: Command Line Tools**
```bash
# macOS/Linux
wget https://dl.google.com/android/repository/commandlinetools-mac-9477386_latest.zip
unzip commandlinetools-*.zip
mkdir -p ~/android-sdk/cmdline-tools/latest
mv cmdline-tools/* ~/android-sdk/cmdline-tools/latest/

# Add to PATH
export ANDROID_HOME=~/android-sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin
export PATH=$PATH:$ANDROID_HOME/build-tools/34.0.0
```

**Verify Installation:**
```bash
apksigner --version
# Expected: 34.0.0 or higher
```

---

### Optional Advanced Tools

#### 8. Frida (Dynamic Instrumentation)
**Purpose:** Runtime hooking and analysis

```bash
pip3 install frida-tools
```

#### 9. objection
**Purpose:** Frida-based mobile exploration toolkit

```bash
pip3 install objection
```

#### 10. Android Backup Extractor (ABE)
**Purpose:** Extract .ab backup files

Download: [ABE on GitHub](https://github.com/nelenkov/android-backup-extractor/releases)

---

## 📲 Android Device Setup

### Option 1: Physical Android Device (Recommended)

#### Enable Developer Options
1. Go to **Settings** → **About Phone**
2. Find **Build Number**
3. Tap **Build Number** 7 times
4. Enter your PIN/Pattern if prompted
5. You should see "You are now a developer!"

#### Enable USB Debugging
1. Go to **Settings** → **System** → **Developer Options**
2. Enable **USB Debugging**
3. (Optional) Enable **Stay Awake** - keeps screen on while charging

#### Connect to Computer
1. Connect device via USB cable
2. On device, authorize the computer when prompted
3. Verify connection:
```bash
adb devices
# Should show your device
```

---

### Option 2: Android Emulator

#### Using Android Studio Emulator

1. **Install Android Studio**
   - Download from [developer.android.com](https://developer.android.com/studio)

2. **Create Virtual Device**
   - Open Android Studio
   - Tools → Device Manager → Create Device
   - Choose: **Pixel 5** or **Pixel 6**
   - System Image: **API 33** (Android 13) or **API 34** (Android 14)
   - **Important:** Choose **x86_64** images (not ARM) for better performance
   - Download system image if prompted
   - Finish setup

3. **Launch Emulator**
   - Click Play button in Device Manager
   - Or from terminal:
   ```bash
   emulator -list-avds
   emulator -avd <avd_name>
   ```

4. **Verify Connection**
   ```bash
   adb devices
   # Should show emulator-5554 or similar
   ```

#### Using Genymotion (Alternative)

1. Download from [genymotion.com](https://www.genymotion.com/)
2. Create account (free for personal use)
3. Install and create virtual device
4. Launch device

---

## ✅ Pre-Competition Checklist

Complete this checklist **before the competition starts**:

### Tools Verification
- [ ] ADB installed and working (`adb --version`)
- [ ] ADB can detect devices (`adb devices`)
- [ ] SQLite3 installed (`sqlite3 --version`)
- [ ] Python 3 installed (`python3 --version`)
- [ ] Java/JDK installed (`java -version`, `keytool`)
- [ ] apktool installed (`apktool --version`)
- [ ] jadx installed (`jadx --version`)
- [ ] apksigner available (part of Android SDK)

### Device Setup
- [ ] Android device/emulator ready
- [ ] Device running Android 5.0 (API 21) or higher
- [ ] USB Debugging enabled (physical device)
- [ ] Device appears in `adb devices`
- [ ] Can install APK: `adb install test.apk` works

### Skills Check
- [ ] Know how to use `adb shell`
- [ ] Can navigate Linux filesystem (`cd`, `ls`, `find`)
- [ ] Can use `sqlite3` to query databases
- [ ] Understand Base64 encoding/decoding
- [ ] Familiar with basic Python scripting
- [ ] Know how to decompile APK with apktool
- [ ] Can view decompiled code with jadx

### Environment
- [ ] Stable internet connection (for downloading tools if needed)
- [ ] Text editor installed (VSCode, Sublime, Notepad++, vim)
- [ ] Terminal/Command Prompt ready
- [ ] Hex editor available (optional: HxD, hexdump, xxd)
- [ ] Note-taking tool ready (for flags, credentials, etc.)

---

## 🧪 Test Your Setup

Run these commands to verify everything works:

```bash
# 1. Check ADB
adb version
adb devices

# 2. Check SQLite
sqlite3 --version
echo "SELECT 'SQLite Works';" | sqlite3

# 3. Check Python
python3 --version
python3 -c "print('Python Works')"

# 4. Check Java Tools
java -version
keytool -help

# 5. Check apktool (if installed)
apktool --version

# 6. Check jadx (if installed)
jadx --version

# 7. Check apksigner (if installed)
apksigner --version

# 8. Test ADB Install (optional)
# Download any small APK and test:
adb install test.apk
adb uninstall com.package.name
```

---

## 📚 Useful Commands Reference

### ADB Commands
```bash
# List devices
adb devices

# Install APK
adb install app.apk
adb install -r app.apk  # Reinstall

# Uninstall app
adb uninstall com.package.name

# Shell access
adb shell

# Pull files from device
adb pull /path/on/device /path/on/computer

# Push files to device
adb push /path/on/computer /path/on/device

# List installed packages
adb shell pm list packages

# Get app info
adb shell dumpsys package com.package.name

# Create backup
adb backup -noapk com.package.name
```

### SQLite Commands
```bash
# Open database
sqlite3 database.db

# Show tables
.tables

# Show schema
.schema

# Query data
SELECT * FROM table_name;

# Exit
.quit
```

### File Operations
```bash
# Find files
find /path -name "*.db"
find . -type f -name "config*"

# Search in files
grep -r "pattern" /path

# View files
cat file.txt
head -20 file.txt
tail -20 file.txt
less file.txt

# Base64 decode
echo "encoded_string" | base64 -d
```

---

## 🔧 Troubleshooting Common Issues

### ADB Issues

**Problem:** `adb: command not found`
- **Solution:** Add ADB to PATH or use full path to adb executable

**Problem:** `device unauthorized`
- **Solution:** Check device for authorization prompt, unlock screen

**Problem:** `no devices/emulators found`
- **Solution:** 
  ```bash
  adb kill-server
  adb start-server
  adb devices
  ```

### Emulator Issues

**Problem:** Emulator won't start
- **Solution:** Enable virtualization in BIOS (Intel VT-x / AMD-V)
- Try x86_64 image instead of ARM
- Allocate more RAM (4GB recommended)

**Problem:** Emulator is very slow
- **Solution:** Use x86_64 system images, not ARM
- Enable hardware acceleration
- Allocate more RAM and CPU cores

### Installation Issues

**Problem:** Can't install APK
- **Solution:** 
  - Check minimum Android version (5.0+)
  - Uninstall existing version first
  - Enable "Install from Unknown Sources" in settings

---

## 💡 Learning Resources

### Before the Competition
- [ADB Documentation](https://developer.android.com/tools/adb)
- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [Android App Structure](https://developer.android.com/guide/components/fundamentals)
- [APK Analysis Basics](https://github.com/ashishb/android-security-awesome)

### Practice Resources
- [OWASP UnCrackable Apps](https://github.com/OWASP/owasp-mastg/tree/master/Crackmes)
- [Android CTF Challenges](https://github.com/topics/android-ctf)

---

## 📋 Quick Reference Card

### Minimum System Requirements
| Component | Requirement |
|-----------|-------------|
| Android OS | 5.0 Lollipop (API 21) minimum |
| Storage | 500MB free |
| Computer OS | Windows 10+, macOS 10.14+, Linux |
| ADB Version | 1.0.41+ |
| Python | 3.7+ |
| Java | JDK 11+ |

### Essential Tools Priority
1. **Critical:** ADB, Android Device/Emulator
2. **Very Important:** SQLite3, Python 3
3. **Important:** Java/JDK (for keytool, jarsigner)
4. **Recommended:** apktool, jadx, apksigner
5. **Optional:** Frida, objection, ABE

---

## 🆘 Getting Help

### During Setup (Before Competition)
- Check official tool documentation
- Search StackOverflow
- Review Android Developer documentation
- Test on a simple APK first

### During Competition
- Use the official hint system (may cost points)
- Check CTF platform FAQ
- Contact admins for **technical issues only** (not for solution hints)

---

## ⏱️ Time Recommendations

**Setup Time:** 1-2 hours before competition

**Tool Installation:** 30-60 minutes  
**Device Setup:** 15-30 minutes  
**Testing & Verification:** 15-30 minutes  
**Familiarization:** 30 minutes

**Start your setup at least 3 hours before the competition!**

---

## 🎯 Final Notes

1. **Test everything before the competition**
2. **Have a backup plan** (second device, different emulator)
3. **Keep tools updated** but verify they work
4. **Read documentation** for tools you're unfamiliar with
5. **Practice basic commands** before competing
6. **Take notes** during your setup process
7. **Save your setup scripts** for future use

---

## 📞 Support Contact

For technical issues with setup (not challenge hints):
- **Email:** [CTF Admin Email]
- **Discord:** [CTF Discord Server]
- **Platform:** [CTF Platform Support]

**Important:** Do not ask for challenge solutions. Use the hint system during the competition.

---

**Good luck with your setup, and see you at the competition! 🏆**

---

**Document Version:** 1.0  
**Last Updated:** November 13, 2025  
**Challenge Author:** kavix  
**Event:** MEDUSA 2.0
