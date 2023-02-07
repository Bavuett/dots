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

    process = subprocess.Popen('ls -1 /sys/class/backlight', shell=True, stdout=subprocess.PIPE)
    output = process.communicate()[0].decode()

    output_to_arr = output.split('\n')
    output_to_arr.pop()

    result.append(output_to_arr[0])

    return result


def main():
    print('Installing dotfiles...\n')

    # Get the current directory.
    current_dir = os.path.dirname(os.path.realpath(__file__))
    print(f'Current directory: {str(current_dir)}')

    # Get the home directory.
    home_dir = os.path.expanduser("~")
    print(f'Home directory: {home_dir}')

    # Get the list of files in the .config directory.
    files = os.listdir(current_dir + "/.config")
    print(f'Directory structure: {str(files)}')

    for file in files:
        source = f'{current_dir}/.config/{file}'
        destination = f'{home_dir}/.config/{file}'

        if os.path.isdir(source):
            print(f'Copying directory [{source}] to [{destination}]')

            if os.path.exists(destination):
                print(f'Directory [{destination}] already exists. Removing it...')
                
                itemsInDir = os.listdir(destination)

                for item in itemsInDir:
                    itemPath = os.path.join(destination, item)
                    print(f'Removing item [{itemPath}]')
                    os.remove(itemPath)

                os.rmdir(destination)

            try:
                shutil.copytree(source, destination)
            except IOError as e:
                print(f'Couldn\'t copy the directory. Reason: {e}')

            if str(file) == 'polybar':
                variables_to_add = generate_polybar_vars()
                print(f'Found these variables: {variables_to_add}.')

                try:
                    f = open(f'{destination}/variables.ini', 'x')

                    # Output from generate_polybar_vars() looks like this: [ADAPTER, BATTERY, BACKLIGHT].
                    # For this reason we do adapter first, then battery, and we finish with backlight.
                    # Could be improved but do not care - for now.
                    content_to_write = f'[vars]\nadapter = {variables_to_add[0]}\nbattery = {variables_to_add[1]}\nbacklight = {variables_to_add[2]}'

                    f.write(content_to_write)
                    f.close()
                except IOError as e:
                    print(f'Couldn\'t create variables file. Reason: {e}')
                    sys.exit(1)
        else:
            # Copy file which is not a directory.
            print(f'Copying file [{source}] to [{destination}]')

            if os.path.exists(destination):
                print(f'File [{destination}] already exists. Removing it...')
                os.remove(destination)

            try:
                shutil.copy(source, destination)
            except IOError as e:
                print(f'Couldn\'t copy the file. Reason: {e}')

        print('Done!\n')

    print('Finished installing dotfiles!\nEnjoy some coffee and relax! :)')

if __name__ == "__main__":
    main()
