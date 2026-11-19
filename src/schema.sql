CREATE TABLE books (
  id INTEGER PRIMARY KEY,
  author TEXT,
  title TEXT,
  publisher TEXT,
  year TEXT
);

CREATE TABLE articles (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author TEXT NOT NULL,
  title TEXT NOT NULL,
  journal TEXT NOT NULL,
  year INTEGER NOT NULL,
  volume TEXT,
  number TEXT,
  pages TEXT
);

CREATE TABLE inproceedings (
  id INTEGER PRIMARY KEY,
  author TEXT,
  title TEXT,
  booktitle TEXT,
  year TEXT,
  pages TEXT
);
