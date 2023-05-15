CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'film_state') THEN 
        CREATE TYPE film_state AS ENUM ('DOWNLOADING', 'IN QUEUE', 'COMPLETE'); 
    END IF; 
END $$;


-- Rating table
CREATE TABLE IF NOT EXISTS rating (
  uuid uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  average float check (
    average BETWEEN 0
    AND 10
  ),
  story integer NOT NULL CHECK (
    story BETWEEN 0
    AND 10
  ),
  positions integer NOT NULL CHECK (
    positions BETWEEN 0
    AND 10
  ),
  pussy integer NOT NULL CHECK (
    pussy BETWEEN 0
    AND 10
  ),
  shots integer NOT NULL CHECK (
    shots BETWEEN 0
    AND 10
  ),
  boobs integer NOT NULL CHECK (
    boobs BETWEEN 0
    AND 10
  ),
  face integer NOT NULL CHECK (
    face BETWEEN 0
    AND 10
  ),
  rearview integer NOT NULL CHECK (
    rearview BETWEEN 0
    AND 10
  )
);

-- Film table
CREATE TABLE IF NOT EXISTS film (
  uuid uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  title text NOT NULL,
  duration interval NOT NULL,
  date_added date NOT NULL,
  filename text NOT NULL,
  watched boolean NOT NULL,
  state film_state NOT NULL,
  thumbnail bytea NOT NULL,
  poster bytea NOT NULL,
  download_progress integer NOT NULL CHECK (
    download_progress BETWEEN 0
    AND 100
  ),
  actresses text[] NOT NULL,
  rating uuid REFERENCES rating(uuid)
);

-- Indexed
CREATE TABLE IF NOT EXISTS indexed (
  uuid uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  film_id integer not null,
  title text NOT NULL,
  actresses text [] NOT NULL,
  thumbnail bytea NOT NULL,
  url text NOT NULL
);

-- Queue
CREATE TABLE IF NOT EXISTS queue (
  uuid uuid PRIMARY KEY DEFAULT uuid_generate_v4(),
  url text NOT NULL,
  film_uuid uuid REFERENCES film(uuid)
);


CREATE OR REPLACE FUNCTION update_rating_average() RETURNS TRIGGER AS $$
BEGIN
  UPDATE rating SET average = (story * 0.2 + positions * 0.15 + pussy * 0.3 + shots * 0.1 + boobs * 0.15 + rearview * 0.1) / 1.0
  WHERE uuid = NEW.uuid;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger on rating table
CREATE OR REPLACE TRIGGER update_rating_average_trigger
AFTER INSERT OR UPDATE OF story, positions, pussy, shots, boobs, rearview ON rating
FOR EACH ROW
EXECUTE FUNCTION update_rating_average();


-- important select query
-- SELECT * FROM queue WHERE uuid = (
--   SELECT uuid FROM queue ORDER BY uuid LIMIT 1 FOR UPDATE SKIP LOCKED
-- ) LIMIT 1 FOR UPDATE;



