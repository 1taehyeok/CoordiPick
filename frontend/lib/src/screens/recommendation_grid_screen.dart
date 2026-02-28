import 'package:flutter/material.dart';

import '../api/user_api_client.dart';
import '../models/user_models.dart';
import 'recommendation_detail_screen.dart';

class RecommendationGridScreen extends StatelessWidget {
  const RecommendationGridScreen({
    super.key,
    required this.client,
    required this.sessionId,
    required this.cards,
  });

  final UserApiClient client;
  final String sessionId;
  final List<RecommendationCard> cards;

  Future<void> _openDetail(BuildContext context, RecommendationCard card) async {
    await client.createEvent(
      CreateEventRequest(
        sessionId: sessionId,
        eventType: EventType.click,
        recommendationId: card.recommendationId,
      ),
    );

    if (!context.mounted) return;
    await Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => RecommendationDetailScreen(
          client: client,
          sessionId: sessionId,
          recommendationId: card.recommendationId,
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (cards.isEmpty) {
      return const Center(child: Text('No recommendations found.'));
    }

    return GridView.builder(
      padding: const EdgeInsets.all(12),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        childAspectRatio: 0.72,
        crossAxisSpacing: 10,
        mainAxisSpacing: 10,
      ),
      itemCount: cards.length,
      itemBuilder: (context, index) {
        final card = cards[index];
        return InkWell(
          onTap: () => _openDetail(context, card),
          child: Card(
            child: Padding(
              padding: const EdgeInsets.all(10),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(8),
                      child: Image.network(
                        card.thumbnailUrl,
                        fit: BoxFit.cover,
                        width: double.infinity,
                        errorBuilder: (_, __, ___) => const ColoredBox(
                          color: Colors.black12,
                          child: Center(child: Text('Image load failed')),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(card.title, maxLines: 1, overflow: TextOverflow.ellipsis),
                  if (card.subtitle != null)
                    Text(
                      card.subtitle!,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: Theme.of(context).textTheme.bodySmall,
                    ),
                  Text('\${card.totalPriceKrw}'),
                  if (card.reasonTags.isNotEmpty)
                    Text(
                      card.reasonTags.join(', '),
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: Theme.of(context).textTheme.labelSmall,
                    ),
                ],
              ),
            ),
          ),
        );
      },
    );
  }
}