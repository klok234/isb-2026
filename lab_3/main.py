import argparse
import json

from key_gen import key_gen
from Camellia import encrypt, decrypt


def parse_settings():
    """Parse settings.json. Returns dict with values"""
    try:
        with open("settings.json") as json_file:
            json_data = json.load(json_file)
            return json_data
    except FileNotFoundError:
        print("Error: File settigns.json not found!")
        exit(1)
    except Exception as e:
        print(e)
        exit(2)


def parse_args(settings):
    """Parse command line arguments"""
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-gen",
        "--generation",
        type=int,
        choices=[128, 192, 256],
        default=128,
        help="Generation mode (-gen=128)",
    )
    group.add_argument(
        "-enc", "--encryption", action="store_true", help="Encryption mode"
    )
    group.add_argument(
        "-dec", "--decryption", action="store_true", help="Decryption mode"
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
    """Main function. Entry point"""
    settings = parse_settings()
    print(
        "\n\n\nThis program is coded by Dolzhikov D.A. 6212-100503D Var 11\n\
use the Camellia symmetric encryption algorithm with a key that is encrypted using RSA\n"
    )
    parse_args(settings)


if __name__ == "__main__":
    main()
