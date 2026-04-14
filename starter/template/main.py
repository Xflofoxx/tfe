import argparse


def main(name: str = "StarterProject"):
    print(f"Starter project '{name}' is ready to develop!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Starter template CLI")
    parser.add_argument("name", nargs="?", default="StarterProject", help="Project name to display")
    args = parser.parse_args()
    main(args.name)
