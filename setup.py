import os
import sys
import shutil
import subprocess


def generate_polybar_vars():
    process = subprocess.Popen('ls -1 /sys/class/power_supply/', shell=True, stdout=subprocess.PIPE)
    output = process.communicate()[0].decode()

    output_to_arr = output.split('\n')
    output_to_arr.pop()

    result = output_to_arr

    print(result)

    process = subprocess.Popen('ls -1 /sys/class/backlight', shell=True, stdout=subprocess.PIPE)
    output = process.communicate()[0].decode()

    output_to_arr = output.split('\n')
    output_to_arr.pop()

    result.append(output_to_arr[0])

    return result


def main():
    print("Installing dotfiles...")

    # Get the current directory.
    current_dir = os.path.dirname(os.path.realpath(__file__))
    print(f'Current directory: {str(current_dir)}')

    # Get the home directory.
    home_dir = os.path.expanduser("~")
    print(f'Home directory: {home_dir}')

    # Get the list of files in the .config directory.
    files = os.listdir(current_dir + "/.config")
    print(f'Files: {str(files)}')

    for file in files:
        # Get the source and destination paths.
        source = f'{current_dir}/.config/{file}'

        # If the file is a directory, then we need to copy the contents of the directory.
        if os.path.isdir(source):
            destination = f'{home_dir}/.config/{file}'

            print(f'Copying directory [{source}] to [{destination}]')
            # shutil.copytree(source, destination)

            if str(file) == 'polybar':
                variables_to_add = generate_polybar_vars()
                print(f'Found these variables: {variables_to_add}.')

                try:
                    f = open(f'{destination}/variables.ini', 'x')

                    content_to_write = f'[vars]\nbattery = {variables_to_add[2]}\nadapter = {variables_to_add[1]}\nbacklight = {variables_to_add[0]}'

                    f.write(content_to_write)
                    f.close()
                except IOError as e:
                    print(f'Couldn\'t create variables file. Reason: {e}')
                    sys.exit(1)
            else:
                pass


if __name__ == "__main__":
    main()
