# cs50p-final-project
### [Video Demo](https://youtu.be/BSphT03alDo)

# Overview
This is a Python project that uses the Spotify Web API to analyze and recommend songs, artists, and albums to users. The project provides a menu that allows the user to choose one of four options:

1. Playlist Analysis
This option allows the user to input the URL of a Spotify playlist, and the program will analyze the playlist's audio features (danceability, energy, and valence) to determine the playlist's personality traits. The personality traits will be described using a dictionary of personality trait types and the corresponding personality traits that fit each personality type. Then, a textual description of the personality traits that best fit the playlist is provided to the user.

2. Similar Song Recommendations
This option allows the user to input the URL of a Spotify track, and the program will use the track's audio features to recommend ten similar tracks to the user. The recommended tracks have similar energy, danceability, and valence values to the input track.

3. Similar Artist Recommendations
This option allows the user to input the URL of a Spotify artist page, and the program will recommend ten similar artists to the user. The recommended artists have a similar musical style to the input artist.

4. Similar Album Recommendations
This option allows the user to input the URL of a Spotify album, and the program will recommend ten similar albums to the user. The recommendation is based on the five most popular tracks from the input album. The recommended albums have similar energy, danceability, and valence values to the input album.

The project is written in Python and uses the Spotipy library to communicate with the Spotify Web API. The code is well-organized and contains comments that explain the purpose and functionality of each function. The program is designed to be user-friendly and intuitive, making it easy for users to understand and navigate the different options.

To use the program, the user needs to have a Spotify account and register an application with the Spotify Developer Dashboard to obtain a client ID and client secret. Then, the user can set up the Spotipy library by providing the client ID and client secret. The user also needs to grant the program access to their Spotify account to use the Spotify Web API.

Overall, this project provides a useful and informative tool for Spotify users who want to discover new music that matches their personal tastes and preferences.

# Technologies

- Python
- Spotipy (Python library for the Spotify Web API)
- Spotify Developer Dashboard (for client and secret IDs)

# Basic Functionality

- valid_url(url) function: Validates the input URL and extracts the ID of the Spotify object (track, artist, album, or playlist).
- get_playlist_analysis(playlist_id) function: Analyzes the given Spotify playlist and returns a brief description of the playlist.
- get_similar_songs(track_id, exclude_track_id=None) function: Provides recommendations for similar songs based on the given track ID.
- get_similar_artists(artist_id) function: Provides recommendations for similar artists based on the given artist ID.
- get_similar_albums(album_id, exclude_album_id=None) function: Provides recommendations for similar albums based on the given album ID.
- get_audio_features(track_ids) function: Retrieves audio features for a list of tracks.

# How to Use

1. Clone the repository onto your local machine.
2. Create an app on the Spotify Developer Dashboard and get the client and secret IDs.
3. In the command line, navigate to the project directory and install Spotipy by running pip install spotipy.
4. Run python main.py to start the application.
5. Select one of the following options:
- Playlist Analysis: Enter the Spotify playlist page URL to get a brief analysis of the playlist.
- Similar Song Recommendations: Enter the Spotify track page URL to get recommendations for similar songs.
- Similar Artist Recommendations: Enter the Spotify artist page URL to get recommendations for similar artists.
- Similar Album Recommendations: Enter the Spotify album page URL to get recommendations for similar albums.
6. The application will display the results based on your input.

# How to Use

1. Go to https://developer.spotify.com/dashboard/ and log in with your Spotify account.
2. Click on the "Create an App" button and fill in the necessary details.
3. Once the app is created, you will see the client ID and client secret. Use these in the application to authorize access to the Spotify API.
