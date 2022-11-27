import pandas as pd
import numpy as np
from pandas import options
import os
import xlrd

TEMP_INDEX = "new_index"

options.io.excel.xls.writer = "xlwt"


def combine(data_directory, selected):
    dfs = []  # [(building_name, header, df), (building_name, header, df)]
    # since the intersection over the dataframes is used anyway, one of the two headers can be used
    # df_raw_header = pd.DataFrame()

    # load dataframes
    for building_path in selected:
        wb = xlrd.open_workbook(building_path, logfile=open(os.devnull, 'w'))
        df_raw = pd.read_excel(wb, index_col=0, parse_dates=True)
        # rename columns to unique value based on OBIS
        df_building_name = os.path.basename(building_path).rsplit('.', 1)[0]
        print(df_building_name)
        df_raw.columns = df_raw.columns.map(
            lambda x: df_raw[x][1] + "_" + df_raw[x][2] + "_" + str(x).split('.')[0] + "_" + df_building_name)
        df_raw_header = df_raw.iloc[:5]
        df_raw = df_raw.iloc[5:]
        # df_raw.index.names = ['Date']
        dfs.append((df_building_name, df_raw_header, df_raw))

    start_a = np.datetime64(dfs[0][2].index[-1])
    start_b = np.datetime64(dfs[1][2].index[-1])
    end_a = np.datetime64(dfs[0][2].index[0])
    end_b = np.datetime64(dfs[1][2].index[0])
    min_start = min(start_a, start_b)
    max_end = max(end_a, end_b)
    offset_a = np.datetime64(dfs[0][2].index[0]) - np.datetime64(dfs[0][2].index[1])
    offset_b = np.datetime64(dfs[1][2].index[0]) - np.datetime64(dfs[1][2].index[1])
    min_offset = min(offset_a, offset_b)
    length_a = len(dfs[0][2].index)
    length_b = len(dfs[1][2].index)
    index_a = [(0 if start_a == min_start else int((start_a-min_start)/min_offset)) + (offset_a / min_offset) * i for i in range(length_a)]  # range(0 if start_a == min_start else int((start_a-min_start)/min_offset), length_a, int(offset_a / min_offset))
    index_b = [(0 if start_b == min_start else int((start_b-min_start)/min_offset)) + (offset_b / min_offset) * i for i in range(length_b)]  # range(0 if start_b == min_start else int((start_b-min_start)/min_offset), length_b, int(offset_b / min_offset))

    # print(f"{length_a} : {len(index_a)}")
    # print(f"{length_b} : {len(index_b)}")
    #
    # print(f"Min start: {min_start}")
    # print(f"Max end: {max_end}")
    # print(f"Offset A: {offset_a}")
    # print(f"Offset B: {offset_b}")
    # print((min_start-max_end)/min_offset)
    # combined_index = [min_start + i*min_offset for i in range(int((max_end-min_start)/min_offset))]

    keys_before = set(dfs[0][2].columns.values.tolist())
    dfs[0][2][TEMP_INDEX] = index_a[::-1]
    dfs[0][2].reset_index(inplace=True)
    # dfs[0][2].set_index("new_index", inplace=True, drop=False)
    dfs[1][2][TEMP_INDEX] = index_b[::-1]
    dfs[1][2].reset_index(inplace=True)
    # dfs[1][2].set_index("new_index", inplace=True, drop=False)
    keys_after = set(dfs[0][2].columns.values.tolist())
    keys_before.add(TEMP_INDEX)
    old_index_key = (keys_after - keys_before).pop()

    # df_comb = pd.merge(dfs[0][2], dfs[1][2], left_index=True, right_index=True, how="outer")
    df_comb = pd.merge(dfs[0][2], dfs[1][2], on=[TEMP_INDEX, old_index_key], how="outer")
    # df_comb = df_comb.iloc[::-1]
    df_comb.set_index(old_index_key, inplace=True)
    df_comb.drop(TEMP_INDEX, axis=1, inplace=True)

    df_comb_headers = pd.concat([i for (_, i, _) in dfs], axis=1)
    df_comb = pd.concat([df_comb_headers, df_comb])

    new_file_name = f"{os.path.basename(selected[0]).rsplit('.', 1)[0]}_{os.path.basename(selected[1]).rsplit('.', 1)[0]}_comb.xls"
    df_comb.to_excel(os.path.join(data_directory, new_file_name), index=True)
    print(f"Successfully combined the two files and exported to '{data_directory}/{new_file_name}'")
