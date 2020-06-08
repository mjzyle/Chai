import pandas as pd
from os import listdir


def main():
    files = listdir('raw_data/valid_data')
    master_data = pd.DataFrame(columns=['Game', 'Move', 'Turn', 'Moving Player', 'Starting Board', 'Ending Board', 'In Check', 'Coverage Start', 'Coverage End', 'Winner'])

    i = 1
    for file in files:
        temp = pd.read_csv('raw_data/valid_data/' + file)
        temp['Game'] = i
        winner = temp.loc[len(temp)-1, 'In Check']
        temp['Winner'] = winner

        for j in range(0, len(temp)):
            temp.loc[j, 'Move'] = int(j+1)

        master_data = master_data.append(temp, ignore_index=True)
        
        print(str(i) + ' of ' + str(len(files)) + ' added')
        i += 1

    return master_data


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


mean, median, ran, minm, maxm = get_num_turns_to_win(['raw_data/run5_n40_random_style_selection_w_timing/wins', 'raw_data/run4_n40_random_style_selection/wins'])
print(mean)
print(median)
print(minm)
print(maxm)
print(ran)