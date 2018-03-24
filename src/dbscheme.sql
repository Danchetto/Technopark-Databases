CREATE EXTENSION IF NOT EXISTS CITEXT;

CREATE TABLE users
(
  id BIGSERIAL PRIMARY KEY ,
  nickname CITEXT COLLATE ucs_basic NOT NULL UNIQUE,
  about CITEXT,
  email CITEXT not null unique,
  fullname TEXT
)
;

CREATE TABLE forums
(
  id BIGSERIAL primary key,
  slug CITEXT not null unique,
  title TEXT,
  author CITEXT references users(nickname),
  threads BIGINT DEFAULT 0,
  posts BIGINT DEFAULT 0
)
;

CREATE TABLE threads
(
  id         BIGSERIAL PRIMARY KEY,
  slug       CITEXT UNIQUE,
  created    TIMESTAMP WITH TIME ZONE,
  message    TEXT,
  title      TEXT,
  author     CITEXT REFERENCES users (nickname),
  forum    TEXT,
  votes    BIGINT DEFAULT 0
)
;

CREATE TABLE votes
(
  voice      INT CHECK (voice in (1, -1)),
  nickname     CITEXT REFERENCES users (nickname)
--   threadid   BIGINT REFERENCES threads (id),
--   CONSTRAINT unique_vote UNIQUE (userid, threadid)
)
;