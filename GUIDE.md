# Perseus CTF Challenge - Solver Guide

flutter build apk --debug

## Challenge Overview
**Perseus** is an Android CTF challenge that combines multiple techniques:
- Android app reverse engineering
- SQLite database forensics
- Cryptographic analysis (XOR encryption)
- ADB shell exploration
- Base64 decoding

## Challenge Structure

### 📱 Application Components

1. **Login System**: Requires valid credentials from SQLite database
2. **Encrypted Flag**: Flag is encrypted with XOR using SHA-256(username + password)
3. **Hidden Database**: SQLite DB stored in obfuscated location
4. **Event Information**: Base64-encoded data in SharedPreferences

---

## Solution Walkthrough

### Method 1: Database Extraction (Recommended)

#### Step 1: Install ADB and Connect Device
```bash
# Check connected devices
adb devices

# Install the APK
adb install perseus.apk
```

#### Step 2: Locate the Database
The database is intentionally hidden in a fake Google Analytics path.

```bash
# Connect to device shell
adb shell

# Navigate to external storage
cd /storage/emulated/0/Android/data/com.example.perseus/files

# Find all databases
find . -name "*.db"
```

**Expected path:**
```
/storage/emulated/0/Android/data/com.example.perseus/files/logs/com.ecsc-uok.medusa.kavix/config.db
```

#### Step 3: Extract the Database
```bash
# From your computer (not in adb shell)
adb pull /storage/emulated/0/Android/data/com.example.perseus/files/logs/com.ecsc-uok.medusa.kavix/config.db

# Alternative: if you have root access
adb shell
su
cat /storage/emulated/0/Android/data/com.example.perseus/files/logs/com.ecsc-uok.medusa.kavix/config.db > /sdcard/config.db
exit
adb pull /sdcard/config.db
```

#### Step 4: Analyze the Database
```bash
# Open with SQLite
sqlite3 config.db

# List tables
.tables

# View credentials table
SELECT * FROM credentials;
```

**Expected output:**
```
id | username | password
---|----------|-------------
1  | zeus     | olympus_2024
```

#### Step 5: Extract the Flag

The flag is encrypted in the source code. You need to:

1. **Find the encrypted flag bytes** (in `database_helper.dart`):
```dart
final List<int> encryptedFlag = [
    0xcf, 0xfc, 0xa8, 0xab, 0xda, 0xa7, 0x12, 0xd4, 0xbc, 0xe8,
    0x47, 0xdd, 0x3d, 0x6d, 0x70, 0xb5, 0xb5, 0xae, 0xe3, 0x21,
    0xc5, 0x73, 0x60, 0xe0, 0x05, 0x44, 0x1a, 0x52, 0x5b, 0x42,
    0xf6, 0x17, 0xec, 0xca, 0x91,
];
```

2. **Decrypt using Python**:
```python
import hashlib

username = "zeus"
password = "olympus_2024"

# Generate SHA-256 key
key = hashlib.sha256((username + password).encode()).digest()

# Encrypted flag
encrypted = [
    0xcf, 0xfc, 0xa8, 0xab, 0xda, 0xa7, 0x12, 0xd4, 0xbc, 0xe8,
    0x47, 0xdd, 0x3d, 0x6d, 0x70, 0xb5, 0xb5, 0xae, 0xe3, 0x21,
    0xc5, 0x73, 0x60, 0xe0, 0x05, 0x44, 0x1a, 0x52, 0x5b, 0x42,
    0xf6, 0x17, 0xec, 0xca, 0x91,
]

# XOR decrypt
decrypted = []
for i, byte in enumerate(encrypted):
    decrypted.append(byte ^ key[i % len(key)])

flag = bytes(decrypted).decode('utf-8')
print(f"Flag: {flag}")
```

---

### Method 2: APK Decompilation

#### Step 1: Verify APK Signature (Optional)
```bash
# View APK certificate information
keytool -printcert -jarfile perseus.apk

# Or use apksigner (part of Android SDK build-tools)
apksigner verify --print-certs perseus.apk

# Check if APK is signed
jarsigner -verify -verbose -certs perseus.apk
```

#### Step 2: Decompile the APK
```bash
# Using apktool
apktool d perseus.apk -o perseus_decompiled

# Using jadx (for Java/Kotlin code)
jadx perseus.apk -d perseus_jadx
```

#### Step 3: Inspect APK Metadata
```bash
# Using aapt (Android Asset Packaging Tool)
aapt dump badging perseus.apk | grep -E "package:|sdkVersion:|targetSdk"

# List all files in APK
aapt list -v perseus.apk

# Extract specific file from APK
unzip perseus.apk assets/config.enc
```

#### Step 4: Extract Encrypted Database
The database is stored as `assets/config.enc` (encrypted).

```bash
cd perseus_decompiled/assets
ls -la
# You'll find config.enc
```

#### Step 5: Decrypt the Database
Look for the decryption key in the source code (`database_helper.dart`):

