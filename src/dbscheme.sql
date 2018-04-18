CREATE EXTENSION IF NOT EXISTS CITEXT;

CREATE TABLE users
(
  nickname VARCHAR PRIMARY KEY,
  about TEXT,
  email CITEXT NOT NULL UNIQUE,
  fullname CITEXT
);

CREATE TABLE forums
(
  id BIGSERIAL primary key,
  slug CITEXT not null unique,
  title CITEXT,
  author CITEXT references users(nickname),
  threads INTEGER DEFAULT 0,
  posts INTEGER DEFAULT 0
);

CREATE TABLE threads
(
  id         BIGSERIAL PRIMARY KEY,
  slug       CITEXT UNIQUE,
  created    TIMESTAMP WITH TIME ZONE,
  message    TEXT,
  title      TEXT,
  author     VARCHAR REFERENCES users (nickname),
  forum    TEXT,
  votes    BIGINT DEFAULT 0
);

CREATE TABLE posts (
  id        SERIAL                      NOT NULL PRIMARY KEY,
  author    VARCHAR                     NOT NULL REFERENCES users(nickname),
  created   TIMESTAMP WITH TIME ZONE    DEFAULT current_timestamp,
  forum     VARCHAR,
  isEdited  BOOLEAN                     DEFAULT FALSE,
  message   TEXT                        NOT NULL,
  parent    INTEGER                     DEFAULT 0,
  thread    INTEGER                     NOT NULL REFERENCES threads(id),
  path      BIGINT                      ARRAY
);


CREATE TABLE votes
(
  voice      INT CHECK (voice in (1, -1)),
  nickname     CITEXT REFERENCES users (nickname)
--   threadid   BIGINT REFERENCES threads (id),
--   CONSTRAINT unique_vote UNIQUE (userid, threadid)
);