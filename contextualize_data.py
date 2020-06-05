import pandas as pd
import aggregate_data

data = aggregate_data.main()
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

cont_data.to_csv('raw_data/valid_data/context.csv')