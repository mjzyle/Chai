import pandas as pd
import math
import mysql.connector
import getpass
from shutil import copyfile
from os import listdir
from os import scandir


# Read from a directory with gameplay data, copying only records where one of the players wins into a subdirectory
def filter_wins(loc):
    files = listdir(loc)

    # Move only games with a clear winner to a separate directory
    i = 1
    white_wins = 0
    black_wins = 0
    tot_games = 0

    for file in files:
        if 'training_data' in file:
            continue
        if file[-4:] == '.csv':
            tot_games += 1
            data = pd.read_csv(loc + '//' + file)
            if str(data.loc[0, 'Winner']) != 'Draw':
                copyfile(loc + '//' + file, loc + '//' + 'wins/game_' + str(i) + '.csv')
                if data.loc[0, 'Winner'] == 'White':
                    white_wins += 1
                else:
                    black_wins += 1
                i += 1

    print('Total games: ' + str(tot_games))
    print('White wins: ' + str(white_wins) + ' (' + str(white_wins/tot_games) + ')')
    print('Black wins: ' + str(black_wins) + ' (' + str(black_wins/tot_games) + ')')


# Read from a directory with gameplay data and count wins for white/black players
def count_wins(loc='raw_data'):
    files = listdir(loc)

    white_wins = 0
    black_wins = 0
    tot_games = 0

    for file in files:
        if 'training_data' in file:
            continue
        if file[-4:] == '.csv':
            tot_games += 1
            data = pd.read_csv(loc + '//' + file)
            if str(data.loc[0, 'Winner']) != 'Draw':
                if data.loc[0, 'Winner'] == 'White':
                    white_wins += 1
                else:
                    black_wins += 1

    print('Total games: ' + str(tot_games))
    print('White wins: ' + str(white_wins) + ' (' + str(white_wins/tot_games) + ')')
    print('Black wins: ' + str(black_wins) + ' (' + str(black_wins/tot_games) + ')')


# Determine the total number of turns in a winning game
def get_num_turns_to_win(directories):
    mean = 0
    median = 0
    ran = 0
    minm = 0
    maxm = 0
    df = pd.DataFrame()

    i = 0
    for direc in directories:
        files = listdir(direc)

        for file in files:
            temp = pd.read_csv(direc + '/' + file)
            df = df.append({
                'Game': i,
                'Turns to win': int(len(temp)/2)
            }, ignore_index=True)
            i += 1

    mean = df['Turns to win'].mean()
    median = df['Turns to win'].median()
    minm = df['Turns to win'].min()
    maxm = df['Turns to win'].max()
    ran = maxm - minm

    return mean, median, ran, minm, maxm


# Aggregate data from multiple game files into a single master dataset
def aggregate_data(loc):
    files = listdir(loc)
    master_data = pd.DataFrame(columns=['Game', 'Move', 'Turn', 'Moving Player', 'Starting Board', 'Ending Board', 'In Check', 'Coverage Start', 'Coverage End', 'Winner'])

    i = 1
    for file in files:
        temp = pd.read_csv(loc + '//' + file)
        temp['Game'] = i
        winner = temp.loc[len(temp)-1, 'In Check']
        temp['Winner'] = winner

        for j in range(0, len(temp)):
            temp.loc[j, 'Move'] = int(j+1)

        master_data = master_data.append(temp, ignore_index=True)
        
        print(str(i) + ' of ' + str(len(files)) + ' added')
        i += 1

    return master_data


