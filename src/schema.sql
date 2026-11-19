CREATE TABLE todos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  content TEXT NOT NULL,
  done BOOLEAN DEFAULT FALSE
);

CREATE TABLE reference_entries (
  reference_type TEXT NOT NULL,
  citation_key TEXT PRIMARY KEY NOT NULL
);

CREATE TABLE reference_fields (
  reference_key TEXT REFERENCES reference_entries(citation_key) ON DELETE CASCADE,
  name TEXT NOT NULL,
  value TEXT
);