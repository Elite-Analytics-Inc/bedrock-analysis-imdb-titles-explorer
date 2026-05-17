---
title: IMDB Titles Explorer
---

# IMDB Titles Explorer

## Titles by Type

```sql titles_by_type
SELECT * FROM titles_by_type ORDER BY total_titles DESC
```

*The IMDb catalog spans many formats — feature films ("movie"), TV episodes, shorts, TV specials, etc. This is the year-eligible count of each. TV episodes always dominate; "movie" is what most people picture when they hear "IMDb".*

{% grid cols=2 %}
{% bar_chart data="$titles_by_type" x="title_type" y="total_titles" title="Total Titles by Type" colors=["#6366f1"] info="Counts per IMDb title type. tvEpisode dominates because every episode of every series gets its own row; 'movie' is the headline-grabbing format but is a small slice of total volume." /%}
{% data_table data="$titles_by_type" info="Same data as the bar chart, with exact counts. Useful for citing precise stats like 'X movies vs Y TV episodes'." %}
{% column id="title_type" title="Type" /%}
{% column id="total_titles" title="Titles" fmt="num0" /%}
{% /data_table %}
{% /grid %}

## Production Volume by Decade

*How global filmmaking output grew over time. Almost-flat until the 1950s, slow climb through the 1980s, then a hockey-stick from the 1990s as TV episodes + streaming originals exploded. Useful for putting "more titles in 2020 than in all of pre-1950" claims in perspective.*

```sql titles_per_decade
SELECT * FROM titles_per_decade ORDER BY decade
```

{% line_chart data="$titles_per_decade" x="decade" y=["total_titles"] title="Titles Produced Per Decade" colors=["#3b82f6"] info="Titles whose release year falls in each decade bucket. The hockey-stick after 1990 reflects two things: cheaper production tools democratizing filmmaking, and IMDb's catalog itself getting more complete for the recent past (recency bias). Pre-1930 counts are sparse; pre-1900 is essentially the Lumière brothers' shorts." /%}

## Top 25 Genres

*Genres ranked by raw title count. Note that titles can belong to multiple genres, so the bars aren't mutually exclusive. Drama dominates because nearly every serious film carries the tag; lighter labels like "Talk-Show" or "Game-Show" tend to be TV-only.*

```sql genre_counts
SELECT * FROM genre_counts ORDER BY total_titles DESC
```

{% bar_chart data="$genre_counts" x="genre" y="total_titles" title="Top 25 Genres by Volume" swapXY=true colors=["#f59e0b"] info="Genres ranked by title count. Multi-tag: a single title can carry multiple genres (a Drama-Romance counts in both). Drama is the universal tag; specialized labels like 'Film-Noir' or 'Game-Show' sit lower because they apply to narrower windows of history." /%}

## Genre Trends Over Time

*How genre popularity shifted decade by decade. Use this to spot eras (Westerns peaking in the 50s-60s, Reality in the 2000s, Sci-Fi rising with CGI affordability).*

```sql genre_by_decade
SELECT * FROM genre_by_decade ORDER BY decade
```

{% line_chart data="$genre_by_decade" x="decade" y=["total_titles"] title="Genre Popularity by Decade" colors=["#22c55e"] info="How genre output evolved over time. Use it to find each genre's heyday — Westerns peaked in the 50s, Reality TV in the 2000s, Sci-Fi tracks CGI affordability. The overall hockey-stick reflects the catalog growth shown in the previous chart, not just that one genre." /%}

## Top 50 Rated Titles

*Highest-rated titles that cleared the "min votes" floor you set in the form. The vote floor is critical: without it, a single perfect-10 review on an obscure title would top the list. With 1,000+ votes you get a representative consensus; with 100,000+ you get only mainstream blockbusters.*

```sql top_rated
SELECT * FROM top_rated ORDER BY average_rating DESC, num_votes DESC
```

{% data_table data="$top_rated" rows=25 rowShading=true info="Highest-rated titles meeting the min-votes floor from the form. Type column distinguishes movies/series/episodes — top of the list is often individual prestige TV episodes, not feature films. Votes column shows just how mainstream each entry is." %}
{% column id="primary_title" title="Title" /%}
{% column id="title_type" title="Type" /%}
{% column id="start_year" title="Year" /%}
{% column id="average_rating" title="Rating" fmt="num1" contentType="colorscale" scaleColor=["#fecaca","#22c55e"] /%}
{% column id="num_votes" title="Votes" fmt="num0" /%}
{% /data_table %}

## Rating Distribution

*Where titles fall on the 1-10 user-rating scale. IMDb ratings have a well-known bias: most titles cluster between 6 and 8 — terrible films get review-bombed below 4, mediocre ones rarely break 5, and only beloved ones cross 8.*

```sql rating_distribution
SELECT * FROM rating_distribution ORDER BY rating_bucket
```

{% bar_chart data="$rating_distribution" x="rating_bucket" y="total_titles" title="Rating Distribution" colors=["#8b5cf6"] info="Histogram of titles by average user rating (1-10 in half-point buckets). Almost everything lives in 6-8: bad films get downvoted to a small left tail, mediocre ones rarely cross 5, and only beloved titles break 8. Anything 9+ is a small handful of universally-loved prestige releases." /%}

## Runtime Trends by Decade

*Average runtime by decade. Films got longer through the 50s-70s "epic" era, settled around ~110 min for the multiplex era, and have been creeping back up since 2010 (Marvel + prestige TV-as-cinema effect).*

```sql runtime_by_decade
SELECT * FROM runtime_by_decade ORDER BY decade
```

{% line_chart data="$runtime_by_decade" x="decade" y=["avg_runtime"] title="Average Runtime (Minutes) by Decade" colors=["#ef4444"] info="Average runtime in minutes by release decade. Silent era was short; the 50s-70s 'epic' era pushed films to 130+; multiplexes pulled average runtimes back to ~100; the streaming + Marvel era has been creeping up since 2010 (longer cuts as bandwidth gets cheaper)." /%}
