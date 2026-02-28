import 'dart:convert';

import 'package:http/http.dart' as http;

import '../models/user_models.dart';

class ApiException implements Exception {
  ApiException({required this.statusCode, required this.message, this.code});

  final int statusCode;
  final String message;
  final String? code;

  @override
  String toString() => 'ApiException($statusCode, $code, $message)';
}

class UserApiClient {
  UserApiClient({required this.baseUrl, http.Client? client})
    : _client = client ?? http.Client();

  final String baseUrl;
  final http.Client _client;

  Uri _uri(String path) => Uri.parse('$baseUrl$path');

  Future<List<RecommendationCard>> generateRecommendations(
    GenerateRecommendationRequest request,
  ) async {
    final response = await _client.post(
      _uri('/recommendations/generate'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(request.toJson()),
    );

    final json = _decodeJson(response.body);
    if (response.statusCode != 200) {
      throw _toApiException(response.statusCode, json);
    }

    final parsed = RecommendationListResponse.fromJson(_requireMap(json));
    return parsed.data.cards;
  }

  Future<RecommendationDetail> getRecommendationDetail(String recommendationId) async {
    final response = await _client.get(_uri('/recommendations/$recommendationId'));
    final json = _decodeJson(response.body);

    if (response.statusCode != 200) {
      throw _toApiException(response.statusCode, json);
    }

    final parsed = RecommendationDetailResponse.fromJson(_requireMap(json));
    return parsed.data;
  }

  Future<void> createEvent(CreateEventRequest request) async {
    final response = await _client.post(
      _uri('/events'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(request.toJson()),
    );

    final json = _decodeJson(response.body);
    if (response.statusCode != 201) {
      throw _toApiException(response.statusCode, json);
    }
  }

  dynamic _decodeJson(String body) {
    if (body.trim().isEmpty) {
      return <String, dynamic>{};
    }
    return jsonDecode(body);
  }

  Map<String, dynamic> _requireMap(dynamic value) {
    if (value is Map<String, dynamic>) {
      return value;
    }
    throw ApiException(statusCode: 500, message: 'Invalid JSON response shape');
  }

  ApiException _toApiException(int statusCode, dynamic json) {
    final asMap = json is Map<String, dynamic> ? json : <String, dynamic>{};
    final error = asMap['error'] as Map<String, dynamic>?;
    return ApiException(
      statusCode: statusCode,
      code: error?['code']?.toString(),
      message: error?['message']?.toString() ?? 'Request failed',
    );
  }
}