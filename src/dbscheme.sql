CREATE EXTENSION IF NOT EXISTS CITEXT;

CREATE TABLE "user"
(
  id bigserial PRIMARY KEY ,
  nickname citext COLLATE ucs_basic NOT NULL UNIQUE,
  about citext,
  email citext not null unique,
  fullname text
)
;

CREATE TABLE forum
(
  id bigserial primary key,
  slug citext not null unique,
  title text,
  userid bigint references "user"(id)
)
;

create table thread
(
  id         BIGSERIAL PRIMARY KEY,
  slug       CITEXT UNIQUE,
  created_on TIMESTAMP,
  message    TEXT,
  title      TEXT,
  authorid   BIGINT REFERENCES "user" (id),
  forumid    BIGINT REFERENCES forum (id)
)
;

create table message
(
  id         BIGSERIAL PRIMARY KEY,
  created_on TIMESTAMP,
  message    TEXT,
  isedited   BOOLEAN,
  authorid   BIGINT REFERENCES "user" (id),
  parentid   BIGINT REFERENCES message (id) DEFAULT 0,
  threadid   BIGINT REFERENCES thread (id),
  forumid    BIGINT REFERENCES forum (id),
  parenttree BIGINT[] DEFAULT '{0}'

)
;

create table vote
(
  voice      INT CHECK (voice in (1, -1)),
  userid     BIGINT REFERENCES "user" (id),
  threadid   BIGINT REFERENCES thread (id),
  CONSTRAINT unique_vote UNIQUE (userid, threadid)
)
;