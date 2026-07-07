# 🏛️ Perseus - Android CTF Challenge

[![License: Educational](https://img.shields.io/badge/License-Educational-blue.svg)](LICENSE)
[![Flutter](https://img.shields.io/badge/Built%20with-Flutter-02569B?logo=flutter)](https://flutter.dev)
[![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite)](https://www.sqlite.org)
[![Python](https://img.shields.io/badge/Scripts-Python3-3776AB?logo=python)](https://www.python.org)
[![Dart](https://img.shields.io/badge/Language-Dart-0175C2?logo=dart)](https://dart.dev)
[![Android](https://img.shields.io/badge/Platform-Android-3DDC84?logo=android)](https://www.android.com)

> A medium-difficulty Android exploitation and forensics CTF challenge for **MEDUSA 2.0** cybersecurity competition.

## 📱 Overview

**Perseus** is a comprehensive Android CTF challenge that tests participants' skills in mobile security, reverse engineering, cryptography, and digital forensics. Players must navigate the Android filesystem, extract hidden databases, decrypt encrypted data, and ultimately retrieve the flag.

### Challenge Details

| Attribute | Value |
|-----------|-------|
| **Category** | Mobile / Android Forensics |
| **Difficulty** | Medium |
| **Event** | MEDUSA 2.0 (University of Kelaniya) |
| **Author** | [@kavix](https://github.com/kavix) |
| **Platform** | Android 5.0+ (API 21+) |
| **APK Size** | ~20-25 MB |
| **Expected Time** | 1-4 hours (varies by skill level) |

---

## 🎯 Challenge Objectives

Players must complete the following tasks to solve the challenge:

1. ✅ **Install** the Perseus APK on an Android device/emulator
2. ✅ **Navigate** the Android filesystem using ADB
3. ✅ **Locate** the hidden SQLite database (obfuscated path)
4. ✅ **Extract** the database from the device
5. ✅ **Query** the database to find credentials
6. ✅ **Decrypt** the encrypted flag using cryptographic principles
7. ✅ **Submit** the flag in format: `MEDUSA{...}`

### Skills Tested

- Android Debug Bridge (ADB) proficiency
- Android filesystem navigation and forensics
- SQLite database analysis
- Cryptography (XOR cipher, SHA-256 hashing)
- APK reverse engineering
- Python scripting and cryptographic algorithms
- Problem-solving and persistence

---

## 🚀 Quick Start

### Prerequisites

- **ADB (Android Debug Bridge)** - Device/emulator interaction
- **Android Device or Emulator** - API 21+ (Android 5.0 Lollipop)
- **SQLite3** - Database analysis
- **Python 3** - Flag decryption scripts
- **Optional:** apktool, jadx for advanced analysis

### Installation

```bash
# 1. Install ADB (choose your OS)
# macOS
brew install android-platform-tools

# Linux (Debian/Ubuntu)
sudo apt-get install android-tools-adb

# Windows
# Download from https://developer.android.com/tools/releases/platform-tools

# 2. Verify installation
adb --version

# 3. Install the APK
adb install perseus.apk

# 4. Launch the app
adb shell am start -n com.example.perseus/.MainActivity
```

### Getting Started

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

## 📂 Project Structure

```
perseus/
├── assets/
│   ├── images/
│   │   └── logo 1 - white.png          # Application logo
│   └── config.enc                      # Encrypted SQLite database
│
├── lib/
│   ├── main.dart                       # Flutter UI & authentication
│   ├── database_helper.dart            # SQLite & encryption logic
│   └── event_prefs.dart                # SharedPreferences management
│
├── android/                            # Android native config
├── tools/                              # Build utilities
│
├── pubspec.yaml                        # Flutter dependencies
├── pubspec.lock                        # Dependency lock file
├── analysis_options.yaml               # Dart analysis config
│
├── CTF_PLAYER_GUIDE.md                # Player setup guide
├── GUIDE.md                           # Complete solver guide
├── IMPLEMENTATION_GUIDE.md            # Technical implementation
├── PREREQUISITES.md                   # Requirements & tools
├── HINTS.txt                          # Progressive hints
│
└── README.md                          # This file
```

---

## 🔐 Technical Architecture

### Database Schema

The SQLite database contains a `credentials` table:

```sql
CREATE TABLE credentials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

-- Test Data
INSERT INTO credentials (username, password) 
VALUES ('admin', 'medusa2024');
```

### Encryption System

**Algorithm:** XOR cipher with SHA-256 key derivation

```
1. Key Generation: SHA256(username + password)
2. Plaintext Flag: MEDUSA{round_2_task_is_comp}
3. Encryption: Each byte XOR with corresponding key byte
```

**Example Decryption (Python):**

```python
import hashlib

username = "admin"
password = "medusa2024"

# Generate SHA-256 key
key = hashlib.sha256((username + password).encode()).digest()

# Encrypted flag bytes
encrypted = [
    0xfd, 0xd7, 0x6d, 0xbc, 0xaf, 0x0c, 0x9e, 0xd5, 0x89, 0xc3,
    0x87, 0x26, 0x9c, 0xa2, 0x64, 0x15, 0x8a, 0x28, 0xf2, 0xa5,
    0x88, 0x78, 0xf7, 0x8e, 0xd1, 0xd7, 0x82, 0x93
]

# XOR decryption
decrypted = bytes([encrypted[i] ^ key[i % len(key)] for i in range(len(encrypted))])
flag = decrypted.decode('utf-8')

print(f"Flag: {flag}")  # Output: MEDUSA{round_2_task_is_comp}
```

### Application Components

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **UI Framework** | Flutter | Cross-platform Android app |
| **Database** | SQLite 3 | Credential storage |
| **Cryptography** | Dart crypto | XOR + SHA-256 |
| **Storage** | External + Internal | Database and preferences |
| **Animations** | Flutter Animations | Smooth UI effects |

---

## 📋 Solution Walkthrough

### Method 1: Database Extraction (Recommended)

```bash
# 1. Connect device and install APK
adb devices
adb install perseus.apk

# 2. Navigate to app storage
adb shell
cd /storage/emulated/0/Android/data/com.example.perseus/files
find . -name "*.db"

# Expected output:
# /storage/emulated/0/Android/data/com.example.perseus/files/logs/com.ecsc-uok.medusa.kavix/config.db

# 3. Extract database
adb pull /storage/emulated/0/Android/data/com.example.perseus/files/logs/com.ecsc-uok.medusa.kavix/config.db

# 4. Analyze database
sqlite3 config.db
sqlite> SELECT * FROM credentials;
# Output: 1|admin|medusa2024

# 5. Decrypt flag using Python script (see above)
```

### Method 2: APK Decompilation

```bash
# Decompile APK to extract source code
apktool d perseus.apk -o perseus_decompiled

# Or use jadx for Java decompilation
jadx perseus.apk -d perseus_jadx

# Find encrypted flag and decryption logic in:
# - lib/database_helper.dart
# - assets/config.enc
```

### Method 3: Runtime Manipulation (Advanced)

```bash
# Use Frida to hook database operations
pip3 install frida-tools

# Create Frida script to intercept credentials
# See GUIDE.md for complete Frida examples
```

---

## 💡 Key Features

### User Interface
- 🎨 **Dark Theme** with neon green accents (#39FF14)
- ✨ **Animated Glowing Logo** with pulsing effects
- 📝 **Form Validation** with error handling
- 🎯 **Shake Animation** on authentication failure
- ✅ **Success Page** with checkmark animation
- 📖 **Mythology Story Page** (Medusa legend)
- 📳 **Haptic Feedback** (vibration and success impacts)
- 🎬 **Page Transitions** with slide + fade animations
- 📱 **Immersive Full-Screen Mode**

### Backend Features
- 🔐 **SQLite Database Management** with singleton pattern
- 📦 **Asset-Based Database Initialization**
- 🔑 **XOR Encryption/Decryption Logic**
- 📲 **SharedPreferences Management**
- 🎭 **Event Data Storage** (Base64 encoded)

---

## 🛠️ Dependencies

**Flutter/Dart:**
```yaml
dependencies:
  flutter:
    sdk: flutter
  sqflite: ^2.3.0
  path_provider: ^2.1.1
  path: ^1.8.3
  crypto: ^3.0.3
  shared_preferences: ^2.2.2
  cupertino_icons: ^1.0.8
```

**Development:**
```yaml
dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^5.0.0
```

**System Requirements:**
- Flutter SDK 3.9.2+
- Dart 3.9.2+
- Android SDK API 21+ (target 34)
- Java JDK 11+

---

## 📚 Documentation

This repository includes comprehensive guides for both players and organizers:

| Document | Purpose | Audience |
|----------|---------|----------|
| **CTF_PLAYER_GUIDE.md** | Setup, tools, troubleshooting | Players |
| **GUIDE.md** | Complete solution walkthrough | Players (spoilers!) |
| **IMPLEMENTATION_GUIDE.md** | Architecture and implementation | Organizers/Developers |
| **PREREQUISITES.md** | Detailed requirements and setup | New players |
| **HINTS.txt** | Progressive hints system | Players |

---

## 🎮 Testing Credentials

**Valid Login:**
```
Username: admin
Password: medusa2024
Expected Flag: MEDUSA{round_2_task_is_comp}
```

**Invalid Login:**
Any other username/password combination will trigger an error state with shake animation.

---

## 📊 Challenge Difficulty Progression

| Skill Level | Estimated Time | Approach |
|------------|----------------|----------|
| **Beginner** | 2-4 hours | Follow guide, learn tools |
| **Intermediate** | 1-2 hours | Use hints, some exploration |
| **Advanced** | 30-60 minutes | Minimal guidance needed |
| **Expert** | <30 minutes | Multiple solution methods |

---

## 🔍 Common Pitfalls

❌ **Don't:**
- Try to brute force the flag
- Assume database is in APK assets (it's created at runtime)
- Skip launching the app (database created on first run)
- Only check `/data/data/` (external storage not accessible)
- Overlook hidden/obfuscated directory names

✅ **Do:**
- Explore filesystem thoroughly
- Check both internal and external storage
- Analyze database files with SQLite tools
- Look for encoded/encrypted data
- Read app source code if decompiling

---

## 🆘 Troubleshooting

### ADB Issues
```bash
# Device not detected
adb kill-server
adb start-server
adb devices

# Device unauthorized
# → Unlock device and tap "Allow" on authorization prompt

# Device offline
adb reconnect
```

### Installation Issues
```bash
# Insufficient storage
# → Free up at least 200MB on device

# Installation failed
# → Use: adb install -r perseus.apk (force reinstall)
```

### Database Not Found
```bash
# Database files created on first app launch
# → Launch app and attempt login before extracting

# Permission denied
# → Use adb pull (external storage is accessible without root)
```

---

## 📖 Learning Resources

### Android Development
- [Android Developer Documentation](https://developer.android.com)
- [Flutter Documentation](https://flutter.dev/docs)
- [ADB Command Reference](https://developer.android.com/tools/adb)

### Mobile Security
- [OWASP Mobile Security Testing Guide](https://owasp.org/www-project-mobile-security-testing-guide/)
- [Android Security Awesome List](https://github.com/ashishb/android-security-awesome)
- [Mobile Security Framework (MobSF)](https://github.com/MobSF/Mobile-Security-Framework-MobSF)

### Reverse Engineering Tools
- [apktool](https://apktool.org/) - APK decompilation
- [jadx](https://github.com/skylot/jadx) - Dex to Java decompiler
- [Frida](https://frida.re/) - Dynamic instrumentation framework
- [objection](https://github.com/sensepost/objection) - Frida-based mobile toolkit

### Cryptography
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Cryptography Basics](https://cryptography.io/)
- [XOR Cipher Explanation](https://en.wikipedia.org/wiki/XOR_cipher)

---

## 🏗️ Building & Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/kavix/perseus.git
cd perseus

# Get Flutter dependencies
flutter pub get

# Analyze code
flutter analyze

# Run on connected device
flutter run

# Build debug APK
flutter build apk --debug

# Build release APK
flutter build apk --release
```

### Useful Commands

```bash
# Check Flutter setup
flutter doctor

# Run tests
flutter test

# Format code
dart format lib/

# Clean build artifacts
flutter clean
```

---

## ⚠️ Security Disclaimer

**Educational Purpose Only**

This is a CTF challenge application designed for learning and competition. In production environments:

- ❌ Never store plaintext passwords in databases
- ❌ Never hardcode encryption keys in source code
- ❌ Use proper password hashing (bcrypt, argon2)
- ❌ Use industry-standard encryption (AES, TLS)
- ❌ Implement proper authentication mechanisms
- ❌ Follow OWASP Mobile Security guidelines

---

## 📝 License

This project is released for **educational and CTF competition use only**.

For any commercial or non-educational use, please contact the author.

---

## 👤 Author

**kavix** - [@kavix](https://github.com/kavix)

- 📧 Contact through GitHub
- 🌐 MEDUSA CTF 2.0 Organizer
- 🏆 Mobile Security Enthusiast

---

## 🤝 Contributing

This is a CTF challenge repository. Contributions are welcome for:

- Bug fixes and improvements
- Documentation enhancements
- Tool recommendations
- Additional solution methods
- Translations of guides

Please open an issue or pull request with your suggestions!

---

## 📞 Support & Issues

If you encounter technical issues (not related to solving the challenge):

1. **Check Troubleshooting Section** - Most issues covered above
2. **Review PREREQUISITES.md** - Verify all tools installed correctly
3. **Read CTF_PLAYER_GUIDE.md** - Step-by-step setup guide
4. **Open a GitHub Issue** - Report bugs and problems
5. **Contact Event Organizers** - Reach out through CTF platform

**Note:** Challenge hints should be requested through official hint system, not direct messages.

---

## 📊 Repository Statistics

```
Repository: kavix/perseus
Language Composition:
  • Dart: 42.7%    (Flutter application)
  • Python: 56.7%  (Documentation & scripts)
  • Other: 0.6%    (Configuration files)

Lines of Code:
  • Dart Application: ~2,000+ lines
  • Documentation: ~25,000+ words
  • Configuration: ~500+ lines

Created: November 2025
Last Updated: November 2025
Platform: Android 5.0+ (API 21+)
APK Size: 20-25 MB
```

---

## 🎓 Educational Value

This project serves as an excellent resource for learning

✅ Android app development with Flutter
✅ Mobile security and forensics
✅ Reverse engineering techniques
✅ Cryptographic implementations
✅ CTF challenge design and deployment
✅ Security best practices (anti-patterns)

---

## 🏁 Ready to Start?

1. **Install prerequisites** - Follow PREREQUISITES.md
2. **Read setup guide** - Check CTF_PLAYER_GUIDE.md
3. **Install APK** - Use adb install command
4. **Start exploring** - Navigate Android filesystem
5. **Solve challenge** - Extract and decrypt flag
6. **Submit solution** - MEDUSA{...}

**Good luck, and may Perseus guide your way! 🏛️**

---

**Made with ❤️ for the MEDUSA 2.0**

[Back to Top](#-perseus---android-ctf-challenge)