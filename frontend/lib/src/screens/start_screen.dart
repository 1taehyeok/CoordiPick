import 'package:flutter/material.dart';

import '../api/user_api_client.dart';
import '../models/user_models.dart';
import 'recommendation_grid_screen.dart';

class StartScreen extends StatefulWidget {
  const StartScreen({super.key});

  @override
  State<StartScreen> createState() => _StartScreenState();
}

class _StartScreenState extends State<StartScreen> {
  final _baseUrlController = TextEditingController(text: 'http://localhost:8000/api/v1');
  final _sessionController = TextEditingController(
    text: 'session_${DateTime.now().millisecondsSinceEpoch}',
  );
  final _moodController = TextEditingController();
  final _tempController = TextEditingController(text: '20');

  Gender _gender = Gender.unisex;
  Tpo _tpo = Tpo.daily;
  bool _isLoading = false;
  String? _error;

  @override
  void dispose() {
    _baseUrlController.dispose();
    _sessionController.dispose();
    _moodController.dispose();
    _tempController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    final temperature = double.tryParse(_tempController.text.trim());
    if (temperature == null) {
      setState(() => _error = 'temperature_c must be a number.');
      return;
    }

    final baseUrl = _baseUrlController.text.trim();
    final sessionId = _sessionController.text.trim();
    if (baseUrl.isEmpty || sessionId.isEmpty) {
      setState(() => _error = 'base URL and session_id are required.');
      return;
    }

    setState(() {
      _isLoading = true;
      _error = null;
    });

    final client = UserApiClient(baseUrl: baseUrl);
    try {
      final cards = await client.generateRecommendations(
        GenerateRecommendationRequest(
          sessionId: sessionId,
          gender: _gender,
          tpo: _tpo,
          mood: _moodController.text.trim(),
          temperatureC: temperature,
        ),
      );

      for (final card in cards) {
        await client.createEvent(
          CreateEventRequest(
            sessionId: sessionId,
            eventType: EventType.impression,
            recommendationId: card.recommendationId,
          ),
        );
      }

      if (!mounted) return;
      await Navigator.of(context).push(
        MaterialPageRoute(
          builder: (_) => RecommendationGridScreen(
            client: client,
            sessionId: sessionId,
            cards: cards,
          ),
        ),
      );
    } catch (e) {
      setState(() => _error = e.toString());
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
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
            controller: _sessionController,
            decoration: const InputDecoration(labelText: 'session_id'),
          ),
          const SizedBox(height: 12),
          DropdownButtonFormField<Gender>(
            value: _gender,
            decoration: const InputDecoration(labelText: 'gender'),
            items: Gender.values
                .map((g) => DropdownMenuItem(value: g, child: Text(g.name)))
                .toList(),
            onChanged: (value) {
              if (value != null) setState(() => _gender = value);
            },
          ),
          const SizedBox(height: 12),
          DropdownButtonFormField<Tpo>(
            value: _tpo,
            decoration: const InputDecoration(labelText: 'tpo'),
            items: Tpo.values.map((t) => DropdownMenuItem(value: t, child: Text(t.name))).toList(),
            onChanged: (value) {
              if (value != null) setState(() => _tpo = value);
            },
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _moodController,
            decoration: const InputDecoration(labelText: 'mood (optional)'),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _tempController,
            keyboardType: const TextInputType.numberWithOptions(decimal: true),
            decoration: const InputDecoration(labelText: 'temperature_c'),
          ),
          const SizedBox(height: 20),
          FilledButton(
            onPressed: _isLoading ? null : _submit,
            child: _isLoading
                ? const SizedBox(
                    width: 18,
                    height: 18,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : const Text('Generate 6 Recommendations'),
          ),
          if (_error != null) ...[
            const SizedBox(height: 12),
            Text(_error!, style: TextStyle(color: Theme.of(context).colorScheme.error)),
          ],
        ],
      ),
    );
  }
}