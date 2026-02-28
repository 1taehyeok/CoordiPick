import 'package:flutter/material.dart';

import '../api/user_api_client.dart';
import '../models/user_models.dart';

class RecommendationDetailScreen extends StatefulWidget {
  const RecommendationDetailScreen({
    super.key,
    required this.client,
    required this.sessionId,
    required this.recommendationId,
  });

  final UserApiClient client;
  final String sessionId;
  final String recommendationId;

  @override
  State<RecommendationDetailScreen> createState() => _RecommendationDetailScreenState();
}

class _RecommendationDetailScreenState extends State<RecommendationDetailScreen> {
  RecommendationDetail? _detail;
  bool _isLoading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    try {
      final detail = await widget.client.getRecommendationDetail(widget.recommendationId);
      await widget.client.createEvent(
        CreateEventRequest(
          sessionId: widget.sessionId,
          eventType: EventType.detailView,
          recommendationId: widget.recommendationId,
        ),
      );

      if (!mounted) return;
      setState(() => _detail = detail);
    } catch (e) {
      if (!mounted) return;
      setState(() => _error = e.toString());
    } finally {
      if (mounted) {
        setState(() => _isLoading = false);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }

    if (_error != null) {
      return Scaffold(
        appBar: AppBar(title: const Text('Recommendation Detail')),
        body: Center(child: Text(_error!)),
      );
    }

    final detail = _detail;
    if (detail == null) {
      return Scaffold(
        appBar: AppBar(title: const Text('Recommendation Detail')),
        body: const Center(child: Text('No detail data.')),
      );
    }

    return Scaffold(
      appBar: AppBar(title: const Text('Recommendation Detail')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(detail.title, style: Theme.of(context).textTheme.headlineSmall),
          if (detail.subtitle != null)
            Padding(
              padding: const EdgeInsets.only(top: 4),
              child: Text(detail.subtitle!, style: Theme.of(context).textTheme.bodyMedium),
            ),
          const SizedBox(height: 8),
          Text('Total: \${detail.totalPriceKrw}'),
          const SizedBox(height: 16),
          if (detail.items.isEmpty)
            const Center(child: Text('No outfit items.'))
          else
            ...detail.items.map(
              (item) => Card(
                child: ListTile(
                  leading: SizedBox(
                    width: 48,
                    child: Image.network(
                      item.imageUrl,
                      fit: BoxFit.cover,
                      errorBuilder: (_, __, ___) => const ColoredBox(color: Colors.black12),
                    ),
                  ),
                  title: Text(item.name),
                  subtitle: Text('slot: ${item.slot.name}${item.locationZone != null ? ', zone: ${item.locationZone}' : ''}'),
                  trailing: Text('\${item.priceKrw}'),
                ),
              ),
            ),
        ],
      ),
    );
  }
}