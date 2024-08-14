import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import csv

class GeneralApplicationGUI:
    def __init__(self, master):
        self.master = master
        self.master.geometry("800x500")
        self.master.title("Video Player Manager")
        self.playlist = []  # Initialize the playlist attribute

        # Create the video details entry
        self.video_details_entry = tk.Entry(self.master)
        self.video_details_entry.grid(row=0, column=0, padx=0, pady=0)

        # Create the add button
        self.add_button = tk.Button(self.master, height=1, width=6, text="Add", command=self.add_video)
        self.add_button.grid(row=1, column=0, padx=0, pady=0)

        # Create the playlist listbox
        self.playlist_listbox = tk.Listbox(self.master, height=10, width=120)
        self.playlist_listbox.grid(row=2, column=0, padx=0, pady=0)

        # Create the play button
        self.play_button = tk.Button(self.master, text="Play", command=self.play_video)
        self.play_button.grid(row=5, column=0, padx=0, pady=0)

        # Create the refresh button
        self.refresh_button = tk.Button(self.master, text="Refresh", command=self.refresh_text_area, height=0, width=0)
        self.refresh_button.grid(row=6, column=0, padx=0, pady=0)

        # Create the search entry
        self.search_entry = tk.Entry(self.master,)
        self.search_entry.grid(row=3, column=0, padx=0, pady=0)

        # Create the search button
        self.search_button = tk.Button(self.master, text="Search", command=self.search_video)
        self.search_button.grid(row=4, column=0, padx=0, pady=0)

        # Create the update button
        self.update_button = tk.Button(self.master, text="Update", command=self.update_video_with_slider)
        self.update_button.grid()

        # Create the delete button
        self.delete_button = tk.Button(self.master, text="Delete", command=self.delete_video)
        self.delete_button.grid()

        # Create the dark mode button
        self.dark_mode_button = tk.Button(self.master, text="Dark Mode", command=self.toggle_theme)
        self.dark_mode_button.grid()

        # Bind the double-click event to the playlist listbox
        self.playlist_listbox.bind("<Double-Button-1>", self.show_video_info)

        # Initialize the playlist
        self.playlist = []

        # Load videos from the CSV file
        self.load_videos()

    def display_playlist(self):
        self.playlist_listbox.delete(0, tk.END)
        for video in self.playlist:
            if len(video) == 3:
                self.playlist_listbox.insert(tk.END, f"{video[0]}: {video[1]}: {video[2]}")

    def add_video(self):
        video_name = self.video_details_entry.get()

        if video_name:
            # Generate the video ID based on the current length of the playlist
            video_id = str(len(self.playlist) + 1).zfill(2)

            # Add the video to the playlist
            self.playlist.append((video_id, video_name, ""))

            # Write the video data to the CSV file
            with open('video_library.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([video_id, video_name, ""])

            # Display the playlist in the listbox
            self.display_playlist()
        else:
            messagebox.showerror("Error", "Please enter a video name.")
    
    def delete_video(self):
        video_id = simpledialog.askstring("Delete Video", "Enter the ID of the video to delete:")

        if len(video_id) == 1:
            video_id = "0" + video_id

        selected_video = next((video for video in self.playlist if video[0] == video_id), None)

        if selected_video:
            # Remove the video from the playlist
            self.playlist.remove(selected_video)

            # Update the IDs of the remaining videos
            for i, video in enumerate(self.playlist):
                video[0] = str(i + 1).zfill(2)

            # Write the updated video data to the CSV file
                with open('video_library.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(self.playlist)

            # Update the playlist listbox
            self.display_playlist()

            # Display a confirmation message
            video_name = selected_video[1]
            messagebox.showinfo("Delete Video", f"Video '{video_name}' deleted successfully.")
        else:
            messagebox.showerror("Error", "Video not found.")

    def refresh_text_area(self):
        # Refresh the listbox
        self.video_details_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)
        self.playlist = []
        self.load_videos()

    def search_video(self):
        search_query = self.search_entry.get()

        # Search for the video in the playlist
        search_results = [video for video in self.playlist if search_query.lower() in video[0].lower() or search_query.lower() in video[1].lower()]

        # If no search results are found, display a warning message
        if not search_results:
            messagebox.showwarning("Warning", "No videos found with the given ID or name.")

        # Display the search results in the listbox
        self.playlist_listbox.delete(0, tk.END)
        for video in search_results:
            self.playlist_listbox.insert(tk.END, f"{video[0]}: {video[1]}: {video[2]}")

    def update_video_with_slider(self):
        video_id = simpledialog.askstring("Update Video", "Enter the ID of the video to update:")

        if len(video_id) == 1:
            video_id = "0" + video_id

        selected_video = next((video for video in self.playlist if video[0] == video_id), None)

        if selected_video:
            # Create a new top-level window for updating the video information
            top = tk.Toplevel()
            top.title("Update Video")

            # Create a label for the video name
            video_name_label = tk.Label(top, text=f"Video Name: {selected_video[1]}")
            video_name_label.grid(row=0, column=0, padx=5, pady=5)

             # Create a label for the video name
            video_name_label = tk.Label(top, text=f"Video Name: {selected_video[1]}")
            video_name_label.grid(row=0, column=0, padx=5, pady=5)

            # Create an entry field for the new video name
            new_name_entry = tk.Entry(top)
            new_name_entry.grid(row=1, column=0, padx=5, pady=5)

            # Create a rating label
            rating_label = ttk.Label(top, text="Rating:")
            rating_label.grid(row=2, column=0, padx=5, pady=5)

            # Create a rating slider with a scale from 1 to 5
            rating_slider = ttk.Scale(top, from_=1, to=5, orient=tk.HORIZONTAL)
            rating_slider.grid(row=2, column=0, padx=5, pady=5)

            # Create an update name button
            update_name_button = tk.Button(top, text="Update Name", command=lambda: self.save_updated_name(top, selected_video, new_name_entry.get()))
            update_name_button.grid(row=4, column=0, padx=5, pady=5)

            # Create an update rating button
            update_rating_button = tk.Button(top, text="Update Rating", command=lambda: self.save_updated_rating(top, selected_video, rating_slider.get()))
            update_rating_button.grid(row=3, column=0, padx=5, pady=5)
        else:
            messagebox.showerror("Error", "Video not found.")

    def save_updated_rating(self, top, selected_video, new_rating):
        updated_video = list(selected_video)  # Create a new list to store the updated video information
        updated_video[2] = str(new_rating)  # Update the video rating

        # Update the playlist list with the updated video information
        self.playlist = [video if video[0] != selected_video[0] else updated_video for video in self.playlist]

        # Write the updated video data to the CSV file
        with open('video_library.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.playlist)

        # Update the playlist listbox
        self.display_playlist()

        # Display a confirmation message
        video_name = selected_video[1]
        messagebox.showinfo("Update Video", f"Rating of video '{video_name}' updated successfully.")
        top.destroy()

    def save_updated_name(self, top, selected_video, new_name):
        updated_video = list(selected_video)  # Create a new list to store the updated video information
        updated_video[1] = new_name  # Update the video name

        # Update the playlist list with the updated video information
        self.playlist = [video if video[0] != selected_video[0] else updated_video for video in self.playlist]

        # Write the updated video data to the CSV file
        with open('video_library.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.playlist)

        # Update the playlist listbox
        self.display_playlist()

        # Display a confirmation message
        video_name = updated_video[1]
        messagebox.showinfo("Update Video", f"Name of video '{video_name}' updated successfully.")
        top.destroy()

    def load_videos(self):
        try:
            with open('video_library.csv', 'r') as file:
                reader = csv.reader(file)
                self.playlist = []
                for video in reader:
                    # Add an empty playcount element if the video has less than three columns
                    if len(video) < 3:
                        video.append("")
                    self.playlist.append(video)
            self.display_playlist()
        except FileNotFoundError:
            pass

    def delete_video(self):
        video_id = simpledialog.askstring("Delete Video", "Enter the ID of the video to delete:")

        if len(video_id) == 1:
            video_id = "0" + video_id

        selected_video = next((video for video in self.playlist if video[0] == video_id), None)

        if selected_video:
            # Remove the video from the playlist
            self.playlist.remove(selected_video)

            # Update the IDs of the remaining videos
            for i, video in enumerate(self.playlist):
                video[0] = str(i + 1).zfill(2)

            # Write the updated video data to the CSV file
            with open('video_library.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(self.playlist)

            # Update the playlist listbox
            self.display_playlist()

            # Display a confirmation message
            video_name = selected_video[1]
            messagebox.showinfo("Delete Video", f"Video '{video_name}' deleted successfully.")
        else:
            messagebox.showerror("Error", "Video not found.")

    def play_video(self):
        # Create a new top-level window for playing the video
        top = tk.Toplevel()
        top.title("Play Video")

        # Create a label for the video ID or name entry
        video_id_label = tk.Label(top, text="Enter Video ID or Name:")
        video_id_label.grid(row=0, column=0, padx=5, pady=5)

        # Create an entry field for the video ID or name
        video_id_entry = tk.Entry(top)
        video_id_entry.grid(row=1, column=0, padx=5, pady=5)

        # Create a play button
        play_button = tk.Button(top, text="Play", command=lambda: self.play_selected_video(video_id_entry.get()))
        play_button.grid(row=2, column=0, padx=5, pady=5)

    def play_selected_video(self, video_id_or_name):
        # If the video ID has only one digit, add a leading zero
        if len(video_id_or_name) == 1:
            video_id_or_name = "0" + video_id_or_name

        # Search for the video in the playlist
        selected_video = next((video for video in self.playlist if video[0] == video_id_or_name or video[1] == video_id_or_name), None)

        if selected_video:
            # Play the selected video (you can add your video playback logic here)
            video_name = selected_video[1]
            messagebox.showinfo("Play Video", f"Playing video: {video_name}")
        else:
            messagebox.showerror("Error", "Video not found.")

    def toggle_theme(self):
        if self.master.cget("bg") == "#ffffff":
            # Set the theme mode to dark
            self.master.configure(bg="#444444")
            self.playlist_listbox.configure(bg="#ffffff", fg="#444444")
            self.search_entry.configure(bg="#ffffff", fg="#444444")
            self.dark_mode_button.configure(text="Light Mode")
        else:
            # Set the theme mode to light
            self.master.configure(bg="#ffffff")
            self.playlist_listbox.configure(bg="#ffffff", fg="#444444")
            self.search_entry.configure(bg="#ffffff")
            self.dark_mode_button.configure(text="Dark Mode")

    def show_video_info(self, event):
        # Get the selected video index
        selected_video_index = self.playlist_listbox.curselection()[0]
        selected_video = self.playlist[selected_video_index]

        # Create a new top-level window for the video information
        top = tk.Toplevel()
        top.title("Video Information")

        # Create labels for the video ID, name, and rating
        video_id_label = tk.Label(top, text=f"Video ID: {selected_video[0]}")
        video_id_label.grid(row=0, column=0, padx=5, pady=5)

        video_name_label = tk.Label(top, text=f"Video Name: {selected_video[1]}")
        video_name_label.grid(row=1, column=0, padx=5, pady=5)

        video_rating_label = tk.Label(top, text=f"Video Rating: {selected_video[2]}")
        video_rating_label.grid(row=2, column=0, padx=5, pady=5)
        
# Create the main window
window = tk.Tk()
general_gui = GeneralApplicationGUI(window)
window.mainloop()