-- Step 1: Create the flow_capture user with replication role
CREATE USER flow_capture WITH REPLICATION PASSWORD 'password';

-- Step 2: Grant read access and necessary privileges to flow_capture
GRANT pg_read_all_data TO flow_capture;
GRANT pg_write_all_data TO flow_capture;

-- Step 3: Create the flow_watermarks table and assign privileges
CREATE TABLE IF NOT EXISTS public.flow_watermarks (
    slot TEXT PRIMARY KEY,
    watermark TEXT
);

-- Grant privileges to flow_capture for the flow_watermarks table
GRANT ALL PRIVILEGES ON TABLE public.flow_watermarks TO flow_capture;

-- Step 4: Create the publication and add tables
CREATE PUBLICATION flow_publication;
ALTER PUBLICATION flow_publication SET (publish_via_partition_root = true);

-- Add flow_watermarks table to the publication
ALTER PUBLICATION flow_publication ADD TABLE public.flow_watermarks;

-- Step 5: Create the imdb table
CREATE TABLE IF NOT EXISTS public.imdb (
    record_id SERIAL PRIMARY KEY,
    poster_link VARCHAR(1000), -- Link of the poster that imdb using
    series_title VARCHAR(1000), -- Name of the movie
    released_year VARCHAR(50), -- Year at which that movie released
    _certificate VARCHAR(10), -- Certificate earned by that series
    runtime VARCHAR(20), -- Total runtime of the movie
    genre VARCHAR(500), -- Genre of the movie
    imdb_rating FLOAT, -- Rating of the movie at IMDB site
    overview VARCHAR(1000), -- mini story/ summary
    meta_score VARCHAR, -- Score earned by the movie
    director VARCHAR(100), -- Name of the Director
    star1 VARCHAR(100),  -- Name of the Stars
    star2 VARCHAR(100),
    star3 VARCHAR(100),
    star4 VARCHAR(100),
    no_of_votes INTEGER NULL, -- Total number of votes
    gross VARCHAR(100) -- Money earned by that movie
);

-- Add the imdb table to the publication
ALTER PUBLICATION flow_publication ADD TABLE public.imdb;

