# Snhala_songs_search_engine

- Corpus including 2270 Sinhala songs each with 10 attributes(meta data).

###Meta data
1. track_id - track identifier
2. track_name_en - track name in Sinhala+English
3. track_name_si - track name in Sinhala unicode
4. track_rating - ratings for the song track
5. album_name_en - album name in Sinhala+English
6. album_name_si - album name in Sinhala unicode
7. artist_name_en - artist name in Sinhala + English
8. artist_name_si - artist name in Sinhala unicode
9. artist_rating - ratings of the artist
10. lyrics - Sinhala lyrics of the song in Sinhala unicode

###Directory

- Lyrics: Web scraping using Elasticsearch
- newSongs.json: Corpus for search engine
- create_index.js: Indexing the dataset
- Postman_queries.json: Postman queries for indexing and adding custom analyzers
- search_with_keywords.py: Support searching Sinhala queries using set of words defined. This search terms applies to search queries related to sinhala artist name, lyrics and sinhala album name fields.

####Keywrods used for diffrent fileds:
- artist_name_key_words = ['ගෙ', 'ගැයූ','ගයන', 'කියන', 'කියූ', 'ගායනා']
- lyrics_key_words = ['ලියූ', 'ලියන', 'ලිව්ව', 'රචනා', 'රචිත', 'ලීව']
- album_name_key_words = ['ඇල්බමය', 'ඇල්බමයේ', 'ඇල්බම']
