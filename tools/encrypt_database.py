#!/usr/bin/env python3
"""
Encrypt the config.db database for use in the Perseus CTF app.
This makes it harder to extract the database from the APK.
"""

def encrypt_database(input_file, output_file, key):
    """XOR encrypt a file with a repeating key."""
    with open(input_file, 'rb') as f:
        data = f.read()
    
    key_bytes = key.encode('utf-8')
    encrypted = bytearray()
    
    for i, byte in enumerate(data):
        encrypted.append(byte ^ key_bytes[i % len(key_bytes)])
    
    with open(output_file, 'wb') as f:
        f.write(encrypted)
    
    print(f"✓ Encrypted {input_file}")
    print(f"✓ Output: {output_file}")
    print(f"✓ Size: {len(encrypted)} bytes")

if __name__ == '__main__':
    # Same key as in database_helper.dart
    KEY = 'medusa_ctf_2024_key'
    
    INPUT = 'assets/config.db'
    OUTPUT = 'assets/config.enc'
    
    encrypt_database(INPUT, OUTPUT, KEY)
    print("\n✓ Done! Now you can delete assets/config.db")
    print("  The encrypted file config.enc will be used instead.")
