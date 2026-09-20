# This is a script to load the legacy scheduling data into the Postgres database
from database.data_parsing import parse_legacy_data
from settings import settings

path = settings.path_to_legacy_docking_data


def main():
    print(parse_legacy_data(path=path))


if __name__ == "__main__":
    main()
