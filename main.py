import os
import base64
import json
import random
import time
from dotenv import load_dotenv
from requests import post, get
from PIL import Image, ImageTk, ImageOps  # ImageOps for black-and-white filter
import requests
from io import BytesIO
import tkinter as tk

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# High score file
HIGHSCORE_FILE = "highscore.txt"

# Functions to get token and make API calls
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {"Authorization": "Basic " + auth_base64, "Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    return json_result["access_token"]

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    result = get(url + query, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    return json_result[0] if json_result else None

def get_albums_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    return json.loads(result.content)["items"][:10]  # Top 10 albums

def save_album_cover_art(url, grayscale=False):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        pixel_size = 55
        img = img.resize((img.size[0] // pixel_size, img.size[1] // pixel_size), Image.NEAREST)
        img = img.resize((img.size[0] * pixel_size, img.size[1] * pixel_size), Image.NEAREST)
        if grayscale:
            img = ImageOps.grayscale(img)
        return img
    else:
        return None

# Game variables
albums = []
score = 0
high_score = 0
difficulty = "Easy"  # Default difficulty
current_album = None  # Track current album for year guessing
previous_album = None  # Track previous album to avoid repeats

# Load high score from file
def load_high_score():
    global high_score
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as file:
            high_score = int(file.read().strip())
    else:
        high_score = 0

# Save high score to file
def save_high_score():
    with open(HIGHSCORE_FILE, "w") as file:
        file.write(str(high_score))

# UI Functions
def start_game(selected_difficulty):
    global difficulty, albums, score
    difficulty = selected_difficulty
    artist_name = entry_artist.get().strip()
    
    if not artist_name:
        display_feedback("Please enter an artist name", color="red")
        return

    token = get_token()
    artist = search_for_artist(token, artist_name)
    if not artist:
        display_feedback("Artist not found", color="red")
        return

    albums = get_albums_by_artist(token, artist["id"])
    if len(albums) < 4:
        display_feedback("Not enough albums to play the game", color="red")
        return

    # Hide menu frame and show game frame
    frame_menu.pack_forget()
    frame_game.pack(fill="both", expand=True)
    
    score = 0
    update_score()
    start_new_round()

def start_new_round():
    global current_album, previous_album, round_start_time
    
    # Check win condition for Easy and Normal mode
    if score >= 3:
        display_feedback("You won the game!", color="green")
        update_high_score()
        reset_game()
        return

    if not albums:
        display_feedback("No more albums available.", color="red")
        reset_game()
        return

    # Choose a random album, ensuring it's not the same as the previous one
    while True:
        current_album = random.choice(albums)
        if current_album != previous_album:
            break
    previous_album = current_album
    album_cover_url = current_album["images"][0]["url"]
    grayscale = difficulty == "Expert"

    # Clear previous widgets
    for widget in frame_game.winfo_children():
        widget.destroy()
  

      # Display the album cover
    img = save_album_cover_art(album_cover_url, grayscale=grayscale)
    
    # Resize the image to a smaller size, e.g., 100x100 pixels
    if img:
        img = img.resize((340, 340), Image.LANCZOS)  # Adjust the width and height as needed
        img_tk = ImageTk.PhotoImage(img)
        
        label_img = tk.Label(frame_game, image=img_tk, bg="#f0f4f7")
        label_img.image = img_tk
        label_img.pack(pady=10)

    # Generate answer options for album name
    album_names = [album["name"] for album in albums]
    wrong_answers = random.sample([name for name in album_names if name != current_album["name"]], 3)
    options = wrong_answers + [current_album["name"]]
    random.shuffle(options)

    # Display answer buttons for album name
    for option in options:
        button = tk.Button(
            frame_game,
            text=option,
            command=lambda o=option: check_album_name(o),
            font=("Helvetica", 12),
            bg="#d1e7f3",
            fg="#34495e",
            activebackground="#a6d2e6",
            width=30,
            height=2,
            relief="solid",
            bd=1,
        )
        button.pack(pady=5)

def check_album_name(selected_name):
    if selected_name == current_album["name"]:
        increment_score()
        display_feedback("Correct!", color="green")
        start_new_round()
    else:
        reset_round("Incorrect! Score reset. Try again.")

def increment_score():
    global score
    score += 1
    update_score()

def update_score():
    score_label.config(text=f"Score: {score} | High Score: {high_score}")

def update_high_score():
    global high_score
    if score > high_score:
        high_score = score
        save_high_score()
        display_feedback("New High Score!", color="blue")

def display_feedback(message, color="black"):
    feedback_label.config(text=message, fg=color)
    feedback_label.after(2000, lambda: feedback_label.config(text=""))  # Clear feedback after 2 seconds

def reset_round(message):
    global score
    score = 0
    update_score()
    display_feedback(message, color="red")
    start_new_round()

def reset_game():
    global score
    score = 0
    update_score()
    frame_game.pack_forget()
    show_menu()

def show_menu():
    frame_menu.pack(fill="both", expand=True)
    frame_game.pack_forget()

# UI Components
root = tk.Tk()
root.title("SPOTIFY_8BIT")
root.geometry("450x600")
root.configure(bg="#f0f4f7")  # Light background color

# Menu Frame
frame_menu = tk.Frame(root, bg="#f0f4f7")
label_title = tk.Label(frame_menu, text="SPOTIFY_8BIT", font=("Helvetica", 20, "bold"), bg="#f0f4f7", fg="#34495e")
label_title.pack(pady=20)

entry_artist = tk.Entry(frame_menu, width=30, font=("Helvetica", 12))
entry_artist.pack(pady=10)

button_easy = tk.Button(frame_menu, text="Easy", command=lambda: start_game("Easy"), font=("Helvetica", 14), width=10)
button_normal = tk.Button(frame_menu, text="Normal", command=lambda: start_game("Normal"), font=("Helvetica", 14), width=10)
button_expert = tk.Button(frame_menu, text="Expert", command=lambda: start_game("Expert"), font=("Helvetica", 14), width=10)

button_easy.pack(pady=5)
button_normal.pack(pady=5)
button_expert.pack(pady=5)

frame_menu.pack(fill="both", expand=True)

# Game Frame
frame_game = tk.Frame(root, bg="#f0f4f7", padx=10, pady=10, relief="solid", bd=1)

score_label = tk.Label(root, font=("Helvetica", 12), bg="#f0f4f7", fg="black")
score_label.pack()
feedback_label = tk.Label(root, font=("Helvetica", 12), bg="#f0f4f7", fg="black")
feedback_label.pack(pady=5)

# Load high score on start
load_high_score()
update_score()

root.mainloop()
