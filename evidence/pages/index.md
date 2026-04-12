---
title: IMDB Titles Explorer
---

# 🎬 IMDB Titles Explorer

Explore genre trends, ratings, and production history across IMDB's title catalog.

## Titles by Type

```sql titles_by_type
select * from titles_by_type order by total_titles desc
```

<BarChart
    data={titles_by_type}
    x=title_type
    y=total_titles
    title="Total Titles by Type"
/>

<DataTable data={titles_by_type} />

---

## 📈 Production Volume by Decade

```sql titles_per_decade
select * from titles_per_decade order by decade
```

<LineChart
    data={titles_per_decade}
    x=decade
    y=total_titles
    series=title_type
    title="Titles Produced Per Decade by Type"
/>

---

## 🎭 Top 25 Genres

```sql genre_counts
select * from genre_counts order by total_titles desc
```

<BarChart
    data={genre_counts}
    x=genre
    y=total_titles
    title="Top 25 Genres by Volume"
    swapXY=true
/>

<DataTable data={genre_counts} />

---

## 📊 Genre Trends Over Time

```sql genre_by_decade
select * from genre_by_decade order by decade
```

<LineChart
    data={genre_by_decade}
    x=decade
    y=total_titles
    series=genre
    title="Genre Popularity by Decade"
/>

---

## ⭐ Top 50 Rated Titles

```sql top_rated
select * from top_rated order by average_rating desc, num_votes desc
```

<DataTable data={top_rated} search=true />

---

## 📉 Rating Distribution

```sql rating_distribution
select * from rating_distribution order by title_type, rating_bucket
```

<BarChart
    data={rating_distribution}
    x=rating_bucket
    y=total_titles
    series=title_type
    title="Rating Distribution by Title Type"
/>

---

## ⏱️ Runtime Trends by Decade

```sql runtime_by_decade
select * from runtime_by_decade order by decade
```

<LineChart
    data={runtime_by_decade}
    x=decade
    y=avg_runtime
    series=title_type
    title="Average Runtime (Minutes) by Decade"
/>
