import os
import shutil
import subprocess

def main():
    print("Installing dotfiles...")

    # Get the current directory.
    current_dir = os.path.dirname(os.path.realpath(__file__))
    print("Current directory: " + current_dir)

    # Get the home directory.
    home_dir = os.path.expanduser("~")
    print("Home directory: " + home_dir)

    # Get the list of files in the .config directory.
    files = os.listdir(current_dir + "/.config")
    print("Files: " + str(files))

    for file in files:
        # Get the source and destination paths.
        source = current_dir + "/.config/" + file

        # If the file is a directory, then we need to copy the contents of the directory.
        if os.path.isdir(source):
            destination = home_dir + "/.config/" + file
            print("Copying directory: " + source + " to " + destination)
            # shutil.copytree(source, destination)

if __name__ == "__main__":
    main()