import os
import sys

class FileManager:
    def get_base_path(self):
        if getattr(sys, 'frozen', False):
            # Running in a PyInstaller bundle
            return getattr(sys, '_MEIPASS2', os.path.dirname(sys.executable))
        else:
            # Running in a normal Python environment
            return os.path.dirname(os.path.abspath(__file__))

    def get_file_path(self, filename):
        return os.path.join(self.get_base_path(), filename)



