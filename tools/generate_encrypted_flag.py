#!/usr/bin/env python3
"""
MEDUSA CTF - Flag Encryption Generator
This script generates the encrypted flag bytes for database_helper.dart
"""

import hashlib

def generate_encrypted_flag(username, password, plaintext_flag):
    """
    Generates encrypted flag bytes using XOR cipher with SHA-256 key.
    
    Args:
        username: The username credential
        password: The password credential
        plaintext_flag: The flag to encrypt (e.g., "MEDUSA{your_flag_here}")
    
    Returns:
        List of encrypted bytes as hex values
    """
    # Generate SHA-256 key from username + password
    key = hashlib.sha256((username + password).encode('utf-8')).digest()
    
    # Convert flag to bytes
    flag_bytes = plaintext_flag.encode('utf-8')
    
    # XOR encrypt each byte
    encrypted = []
    for i in range(len(flag_bytes)):
        encrypted.append(flag_bytes[i] ^ key[i % len(key)])
    
    return encrypted


def print_dart_format(encrypted):
    """Print encrypted bytes in Dart list format"""
    print("\nCopy this into database_helper.dart:")
    print("=" * 60)
    print("final List<int> encryptedFlag = [")
    
    # Print in rows of 10 for readability
    for i in range(0, len(encrypted), 10):
        chunk = encrypted[i:i+10]
        hex_values = ', '.join(f'0x{b:02x}' for b in chunk)
        print(f'  {hex_values},')
    
    print("];")
    print("=" * 60)


def verify_decryption(username, password, encrypted):
    """Verify the encryption works by decrypting"""
    key = hashlib.sha256((username + password).encode('utf-8')).digest()
    
    decrypted = []
    for i in range(len(encrypted)):
        decrypted.append(encrypted[i] ^ key[i % len(key)])
    
    return bytes(decrypted).decode('utf-8')


def main():
    print("=" * 60)
    print("MEDUSA CTF - Flag Encryption Generator")
    print("=" * 60)
    
    # Get user input
    print("\nEnter credentials and flag:")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    plaintext_flag = input("Plaintext Flag: ").strip()
    
    # Generate encrypted flag
    encrypted = generate_encrypted_flag(username, password, plaintext_flag)
    
    # Print in Dart format
    print_dart_format(encrypted)
    
    # Verify
    decrypted = verify_decryption(username, password, encrypted)
    print(f"\nVerification:")
    print(f"  Original:  {plaintext_flag}")
    print(f"  Decrypted: {decrypted}")
    print(f"  Match: {'✓ YES' if decrypted == plaintext_flag else '✗ NO'}")
    print()


if __name__ == "__main__":
    main()