# Provide additional context details to aggregated dataset
def contextualize_data(loc):
    data = aggregate_data(loc)
    points = {
        'P': 1,
        'K': 1,
        'R': 2,
        'B': 3,
        'N': 3,
        'Q': 4
    }

    cont_data = pd.DataFrame(columns=['Board', 'Coverage', 'White Cover Score', 'Black Cover Score', 'White Piece Score', 'Black Piece Score'])

    for index, row in data.iterrows():
        # Determine coverage scores
        coverage = row['Coverage']
        black_coverage = 0
        white_coverage = 0
        
        for i in range(0, len(coverage)):
            color = coverage[i]
            score = int(coverage[i+1])
            
            if color == 'B':
                black_coverage += score
            elif color == 'W':
                white_coverage += score

        # Determine piece value scores
        board = row['Board']
        black_score = 0
        white_score = 0

        for i in range(0, len(board)):
            color = board[i]
            piece = board[i+1]

            if color == 'B':
                black_score += points[piece]
            elif color == 'W':
                black_score += points[piece]

        cont_data = cont_data.append({
            'Board': board,
            'Coverage': coverage,
            'White Cover Score': white_coverage,
            'Black Cover Score': black_coverage,
            'White Piece Score': white_score,
            'Black Piece Score': black_score
        }, ignore_index=True)

    cont_data.to_csv(loc + '//' + 'context.csv')


# Aggregate training data into a formate suitable for use by the AI neural network
def get_training_data(root):
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
    files = []
    for loc in scandir(root):
        temp = listdir(loc.path)
        for file in temp:
            files.append(loc.path + '\\' + file)

    # Determine total number of games played with a winner
    tot_wins = 0
    for file in files:
        temp = pd.read_csv(file)
        if temp.loc[0]['Winner'] != 'Draw':
            tot_wins += 1

    games_used = len(files)
    count = 1
    for file in files:    
        game = pd.read_csv(file)
        temp = pd.DataFrame()

        # Record each dataset twice (once as a win and once as a loss, but oriented to the opposite player)
        print('Processing file ' + str(count) + ' of ' + str(len(files)))

        rec_as_winner = True
        for i in range(0, 2):
            # Aggregate training data to identify wins (both black and white wins)
            for index, row in game.iterrows():
                cover = row['Ending Coverage']
                board = row['Ending Board']
                winner = row['Winner']
                new_row = {}

                #if winner == 'Draw':
                #    break

                rec_index = 0

                if rec_as_winner:
                    new_row['win'] = 1
                    if winner == 'White':
                        i = 0
                        while i < 128:
                            if cover[i] == 'W':
                                new_row['cover' + str(rec_index)] = int(cover[i+1])
                            elif cover[i] == 'B':
                                new_row['cover' + str(rec_index)] = int(cover[i+1]) * -1
                            else:
                                new_row['cover' + str(rec_index)] = 0

                            if board[i] == 'W':
                                new_row['pieces' + str(rec_index)] = int(points[board[i+1]])
                            elif board[i] == 'B':
                                new_row['pieces' + str(rec_index)] = int(points[board[i+1]]) * -1
                            else:
                                new_row['pieces' + str(rec_index)] = 0

                            i += 2
                            rec_index += 1

                    elif winner == 'Black' or winner == 'Draw':
                        i = 126
                        while i > -1:
                            if cover[i] == 'B':
                                new_row['cover' + str(rec_index)] = int(cover[i+1])
                            elif cover[i] == 'W':
                                new_row['cover' + str(rec_index)] = int(cover[i+1]) * -1
                            else:
                                new_row['cover' + str(rec_index)] = 0

                            if board[i] == 'B':
                                new_row['pieces' + str(rec_index)] = int(points[board[i+1]])
                            elif board[i] == 'W':
                                new_row['pieces' + str(rec_index)] = int(points[board[i+1]]) * -1
                            else:
                                new_row['pieces' + str(rec_index)] = 0

                            i -= 2
                            rec_index += 1
                    
                    else:
                        print('ERROR: Invalid game outcome')

                else:
                    new_row['win'] = 0
                    if winner == 'Black':
                        i = 0
                        while i < 128:
                            if cover[i] == 'W':
                                new_row['cover' + str(rec_index)] = int(cover[i+1])
                            elif cover[i] == 'B':
                                new_row['cover' + str(rec_index)] = int(cover[i+1]) * -1
                            else:
                                new_row['cover' + str(rec_index)] = 0

                            if board[i] == 'W':
                                new_row['pieces' + str(rec_index)] = int(points[board[i+1]])
                            elif board[i] == 'B':
                                new_row['pieces' + str(rec_index)] = int(points[board[i+1]]) * -1
                            else:
                                new_row['pieces' + str(rec_index)] = 0

                            i += 2
                            rec_index += 1

                    elif winner == 'White' or winner == 'Draw':
                        i = 126
                        while i > -1:
                            if cover[i] == 'B':
                                new_row['cover' + str(rec_index)] = int(cover[i+1])
                            elif cover[i] == 'W':
                                new_row['cover' + str(rec_index)] = int(cover[i+1]) * -1
                            else:
                                new_row['cover' + str(rec_index)] = 0

                            if board[i] == 'B':
                                new_row['pieces' + str(rec_index)] = int(points[board[i+1]])
                            elif board[i] == 'W':
                                new_row['pieces' + str(rec_index)] = int(points[board[i+1]]) * -1
                            else:
                                new_row['pieces' + str(rec_index)] = 0

                            i -= 2
                            rec_index += 1

                    else:
                        print('ERROR: Invalid game outcome')

                # Undo any cases where a draw is recorded as a winner (code uses the win/loss logic to record draws twice for both board orientations, but they should all be losses)
                if winner == 'Draw':
                    new_row['win'] = 0

                data = data.append(new_row, ignore_index=True)
                rec_as_winner = not rec_as_winner

            #if winner == 'Draw':
                #games_used -= 1
                #break

        count += 1
        print('Datapoints: ' + str(len(data)))


    data.to_csv('raw_data/training_data.csv')
    print('Games used: ' + str(games_used))
    print('Datapoints: ' + str(len(data)))


