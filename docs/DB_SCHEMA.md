# CoordiPick DB Schema (Draft)

## core.items
- `item_id` BIGINT PK
- `category` TEXT NOT NULL
- `sub_category` TEXT NOT NULL
- `gender` TEXT NOT NULL
- `fit` TEXT NOT NULL
- `color_tone` TEXT NOT NULL
- `moods` TEXT[] NOT NULL DEFAULT '{}'
- `tpos` TEXT[] NOT NULL DEFAULT '{}'
- `temperature_min` INT NOT NULL
- `temperature_max` INT NOT NULL
- `price_krw` INT NOT NULL
- `stock_qty` INT NOT NULL DEFAULT 0
- `image_url` TEXT NOT NULL
- `location_zone` TEXT
- `is_active` BOOLEAN NOT NULL DEFAULT TRUE
- `created_at` TIMESTAMPTZ NOT NULL DEFAULT NOW()
- `updated_at` TIMESTAMPTZ NOT NULL DEFAULT NOW()

## core.outfits
- `outfit_id` BIGSERIAL PK
- `title` TEXT NOT NULL
- `subtitle` TEXT
- `gender_target` TEXT NOT NULL
- `tpo` TEXT NOT NULL
- `mood` TEXT
- `total_price_krw` INT NOT NULL
- `generation_source` TEXT NOT NULL  -- rule | ai | admin
- `score` NUMERIC(10,4)
- `created_by` TEXT
- `created_at` TIMESTAMPTZ NOT NULL DEFAULT NOW()

## core.outfit_items
- `outfit_id` BIGINT NOT NULL REFERENCES core.outfits(outfit_id)
- `item_id` BIGINT NOT NULL REFERENCES core.items(item_id)
- `slot` TEXT NOT NULL               -- top | bottom | outer | shoes | acc
- `sort_order` INT NOT NULL DEFAULT 0
- PK (`outfit_id`, `item_id`, `slot`)

## admin.store_settings
- `store_id` TEXT PRIMARY KEY
- `target_gender` TEXT NOT NULL
- `price_band_min_krw` INT
- `price_band_max_krw` INT
- `mood_weights` JSONB NOT NULL DEFAULT '{}'
- `updated_at` TIMESTAMPTZ NOT NULL DEFAULT NOW()

## analytics.events
- `event_id` BIGSERIAL PK
- `session_id` TEXT NOT NULL
- `event_type` TEXT NOT NULL         -- impression | click | detail_view
- `outfit_id` BIGINT
- `context` JSONB NOT NULL DEFAULT '{}'
- `created_at` TIMESTAMPTZ NOT NULL DEFAULT NOW()

## analytics.daily_metrics
- `date` DATE PRIMARY KEY
- `recommendation_count` INT NOT NULL DEFAULT 0
- `click_count` INT NOT NULL DEFAULT 0
- `ctr` NUMERIC(8,4) NOT NULL DEFAULT 0
- `top3_outfits` JSONB NOT NULL DEFAULT '[]'
- `tpo_ratio` JSONB NOT NULL DEFAULT '{}'
- `low_stock_items` JSONB NOT NULL DEFAULT '[]'

## 인덱스 권장
- `core.items(gender, category, sub_category)`
- `core.items USING GIN (moods)`
- `core.items USING GIN (tpos)`
- `core.items(temperature_min, temperature_max)`
- `analytics.events(created_at, event_type)`
