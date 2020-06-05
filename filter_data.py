import pandas as pd
from shutil import copyfile
from os import listdir


files = listdir('raw_data')

# Move only games with a clear winner to a separate directory
i = 1
for file in files:
    if file[-4:] == '.csv':
        data = pd.read_csv('raw_data/' + file)
        if data.loc[len(data)-1, 'In Check'] != '':
            copyfile('raw_data/' + file, 'raw_data/valid_data/run_2_game_' + str(i) + '.csv')
            i += 1