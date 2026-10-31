DROP TABLE posts;

CREATE TABLE posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  myname TEXT NOT NULL,
  email TEXT NOT NULL,
  message_main TEXT NOT NULL,
  image TEXT,
  likes INTEGER DEFAULT 0,
  created_at TEXT NOT NULL
);


