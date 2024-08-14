import pytest
from tkinter import Tk
from general_application import GeneralApplicationGUI

class TestGeneralApplicationGUI:
    def setup_method(self):
        self.root = Tk()
        self.gui = GeneralApplicationGUI(self.root)
        self.gui.playlist = []  # Initialize the playlist attribute

    def test_delete_video(self):
        # Test deleting a video
        self.gui.playlist = [["01", "Video 1", "4"], ["02", "Video 2", "5"]]
        self.gui.delete_video()


if __name__ == "__main__":
    pytest.main()