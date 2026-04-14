import argparse
import json

from key_gen import key_gen


def parse_settings():
    with open("settings.json") as json_file:
        json_data = json.load(json_file)
        print(json_data)
        return json_data


def parse_args(settings):
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-gen",
        "--generation",
        type=int,
        default=128,
        help="Запускает режим генерации ключей (-gen=128)",
    )
    group.add_argument("-enc", "--encryption", help="Запускает режим шифрования")
    group.add_argument("-dec", "--decryption", help="Запускает режим дешифрования")

    args = parser.parse_args()
    if args.generation is not None:
        key_gen(
            args.generation,
            settings["public_key"],
            settings["secret_key"],
            settings["symmetric_key"],
        )
    elif args.encryption is not None:
        pass
        # encryption()
    elif args.decryption is not None:
        pass
        # decryption()
    else:
        print("Usage: python main.py [-gen=128 | -enc | -dec]")


def main():
    settings = parse_settings()
    parse_args(settings)


if __name__ == "__main__":
    main()
