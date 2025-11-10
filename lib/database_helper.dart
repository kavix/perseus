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

  // Encrypted flag as specified
  final List<int> encryptedFlag = [
    0xfd, 0xd7, 0x6d, 0xbc, 0xaf, 0x0c, 0x9e, 0xd5, 0x89, 0xc3,
    0x87, 0x26, 0x9c, 0xa2, 0x64, 0x15, 0x8a, 0x28, 0xf2, 0xa5,
    0x88, 0x78, 0xf7, 0x8e, 0xd1, 0xd7, 0x82, 0x93,
  ];

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDB();
    return _database!;
  }

  Future<Database> _initDB() async {
    Directory documentsDirectory = await getApplicationDocumentsDirectory();
    String path = join(documentsDirectory.path, 'medusa.db');

    // Check if database exists
    bool exists = await databaseExists(path);

    if (!exists) {
      // Copy from assets
      try {
        await Directory(dirname(path)).create(recursive: true);
      } catch (_) {}

      // Load database from asset and copy
      ByteData data = await rootBundle.load('assets/medusa.db');
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

    // Convert bytes to string
    return utf8.decode(decrypted);
  }
}
