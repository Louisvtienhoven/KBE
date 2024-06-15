import pandas as pd
import os

dir = "../wiring/saved_orientations"

compiled_data = pd.DataFrame()
for file in os.listdir(dir):
    dat = pd.read_csv(f'{dir}/{file}', index_col=0)

    compiled_data = pd.concat([compiled_data, dat], join='outer', axis=1)

overview = compiled_data.fillna(False)