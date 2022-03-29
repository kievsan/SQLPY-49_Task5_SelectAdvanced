# [SQLPY-49] 5. Музыкальный сервис
# к лекции «Группировки, выборки из нескольких таблиц» 25.03.2022
# ДЗ Написать SELECT-запросы и вывести информацию


def get_tasks():
    task5_singer = 'исполнитель-5'
    select_list = [
        {'task': '--1. количество исполнителей в каждом жанре',
         'select':
            """
            SELECT genre_name, COUNT(artist_id) исполнителей
            FROM relate_genre_into_artist ga
            JOIN music_genres g ON g.genre_id = ga.genre_id
            GROUP BY ga.genre_id, genre_name
            ORDER BY genre_name ;
        """},
        {'task': '--2. количество треков, вошедших в альбомы 2019-2020 годов',
         'select':
            """
            SELECT COUNT(*) альбомов, SUM(треков) треков 
            FROM ( SELECT t.album_id альбом, COUNT(track_id) треков 
                    FROM music_tracks t
                    JOIN music_albums a ON a.album_id = t.album_id
                    WHERE album_release_year BETWEEN 2019 AND 2020
                    GROUP BY t.album_id 
                ) треков_в_искомых_альбомах ;
        """},
        {'task': '--3. средняя продолжительность треков по каждому альбому',
         'select':
            """
            SELECT album_name Альбом, 
                ROUND(AVG(track_duration), 1) средняя_длит
            FROM music_tracks t
            JOIN music_albums a ON a.album_id = t.album_id
            GROUP BY t.album_id, album_name
            ORDER BY album_name ;
        """},
        {'task': '--4. все исполнители, которые не выпустили альбомы в 2020 году',
         'select':
            """
            SELECT artist_name Исполнители
            FROM music_artists ar
            LEFT JOIN (SELECT artist_id 
                    FROM relate_artist_into_album aa
                    JOIN music_albums al 
                        ON al.album_id = aa.album_id
                    WHERE album_release_year = 2020) no
                ON ar.artist_id = no.artist_id
            WHERE no.artist_id IS NULL
            ORDER BY Исполнители ;
        """},
        {'task': f'--5. названия сборников, в которых присутствует конкретный исполнитель'
                 f' ({task5_singer})',
         'select':
            f"""
            SELECT c.collection_name Сборники
            FROM relate_track_into_collection tc
            JOIN music_collections c
                ON c.collection_id = tc.collection_id
            JOIN music_tracks t
                ON t.track_id = tc.track_id
            JOIN music_albums al
                ON al.album_id = t.album_id
            JOIN relate_artist_into_album aa
                ON aa.album_id = al.album_id
            JOIN music_artists ar
                ON ar.artist_id = aa.artist_id
            WHERE lower(ar.artist_name) = '{task5_singer}'
            ORDER BY Сборники ;
        """},
        {'task': '--6. название альбомов, в которых присутствуют исполнители более 1 жанра',
         'select':
            """
            SELECT al.album_name Альбомы
                    -- , ga.artist_id артисты,
                    --   COUNT(ga.genre_id) жанров
            FROM relate_artist_into_album aa
            JOIN music_albums al
                ON al.album_id = aa.album_id
            JOIN relate_genre_into_artist ga
                ON ga.artist_id = aa.artist_id
            GROUP BY ga.artist_id, al.album_name
            HAVING COUNT(ga.genre_id) > 1
            ORDER BY Альбомы ;
        """},
        {'task': '--7. наименование треков, которые не входят в сборники',
         'select':
            """
            SELECT track_name Треки 
                    -- , t.track_id
            FROM music_tracks t 
            LEFT JOIN relate_track_into_collection no
                ON t.track_id = no.track_id
            WHERE no.track_id IS NULL
            ORDER BY Треки ;
        """},
        {'task': '--8. исполнителя(-ей), написавшего(-их)'
                 ' самый короткий по продолжительности трек'
                 '\n\t(теоретически таких треков может быть несколько)',
         'select':
            """
            SELECT artist_name Исполнители
            FROM music_artists ar
            JOIN relate_artist_into_album aa
                ON aa.artist_id = ar.artist_id
            JOIN music_albums al 
                ON al.album_id = aa.album_id
            JOIN music_tracks t 
                ON t.album_id = al.album_id
            WHERE track_duration = ( SELECT MIN(track_duration)
                        FROM music_tracks t )
            ORDER BY Исполнители ;
        """},
        {'task': '--9. название альбомов, содержащих наименьшее количество треков',
         'select':
            """
            SELECT album_name альбомы 
                -- , COUNT(track_id) треков
            FROM music_albums al
            JOIN music_tracks t 
                ON t.album_id = al.album_id
            GROUP BY al.album_id
            HAVING  COUNT(track_id) = ( SELECT COUNT(track_id) треков
                                FROM music_albums al
                                JOIN music_tracks t 
                                    ON t.album_id = al.album_id
                                GROUP BY al.album_id
                                ORDER BY треков
                                LIMIT 1)
            ORDER BY альбомы ;
        """}
    ]
    return select_list
