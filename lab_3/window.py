import sys
import json

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel,
    QFileDialog,
    QRadioButton,
    QGroupBox,
    QMessageBox,
)

from Camellia import encrypt, decrypt
from key_gen import key_gen


class CryptoApp(QMainWindow):
    def __init__(self):
        """Constructor object of class"""
        super().__init__()
        self.settings = self.load_settings()
        self.init_ui()
        self.apply_settings()

    def load_settings(self):
        """Loads the settings from settings.json"""
        settings = {
            "initial_file": "",
            "encrypted_file": "",
            "decrypted_file": "",
            "symmetric_key": "",
            "public_key": "",
            "secret_key": "",
        }
        try:
            with open("settings.json", "r", encoding="utf-8") as f:
                loaded = json.load(f)
                for key, val in loaded.items():
                    try:
                        with open(val, "r") as f:
                            pass
                    except:
                        loaded[key] = ""
                settings.update(loaded)
        except FileNotFoundError:
            with open("settings.json", "w", encoding="utf-8") as f:
                json.dump(settings, f)
        return settings

    def init_ui(self):
        """Creates and fills in the user interface"""
        self.setWindowTitle("Шифрователь 2000 (RSA + Camellia)")
        self.setMinimumSize(600, 350)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        mode_group = QGroupBox("Режим работы")
        mode_layout = QHBoxLayout()
        self.radio_encrypt = QRadioButton("Шифрование")
        self.radio_decrypt = QRadioButton("Расшифрование")
        self.radio_encrypt.setChecked(True)
        mode_layout.addWidget(self.radio_encrypt)
        mode_layout.addWidget(self.radio_decrypt)
        mode_group.setLayout(mode_layout)
        main_layout.addWidget(mode_group)

        self.file_widgets = {}
        file_labels = [
            ("initial_file", "Исходный файл:"),
            ("symmetric_key", "Зашифрованный симм. ключ:"),
            ("public_key", "Публичный ключ RSA (собеседника):"),
            ("secret_key", "Приватный ключ RSA (Ваш):"),
            ("encrypted_file", "Зашифрованный файл:"),
            ("decrypted_file", "Расшифрованный файл:"),
        ]
        for key, label_text in file_labels:
            layout = QHBoxLayout()
            label = QLabel(label_text)
            label.setFixedWidth(180)
            line_edit = QLineEdit()
            line_edit.editingFinished.connect(self.update_file_settings)
            button = QPushButton("Обзор...")
            button.clicked.connect(lambda k=key: self.browse_file(k))
            layout.addWidget(label)
            layout.addWidget(line_edit)
            layout.addWidget(button)
            main_layout.addLayout(layout)
            self.file_widgets[key] = line_edit

        bottom_layout = QHBoxLayout()

        self.start_button = QPushButton("Старт")
        self.start_button.clicked.connect(self.start_process)
        bottom_layout.addWidget(self.start_button)

        gen_group = QGroupBox("Генерация ключей")
        gen_layout = QVBoxLayout()

        key_len_layout = QHBoxLayout()
        key_len_layout.addWidget(QLabel("Длина ключа:"))
        self.len_128 = QRadioButton("128")
        self.len_192 = QRadioButton("192")
        self.len_256 = QRadioButton("256")
        self.len_256.setChecked(True)
        key_len_layout.addWidget(self.len_128)
        key_len_layout.addWidget(self.len_192)
        key_len_layout.addWidget(self.len_256)
        gen_layout.addLayout(key_len_layout)

        self.gen_button = QPushButton("Сгенерировать ключи")
        self.gen_button.clicked.connect(self.generate_keys)
        gen_layout.addWidget(self.gen_button)

        gen_group.setLayout(gen_layout)
        bottom_layout.addWidget(gen_group)

        main_layout.addLayout(bottom_layout)

    def browse_file(self, key):
        """Opens the file selection dialog and inserts path to field."""
        if key in (
            "public_key",
            "private_key",
            "symmetric_key",
            "encrypted_file",
            "decrypted_file",
        ):
            if key in ("encrypted_file", "decrypted_file"):
                path, _ = QFileDialog.getSaveFileName(self, f"Сохранить как {key}")
            else:
                path, _ = QFileDialog.getOpenFileName(self, f"Выберите файл {key}")
        else:
            path, _ = QFileDialog.getOpenFileName(self, f"Выберите файл {key}")
        if path:
            self.file_widgets[key].setText(path)
            self.update_file_settings()

    def update_file_settings(self):
        """Updates file settings.json when change value in UI."""
        self.settings.update(self.get_current_paths())
        with open("settings.json", "w", encoding="utf-8") as f:
            json.dump(self.settings, f)

    def generate_keys(self):
        """Generate public private and symmetric keys"""
        if self.len_128.isChecked():
            length = 128
        elif self.len_192.isChecked():
            length = 192
        else:
            length = 256

        paths = self.get_current_paths()
        if (
            not paths["public_key"]
            or not paths["secret_key"]
            or not paths["symmetric_key"]
        ):
            QMessageBox.warning(
                self,
                "Предупреждение",
                "Укажите пути для сохранения публичного, приватного и симметричного ключей.",
            )
            return

        try:
            key_gen(
                length,
                paths["public_key"],
                paths["secret_key"],
                paths["symmetric_key"],
            )
            QMessageBox.information(self, "Успех", "Ключи успешно сгенерированы.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка генерации ключей:\n{str(e)}")

    def apply_settings(self):
        """Load fields from settings.json."""
        for key, widget in self.file_widgets.items():
            if key in self.settings:
                widget.setText(self.settings[key])

    def get_current_paths(self):
        """Get paths from UI fields."""
        return {key: widget.text().strip() for key, widget in self.file_widgets.items()}

    def start_process(self):
        """Start decrypt or encrypt data."""
        paths = self.get_current_paths()
        mode = "encrypt" if self.radio_encrypt.isChecked() else "decrypt"

        try:
            if mode == "encrypt":
                required = [
                    "public_key",
                    "initial_file",
                    "symmetric_key",
                    "encrypted_file",
                ]
                for req in required:
                    if not paths[req]:
                        raise ValueError(f"Поле '{req}' не заполнено.")
                    try:
                        if req in required[:3]:
                            with open(paths[req], "r") as f:
                                pass
                    except:
                        raise FileNotFoundError(f"Не найден файл '{paths[req]}'")
                encrypt(
                    self.settings["initial_file"],
                    self.settings["symmetric_key"],
                    self.settings["secret_key"],
                    self.settings["encrypted_file"],
                )

                QMessageBox.information(
                    self,
                    "Успех",
                    f"Файл зашифрован.\nРезультат сохранён в:\n{self.settings["encrypted_file"]}",
                )
            else:
                required = [
                    "secret_key",
                    "encrypted_file",
                    "symmetric_key",
                    "decrypted_file",
                ]
                for req in required:
                    if not paths[req]:
                        raise ValueError(f"Поле '{req}' не заполнено.")
                    try:
                        if req in required[:3]:
                            with open(paths[req], "r") as f:
                                pass
                    except:
                        raise FileNotFoundError(f"Не найден файл '{paths[req]}'")
                decrypt(
                    self.settings["encrypted_file"],
                    self.settings["symmetric_key"],
                    self.settings["secret_key"],
                    self.settings["decrypted_file"],
                )

                QMessageBox.information(
                    self,
                    "Успех",
                    f"Файл расшифрован.\nРезультат сохранён в:\n{self.settings['decrypted_file']}",
                )

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", str(e))


def main():
    """Entry point. Main function"""
    app = QApplication(sys.argv)
    window = CryptoApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
