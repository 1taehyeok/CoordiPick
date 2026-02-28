import 'dart:convert';

import 'package:http/http.dart' as http;

import 'user_api_client.dart';

class AdminApiClient {
  AdminApiClient({required this.baseUrl, required this.bearerToken, http.Client? client})
    : _client = client ?? http.Client();

  final String baseUrl;
  final String bearerToken;
  final http.Client _client;

  Uri _uri(String path) => Uri.parse('$baseUrl$path');

  Map<String, String> get _headers => {
    'Authorization': 'Bearer $bearerToken',
    'Content-Type': 'application/json',
  };

  Future<dynamic> getDashboardSummary() => _get('/admin/dashboard/summary');

  Future<dynamic> getDashboardTop3() => _get('/admin/dashboard/top3');

  Future<dynamic> getDashboardTpoRatio() => _get('/admin/dashboard/tpo-ratio');

  Future<dynamic> getDashboardLowStock() => _get('/admin/dashboard/low-stock');

  Future<dynamic> listItems() => _get('/admin/items');

  Future<dynamic> listOutfits() => _get('/admin/outfits');

  Future<dynamic> getStoreSettings() => _get('/admin/store-settings');

  Future<dynamic> _get(String path) async {
    final response = await _client.get(_uri(path), headers: _headers);
    final decoded = response.body.trim().isEmpty ? <String, dynamic>{} : jsonDecode(response.body);

    if (response.statusCode < 200 || response.statusCode >= 300) {
      final asMap = decoded is Map<String, dynamic> ? decoded : <String, dynamic>{};
      final error = asMap['error'] as Map<String, dynamic>?;
      throw ApiException(
        statusCode: response.statusCode,
        code: error?['code']?.toString(),
        message: error?['message']?.toString() ?? 'Admin request failed',
      );
    }

    return decoded;
  }
}