PRAGMA foreign_keys = ON;

CREATE TABLE items (
    id        INTEGER PRIMARY KEY,
    name      TEXT NOT NULL UNIQUE,
    category  TEXT NOT NULL,
    meal      TEXT NOT NULL DEFAULT 'Any',
    unit      TEXT NOT NULL,
    store     TEXT NOT NULL,
    archived  INTEGER NOT NULL DEFAULT 0 CHECK (archived IN (0, 1))
);

CREATE TABLE shopping_list (
    id        INTEGER PRIMARY KEY,
    item_id   INTEGER NOT NULL REFERENCES items(id),
    qty       REAL NOT NULL DEFAULT 1,
    bought    INTEGER NOT NULL DEFAULT 0 CHECK (bought IN (0, 1)),
    added_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    bought_at TEXT
);

CREATE UNIQUE INDEX one_open_row_per_item
    ON shopping_list(item_id) WHERE bought = 0;

CREATE TABLE meals (
    id        INTEGER PRIMARY KEY,
    name      TEXT NOT NULL UNIQUE,
    archived  INTEGER NOT NULL DEFAULT 0 CHECK (archived IN (0, 1))
);

CREATE TABLE meal_ingredients (
    meal_id    INTEGER NOT NULL REFERENCES meals(id),
    item_id    INTEGER NOT NULL REFERENCES items(id),
    usual_qty  REAL,
    PRIMARY KEY (meal_id, item_id)
);

CREATE TABLE meal_events (
    id          INTEGER PRIMARY KEY,
    meal_id     INTEGER NOT NULL REFERENCES meals(id),
    event_date  TEXT NOT NULL DEFAULT (date('now')),
    headcount   INTEGER
);

CREATE TABLE event_items (
    event_id     INTEGER NOT NULL REFERENCES meal_events(id),
    item_id      INTEGER NOT NULL REFERENCES items(id),
    planned_qty  REAL,
    qty_used     REAL,
    verdict      TEXT CHECK (verdict IN ('too much', 'about right', 'ran short')),
    PRIMARY KEY (event_id, item_id)
);