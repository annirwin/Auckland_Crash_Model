import pandas as pd


meshblock_df = pd.read_csv('meshblock-higher-geographies-2024.csv')
meshblock_auckland_df = meshblock_df[meshblock_df.FUA2023_V1_00_NAME.isin(['Auckland','Warkworth'])]
meshblock_auckland_df.to_csv('meshblock-higher-geographies-2024-auckland.csv', index=False)