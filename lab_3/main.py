import argparse
import json

from key_gen import key_gen
from Camellia import encrypt, decrypt


def parse_settings():
    with open("settings.json") as json_file:
        json_data = json.load(json_file)
        return json_data


def parse_args(settings):
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-gen",
        "--generation",
        type=int,
        choices=[128, 192, 256],
        default=128,
        help="Запускает режим генерации ключей (-gen=128)",
    )
    group.add_argument(
        "-enc", "--encryption", action="store_true", help="Запускает режим шифрования"
    )
    group.add_argument(
        "-dec", "--decryption", action="store_true", help="Запускает режим дешифрования"
    )

    args = parser.parse_args()
    if args.encryption:
        encrypt(
            settings["initial_file"],
            settings["symmetric_key"],
            settings["secret_key"],
            settings["encrypted_file"],
        )
    elif args.decryption:
        decrypt(
            settings["encrypted_file"],
            settings["symmetric_key"],
            settings["secret_key"],
            settings["decrypted_file"],
        )
    elif args.generation is not None:
        key_gen(
            args.generation,
            settings["public_key"],
            settings["secret_key"],
            settings["symmetric_key"],
        )
    else:
        print("Usage: python main.py [-gen=128 | -enc | -dec]")


def main():
    settings = parse_settings()
    parse_args(settings)


if __name__ == "__main__":
    main()
