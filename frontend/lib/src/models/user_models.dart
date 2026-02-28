enum Gender { male, female, unisex }

enum Tpo { commute, date, friends, travel, daily, special }

enum Slot { top, bottom, outer, shoes, acc }

enum EventType { impression, click, detailView }

extension EventTypeWire on EventType {
  String get wire {
    switch (this) {
      case EventType.impression:
        return 'impression';
      case EventType.click:
        return 'click';
      case EventType.detailView:
        return 'detail_view';
    }
  }
}

class GenerateRecommendationRequest {
  GenerateRecommendationRequest({
    required this.sessionId,
    required this.gender,
    required this.tpo,
    required this.temperatureC,
    this.mood,
  });

  final String sessionId;
  final Gender gender;
  final Tpo tpo;
  final double temperatureC;
  final String? mood;

  Map<String, dynamic> toJson() => {
    'session_id': sessionId,
    'gender': gender.name,
    'tpo': tpo.name,
    'temperature_c': temperatureC,
    if (mood != null && mood!.trim().isNotEmpty) 'mood': mood,
  };
}

class RecommendationCard {
  RecommendationCard({
    required this.recommendationId,
    required this.title,
    this.subtitle,
    required this.totalPriceKrw,
    required this.thumbnailUrl,
    required this.reasonTags,
  });

  final String recommendationId;
  final String title;
  final String? subtitle;
  final int totalPriceKrw;
  final String thumbnailUrl;
  final List<String> reasonTags;

  factory RecommendationCard.fromJson(Map<String, dynamic> json) {
    return RecommendationCard(
      recommendationId: json['recommendation_id'].toString(),
      title: json['title'].toString(),
      subtitle: json['subtitle']?.toString(),
      totalPriceKrw: (json['total_price_krw'] as num).toInt(),
      thumbnailUrl: json['thumbnail_url'].toString(),
      reasonTags:
          (json['reason_tags'] as List<dynamic>?)?.map((e) => e.toString()).toList() ??
          const <String>[],
    );
  }
}

class RecommendationListData {
  RecommendationListData({required this.cards});

  final List<RecommendationCard> cards;

  factory RecommendationListData.fromJson(Map<String, dynamic> json) {
    final rawCards = json['cards'] as List<dynamic>? ?? const <dynamic>[];
    return RecommendationListData(
      cards: rawCards
          .whereType<Map<String, dynamic>>()
          .map(RecommendationCard.fromJson)
          .toList(),
    );
  }
}

class RecommendationListResponse {
  RecommendationListResponse({required this.success, required this.data, this.generatedAt});

  final bool success;
  final RecommendationListData data;
  final String? generatedAt;

  factory RecommendationListResponse.fromJson(Map<String, dynamic> json) {
    final meta = json['meta'] as Map<String, dynamic>?;
    return RecommendationListResponse(
      success: json['success'] == true,
      data: RecommendationListData.fromJson((json['data'] as Map<String, dynamic>?) ?? {}),
      generatedAt: meta?['generated_at']?.toString(),
    );
  }
}

class OutfitItem {
  OutfitItem({
    required this.itemId,
    required this.name,
    required this.slot,
    required this.priceKrw,
    this.locationZone,
    required this.imageUrl,
  });

  final String itemId;
  final String name;
  final Slot slot;
  final int priceKrw;
  final String? locationZone;
  final String imageUrl;

  factory OutfitItem.fromJson(Map<String, dynamic> json) {
    return OutfitItem(
      itemId: json['item_id'].toString(),
      name: json['name'].toString(),
      slot: Slot.values.byName(json['slot'].toString()),
      priceKrw: (json['price_krw'] as num).toInt(),
      locationZone: json['location_zone']?.toString(),
      imageUrl: json['image_url'].toString(),
    );
  }
}

class RecommendationDetail {
  RecommendationDetail({
    required this.recommendationId,
    required this.title,
    this.subtitle,
    required this.totalPriceKrw,
    required this.items,
  });

  final String recommendationId;
  final String title;
  final String? subtitle;
  final int totalPriceKrw;
  final List<OutfitItem> items;

  factory RecommendationDetail.fromJson(Map<String, dynamic> json) {
    final rawItems = json['items'] as List<dynamic>? ?? const <dynamic>[];
    return RecommendationDetail(
      recommendationId: json['recommendation_id'].toString(),
      title: json['title'].toString(),
      subtitle: json['subtitle']?.toString(),
      totalPriceKrw: (json['total_price_krw'] as num).toInt(),
      items: rawItems.whereType<Map<String, dynamic>>().map(OutfitItem.fromJson).toList(),
    );
  }
}

class RecommendationDetailResponse {
  RecommendationDetailResponse({required this.success, required this.data});

  final bool success;
  final RecommendationDetail data;

  factory RecommendationDetailResponse.fromJson(Map<String, dynamic> json) {
    return RecommendationDetailResponse(
      success: json['success'] == true,
      data: RecommendationDetail.fromJson((json['data'] as Map<String, dynamic>?) ?? {}),
    );
  }
}

class CreateEventRequest {
  CreateEventRequest({
    required this.sessionId,
    required this.eventType,
    required this.recommendationId,
    this.payload,
  });

  final String sessionId;
  final EventType eventType;
  final String recommendationId;
  final Map<String, dynamic>? payload;

  Map<String, dynamic> toJson() => {
    'session_id': sessionId,
    'event_type': eventType.wire,
    'recommendation_id': recommendationId,
    if (payload != null) 'payload': payload,
  };
}