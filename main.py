from create_table import main as create
from etl import main as process

if __name__ == "__main__":
    create()
    process()
    print("\n\nFinished processing!!!\n\n")