import pandas as pd
import os

def concatenate(data_directory, selected):
    dfs = []

    # load dataframes
    for building_path in selected:
        df_raw = pd.DataFrame()
        df_raw = pd.read_excel(building_path, index_col=0, parse_dates=True)
        # rename columns to unique value based on OBIS
        df_raw.columns = df_raw.columns.map(
            lambda x: df_raw[x][1] + "_" + df_raw[x][2] + "_" + str(x).split('.')[0])
        df_raw = df_raw.iloc[5:]
        df_raw.index.names = ['Date']
        dfs.append(df_raw)

    # combine/append/concat on index and common columns
    df_new = dfs[0].combine_first(dfs[1])

    new_file_name = f"{os.path.basename(selected[0]).rsplit('.', 1)[0]}_comb.xls"
    df_new.to_excel(new_file_name)
    print(
        f"Succesfully combined the two files and exported to '{data_directory}/{new_file_name}'")