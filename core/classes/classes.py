class Album:
    def __init__(self, title, songs):
        # Init elements #
        self.title = title
        self.count = len(songs)
        self.songs = songs

    def calculate_average_streams(self):
        songs = self.songs
        # To sort the list in place...
        songs.sort(key=lambda x: x.streams, reverse=True)
        songs = songs[3:-1]
        # most_streamed_song = max(songs, key=lambda x: x.streams)
        # songs.pop(songs.index(most_streamed_song))
        # most_streamed_song = max(songs, key=lambda x: x.streams)
        # songs.pop(songs.index(most_streamed_song))
        total_streams = sum(song.streams for song in songs)
        return int(total_streams / self.count)

    def __repr__(self) -> str:
        return f"{self.title} ({self.count})"

class Song:
    def __init__(
        self,
        title=str,
        sequence=int,
        streams=int,
        listeners=int,
        views=int,
        saves=int,
        first_released=str,
    ):
        # Init elements #
        self.title = title
        self.sequence = sequence
        self.streams = streams
        self.listeners = listeners
        self.views = views
        self.saves = saves
        self.first_released = first_released

    def __repr__(self) -> str:
        return f"{self.title} ({self.streams})"