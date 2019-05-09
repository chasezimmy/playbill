from helpers import helpers


def main():
    auditions = helpers.get_auditions()
    helpers.save_auditions(auditions)


if __name__ == "__main__":
    main()
