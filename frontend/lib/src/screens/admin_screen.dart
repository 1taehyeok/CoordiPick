import 'dart:convert';

import 'package:flutter/material.dart';

import '../api/admin_api_client.dart';

class AdminScreen extends StatefulWidget {
  const AdminScreen({super.key});

  @override
  State<AdminScreen> createState() => _AdminScreenState();
}

class _AdminScreenState extends State<AdminScreen> {
  final _baseUrlController = TextEditingController(text: 'http://localhost:8000/api/v1');
  final _tokenController = TextEditingController();

  bool _isLoading = false;
  String? _error;
  String _result = 'No data loaded.';

  @override
  void dispose() {
    _baseUrlController.dispose();
    _tokenController.dispose();
    super.dispose();
  }

  Future<void> _call(Future<dynamic> Function(AdminApiClient client) action) async {
    final baseUrl = _baseUrlController.text.trim();
    final token = _tokenController.text.trim();
    if (baseUrl.isEmpty || token.isEmpty) {
      setState(() => _error = 'base URL and bearer token are required.');
      return;
    }

    setState(() {
      _isLoading = true;
      _error = null;
    });

    final client = AdminApiClient(baseUrl: baseUrl, bearerToken: token);

    try {
      final data = await action(client);
      const encoder = JsonEncoder.withIndent('  ');
      setState(() => _result = encoder.convert(data));
    } catch (e) {
      setState(() => _error = e.toString());
    } finally {
      setState(() => _isLoading = false);
    }
  }

  Widget _button(String label, Future<dynamic> Function(AdminApiClient client) action) {
    return FilledButton.tonal(
      onPressed: _isLoading ? null : () => _call(action),
      child: Text(label),
    );
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          TextField(
            controller: _baseUrlController,
            decoration: const InputDecoration(labelText: 'Base URL (/api/v1)'),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _tokenController,
            decoration: const InputDecoration(labelText: 'Bearer JWT'),
            obscureText: true,
          ),
          const SizedBox(height: 16),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              _button('Dashboard Summary', (c) => c.getDashboardSummary()),
              _button('Dashboard Top3', (c) => c.getDashboardTop3()),
              _button('Dashboard TPO Ratio', (c) => c.getDashboardTpoRatio()),
              _button('Dashboard Low Stock', (c) => c.getDashboardLowStock()),
              _button('List Items', (c) => c.listItems()),
              _button('List Outfits', (c) => c.listOutfits()),
              _button('Store Settings', (c) => c.getStoreSettings()),
            ],
          ),
          const SizedBox(height: 16),
          if (_isLoading) const LinearProgressIndicator(),
          if (_error != null) ...[
            const SizedBox(height: 8),
            Text(_error!, style: TextStyle(color: Theme.of(context).colorScheme.error)),
          ],
          const SizedBox(height: 8),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              border: Border.all(color: Theme.of(context).dividerColor),
              borderRadius: BorderRadius.circular(8),
            ),
            child: SelectableText(_result),
          ),
        ],
      ),
    );
  }
}