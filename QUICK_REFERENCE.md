# MEDUSA CTF 2.0 - Quick Reference

## Valid Credentials
```
Username: admin
Password: medusa2024
```

## Expected Flag
```
MEDUSA{round_2_task_is_comp}
```

## How to Run
```bash
cd perseus
flutter pub get
flutter run
```

## How to Build APK
```bash
flutter build apk --release
```
The APK will be located at: `build/app/outputs/flutter-apk/app-release.apk`

## Verification

### Test Database
```bash
sqlite3 assets/medusa.db "SELECT * FROM credentials;"
```
Expected output: `1|admin|medusa2024`

### Test Flag Decryption
```bash
python3 << 'EOF'
import hashlib
key = hashlib.sha256(b'adminmedusa2024').digest()
encrypted = [0xfd, 0xd7, 0x6d, 0xbc, 0xaf, 0x0c, 0x9e, 0xd5, 0x89, 0xc3, 0x87, 0x26, 0x9c, 0xa2, 0x64, 0x15, 0x8a, 0x28, 0xf2, 0xa5, 0x88, 0x78, 0xf7, 0x8e, 0xd1, 0xd7, 0x82, 0x93]
decrypted = bytes([encrypted[i] ^ key[i] for i in range(len(encrypted))])
print(decrypted.decode())
EOF
```
Expected output: `MEDUSA{round_2_task_is_comp}`

## Project Structure
```
perseus/
├── assets/
│   ├── images/
│   │   └── logo 1 - white.png
│   └── medusa.db
├── lib/
│   ├── main.dart
│   └── database_helper.dart
├── pubspec.yaml
└── IMPLEMENTATION_GUIDE.md
```

## Features Checklist
- [x] SQLite database with credentials
- [x] XOR encryption with SHA-256 key
- [x] Login page with validation
- [x] Flag display page
- [x] Story page with mythology
- [x] Animations and effects
- [x] Haptic feedback
- [x] Immersive UI mode
- [x] Page transitions
- [x] Error handling
