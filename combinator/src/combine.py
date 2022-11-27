import pandas as pd
from pandas import options
import os
import xlrd

options.io.excel.xls.writer = "xlwt"

def combine(data_directory, selected):
    dfs = []
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

    df_comb = pd.merge(dfs[0][2], dfs[1][2], left_index=True, right_index=True, how="outer")
    df_comb = df_comb.iloc[::-1]
    
    df_comb_headers = pd.concat([i for (_, i, _) in dfs], axis=1)
    df_comb = pd.concat([df_comb_headers, df_comb])
    
    new_file_name = f"{os.path.basename(selected[0]).rsplit('.', 1)[0]}_{os.path.basename(selected[1]).rsplit('.', 1)[0]}_comb.xls"
    df_comb.to_excel(os.path.join(data_directory, new_file_name), index=True)
    print(
        f"Successfully combined the two files and exported to '{data_directory}/{new_file_name}'")