# Establish MySQL database connection (prompts caller for username and password)
def establish_db_connection():
    connected = False
    
    while not connected:
        try:
            # Prompt user for DB username and password
            user = input('DB User: ')
            pwd = getpass.getpass()

            # Connect to database
            cnx = mysql.connector.connect(user=user, password=pwd)
            cursor = cnx.cursor()

            connected = True

        except mysql.connector.errors.ProgrammingError:
            print('User/password combination incorrect')
            connected = False

    print('Connection successful')
    return cnx, cursor


# Connect to MySQL database and save data to correct table(s)
def save_training_data(root):
    cnx, cursor = establish_db_connection()
    cursor.execute("USE chai")

    # Setup MySQL insertion command
    query = 'INSERT INTO training_data (game_id, win, '

    for i in range(0, 64):
        query += 'pieces' + str(i) + ', '
    for i in range(0, 63):
        query += 'cover' + str(i) + ', '
    
    query += 'cover63) VALUES ('

    points = {
        'P': 1,
        'R': 2,
        'B': 3,
        'N': 3,
        'Q': 4,
        'K': 9
    }

    # Determine directories for all game datafiles
    files = []
    for loc in scandir(root):
        temp = listdir(loc.path)
        for file in temp:
            files.append(loc.path + '\\' + file)

    count = 1
    for file in files:    
        game = pd.read_csv(file)

        # Record each dataset twice (once as a win and once as a loss, but oriented to the opposite player)
        print('Processing file ' + str(count) + ' of ' + str(len(files)))

        rec_as_winner = True
        # Aggregate training data to identify wins (both black and white wins)
        for index, row in game.iterrows():
            for i in range(0, 2):
                cover = row['Ending Coverage']
                board = row['Ending Board']
                winner = row['Winner']
                new_row = {}

                #if winner == 'Draw':
                #    break

                rec_index = 0

                if rec_as_winner:
                    new_row['win'] = 1
                    if winner == 'White':
                        i = 0
                        while i < 128:
                            if cover[i] == 'W':
                                new_row['cover' + str(rec_index)] = int(cover[i+1])
                            elif cover[i] == 'B':
                                new_row['cover' + str(rec_index)] = int(cover[i+1]) * -1
                            else:
                                new_row['cover' + str(rec_index)] = 0

                            if board[i] == 'W':
                                new_row['pieces' + str(rec_index)] = int(points[board[i+1]])
                            elif board[i] == 'B':
                                new_row['pieces' + str(rec_index)] = int(points[board[i+1]]) * -1
                            else:
                                new_row['pieces' + str(rec_index)] = 0

                            i += 2
                            rec_index += 1

                    elif winner == 'Black' or winner == 'Draw':
                        i = 126
                        while i > -1:
                            if cover[i] == 'B':
                                new_row['cover' + str(rec_index)] = int(cover[i+1])
                            elif cover[i] == 'W':
                                new_row['cover' + str(rec_index)] = int(cover[i+1]) * -1
                            else:
                                new_row['cover' + str(rec_index)] = 0

                            if board[i] == 'B':
                                new_row['pieces' + str(rec_index)] = int(points[board[i+1]])
                            elif board[i] == 'W':
                                new_row['pieces' + str(rec_index)] = int(points[board[i+1]]) * -1
                            else:
                                new_row['pieces' + str(rec_index)] = 0

                            i -= 2
                            rec_index += 1
                    
                    else:
                        print('ERROR: Invalid game outcome')

                else:
                    new_row['win'] = 0
                    if winner == 'Black':
                        i = 0
                        while i < 128:
                            if cover[i] == 'W':
                                new_row['cover' + str(rec_index)] = int(cover[i+1])
                            elif cover[i] == 'B':
                                new_row['cover' + str(rec_index)] = int(cover[i+1]) * -1
                            else:
                                new_row['cover' + str(rec_index)] = 0

                            if board[i] == 'W':
                                new_row['pieces' + str(rec_index)] = int(points[board[i+1]])
                            elif board[i] == 'B':
                                new_row['pieces' + str(rec_index)] = int(points[board[i+1]]) * -1
                            else:
                                new_row['pieces' + str(rec_index)] = 0

                            i += 2
                            rec_index += 1

                    elif winner == 'White' or winner == 'Draw':
                        i = 126
                        while i > -1:
                            if cover[i] == 'B':
                                new_row['cover' + str(rec_index)] = int(cover[i+1])
                            elif cover[i] == 'W':
                                new_row['cover' + str(rec_index)] = int(cover[i+1]) * -1
                            else:
                                new_row['cover' + str(rec_index)] = 0

                            if board[i] == 'B':
                                new_row['pieces' + str(rec_index)] = int(points[board[i+1]])
                            elif board[i] == 'W':
                                new_row['pieces' + str(rec_index)] = int(points[board[i+1]]) * -1
                            else:
                                new_row['pieces' + str(rec_index)] = 0

                            i -= 2
                            rec_index += 1

                    else:
                        print('ERROR: Invalid game outcome')

                # Undo any cases where a draw is recorded as a winner (code uses the win/loss logic to record draws twice for both board orientations, but they should all be losses)
                if winner == 'Draw':
                    new_row['win'] = 0

                # Setup query
                temp_query = query
                temp_query += str(count) + ', ' + str(new_row['win']) + ', '

                for i in range(0, 64):
                    temp_query += str(new_row['pieces' + str(i)]) + ', '
                for i in range(0, 63):
                    temp_query += str(new_row['cover' + str(i)]) + ','

                temp_query += str(new_row['cover63']) + ');'

                # Commit data to database
                cursor.execute(temp_query)
                rec_as_winner = not rec_as_winner

            #if winner == 'Draw':
                #games_used -= 1
                #break

        cnx.commit()
        count += 1

    cnx.close()


# Count the number of training datapoints in CSV files
def count_training_data(root):
    # Determine directories for all game datafiles
    data = pd.DataFrame()
    files = []
    for loc in scandir(root):
        temp = listdir(loc.path)
        for file in temp:
            files.append(loc.path + '\\' + file)

    tot_len = 0

    for file in files:
        temp = pd.read_csv(file)
        tot_len += len(temp)

    print(tot_len)
    print(tot_len * 2)