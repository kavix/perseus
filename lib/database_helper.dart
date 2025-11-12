import 'dart:io';
import 'package:flutter/services.dart';
import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';
import 'package:path_provider/path_provider.dart';
import 'package:crypto/crypto.dart';
import 'dart:convert';

class DatabaseHelper {
  DatabaseHelper._privateConstructor();
  static final DatabaseHelper instance = DatabaseHelper._privateConstructor();

  static Database? _database;

  // Encrypted flag for zeus / thund3r_b0lt
  // Decrypts to: MEDUSA{z3us_th3_thund3r_g0d_r31gns}
  final List<int> encryptedFlag = [
    0xcf, 0xfc, 0xa8, 0xab, 0xda, 0xa7, 0x12, 0xd4, 0xbc, 0xe8,
    0x47, 0xdd, 0x3d, 0x6d, 0x70, 0xb5, 0xb5, 0xae, 0xe3, 0x21,
    0xc5, 0x73, 0x60, 0xe0, 0x05, 0x44, 0x1a, 0x52, 0x5b, 0x42,
    0xf6, 0x17, 0xec, 0xca, 0x91,
  ];

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB();
    return _database!;
  }

  Future<Database> _initDB() async {
    // Use innocuous location and name to hide database
    String basePath = '/storage/emulated/0/Android/logs/com.google.analytics.sdk';
    String path = join(basePath, 'config.dat');

    // Check if database exists
    bool exists = await databaseExists(path);

    if (!exists) {
      // Copy from assets
      try {
        await Directory(dirname(path)).create(recursive: true);
      } catch (_) {}

      // Load database from asset and copy
      ByteData data = await rootBundle.load('assets/config.dat');
      List<int> bytes = data.buffer.asUint8List(data.offsetInBytes, data.lengthInBytes);

      // Write and flush the bytes written
      await File(path).writeAsBytes(bytes, flush: true);
    }

    // Open the database
    return await openDatabase(path, version: 1);
  }

  Future<Map<String, dynamic>?> verifyCredentials(String username, String password) async {
    final db = await database;
    
    // Query the database for matching credentials
    final List<Map<String, dynamic>> results = await db.query(
      'credentials',
      where: 'username = ? AND password = ?',
      whereArgs: [username, password],
    );

    if (results.isNotEmpty) {
      // Credentials are correct, decrypt the flag
      String decryptedFlag = _decryptFlag(username, password);
      return {'flag': decryptedFlag};
    }

    // Credentials are incorrect
    return null;
  }

  String _decryptFlag(String username, String password) {
    // Generate SHA-256 key from username + password
    var key = sha256.convert(utf8.encode(username + password));
    List<int> keyBytes = key.bytes;

    // XOR decrypt the flag
    List<int> decrypted = [];
    for (int i = 0; i < encryptedFlag.length; i++) {
      decrypted.add(encryptedFlag[i] ^ keyBytes[i % keyBytes.length]);
    }

    // Try to convert bytes to string
    try {
      return utf8.decode(decrypted);
    } catch (e) {
      // If decryption fails (wrong credentials), return hex representation
      return 'FakeFlag{${decrypted.map((b) => b.toRadixString(16).padLeft(2, '0')).join('')}}';
    }
  }
}
