import 'package:shared_preferences/shared_preferences.dart';

class EventPrefs {
  // Keys for SharedPreferences
  static const String _venueKey = 'venue';
  static const String _dateKey = 'date';
  static const String _timeKey = 'time';
  static const String _hintKey = 'HINT';

  // Store event information
  static Future<void> saveEventInfo() async {
    final prefs = await SharedPreferences.getInstance();
    
    await prefs.setString(_venueKey, 'RGhhcm1hbG9rYSBIYWxsLCBVbml2ZXJzaXR5IG9mIEtlbGFuaXlh');
    await prefs.setString(_dateKey, 'RGVjZW1iZXIgLSAwNiBTYXR1cmRheQ==');
    await prefs.setString(_timeKey, 'ODowMCBBTSBPbndhcmQ=');
    await prefs.setString(_hintKey, 'IkZvY3VzIG9uIGV4dGVybmFsIHN0b3JhZ2UgcmF0aGVyIHRoYW4gaW50ZXJuYWwgYXBwIGRhdGEuIg==');
  }

  // Retrieve venue
  static Future<String?> getVenue() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_venueKey);
  }

  // Retrieve date
  static Future<String?> getDate() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_dateKey);
  }

  // Retrieve time
  static Future<String?> getTime() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_timeKey);
  }

  // Clear all event info
  static Future<void> clearEventInfo() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_venueKey);
    await prefs.remove(_dateKey);
    await prefs.remove(_timeKey);
  }

  // Check if event info exists
  static Future<bool> hasEventInfo() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.containsKey(_venueKey) && 
           prefs.containsKey(_dateKey) && 
           prefs.containsKey(_timeKey);
  }
}
