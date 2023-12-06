

class AlbumResource(Resource):
    @marshal_with(album_fields)
    def get(self, album_id):
        album = Album.query.get_or_404(album_id)
        # Fetch associated songs for the album
        songs = Song.query.filter_by(album_id=album_id).all()
        album.songs = songs
        return album


class AlbumListResource(Resource):
    @marshal_with(album_fields)
    def get(self):
        albums = Album.query.all()
        return albums

