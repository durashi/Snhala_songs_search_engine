#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import json
import requests

artist_name_key_words = ['ගෙ', 'ගැයූ','ගයන', 'කියන', 'කියූ', 'ගායනා']
lyrics_key_words = ['ලියූ', 'ලියන', 'ලිව්ව', 'රචනා', 'රචිත', 'ලීව']
album_name_key_words = ['ඇල්බමය', 'ඇල්බමයේ', 'ඇල්බම']

aggs =      {
                "Title filter": {
                "terms": {
                    "field": "track_name_si.keyword",
                    "size": 5
                }
                },
                "Artist name filter": {
                "terms": {
                    "field": "artist_name_si.keyword",
                    "size": 5
                }
                },
                "Lyrics filter": {
                "terms": {
                    "field": "lyrics.keyword",
                    "size": 5
                }
                },
                "Album name filter": {
                "terms": {
                    "field": "album_name_si.keyword",
                    "size": 5
                }
                }
            }

def generate_query(term, size, sort):
    if(sort):
        query = {
                    "size" : size,
                    "sort": [{"Visits": {"order": "desc"}}],
                    "query":{
                        "query_string":{
                            "query": term
                        }
                    },
                    "aggs" : aggs
                    }
    else:
        query = {
                    "size" : size,
                    "query":{
                        "query_string":{
                            "query": term
                        }
                    },
                    "aggs" : aggs
                    }
    
    return query

def generate_query_with_keywords(mustObj, term, size, sort):
    

    if(sort):
        query = {
            "sort": [{"Visits": {"order": "desc"}}],
            "size": size,
            "aggs": aggs,
            "query": {
                "bool": {
                "must": [
                    {
                    "query_string": {
                        "query": term
                    }
                    }
                ],
                "filter":mustObj
                }
            }
        }
    else:
        query = {
            "size": size,
            "aggs": aggs,
            "query": {
                "bool": {
                "must": [
                    {
                    "query_string": {
                        "query": term
                    }
                    }
                ],
                "filter":mustObj
                }
            }
        }

    return query


def detect_keywords(term):
    mustobj = []
    words = term.split()
    text , artist, lyrics, album_name = "", "", "", ""
    for i in range (len(words)):
        word = words[i]
        if word  in artist_name_key_words:
            artist_name_key_words = words[i-2] + " "+ words[i-1]
            matchObjArtist = {"match" : {"artist_name_si" : artist_name_si}}
            mustobj.append(matchObjArtist)

        elif word  in lyrics_key_words:
            lyrics = words[i-2] + " "+ words[i-1]
            matchObjLyrics = {"match" : {"lyrics" : lyrics}}
            mustobj.append(matchObjLyrics)
        
        elif word  in album_name_key_words:
            album_name = words[i-2] + " "+ words[i-1]
            matchObjMusic = {"match" : {"album_name_si" : album_name_si}}
            mustobj.append(matchObjMusic)
        
        else:
            text += word + " "

    text_cleaned = ""
    text_splited = text.split()
    for word in text_splited:
      if not(word in artist_name_si or  word in lyrics or  word in album_name_si):
        text_cleaned += word + " "
    text_cleaned = text_cleaned.strip()
    text_cleaned = (''.join([i for i in text_cleaned if not i.isdigit()])).strip()
    matchObjSong = {"match" : {"Song" : text_cleaned}}

    if len(mustobj) > 0:
        mustobj.append(matchObjSong)
        
    return mustobj

def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)


def perfom_query(query, host):
            URL = "http://localhost:9200/sinhalasongs/_search"
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            response = (requests.post(URL, data = json.dumps(query), headers = headers)).text
            res = json.loads(response)
            hits = res['hits']['hits']
            songs = []

            for song in hits:
                songs.append(song['_source'])

            
            facets = res['aggregations']
            
            # if(sort): 
            #     response_body = {
            #         "results" : songs
            #     }
            # else:
            response_body = {
                    "results" : songs,
                    "facets" : {
                        "Title filter" : facets['Title filter']['buckets'],
                        "Album name filter" : facets['Album name filter']['buckets'],
                        "Artist name filter" : facets['Artist name filter']['buckets'],
                        "Lyrics filter" : facets['Lyrics filter']['buckets'],
                    }      
                }

            return response_body


def get_number(term):
    words = term.split()
    number = 0
    for i in words:
        if hasNumbers(i):
            number = int(i)
    return number

def search_by_term(term, host):
    words = term.split()

    mustObj = detect_keywords(term)

    if len(words) >= 4:
        if(len(mustObj) > 0):
            if(hasNumbers(term)):
                #search by keywords + sort N results + facets
                size = get_number(term)
                term  = (''.join([i for i in term if not i.isdigit()])).strip()
                sort = True
                query = generate_query_with_keywords(mustObj, term, size, sort)
            else:
                #earch by keywords  + facets 
                size = 20
                sort = False
                query = generate_query_with_keywords(mustObj,term, 20, sort)
        else:
            if(hasNumbers(term)):
                #query search + facets + sort N
                size = get_number(term)
                term  = (''.join([i for i in term if not i.isdigit()])).strip()
                sort = True
                query = generate_query(term, size, sort)
            else:
                 #query search + facets
                 size = get_number(term)
                 sort = False
                 query = generate_query(term, 20, sort)

    else:
        if(hasNumbers(term)):
            size = get_number(term)
            sort = True
            query = generate_query(term, size, sort)
        else:
            sort = False
            size = get_number(term)
            query = generate_query(term, 20, sort)
    

    try:
        print(query)
        return perfom_query(query, host)
    except:
        print("Error perform query")
