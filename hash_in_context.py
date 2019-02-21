import base64, hashlib, os, tkinter, timeit

def printable_file_digest(in_file, mode = 'hex'):
    fd = file_digest(in_file)
    if mode == 'b32':
        pd = base64.b32encode(fd)
    elif mode == 'hex':
        pd = fd.hex()
    elif mode == 'b64':
        pd = base64.b64encode(fd)
    elif mode == 'b16':
        pd = base64.b16encode(fd)
    elif mode == 'a85':
        pd = base64.a85encode(fd)
    if type(pd) == bytes:
        pd = pd.decode()
    return pd

def printable_bytes(b, mode = 'hex'):
    if mode == 'b32':
        p = base64.b32encode(b)
    elif mode == 'hex':
        p = b.hex()
    elif mode == 'b64':
        p = base64.b64encode(b)
    elif mode == 'b16':
        p = base64.b16encode(b)
    elif mode == 'a85':
        p = base64.a85encode(b)
    return p.decode()

def file_digest(in_file, hash_function = hashlib.sha256):
    with open(in_file, 'rb') as file_object:
        file_data = file_object.read()
        hash_object = hash_function(file_data)
        digest_bytes = hash_object.digest()
    return digest_bytes

def directory_digest(directory_name, hash_function = hashlib.sha256, verbose = False):
    hashes = ""
    for root, dirs, files in os.walk(directory_name):
        for f in files:
            pd = printable_digest(os.path.join(root,f))
            if verbose:
                print(os.path.join(root,f) + ':\n' + pd + '\n')
            hashes += pd + '\n'
    encoded_hashes = hashes.encode('utf-8')
    superhash = hash_function(encoded_hashes).digest()
    return superhash

def printable_directory_digest(in_dir, mode = 'hex'):
    dd = directory_digest(in_dir)
    if mode == 'b32':
        pd = base64.b32encode(dd)
    elif mode == 'hex':
        pd = dd.hex()
    elif mode == 'b64':
        pd = base64.b64encode(dd)
    elif mode == 'b16':
        pd = base64.b16encode(dd)
    elif mode == 'a85':
        pd = base64.a85encode(dd)
    if type(pd) == bytes:
        pd = pd.decode()
    return pd

def printable_digest(in_obj, mode = 'hex'):
    outval = None
    if os.path.isdir(in_obj):
        outval = printable_directory_digest(in_obj, mode)
    elif os.path.isfile(in_obj):
        outval = printable_file_digest(in_obj, mode)
    return outval

hashit = printable_digest

def compare_directories(dir1, dir2, verbose = True):
    a = hashit(dir1)
    b = hashit(dir2)
    if verbose:
        print(a.upper())
        print(b.upper())
    return a == b

# Getting the clipboard using tkinter doesn't seem to work...
# instance = tkinter.Tk()
# get_clipboard = instance.clipboard_get

def compare_to_clipboard(in_obj, verbose = True):
    a = get_clipboard().upper()
    b = hashit(in_obj).upper()
    if verbose:
        print(a)
        print(b)
    return a == b


print(compare_to_clipboard('D:/tmp'))

# 15B16FD6B3EC32ECA7CBB50ED40579810C132DE8B484FDEF5B626FD74D4650AA


# new context menu items for files --
# # copy file hash to clipboard
# # compare file hash to clipboard

# and for directories --
# # copy hash of all contents to clipboard
# # # note - this could be very slow, may need some QoL like a progress bar
# # # or warning
# # compare hash of all contents with clipboard

# creating context menu items:
# https://www.howtogeek.com/howto/windows-vista/create-a-context-menu-item-to-copy-a-text-file-to-the-clipboard-in-windows-vista/
