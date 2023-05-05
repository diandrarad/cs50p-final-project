# Credits to spotipy library and Spotify API
# -----------------------------------------
# This project uses spotipy, a Python library for the Spotify Web API.
# https://github.com/plamere/spotipy

# It also uses the Spotify API to access music data.
# https://developer.spotify.com/

import re
import spotipy
import sys

from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


def main():
    print()
    print("Welcome to the Spotify playlist analysis and recommendation system")
    print()
    while True:
        try:
            # Prompt user to choose feature
            print("Choose a feature:")
            print("1. Playlist Analysis")
            print("2. Similar Song Recommendations")
            print("3. Similar Artist Recommendations")
            print("4. Similar Album Recommendations")
            print()
            choice = input("Enter choice (1/2/3/4): ")

            # Handle feature selection
            if choice == '1':
                # Prompt user for track ID
                playlist_id = valid_url(input("Enter Spotify playlist page URL: "))
                print()

                # Get audio features for track
                analysis = get_playlist_analysis(playlist_id)

                # Print results
                print(analysis)
                print()

            elif choice == '2':
                # Prompt user for track ID
                track_id = valid_url(input("Enter Spotify track page URL: "))
                print()

                # Get similar songs for track
                similar_tracks = get_similar_songs(track_id)

                # Print results
                print("Similar songs:")
                for i, track in enumerate(similar_tracks):
                    print(i+1, ".", track['name'], "by", track['artists'][0]['name'])
                print()

            elif choice == '3':
                # Prompt user for artist ID
                artist_id = valid_url(input("Enter Spotify artist page URL: "))
                print()

                # Get similar artists
                similar_artist = get_similar_artists(artist_id)

                # Print results
                print("Similar artists:")
                for i, artist in enumerate(similar_artist[:10]):
                    print(i+1, ".", artist)
                print()

            elif choice == '4':
                # Prompt user for album ID
                album_id = valid_url(input("Enter Spotify album page URL: "))
                print()

                # Get similar albums
                similar_albums = get_similar_albums(album_id)

                # Print results
                print("Similar albums:")
                for i, album in enumerate(similar_albums):
                    print(i+1, ".", album['name'], "by", album['artists'][0]['name'])
                print()

        except (KeyboardInterrupt, EOFError):
            sys.exit("")



def valid_url(url):
    # Regular expression to match the track/artist/album ID
    pattern = r"(?:https:\/\/)?(?:www\.)?open\.spotify\.com\/(?P<type>track|artist|album|playlist)\/(?P<id>[a-zA-Z0-9]+)"

    match = re.search(pattern, url)

    if match:
        track_id = match.group('id')
        return track_id
    else:
        sys.exit("Invalid Spotify URL")



def get_playlist_analysis(playlist_id):
    """
    Function to retrieve similar songs for a track
    """
    try:
        # Get tracks of the playlist
        results = sp.playlist_items(playlist_id, fields='items.track.id,total', additional_types=['track'])
    except spotipy.exceptions.SpotifyException as e:
        if e.http_status == 404:
            sys.exit("Invalid playlist ID.")
        else:
            sys.exit("An error occurred: {}".format(e))

    track_ids = []
    total_tracks = results['total']

    while len(track_ids) < total_tracks:
        items = results['items']
        for item in items:
            track = item['track']
            if track is not None:
                track_ids.append(track['id'])

        if 'next' in results:
            results = sp.next(results)
        else:
            break

    # Get average audio features for the playlist
    avg_audio_features = get_audio_features(track_ids)

    # Define personality traits based on average audio features
    personality_traits = {
        'danceability': {
            'low': "You may have a more reserved personality and prefer activities that require less physical exertion and social interaction.",
            'medium': "You are likely to have a balanced personality and enjoy activities that involve moderate physical exertion and social interaction.",
            'high': "You may have an outgoing personality and enjoy activities that involve a lot of physical exertion and social interaction."
        },
        'energy': {
            'low': "You may have a more laid-back personality and enjoy activities that require less effort and stimulation.",
            'medium': "You are likely to have a balanced personality and enjoy activities that involve a moderate level of effort and stimulation.",
            'high': "You may have a driven and ambitious personality and enjoy activities that involve a lot of effort and stimulation."
        },
        'valence': {
            'low': "You may have a more reserved and introspective personality, and prefer activities that allow for quiet reflection and contemplation.",
            'medium': "You are likely to have a balanced personality and enjoy a mix of activities that involve both positive and negative emotions.",
            'high': "You may have an outgoing and positive personality and enjoy activities that evoke a strong sense of happiness and excitement."
        }
    }

    # Determine personality based on average audio features
    personality = {
        'danceability': 'medium',
        'energy': 'medium',
        'valence': 'medium'
    }
    for feature in personality:
        if avg_audio_features[feature] < 0.4:
            personality[feature] = 'low'
        elif avg_audio_features[feature] > 0.6:
            personality[feature] = 'high'

    # Generate philosophical description of user's characteristics
    description = f"{personality_traits['danceability'][personality['danceability']]} " \
        f"{personality_traits['energy'][personality['energy']]} " \
        f"{personality_traits['valence'][personality['valence']]}"

    return description



