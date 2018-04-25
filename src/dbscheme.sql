DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS forums CASCADE;
DROP TABLE IF EXISTS threads CASCADE;
DROP TABLE IF EXISTS posts CASCADE;
DROP TABLE IF EXISTS votes CASCADE;
DROP TABLE IF EXISTS forum_users CASCADE;

CREATE EXTENSION IF NOT EXISTS CITEXT;

CREATE TABLE users
(
  nickname VARCHAR COLLATE ucs_basic PRIMARY KEY,
  about TEXT,
  email CITEXT NOT NULL UNIQUE,
  fullname CITEXT
);

CREATE TABLE forums
(
  id BIGSERIAL PRIMARY KEY,
  slug CITEXT NOT NULL UNIQUE,
  title CITEXT,
  author CITEXT REFERENCES users(nickname),
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
  forum    CITEXT REFERENCES forums(slug),
  votes    BIGINT DEFAULT 0
);

CREATE TABLE posts (
  id        SERIAL                      NOT NULL PRIMARY KEY,
  author    VARCHAR                     NOT NULL REFERENCES users(nickname),
  created   TIMESTAMP WITH TIME ZONE    DEFAULT current_timestamp,
  forum     CITEXT REFERENCES forums(slug),
  isEdited  BOOLEAN                     DEFAULT FALSE,
  message   TEXT                        NOT NULL,
  parent    INTEGER                     DEFAULT 0,
  thread    INTEGER                     NOT NULL REFERENCES threads(id),
  path      BIGINT                      ARRAY
);


CREATE TABLE votes
(
  id        SERIAL      NOT NULL PRIMARY KEY,
  username  VARCHAR     NOT NULL REFERENCES users(nickname),
  voice     INTEGER,
  thread    INTEGER     NOT NULL REFERENCES threads(id),
  UNIQUE(username, thread)
);

CREATE TABLE forum_users (
  user_nickname VARCHAR REFERENCES users(nickname) NOT NULL,
  forum CITEXT REFERENCES forums(slug) NOT NULL
);