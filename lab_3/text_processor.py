def save_text(text: str, path: str):
    """Save data to file"""
    try:
        with open(path, "wb") as file:
            file.write(text)
    except Exception as e:
        print(e)
        exit(2)


def read_text(path: str):
    """Read data from file. Return bytes of data"""
    try:
        with open(path, "rb") as file:
            return file.read()
    except Exception as e:
        print(e)
        exit(2)


def read_chipher(path: str):
    """Read chipher text from file. Return iv sequence and chiphertext"""
    try:
        with open(path, "rb") as f:
            iv = f.read(16)
            c_text = f.read()
            return iv, c_text
    except Exception as e:
        print(e)
        exit(2)
