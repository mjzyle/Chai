import pandas as pd
import os


points = {
    'P': 1,
    'R': 2,
    'B': 3,
    'N': 3,
    'Q': 4,
    'K': 9
}

# Determine directories for all game datafiles
data = pd.DataFrame()
dirs = ['set1', 'set2', 'set3', 'set4', 'set5']
files = []
for direc in dirs:
    temp = os.listdir(r'C:\Projects\Chess-AI\raw_data\training\\' + direc)
    for file in temp:
        files.append(r'C:\Projects\Chess-AI\raw_data\training\\' + direc + '\\' + file)

# Determine total number of games played with a winner
tot_wins = 0
for file in files:
    temp = pd.read_csv(file)
    if temp.loc[0]['Winner'] != 'Draw':
        tot_wins += 1

# Split the dataset so that half are recorded as universal wins (i.e. regardless of color) and half as universal losses
rec_as_winner = True
rec_winners = 0
games_used = len(files)

for file in files:    
    game = pd.read_csv(file)
    temp = pd.DataFrame()

    # Aggregate training data to identify wins (both black and white wins)
    for index, row in game.iterrows():
        cover = row['Ending Coverage']
        board = row['Ending Board']
        winner = row['Winner']
        new_row = {}

        if winner == 'Draw':
            games_used -= 1
            break

        if rec_as_winner:
            new_row['win'] = 1
            rec_winners += 1
            if rec_winners > int(tot_wins/2):
                rec_as_winner = False
        else:
            new_row['win'] = 0

        if rec_as_winner:
            if winner == 'White':
                i = 0
                while i < 128:
                    if cover[i] == 'W':
                        new_row['cover' + str(i)] = int(cover[i+1])
                    elif cover[i] == 'B':
                        new_row['cover' + str(i)] = int(cover[i+1]) * -1
                    else:
                        new_row['cover' + str(i)] = 0

                    if board[i] == 'W':
                        new_row['pieces' + str(i)] = int(points[board[i+1]])
                    elif board[i] == 'B':
                        new_row['pieces' + str(i)] = int(points[board[i+1]]) * -1
                    else:
                        new_row['pieces' + str(i)] = 0

                    i += 2

            elif winner == 'Black':
                i = 126
                while i > -1:
                    if cover[i] == 'B':
                        new_row['cover' + str(i)] = int(cover[i+1])
                    elif cover[i] == 'W':
                        new_row['cover' + str(i)] = int(cover[i+1]) * -1
                    else:
                        new_row['cover' + str(i)] = 0

                    if board[i] == 'B':
                        new_row['pieces' + str(i)] = int(points[board[i+1]])
                    elif board[i] == 'W':
                        new_row['pieces' + str(i)] = int(points[board[i+1]]) * -1
                    else:
                        new_row['pieces' + str(i)] = 0

                    i -= 2
            
        else:
            if winner == 'Black':
                i = 0
                while i < 128:
                    if cover[i] == 'W':
                        new_row['cover' + str(i)] = int(cover[i+1])
                    elif cover[i] == 'B':
                        new_row['cover' + str(i)] = int(cover[i+1]) * -1
                    else:
                        new_row['cover' + str(i)] = 0

                    if board[i] == 'W':
                        new_row['pieces' + str(i)] = int(points[board[i+1]])
                    elif board[i] == 'B':
                        new_row['pieces' + str(i)] = int(points[board[i+1]]) * -1
                    else:
                        new_row['pieces' + str(i)] = 0

                    i += 2

            elif winner == 'White':
                i = 126
                while i > -1:
                    if cover[i] == 'B':
                        new_row['cover' + str(i)] = int(cover[i+1])
                    elif cover[i] == 'W':
                        new_row['cover' + str(i)] = int(cover[i+1]) * -1
                    else:
                        new_row['cover' + str(i)] = 0

                    if board[i] == 'B':
                        new_row['pieces' + str(i)] = int(points[board[i+1]])
                    elif board[i] == 'W':
                        new_row['pieces' + str(i)] = int(points[board[i+1]]) * -1
                    else:
                        new_row['pieces' + str(i)] = 0

                    i -= 2

        data = data.append(new_row, ignore_index=True)


data.to_csv('raw_data/training_data.csv')
print('Games used: ' + str(games_used))
print('Datapoints: ' + str(len(data)))