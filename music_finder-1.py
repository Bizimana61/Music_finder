from apis import spotify, twilio, gui
import customtkinter

## We did Extra Credit: Generate an HTML file. When user clicks the Generate HTML Table button, a table of the recommended tracks and artists with pictures gets saved to Finder. It's in a file labeled tracks_table.html
## We did Exrtra Credit: Allow the user to download a preview of a song. User selects one of their selected tracks and a preview is downloaded to Finder under the song ID which can be opened to the web. 

def main_menu():
    gui.show_text("Select an action via a button!")
    gui.show_text("Currently selected genres: ", append = True)
    gui.show_text(user_selections["genres"], append= True)
    gui.show_text("Currently selected artists: ", append = True)
    gui.show_text(user_selections["artists"], append= True)
    gui.show_text("Currently selected tracks: ", append=True)
    gui.show_text(user_selections["tracks"], append=True)

def quit_program():
    app.destroy()

def select_favorite_genres():
    all_genres = spotify.get_genres(True)
    show_genres = str(gui.show_text(all_genres))
    message = "Type the name of a genre from the below list. Press enter to continue. You may clear selections by typing 'clear'."

    genres = []

    user_genre = gui.popup_input(prompt= message)
    user_selections["genres"].append(user_genre)

    if user_genre == "clear":
        user_selections["genres"].clear()
        main_menu()

    gui.show_text(user_selections["genres"])

    

    # 1. Allow user to select one or more genres using the
    #    spotify.get_genres_abridged() function
    # 2. Allow user to store / modify / retrieve genres
    #    in order to get song recommendations

    # Once done, go back to the main_menu
    main_menu()
          
def select_favorite_artists():
    print("Select favorite artists here...")

    artist_message = "Enter the number corresponding to one of the artists shown in the main window."

    user_artist = gui.popup_input(prompt = "Type in the name of an artist. Type 'clear' to clear your current artist selections.")
    if user_artist == "clear":
        user_selections["artists"].clear()
        main_menu()
        return
    
    spotify_artists = spotify.get_artists(search_term = user_artist, simplify= True)
    table_text = spotify.generate_artists_table(spotify_artists)
        

    gui.show_text(table_text)

    number_input = (gui.popup_input(prompt = artist_message))

    artist_number = int(number_input) - 1 

    specific_artist = spotify_artists[artist_number]
    name = specific_artist["name"]
    id = specific_artist["id"]



    show = user_selections["artists"] [name] = id
    
    gui.show_text(user_selections["artists"])
    # 1. Allow user to search for an artist using
    #    spotify.get_artists() function
    # 2. Allow user to store / modify / retrieve artists
    #    in order to get song recommendations

    # Once done, go back to the main_menu
    main_menu()


def discover_new_music():
    print("Show recommendations here...")
    # 1. Allow user to retrieve song recommendations using the
    #    spotify.get_similar_tracks() function
    # 2. Show them to the user
    # 3. Ask if you want to email them!

    all_genres = user_selections["genres"]
    all_artists_ids = [idx for idx in user_selections["artists"].values()]

    song_recs = spotify.get_similar_tracks(artist_ids=all_artists_ids, genres=all_genres)
    track_table = spotify.generate_tracks_table(song_recs)
    gui.show_text(track_table, append=True)

    email_input = (gui.popup_input("Would you like to send this table to a friend? (y/n)"))

    if email_input.lower() == "y":
        friends_email = (gui.popup_input("Enter the email here: "))

        result = twilio.send_email([friends_email], "Song Recs", spotify.generate_tracks_table(song_recs, to_html = True))

        if result:
            gui.popup("Success!")
        else:
            gui.popup("Email didnt send!")
    elif email_input.lower() == "n":
        x = 1 
    else:
        gui.popup("Enter a valid input!")

    main_menu()

def generate_player_HTML():
    track_ids = [id for id in user_selections["tracks"].values()]

    which_track = int((gui.popup_input("Select which track you want to generate a player of. (eg. 1, 2, 3)"))) - 1

    html_embed = spotify.get_track_player_html(track_ids[which_track])

    file = open(f"{track_ids[which_track]}.html", "w")

    file.write(html_embed)

    gui.popup("Success!")


def generate_html_table():
    all_genres = user_selections["genres"]
    all_artists_ids = [id for id in user_selections["artists"].values()]

    song_recs = spotify.get_similar_tracks(artist_ids=all_artists_ids, genres=all_genres)
    track_table = spotify.generate_tracks_table(song_recs, to_html = True)

    file =  open("tracks_table.html", "w")
    
    file.write("<h2>")
    file.write(track_table)
    file.write("</h2>")

    file.write("<br><h1>Top 5 Song Embeds!</h1>")

    for i in range(5):
        song = song_recs[i]
        html_embed = spotify.get_track_player_html(song["id"])
        file.write(f"<br>{html_embed}<br>")

    gui.popup("Generated Table and Embeds!")

def select_favorite_track():
    print("Select favorite tracks here...")

    track_message = "Enter the number corresponding to one of the tracks shown in the main window."

    user_track = gui.popup_input(prompt = "Type in the name of an track. Type 'clear' to clear your current artist selections.")
    if user_track == "clear":
        user_selections["tracks"].clear()
        main_menu()
        return
    spotify_tracks = spotify.get_tracks(search_term = user_track, simplify= True)
    table_text = spotify.generate_tracks_table(spotify_tracks)
    gui.show_text(table_text)

    number_input = (gui.popup_input(prompt = track_message))

    track_number = int(number_input) - 1 

    specific_track = spotify_tracks[track_number]
    name = specific_track["name"]
    id = specific_track["id"]


    test = user_selections["tracks"] [name] = id
    
    gui.show_text(user_selections["tracks"])

    main_menu()


    


### GLOBAL VARIABLES
user_selections = {
    'genres': [],
    'artists': {},
    'tracks': {}
}

actions = {
    "Main Menu": main_menu,
    "Quit": quit_program,
    "Select Favorite Genres": select_favorite_genres,
    "Select Favorite Artists": select_favorite_artists,
    "Select Favorite Tracks": select_favorite_track,
    "Discover New Music": discover_new_music,
    "Generate Track HTML": generate_player_HTML,
    "Generate HTML Table": generate_html_table
}


######### YOUR CODE ABOVE HERE #################################################
## DO NOT EDIT BELOW THIS LINE WITHOUT ASKING PROF. BAIN FIRST
app = customtkinter.CTk()
gui._setup_window(app, title="Spotify Explorer")
gui._setup_buttons(actions)
main_menu()
app.mainloop()
