# [SQLPY-49] 5. Музыкальный сервис
# к лекции «Группировки, выборки из нескольких таблиц»


def create_tables(connection):
    # --СОЗДАДИМ ОТНОШЕНИЯ:
    connection.execute("""
        CREATE TABLE IF NOT EXISTS music_genres(
            genre_id SERIAL PRIMARY KEY,
            genre_name TEXT NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS music_artists(
            artist_id SERIAL PRIMARY KEY,
            artist_name TEXT NOT NULL UNIQUE
        );
        CREATE TABLE IF NOT EXISTS music_albums(
            album_id SERIAL PRIMARY KEY,
            album_name TEXT NOT NULL,
            album_release_year NUMERIC(4)
        );
        CREATE TABLE IF NOT EXISTS music_tracks(
            track_id SERIAL PRIMARY KEY,
            track_name TEXT NOT NULL,
            track_duration NUMERIC(4)
        );
        CREATE TABLE IF NOT EXISTS music_collections(
            collection_id SERIAL PRIMARY KEY,
            collection_name TEXT NOT NULL,
            collection_release_year NUMERIC(4)
        );
    """)


def create_relations(connection):
    # --ПОСТРОИМ СВЯЗИ:
    connection.execute(""" 
        --добавим в табл.треков огр-е внеш.ключа для столбца с альбомами
        ALTER TABLE music_tracks         
        ADD COLUMN album_id INTEGER  
        REFERENCES music_albums ; 
    """)
    connection.execute(""" 
        --1. создадим табл-связей для таблиц певцов и жанров
        CREATE TABLE IF NOT EXISTS relate_genre_into_artist(
            genre_id INTEGER REFERENCES music_genres(genre_id) ,
            artist_id INTEGER references music_artists(artist_id) ,
            CONSTRAINT pk_artist_into_genre PRIMARY KEY (genre_id , artist_id)
        );
        --2. создадим табл-связей для таблиц альбомов и певцов
        CREATE TABLE IF NOT EXISTS relate_artist_into_album(
            album_id INTEGER REFERENCES music_albums(album_id) ,
            artist_id INTEGER REFERENCES music_artists(artist_id) ,
            CONSTRAINT pk_artist_into_album PRIMARY KEY (album_id , artist_id)
        );
         --3. создадим табл-связей для таблиц альбомов и певцов
        CREATE TABLE IF NOT EXISTS relate_track_into_collection(
            collection_id INTEGER REFERENCES music_collections(collection_id) ,
            track_id INTEGER REFERENCES music_tracks (track_id) ,
            CONSTRAINT pk_track_into_collection PRIMARY KEY (collection_id , track_id)
        );
    """)


def drop_tables(connection):
    # --УДАЛИМ ОТНОШЕНИЯ:
    connection.execute("""
        DROP TABLE IF EXISTS relate_track_into_collection ;
        DROP TABLE IF EXISTS relate_genre_into_artist ;
        DROP TABLE IF EXISTS relate_artist_into_album ;
        
        DROP TABLE IF EXISTS music_genres ;
        DROP TABLE IF EXISTS music_tracks ;
        DROP TABLE IF EXISTS music_collections ;
        DROP TABLE IF EXISTS music_artists ;
        DROP TABLE IF EXISTS music_albums ;
    """)