```python
def decrypt_database(encrypted_file, output_file, key):
    with open(encrypted_file, 'rb') as f:
        encrypted = f.read()
    
    key_bytes = key.encode('utf-8')
    decrypted = bytearray()
    
    for i, byte in enumerate(encrypted):
        decrypted.append(byte ^ key_bytes[i % len(key_bytes)])
    
    with open(output_file, 'wb') as f:
        f.write(decrypted)

# Key from source code
KEY = 'medusa_ctf_2024_key'
decrypt_database('config.enc', 'config.db', KEY)
```

#### Step 6: Query the Database
```bash
sqlite3 config.db "SELECT * FROM credentials;"
```

---

### Method 4: Make APK Debuggable (Advanced)

If you need to use `run-as` to access internal app data but only have the release APK, you can modify it to be debuggable.

#### Step 1: Decompile the APK
```bash
apktool d perseus.apk -o perseus_modified
```

#### Step 2: Modify AndroidManifest.xml
```bash
cd perseus_modified
nano AndroidManifest.xml

# Add android:debuggable="true" to the <application> tag
# Change from:
<application android:label="perseus" ...>

# To:
<application android:debuggable="true" android:label="perseus" ...>
```

#### Step 3: Rebuild the APK
```bash
cd ..
apktool b perseus_modified -o perseus-debug.apk
```

#### Step 4: Sign the APK
```bash
# Generate a keystore (first time only)
keytool -genkey -v -keystore debug.keystore -alias debugkey \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -storepass android -keypass android \
  -dname "CN=Debug,O=CTF,C=US"

# Sign the APK
apksigner sign --ks debug.keystore \
  --ks-key-alias debugkey \
  --ks-pass pass:android \
  --key-pass pass:android \
  --out perseus-debug-signed.apk \
  perseus-debug.apk

# Or use jarsigner (older method)
jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 \
  -keystore debug.keystore \
  -storepass android \
  perseus-debug.apk debugkey

# Verify signature
apksigner verify perseus-debug-signed.apk
```

#### Step 5: Install and Use
```bash
# Uninstall original app first
adb uninstall com.example.perseus

# Install modified app
adb install perseus-debug-signed.apk

# Now run-as will work
adb shell
run-as com.example.perseus
cd /data/data/com.example.perseus
ls -la
cat shared_prefs/FlutterSharedPreferences.xml
```

**Note:** This method allows access to `/data/data/` without root, but requires understanding of APK modification and signing.

---

## Method 5: Runtime Manipulation with Frida

#### Step 1: Hook Database Operations
```javascript
Java.perform(function() {
    var DatabaseHelper = Java.use('com.example.perseus.DatabaseHelper');
    
    DatabaseHelper.verifyCredentials.implementation = function(username, password) {
        console.log('[+] verifyCredentials called');
        console.log('    Username: ' + username);
        console.log('    Password: ' + password);
        
        var result = this.verifyCredentials(username, password);
        if (result != null) {
            console.log('    Flag: ' + result.get('flag'));
        }
        return result;
    };
});
```

#### Step 2: Hook File Operations
```javascript
Java.perform(function() {
    var File = Java.use('java.io.File');
    
    File.$init.overload('java.lang.String').implementation = function(path) {
        if (path.includes('.db') || path.includes('config')) {
            console.log('[+] File created: ' + path);
        }
        return this.$init(path);
    };
});
```

---

### Bonus: SharedPreferences Data

The app also stores event information in SharedPreferences (Base64 encoded).

#### Location:
```
/data/data/com.example.perseus/shared_prefs/FlutterSharedPreferences.xml
```

#### Extract and Decode:
```bash
# With root
adb shell
su
cat /data/data/com.example.perseus/shared_prefs/FlutterSharedPreferences.xml

# Decode the values
echo "RGhhcm1hbG9rYSBIYWxsLCBVbml2ZXJzaXR5IG9mIEtlbGFuaXlh" | base64 -d
# Output: Dharmaloka Hall, University of Kelaniya

echo "RGVjZW1iZXIgLSAwNiBTYXR1cmRheQ==" | base64 -d
# Output: December - 06 Saturday

echo "ODowMCBBTSBPbndhcmQ=" | base64 -d
# Output: 8:00 AM Onward
```

---

## Key Learning Points

### 1. **External vs Internal Storage**
- Internal: `/data/data/com.example.perseus/` (requires root)
- External: `/storage/emulated/0/Android/data/com.example.perseus/` (accessible without root)

### 2. **Obfuscation Techniques**
- Fake directory names (`com.google.analytics.sdk`)
- Encrypted assets (`config.enc` instead of `config.db`)
- XOR encryption for flag

### 3. **Android Forensics Tools**
- `adb shell` - file exploration
- `sqlite3` - database analysis
- `apktool` - APK decompilation
- `jadx` - Java/Kotlin decompilation
- `frida` - dynamic instrumentation

### 4. **Cryptography**
- XOR encryption (reversible)
- SHA-256 hashing
- Base64 encoding

---

## Tools Required

### Essential Tools
- **ADB (Android Debug Bridge)**: Device interaction
- **SQLite3**: Database analysis
- **Python 3**: Decryption scripts
- **Base64**: Decode encoded strings

