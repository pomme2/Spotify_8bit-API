# Spotify 8-Bit Album Guessing Game 🎶

Spotify 8-Bit is an interactive guessing game that challenges players to identify pixelated album covers from a chosen artist. The game uses the Spotify API to retrieve album data and dynamically generates multiple-choice questions. There are various levels of difficulty, including an Expert mode with black-and-white album covers and a timer to test your knowledge under pressure!

## Features 🌟

- **Pixelated Album Covers**: Album covers are pixelated to add a nostalgic 8-bit feel.
- **Difficulty Levels**:
  - **Easy**: Guess the album name correctly 3 times in a row without time pressure.
  - **Normal**: Guess both the album name and release year correctly for each album.
  - **Expert**: Identify black-and-white pixelated covers within 10 seconds, guessing both album name and year.
- **High Score Tracking**: Tracks and saves your highest score for competitive play.
- **Streak Bonus**: Build your streak by answering correctly for additional points.

## Screenshots 📸

- **Easy Mode**: ![game_easy](https://github.com/user-attachments/assets/1965931d-6e43-48a7-ad72-6d0f6ca2dd6b)

- 
- **Expert Mode**: ![hard_mode](https://github.com/user-attachments/assets/f4c06423-7048-46cf-b4d0-bb06659ff15d)


### Example Screenshots:
1. Pixelated album cover (Easy Mode)
2. Black-and-white album cover (Expert Mode)

## How It Works ⚙️

### Spotify API Integration

The application uses the **Spotify Web API** to fetch album data for a chosen artist. Here’s a breakdown of the Spotify API endpoints used:

1. **Authentication**: The app uses **client credentials** flow to request an access token from the Spotify API.
2. **Search for Artist**: The app searches for the artist using the `/v1/search` endpoint.
3. **Retrieve Albums**: Once an artist is identified, the app fetches the top 10 albums using the `/v1/artists/{id}/albums` endpoint.

The app doesn’t use Spotify’s playback API, but it leverages album cover images and metadata to create a unique guessing experience. Album covers are pixelated using PIL (Python Imaging Library) to add a fun retro aesthetic.

### App Logic

- **Difficulty Selection**: The game provides three difficulty levels, impacting the pixelation and additional challenges (like timers and black-and-white filters).
- **Dynamic UI**: Tkinter is used to create a responsive interface that updates based on user choices.
- **Game Flow**:
  - The player selects the correct album from four options.
  - For Normal and Expert modes, players are prompted to guess the release year after selecting the correct album name.
  - The player earns points for consecutive correct guesses, and the game tracks high scores.

## Installation 🛠️

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/spotify-8bit-album-guessing-game.git
   cd spotify-8bit-album-guessing-game
