# Billboard Top 100 Playlist Creator

## Description
This project is a Python application that creates a Spotify playlist of the top 100 songs from a specified date using data from Billboard's Hot 100 chart. It scrapes the Billboard website for song data, logs into Spotify, creates a new playlist, and adds the top 100 songs to it.

## Features
Web Scraping: Uses requests and BeautifulSoup to scrape the Billboard Hot 100 chart for the top 100 songs of a specified date.

Spotify Integration: Uses the spotipy library to interact with the Spotify API, allowing the creation of playlists and adding tracks to them.

Environment Variables: Utilizes environment variables to securely store API keys and tokens.

Data Persistence: Saves the scraped data to a local file to avoid repeated requests to the Billboard website.

## How It Works
Request Tracks: Prompts the user to input a date (in YYYY-MM format) and requests the top 100 tracks from Billboard's Hot 100 chart for that date.

Parse Data: Uses BeautifulSoup to parse the HTML response and extract the track names and artists.

Spotify Login: Logs into Spotify using the spotipy library and OAuth authentication.

Create Playlist: Creates a new playlist on Spotify with the name "YYYY-MM Billboard Top 100".

Find Track URIs: Searches for each track on Spotify and retrieves its URI.

Add Tracks to Playlist: Adds the retrieved track URIs to the newly created Spotify playlist.
