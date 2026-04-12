import os, sys
sys.path.insert(0, "/")
from bedrock_sdk import BedrockJob

job = BedrockJob()
conn = job.connect()

start_year = os.environ.get("PARAM_START_YEAR", "1950")
min_votes = os.environ.get("PARAM_MIN_VOTES", "1000")

job.progress(5, "Fetching titles by type...")
job.fetch("titles_by_type", f"""
    SELECT
        title_type,
        COUNT(*) as total_titles,
        ROUND(AVG(average_rating), 2) as avg_rating,
        ROUND(AVG(runtime_minutes), 1) as avg_runtime_mins,
        SUM(num_votes) as total_votes
    FROM bedrock.entertainment.imdb_titles
    WHERE start_year >= {start_year}
    GROUP BY title_type
    ORDER BY total_titles DESC
""")

job.progress(20, "Fetching production volume by decade...")
job.fetch("titles_per_decade", f"""
    SELECT
        (CAST(start_year AS INTEGER) / 10) * 10 as decade,
        title_type,
        COUNT(*) as total_titles,
        ROUND(AVG(average_rating), 2) as avg_rating
    FROM bedrock.entertainment.imdb_titles
    WHERE start_year >= {start_year}
      AND start_year IS NOT NULL
      AND title_type IN ('movie', 'tvSeries', 'short', 'tvMovie', 'tvMiniSeries')
    GROUP BY decade, title_type
    ORDER BY decade, total_titles DESC
""")

job.progress(35, "Fetching genre stats...")
job.fetch("genre_counts", f"""
    SELECT
        TRIM(genre) as genre,
        COUNT(*) as total_titles,
        ROUND(AVG(average_rating), 2) as avg_rating,
        ROUND(SUM(num_votes) / 1000000.0, 2) as total_votes_millions
    FROM bedrock.entertainment.imdb_titles
    CROSS JOIN UNNEST(string_split(genres, ',')) as t(genre)
    WHERE start_year >= {start_year}
      AND genres IS NOT NULL
      AND genres != '\\N'
    GROUP BY genre
    ORDER BY total_titles DESC
    LIMIT 25
""")

job.progress(50, "Fetching genre trends by decade...")
job.fetch("genre_by_decade", f"""
    SELECT
        (CAST(start_year AS INTEGER) / 10) * 10 as decade,
        TRIM(genre) as genre,
        COUNT(*) as total_titles
    FROM bedrock.entertainment.imdb_titles
    CROSS JOIN UNNEST(string_split(genres, ',')) as t(genre)
    WHERE start_year >= {start_year}
      AND genres IS NOT NULL
      AND genres != '\\N'
      AND TRIM(genre) IN ('Drama', 'Comedy', 'Action', 'Romance', 'Thriller', 'Horror', 'Documentary', 'Crime')
    GROUP BY decade, genre
    ORDER BY decade, total_titles DESC
""")

job.progress(65, "Fetching top rated titles...")
job.fetch("top_rated", f"""
    SELECT
        primary_title,
        title_type,
        start_year,
        genres,
        average_rating,
        num_votes,
        runtime_minutes
    FROM bedrock.entertainment.imdb_titles
    WHERE start_year >= {start_year}
      AND num_votes >= {min_votes}
      AND average_rating IS NOT NULL
    ORDER BY average_rating DESC, num_votes DESC
    LIMIT 50
""")

job.progress(75, "Fetching rating distribution...")
job.fetch("rating_distribution", f"""
    SELECT
        title_type,
        FLOOR(average_rating) as rating_bucket,
        COUNT(*) as total_titles
    FROM bedrock.entertainment.imdb_titles
    WHERE start_year >= {start_year}
      AND average_rating IS NOT NULL
      AND title_type IN ('movie', 'tvSeries', 'short', 'tvMovie')
    GROUP BY title_type, rating_bucket
    ORDER BY title_type, rating_bucket
""")

job.progress(85, "Fetching runtime trends...")
job.fetch("runtime_by_decade", f"""
    SELECT
        (CAST(start_year AS INTEGER) / 10) * 10 as decade,
        title_type,
        ROUND(AVG(runtime_minutes), 1) as avg_runtime,
        COUNT(*) as total_titles
    FROM bedrock.entertainment.imdb_titles
    WHERE start_year >= {start_year}
      AND runtime_minutes IS NOT NULL
      AND runtime_minutes > 0
      AND runtime_minutes < 300
      AND title_type IN ('movie', 'tvSeries', 'short')
    GROUP BY decade, title_type
    ORDER BY decade, title_type
""")

job.progress(90, "Writing outputs...")
job.write_parquet("titles_by_type", "SELECT * FROM titles_by_type")
job.write_parquet("titles_per_decade", "SELECT * FROM titles_per_decade")
job.write_parquet("genre_counts", "SELECT * FROM genre_counts")
job.write_parquet("genre_by_decade", "SELECT * FROM genre_by_decade")
job.write_parquet("top_rated", "SELECT * FROM top_rated")
job.write_parquet("rating_distribution", "SELECT * FROM rating_distribution")
job.write_parquet("runtime_by_decade", "SELECT * FROM runtime_by_decade")

job.update_progress("running_analysis", progress_pct=95, progress_message="Finalizing...",
                    lineage={"inputs": ["bedrock.entertainment.imdb_titles"],
                             "outputs": [
                                 "analytics/bedrock/JOB_ID/data/titles_by_type.parquet",
                                 "analytics/bedrock/JOB_ID/data/titles_per_decade.parquet",
                                 "analytics/bedrock/JOB_ID/data/genre_counts.parquet",
                                 "analytics/bedrock/JOB_ID/data/genre_by_decade.parquet",
                                 "analytics/bedrock/JOB_ID/data/top_rated.parquet",
                                 "analytics/bedrock/JOB_ID/data/rating_distribution.parquet",
                                 "analytics/bedrock/JOB_ID/data/runtime_by_decade.parquet"
                             ]})
job.complete()
