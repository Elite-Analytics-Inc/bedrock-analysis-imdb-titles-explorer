---
title: IMDB Titles Explorer
---

# IMDB Titles Explorer

## Titles by Type

```sql titles_by_type
SELECT * FROM titles_by_type ORDER BY total_titles DESC
```

{% grid cols=2 %}
{% bar_chart data="$titles_by_type" x="title_type" y="total_titles" title="Total Titles by Type" colors=["#6366f1"] /%}
{% data_table data="$titles_by_type" %}
{% column id="title_type" title="Type" /%}
{% column id="total_titles" title="Titles" fmt="num0" /%}
{% /data_table %}
{% /grid %}

## Production Volume by Decade

```sql titles_per_decade
SELECT * FROM titles_per_decade ORDER BY decade
```

{% line_chart data="$titles_per_decade" x="decade" y=["total_titles"] title="Titles Produced Per Decade" colors=["#3b82f6"] /%}

## Top 25 Genres

```sql genre_counts
SELECT * FROM genre_counts ORDER BY total_titles DESC
```

{% bar_chart data="$genre_counts" x="genre" y="total_titles" title="Top 25 Genres by Volume" swapXY=true colors=["#f59e0b"] /%}

## Genre Trends Over Time

```sql genre_by_decade
SELECT * FROM genre_by_decade ORDER BY decade
```

{% line_chart data="$genre_by_decade" x="decade" y=["total_titles"] title="Genre Popularity by Decade" colors=["#22c55e"] /%}

## Top 50 Rated Titles

```sql top_rated
SELECT * FROM top_rated ORDER BY average_rating DESC, num_votes DESC
```

{% data_table data="$top_rated" rows=25 rowShading=true %}
{% column id="primary_title" title="Title" /%}
{% column id="title_type" title="Type" /%}
{% column id="start_year" title="Year" /%}
{% column id="average_rating" title="Rating" fmt="num1" contentType="colorscale" scaleColor=["#fecaca","#22c55e"] /%}
{% column id="num_votes" title="Votes" fmt="num0" /%}
{% /data_table %}

## Rating Distribution

```sql rating_distribution
SELECT * FROM rating_distribution ORDER BY rating_bucket
```

{% bar_chart data="$rating_distribution" x="rating_bucket" y="total_titles" title="Rating Distribution" colors=["#8b5cf6"] /%}

## Runtime Trends by Decade

```sql runtime_by_decade
SELECT * FROM runtime_by_decade ORDER BY decade
```

{% line_chart data="$runtime_by_decade" x="decade" y=["avg_runtime"] title="Average Runtime (Minutes) by Decade" colors=["#ef4444"] /%}
