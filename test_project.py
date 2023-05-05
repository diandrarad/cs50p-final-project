import pytest
from project import valid_url, get_playlist_analysis, get_similar_songs, get_similar_artists, get_similar_albums, get_audio_features

def test_valid_url():
    url1 = "https://open.spotify.com/track/5LYMamLv12UPbemOaTPyeV"
    url2 = "https://open.spotify.com/album/6b4JxTjcHZljZtpDMfsnz2"
    url3 = "https://open.spotify.com/playlist/37i9dQZEVXcXjJlADxMF2c"
    url4 = "https://open.spotify.com/artist/6KImCVD70vtIoJWnq6nGn3"

    assert valid_url(url1) == "5LYMamLv12UPbemOaTPyeV"
    assert valid_url(url2) == "6b4JxTjcHZljZtpDMfsnz2"
    assert valid_url(url3) == "37i9dQZEVXcXjJlADxMF2c"
    assert valid_url(url4) == "6KImCVD70vtIoJWnq6nGn3"

    # Test invalid URL
    with pytest.raises(SystemExit):
        assert valid_url("https://www.spotify.com")


def test_get_playlist_analysis():
    # Test with a playlist containing average energy, high-danceability, and average valence tracks
    playlist_id = '3UTeB206tSHAL2jCyTBcZj'
    expected_description = (
        "You are likely to have a balanced personality and enjoy activities that involve moderate physical exertion and social interaction. "
        "You may have a driven and ambitious personality and enjoy activities that involve a lot of effort and stimulation. "
        "You are likely to have a balanced personality and enjoy a mix of activities that involve both positive and negative emotions."
    )
    assert get_playlist_analysis(playlist_id) == expected_description


def test_get_similar_songs():
    track_id = '5QTxFnGygVM4jFQiBovmRo'  # A valid track ID for testing
    similar_tracks = get_similar_songs(track_id)

    # Check if similar_tracks is a list with length 10
    assert type(similar_tracks) == list
    assert len(similar_tracks) == 10

    # Check if all tracks in similar_tracks have the required keys
    required_keys = ['name', 'artists', 'id']
    for track in similar_tracks:
        assert all(key in track for key in required_keys)


def test_get_similar_artists():
    # Test with valid artist ID
    similar_artists = get_similar_artists('6KImCVD70vtIoJWnq6nGn3')
    assert len(similar_artists) > 0

    # Test with invalid artist ID
    with pytest.raises(SystemExit) as e:
        get_similar_artists('invalid_artist_id')
    assert e.type == SystemExit


def test_get_similar_albums():
    # Test with a valid album ID
    album_id = '1vLSCKG73JSr0uI68aOKOo'
    similar_albums = get_similar_albums(album_id)
    assert len(similar_albums) == 10

    # Test with an invalid album ID
    invalid_album_id = 'invalid_id'
    with pytest.raises(SystemExit):
        get_similar_albums(invalid_album_id)


def test_get_audio_features():
    # Test with a list of tracks that have audio features available
    track_ids = ['4D7BCuvgdJlYvlX5WlN54t', '3HEn14GqygLCNfroOnYiZb']
    expected_output = {'danceability': 0.737, 'energy': 0.4305, 'key': 3.0, 'loudness': -8.9755, 'mode': 1.0, 'speechiness': 0.1918, 'acousticness': 0.565, 'instrumentalness': 0.0002811, 'liveness': 0.11599999999999999, 'valence': 0.383, 'tempo': 120.1065, 'type': 14948.139661938463, 'id': 14948.139661938463, 'uri': 14948.139661938463, 'track_href': 14948.139661938463, 'analysis_url': 14948.139661938463, 'duration_ms': 205610.0, 'time_signature': 4.0}
    assert get_audio_features(track_ids) == expected_output
