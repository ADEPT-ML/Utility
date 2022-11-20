import pandas as pd
import os

def concatenate(data_directory, selected):
    dfs = []
    # since the intersection over the dataframes is used anyway, one of the two headers can be used
    df_raw_header = pd.DataFrame()

    # load dataframes
    for building_path in selected:
        df_raw = pd.DataFrame()
        df_raw = pd.read_excel(building_path, index_col=0, parse_dates=True)
        # rename columns to unique value based on OBIS
        df_raw.columns = df_raw.columns.map(
            lambda x: df_raw[x][1] + "_" + df_raw[x][2] + "_" + str(x).split('.')[0])
        df_raw_header = df_raw.iloc[:5]
        df_raw = df_raw.iloc[5:]
        df_raw.index.names = ['Date']
        dfs.append(df_raw)

    # intersect column names
    df_column_intersection = intersection(
        dfs[0].columns.values.tolist(),
        dfs[1].columns.values.tolist()
    )  
    
    # restrict dataframes to intersecting column names
    dfs[0] = dfs[0][df_column_intersection]
    dfs[1] = dfs[1][df_column_intersection]
    
    # combine/append/concat on index and revert list
    df_new = dfs[0].combine_first(dfs[1])
    df_new = df_new.iloc[::-1]
    
    # re-add header with OBIS Beschreibung, Kennzahl etc.
    df_new_header = df_raw_header[df_new.columns.values.tolist()]
    df_new = pd.concat([df_new_header, df_new])
    df_new.index.names = ['Energieart']

    new_file_name = f"{os.path.basename(selected[0]).rsplit('.', 1)[0]}_comb.xls"
    df_new.to_excel(new_file_name)
    print(
        f"Succesfully combined the two files and exported to '{data_directory}/{new_file_name}'")


def intersection(lst1, lst2):
    intersected_list = [value for value in lst1 if value in lst2]
    return intersected_list
