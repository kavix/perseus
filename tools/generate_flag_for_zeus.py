#!/usr/bin/env python3
"""Generate encrypted flag for zeus/thund3r_b0lt"""

import hashlib

username = 'zeus'
password = 'thund3r_b0lt'
plaintext_flag = 'MEDUSA{z3us_th3_thund3r_g0d_r31gns}'

# Generate SHA-256 key
key = hashlib.sha256((username + password).encode('utf-8')).digest()

# Encrypt
flag_bytes = plaintext_flag.encode('utf-8')
encrypted = []
for i in range(len(flag_bytes)):
    encrypted.append(flag_bytes[i] ^ key[i % len(key)])

# Print in Dart format
print('Copy this into database_helper.dart:')
print('=' * 60)
print('final List<int> encryptedFlag = [')
for i in range(0, len(encrypted), 10):
    chunk = encrypted[i:i+10]
    hex_values = ', '.join(f'0x{b:02x}' for b in chunk)
    print(f'  {hex_values},')
print('];')
print('=' * 60)

# Verify
decrypted = []
for i in range(len(encrypted)):
    decrypted.append(encrypted[i] ^ key[i % len(key)])
result = bytes(decrypted).decode('utf-8')
print(f'\nVerified: {result}')
print(f'Username: {username}')
print(f'Password: {password}')
