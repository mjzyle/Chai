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

data = main()
boards = data['Ending Coverage'].tolist()
print(len(boards))
print(len(set(boards)))