### APK Analysis Tools
- **apktool**: APK decompilation and rebuild
  ```bash
  # macOS
  brew install apktool
  
  # Linux
  sudo apt-get install apktool
  
  # Usage
  apktool d app.apk -o output_folder
  ```

- **jadx**: Dex to Java decompiler
  ```bash
  # macOS
  brew install jadx
  
  # Download from: https://github.com/skylot/jadx/releases
  
  # Usage
  jadx app.apk -d output_folder
  jadx-gui app.apk  # GUI version
  ```

- **keytool**: Java keystore and certificate tool (comes with JDK)
  ```bash
  # View APK signature
  keytool -printcert -jarfile app.apk
  
  # List keystore contents
  keytool -list -v -keystore keystore.jks
  ```

- **apksigner**: APK signing and verification (Android SDK build-tools)
  ```bash
  # Verify APK signature
  apksigner verify --print-certs app.apk
  
  # Check if APK is signed
  apksigner verify app.apk
  
  # Sign APK
  apksigner sign --ks keystore.jks app.apk
  ```

- **aapt / aapt2**: Android Asset Packaging Tool
  ```bash
  # Dump APK info
  aapt dump badging app.apk
  
  # List APK contents
  aapt list -v app.apk
  ```

- **jarsigner**: JAR signing and verification (comes with JDK)
  ```bash
  # Verify APK signature
  jarsigner -verify -verbose -certs app.apk
  ```

### Advanced Tools (Optional)
- **Frida**: Dynamic instrumentation
  ```bash
  pip3 install frida-tools
  ```

- **objection**: Frida-based mobile exploration toolkit
  ```bash
  pip3 install objection
  ```

- **MobSF**: Mobile Security Framework (automated analysis)
  - https://github.com/MobSF/Mobile-Security-Framework-MobSF

- **Bytecode Viewer**: All-in-one reverse engineering tool
  - https://github.com/Konloch/bytecode-viewer

---

## Common Pitfalls

1. ❌ Looking in `/data/data/` instead of `/storage/emulated/0/`
2. ❌ Trying to extract `config.db` from APK directly (it's encrypted as `config.enc`)
3. ❌ Not running the app first (database is created on first launch)
4. ❌ Incorrect XOR decryption key
5. ❌ Forgetting to Base64 decode SharedPreferences values

---

## Flag Format

```
MEDUSA{...}
```

The exact flag is obtained by:
1. Finding credentials: `zeus` / `olympus_2024`
2. Extracting encrypted flag bytes from source code
3. Decrypting with SHA-256(username + password) XOR operation

---

## Hints (Progressive)

**Level 1 (Free):**
- "Android apps can store data in multiple locations. Check both internal and external storage."
- "The app uses SQLite. Where do Android apps typically store databases?"

**Level 2 (50 points):**
- "Look in external storage, not `/data/data/`"
- "The database might be disguised with a misleading path name"

**Level 3 (100 points):**
- "Search for `.db` files in the app's external storage directory"
- "Try: `find /storage/emulated/0/Android/data/com.example.perseus -name '*.db'`"

**Level 4 (150 points):**
- "Path: `/storage/emulated/0/Android/data/com.example.perseus/files/logs/com.ecsc-uok.medusa.kavix/config.db`"
- "The flag is XOR encrypted with SHA-256(username + password)"

---

## Credits

**Challenge Name:** Perseus  
**Category:** Mobile / Android  
**Difficulty:** Medium  
**Author:** kavix  
**Event:** MEDUSA 2.0  

---

## Additional Resources

### Official Documentation
- [Android Debug Bridge (ADB) Documentation](https://developer.android.com/tools/adb)
- [apksigner Documentation](https://developer.android.com/tools/apksigner)
- [keytool Documentation](https://docs.oracle.com/javase/8/docs/technotes/tools/unix/keytool.html)
- [SQLite Tutorial](https://www.sqlitetutorial.net/)

### Reverse Engineering Tools
- [apktool](https://apktool.org/) - APK decompilation
- [jadx](https://github.com/skylot/jadx) - Dex to Java decompiler
- [Frida Dynamic Instrumentation](https://frida.re/)
- [objection](https://github.com/sensepost/objection) - Frida toolkit

### Learning Resources
- [APK Reverse Engineering Guide](https://github.com/ashishb/android-security-awesome)
- [OWASP Mobile Security Testing Guide](https://owasp.org/www-project-mobile-security-testing-guide/)
- [Android App Reverse Engineering 101](https://www.ragingrock.com/AndroidAppRE/)

### APK Analysis Cheat Sheets
```bash
# Quick APK Information
unzip -l app.apk                    # List files in APK
aapt dump badging app.apk           # Get app metadata
aapt dump permissions app.apk       # List permissions
keytool -printcert -jarfile app.apk # Certificate info
apksigner verify --print-certs app.apk # Verify signature

# Extract Assets
unzip app.apk -d extracted/         # Extract all
unzip app.apk assets/* -d assets/   # Extract assets only

# Decompile
apktool d app.apk                   # Decompile to smali
jadx app.apk                        # Decompile to Java

# Recompile (if needed)
apktool b app_folder -o new.apk     # Rebuild APK
apksigner sign --ks key.jks new.apk # Re-sign APK
```