def get_similar_songs(track_id, exclude_track_id=None):
    """
    Function to retrieve similar songs
    """
    try:
        # Get audio features for track
        features = sp.audio_features(tracks=[track_id])[0]
    except spotipy.exceptions.SpotifyException as e:
        if e.http_status == 404:
            sys.exit("Invalid artist ID.")
        else:
            sys.exit("An error occurred: {}".format(e))

    # Set up exclude tracks list if specified
    exclude = [exclude_track_id] if exclude_track_id is not None else []

    # Get similar tracks based on audio features
    similar_tracks = sp.recommendations(seed_tracks=[track_id], target_energy=features['energy'], target_danceability=features['danceability'], target_valence=features['valence'], exclude=exclude, limit=10)['tracks']

    return similar_tracks



def get_similar_artists(artist_id):
    """
    Function to retrieve similar artists
    """
    try:
        # Get similar artists based on artist ID
        similar_artists = sp.artist_related_artists(artist_id)['artists']
    except spotipy.exceptions.SpotifyException as e:
        if e.http_status == 404:
            sys.exit("Invalid artist ID.")
        else:
            sys.exit("An error occurred: {}".format(e))

    # Extract artist names from similar_artists
    similar_artist_names = [artist['name'] for artist in similar_artists]

    return similar_artist_names



def get_similar_albums(album_id, exclude_album_id=None):
    """
    Function to retrieve similar albums
    """
    try:
        # Get tracks of the album
        album_tracks = sp.album_tracks(album_id, limit=50)['items']
    except spotipy.exceptions.SpotifyException as e:
        if e.http_status == 404:
            sys.exit("Invalid album ID.")
        else:
            sys.exit("An error occurred: {}".format(e))
    track_ids = [track['id'] for track in album_tracks][:5]

    # Get average audio features for the album
    avg_audio_features = get_audio_features(track_ids)

    # Get similar tracks based on audio features
    similar_albums = sp.recommendations(seed_tracks=track_ids, target_energy=avg_audio_features['energy'], target_danceability=avg_audio_features['danceability'], target_valence=avg_audio_features['valence'], limit=10)['tracks']

    # Extract album information for the recommended albums
    recommended_albums = []
    for track in similar_albums:
        album_id = track['album']['id']
        if album_id == exclude_album_id:
            continue
        album = sp.album(album_id)
        recommended_albums.append(album)

    return recommended_albums



def get_audio_features(track_ids):
    """
    Given a list of track IDs, returns a dictionary with the average of each audio feature across all tracks.
    """
    # Get audio features for each track
    album_audio_features = []
    for track_id in track_ids:
        features = sp.audio_features(track_id)
        if features:
            album_audio_features.append(features[0])

    # Calculate the average of each audio feature
    avg_audio_features = {}
    for feature in album_audio_features[0]:
        # If the feature is numeric, calculate the average by summing up all the values for the feature and dividing by the number of tracks
        if isinstance(album_audio_features[0][feature], (int, float)):
            avg_audio_features[feature] = sum([track[feature] for track in album_audio_features]) / len(album_audio_features)
        # If the feature is a string, convert numeric values to float and then calculate the average
        else:
            numeric_features = {k: float(v) for k, v in album_audio_features[0].items() if isinstance(v, (int, float))}
            avg_audio_features[feature] = sum([v for v in numeric_features.values()]) / len(numeric_features)

    return avg_audio_features



if __name__ == "__main__":
    main()
