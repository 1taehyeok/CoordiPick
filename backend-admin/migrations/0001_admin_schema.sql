BEGIN;

CREATE SCHEMA IF NOT EXISTS core;
CREATE SCHEMA IF NOT EXISTS admin;
CREATE SCHEMA IF NOT EXISTS analytics;

CREATE TABLE IF NOT EXISTS core.items (
    item_id BIGSERIAL PRIMARY KEY,
    category TEXT NOT NULL,
    sub_category TEXT NOT NULL,
    gender TEXT NOT NULL,
    fit TEXT NOT NULL,
    color_tone TEXT NOT NULL,
    moods TEXT[] NOT NULL DEFAULT '{}',
    tpos TEXT[] NOT NULL DEFAULT '{}',
    temperature_min INT NOT NULL,
    temperature_max INT NOT NULL,
    price_krw INT NOT NULL,
    stock_qty INT NOT NULL DEFAULT 0,
    image_url TEXT NOT NULL,
    location_zone TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS core.outfits (
    outfit_id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    subtitle TEXT,
    gender_target TEXT NOT NULL,
    tpo TEXT NOT NULL,
    mood TEXT,
    total_price_krw INT NOT NULL,
    generation_source TEXT NOT NULL,
    score NUMERIC(10, 4),
    created_by TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS core.outfit_items (
    outfit_id BIGINT NOT NULL REFERENCES core.outfits(outfit_id) ON DELETE CASCADE,
    item_id BIGINT NOT NULL REFERENCES core.items(item_id) ON DELETE RESTRICT,
    slot TEXT NOT NULL,
    sort_order INT NOT NULL DEFAULT 0,
    PRIMARY KEY (outfit_id, item_id, slot)
);

CREATE TABLE IF NOT EXISTS admin.store_settings (
    store_id TEXT PRIMARY KEY,
    target_gender TEXT NOT NULL,
    price_band_min_krw INT,
    price_band_max_krw INT,
    mood_weights JSONB NOT NULL DEFAULT '{}',
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS analytics.daily_metrics (
    date DATE PRIMARY KEY,
    recommendation_count INT NOT NULL DEFAULT 0,
    click_count INT NOT NULL DEFAULT 0,
    ctr NUMERIC(8, 4) NOT NULL DEFAULT 0,
    top3_outfits JSONB NOT NULL DEFAULT '[]',
    tpo_ratio JSONB NOT NULL DEFAULT '{}',
    low_stock_items JSONB NOT NULL DEFAULT '[]'
);

CREATE INDEX IF NOT EXISTS idx_items_gender_category_sub ON core.items (gender, category, sub_category);
CREATE INDEX IF NOT EXISTS idx_items_moods_gin ON core.items USING GIN (moods);
CREATE INDEX IF NOT EXISTS idx_items_tpos_gin ON core.items USING GIN (tpos);
CREATE INDEX IF NOT EXISTS idx_items_temp_range ON core.items (temperature_min, temperature_max);

INSERT INTO admin.store_settings (store_id, target_gender)
VALUES ('default', 'unisex')
ON CONFLICT (store_id) DO NOTHING;

COMMIT;
