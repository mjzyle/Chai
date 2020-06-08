import pandas as pd
from shutil import copyfile
from os import listdir


files = listdir('raw_data')

# Move only games with a clear winner to a separate directory
i = 1
white_wins = 0
black_wins = 0

for file in files:
    if file[-4:] == '.csv':
        data = pd.read_csv('raw_data/' + file)
        if str(data.loc[len(data)-1, 'In Check']) != 'nan':
            copyfile('raw_data/' + file, 'raw_data/run5_n40_random_style_selection_w_timing/wins/game_' + str(i) + '.csv')
            if data.loc[len(data)-1, 'In Check'] == 'W':
                white_wins += 1
            else:
                black_wins += 1
            i += 1

print(white_wins)
print(black_wins)