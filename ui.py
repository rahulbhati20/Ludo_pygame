import pygame
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox


def validate_num_players_input(value):
    try:
        value = int(value)
        if 2 <= value <= 4:
            return value
        else:
            return None
    except ValueError:
        return None

def is_valid_number(s):
    return s in ["2", "3", "4"]  

def get_player_information():
    def bg():
        pygame.mixer.music.load("sound/bg.mp3")
        pygame.mixer.music.play()
    def bg_stop():
        pygame.mixer.music.stop()
    def sub():
        pygame.mixer.music.load("sound/loading.mp3")
        pygame.mixer.music.play()

    bg()
    
    root = tk.Tk()
    root.title("Ludo Player Information")
    root.geometry("750x600+385+100")  # Adjust the window size
    root.resizable(0, 0)  # Make the window not resizable
    colors = ['Red', 'Green', 'Yellow', 'Blue']
    color_index = 0  # Index to track the current color
    bg_image = Image.open("img/bg1.png")
    resized_bg_image = bg_image.resize((750, 600), Image.LANCZOS)
    root.iconbitmap('icon.ico')


    def on_window_close():
        pygame.quit()  # Quit Pygame when the Tkinter window is closed
        root.destroy()  # Destroy the Tkinter window

    root.protocol("WM_DELETE_WINDOW", on_window_close)  # Bind the close event

    def check_number():
        user_input = entry_num_players.get()
        if is_valid_number(user_input):
            pass
        elif user_input== "":
            messagebox.showerror('No Entry','please enter the number first .')
        else:
            label_num_players_1 = tk.Label(root, text=f"{user_input} is not a valid number!", font=("Arial", 18),fg='red', bd=0.5, highlightthickness=0.5)
            label_num_players_1.pack(pady=10) 
    
        def remove_check_number():
            try:
                if label_num_players_1:  
                    label_num_players_1.after(2000, label_num_players_1.destroy)
            except:print("")

        remove_check_number()           
    
    # Convert the resized image to a format that Tkinter can use
    background_image = ImageTk.PhotoImage(resized_bg_image)

    # Create a label with the background image
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    label_num_players = tk.Label(root, text="Enter the number of players (2-4):", font=("Arial", 18), bg='teal',fg='black', bd=1, highlightthickness=1)
    label_num_players.pack(pady=(150, 10))

    entry_num_players = tk.Entry(root, font=("Arial", 20),bd=1, highlightthickness=1)
    entry_num_players.pack(pady=10)
    entry_num_players.focus_set()  # Set focus to this entry box
    
    player_names = []
    num_players_submitted = False  # Flag to track if number of players has been submitted

        
    def submit_num_players():
        nonlocal color_index  # Use nonlocal to modify the color_index
        nonlocal num_players_submitted
        global number_of_players

        number_of_players = entry_num_players.get()
        number_of_players = validate_num_players_input(number_of_players)

        if number_of_players:
            num_players_submitted = True  # Number of players has been submitted
            entry_num_players.config(state=tk.DISABLED)  # Disable the entry box
            submit_button_num_players.config(state=tk.DISABLED)  # Disable the submit button

            # Show the entry box and submit button for entering player names
            entry_player.pack(pady=10)
            submit_button_player.pack(pady=10)
            create_name_entry(1)  # Start with Player 1
        else:
            label_num_players_1 = tk.Label(root, text="Please enter a valid number of players (2-4)!", font=("Arial", 18),
                                        fg='red', bd=0.5, highlightthickness=0.5)
            label_num_players_1.pack(pady=10)

            def remove_check_number():
                try:
                    if label_num_players_1:
                        label_num_players_1.after(2000, label_num_players_1.destroy)
                except:
                    print("")

            remove_check_number()
        
    def submit_num_check_num(event=None): 
        global label_num_players_1
        # Add an event parameter
        submit_num_players()
        check_number()

    # Bind the Enter key to the submit_num_check_num function
    root.bind('<Return>', submit_num_check_num)

    def create_name_entry(player_number):
        nonlocal color_index  # Use nonlocal to modify the color_index
        
        if num_players_submitted:
            if player_number <= number_of_players:
                label_player.config(text=f"Enter name for Player {player_number} (Color: {colors[color_index]}):")
                entry_player.delete(0, tk.END)  # Clear the entry for the next player
                entry_player.focus_set()

                def submit_player_name(event=None):  # Add an event parameter
                    nonlocal color_index  # Use nonlocal to modify the color_index
                    name = entry_player.get()[0:20]  # Limit name to 20 characters
                    entry_player.delete(0, tk.END)  # Clear the entry
                    if name:
                        player_names.append((name, colors[color_index]))
                        create_name_entry(player_number + 1)  # Move to the next player

                submit_button_player.config(command=submit_player_name)

                # Bind the Enter key to the submit_player_name function
                root.bind('<Return>', submit_player_name)

                color_index = (color_index + 1) % len(colors)  # Update color index for the next player
            else:
                root.destroy()
        else:
            entry_player.pack_forget()  # Hide the entry box
            submit_button_player.pack_forget()  # Hide the submit button

    submit_button_num_players = tk.Button(root, text="Proceed", font=("Arial", 18),command=submit_num_check_num)
    submit_button_num_players.pack(pady=10)

    label_player = tk.Label(root, text="", font=("Arial", 18), bg='teal',
                                fg='black', bd=1, highlightthickness=1)
    label_player.pack(pady=10)

    entry_player = tk.Entry(root, font=("Arial", 20), validate="key",bd=1, highlightthickness=1)

    submit_button_player = tk.Button(root, text="Submit", font=("Arial", 18))

    root.mainloop()
    bg_stop()
    sub()

    if number_of_players is None:
        pygame.quit()
        exit()  # Exit if the user canceled the input

    return number_of_players, player_names
