import pandas as pd
import os


def read_files(input_dir, file_name) -> None:
    gen_data = pd.read_csv(input_dir + file_name, header=True)
    if not os.path.exists(input_dir + file_name):
        print(f"{file_name} does not exists!")
