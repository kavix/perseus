# MEDUSA CTF 2.0 - Android Exploitation Challenge
## Implementation Guide

### Project Overview
**Description:** Android Exploitation for MEDUSA 2.0 by kavix

This is a complete Flutter application implementing a CTF (Capture The Flag) challenge with the following features:
- Secure login system with SQLite database
- XOR encryption with SHA-256 key derivation
- Beautiful UI with animations and effects
- Immersive full-screen experience

---

## Project Structure

```
perseus/
├── assets/
│   ├── images/
│   │   └── logo 1 - white.png     # Application logo (placeholder)
│   └── medusa.db                  # SQLite database with credentials
├── lib/
│   ├── main.dart                  # Main app with UI components
│   └── database_helper.dart       # Database and encryption logic
└── pubspec.yaml                   # Dependencies and asset declarations
```

---

## Implementation Details

### 1. Dependencies (pubspec.yaml)
```yaml
dependencies:
  flutter:
    sdk: flutter
  sqflite: ^2.3.0
  path_provider: ^2.1.1
  path: ^1.8.3
  crypto: ^3.0.3
  cupertino_icons: ^1.0.8

flutter:
  uses-material-design: true
  assets:
    - assets/images/
    - assets/medusa.db
```

### 2. Database (assets/medusa.db)

**Schema:**
```sql
CREATE TABLE credentials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
```

**Data:**
- Username: `admin`
- Password: `medusa2024`

### 3. Encryption System

**Algorithm:** XOR cipher with SHA-256 key derivation

**Process:**
1. Key Generation: `SHA256(username + password)`
2. Plaintext Flag: `MEDUSA{round_2_task_is_comp}`
3. Encryption: Each byte of plaintext XOR with corresponding key byte
4. Encrypted Flag (hex):
   ```
   [0xfd, 0xd7, 0x6d, 0xbc, 0xaf, 0x0c, 0x9e, 0xd5, 0x89, 0xc3,
    0x87, 0x26, 0x9c, 0xa2, 0x64, 0x15, 0x8a, 0x28, 0xf2, 0xa5,
    0x88, 0x78, 0xf7, 0x8e, 0xd1, 0xd7, 0x82, 0x93]
   ```

### 4. Database Helper (lib/database_helper.dart)

**Features:**
- Singleton pattern for database access
- Automatic database initialization from assets
- Credential verification
- Flag decryption logic

**Key Methods:**
- `_initDB()`: Copies database from assets to app directory
- `verifyCredentials(username, password)`: Authenticates user
- `_decryptFlag(username, password)`: Decrypts flag using XOR

### 5. UI Components (lib/main.dart)

#### Main App Configuration
- **Theme:** Dark theme with neon green accent (`#39FF14`)
- **System UI:** Immersive full-screen mode
- **Status Bar:** Transparent

#### Login Page
**Features:**
- Gradient background (`#0F172A` → `#1E293B` → `#334155`)
- Animated glowing logo
- Form validation
- Shake animation on error
- Loading state indicator
- Haptic feedback

**Layout:**
- Logo with pulsing glow effect
- Title: "The Gorgon's Challenge"
- Mythology text with link to Story Page
- Username and password fields (neon green styling)
- Animated submit button

#### Flag Page
**Features:**
- Success animation with checkmark
- Flag display in monospace font
- Slide + fade transition from login
- Back button to return to login

**Animations:**
- Scale animation for checkmark (elastic curve)
- Fade-in for content
- Glowing effects

#### Story Page
**Features:**
- Full mythology text about Medusa
- Scrollable content
- Back button
- CTF credit information

---

## Authentication Flow

1. User enters username and password
2. Form validation triggered
3. If valid:
   - Show loading indicator
   - Query database for credentials
   - If match found:
     - Generate SHA-256 key from `username + password`
     - XOR decrypt the flag
     - Trigger success haptic feedback
     - Navigate to Flag Page with 500ms slide/fade transition
   - If no match:
     - Trigger vibration haptic feedback
     - Show error message
     - Shake form fields
4. Reset loading state

---

## Running the Application

### Prerequisites
- Flutter SDK installed
- Android Studio or VS Code with Flutter extensions
- Android emulator or physical device

### Commands

```bash
# Navigate to project directory
cd perseus

# Get dependencies
flutter pub get

# Analyze code
flutter analyze

# Run on connected device/emulator
flutter run

# Build APK
flutter build apk

# Build release APK
flutter build apk --release
```

---

## Testing Credentials

**Valid Login:**
- Username: `admin`
- Password: `medusa2024`
- Expected Flag: `MEDUSA{round_2_task_is_comp}`

**Invalid Login:**
- Any other combination will trigger error state

---

## Key Features Implemented

✅ **Database:**
- SQLite database with credentials table
- Singleton pattern database helper
- Asset-to-app database copying

✅ **Encryption:**
- XOR cipher with SHA-256 key derivation
- Correct encrypted flag bytes
- Verified decryption logic

✅ **UI/UX:**
- Immersive full-screen mode
- Dark theme with neon green accents
- Gradient backgrounds
- Logo with animated glow effect
- Form validation with shake animation
- Loading states
- Error handling with animations
- Haptic feedback (vibration on error, impact on success)

✅ **Navigation:**
- PageRouteBuilder with custom transitions
- Slide + fade transition (500ms)
- Proper back navigation

✅ **Pages:**
- Login Page (with mythology text and story link)
- Flag Page (with success animation)
- Story Page (with full Medusa legend)

✅ **Code Quality:**
- Proper controller disposal
- Memory leak prevention
- Well-structured code
- Animation controllers properly managed

---

## File Checksums

To verify the database was created correctly:
```bash
sqlite3 assets/medusa.db "SELECT * FROM credentials;"
# Should output: 1|admin|medusa2024
```

To verify flag decryption:
```bash
python3 -c "
import hashlib
key = hashlib.sha256(b'adminmedusa2024').digest()
encrypted = [0xfd, 0xd7, 0x6d, 0xbc, 0xaf, 0x0c, 0x9e, 0xd5, 0x89, 0xc3, 0x87, 0x26, 0x9c, 0xa2, 0x64, 0x15, 0x8a, 0x28, 0xf2, 0xa5, 0x88, 0x78, 0xf7, 0x8e, 0xd1, 0xd7, 0x82, 0x93]
decrypted = bytes([encrypted[i] ^ key[i] for i in range(len(encrypted))])
print(decrypted.decode())
"
# Should output: MEDUSA{round_2_task_is_comp}
```

---

## Notes

1. **Logo Image:** A placeholder white PNG logo has been created. You can replace `assets/images/logo 1 - white.png` with your custom logo.

2. **Description Update:** To update the project description, modify the `description` field in `pubspec.yaml`:
   ```yaml
   description: "Android Exploitation for MEDUSA 2.0 by kavix"
   ```

3. **Encrypted Flag:** The encrypted flag bytes have been correctly calculated and verified to decrypt to `MEDUSA{round_2_task_is_comp}` when using credentials `admin/medusa2024`.

4. **Deprecation Warnings:** Some warnings about `withOpacity` are present due to Flutter SDK changes. These are informational and don't affect functionality.

---

## Security Notes

⚠️ **Educational Purpose Only**

This is a CTF challenge application. In production:
- Never store plaintext passwords in databases
- Use proper password hashing (bcrypt, argon2)
- Never hardcode encryption keys
- Use stronger encryption algorithms
- Implement proper authentication mechanisms

---

## Author
Created for MEDUSA CTF 2.0 by kavix

## License
Educational/CTF Challenge Use
