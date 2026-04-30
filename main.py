from src.parser import Parser


def main():
    # print("Hello from github-fly-in!")
    parser = Parser("maps/easy/01_linear_path.txt")
    # parser = Parser("maps/easy/02_simple_fork.txt")
    # parser = Parser("maps/hard/01_maze_nightmare.txt")
    parser._parse_map()


if __name__ == "__main__":
    main()
