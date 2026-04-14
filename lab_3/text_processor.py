def save_text(text: str, path: str):
    with open(path, "wb") as file:
        file.write(text)
        print(f"Сохранено в файл {path}...")


def read_text(path: str):
    with open(path, "rb") as file:
        print(f"Текст {path} прочитан...")
        return file.read()


def read_chipher(path: str):
    with open(path, "rb") as f:
        iv = f.read(16)
        c_text = f.read()
        return iv, c_text
