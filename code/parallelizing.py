'''
This script is designed to carry out the "process_game" function from the notebook
'02_data_preparation.ipynb' in parallel on a virtual Ubuntu machine.  The script
automatically detects whether the "new player" is playing White or Black; it then
gets the top 10 moves for each of that new player's turns.  It also gets the
evaluations of ALL the actual positions achieved during the game.  As it goes,
it records the positions achieved as FEN strings.

The script processes a single CSV file at once; to process e.g. "train_1st.csv",
set the "csv_path" parameter below to the file path leading to "train_1st.csv".
Then to process "test_1st.csv" or "val_1st.csv", change the file path accordingly
and re-run this script.

The script outputs the processed information from each single game as its own
text file.  The name of each text file does NOT directly correspond to the name
of the new player who played that game; instead, it corresponds to the *row number*
in which that new player's game can be found in the inputted dataframe.  For example,
when running this script with train_1st.csv, the outputted file "game123.txt" in the
"train" folder corresponds to the game played in the 123rd row of train_1st.csv.
This was done in order to make it simple for the script to check which games still remain
to be processed and parallelize their processing across all the cores to be used.


To accomplish the parallelization, the script installs a number of copies of the
Stockfish binary equal to the number of cores you will use on your virtual machine.
Specify a parallel_size parameter (below) equal to the number of cores your
virtual machine will use at once.


BEFORE RUNNING THIS SCRIPT:
-Make sure you've installed Stockfish as a binary file
and also installed the "stockfish" and "chess" Python libraries.
-Make sure you've put the train_1st, test_1st and val_1st CSV files in the
same folder as this script (on your virtual machine).
-Make sure that this same folder has subfolders named "train", "test" and "val".
These will be the folders to which the processed games will be sent as text files.
-Make sure you specify all requested parameters in the "CHANGE THESE PARAMETERS"
section below.

'''


import os
import shutil
from multiprocessing import Pool
import time

import pandas as pd
import numpy as np

from stockfish import Stockfish
import chess

from helper_functions import format_game


## CHANGE THESE PARAMETERS ####################################################
#Specify the number of cores to use
parallel_size = 94
#Specify the number of games that each core should process (this can be larger
#than how many it will actually end up processing)
num_games_to_process = 10000

#Specify the path to your Stockfish binary file
#(below is the standard ubuntu path to stockfish when saved with apt-get)
stockfish_path = '/usr/games/stockfish'

#Specify the path to the file whose games you'd like to analyze.
#This should be either train_1st.csv, test_1st.csv or val_1st.csv.
csv_path = './train_1st.csv'
#Specify (with a string) whether this is a "train", "test" or "val" data set
kind = 'train'

###############################################################################

output_path = kind


games = pd.read_csv(csv_path, index_col='name_of_pl_playing_1st_game')

#get total number of games
tot_games = len(games)


def process_game(sf_num, game_num):
    '''
    sf_num: Index specifying which copy of Stockfish to use
    game_num: Which game number to process
    '''
    start = time.time()
    
    #Initialize Stockfish with a search depth of 15
    sf = Stockfish(stockfish_path + str(sf_num), depth=15)
 
    #Set the number of cores and amount of memory Stockfish can use
    sf.update_engine_parameters({
        "Hash":1024
    })
    
    moves = games.iloc[game_num]['moves'].split(' ')
    
    board = chess.Board()
    moves_dict = {}

    #get whether player is white or black
    new_player_type = games.iloc[game_num]['new_pl_color'].lower()
    
    for i, move in enumerate(moves):
        moves_dict[i] = {}
        print(sf_num, game_num)

        fen = board.fen()
        
        #Set Stockfish's position to the current position
        sf.set_fen_position(fen)

        
    
        #Get the evaluation of the current position
        moves_dict[i]['eval'] = sf.get_evaluation()

        #Store the fen position
        moves_dict[i]['fen'] = str(fen)
        
        #If this is the new player's turn, also get the top 10 moves
        if (i%2 == 0 and new_player_type == 'white') or (i % 2 == 1 and new_player_type == 'black'):
            moves_dict[i]['top_10'] = sf.get_top_moves(10)
        
        #Finally, make the move that was actually played
        board.push_san(move)
    
    end = time.time()
    
    print(end-start)

    #write moves_dict to text
    open(f"{output_path}/game{str(game_num)}.txt", "w+").write(str(moves_dict))





def process_multiple_games(sf_num):
    games_already_processed = set(os.listdir(output_path))
    games_to_process = range(sf_num, sf_num + num_games_to_process*parallel_size, parallel_size)
    for game in games_to_process:
        if "game" + str(game) + ".txt" in games_already_processed:
            continue
        process_game(sf_num=sf_num, game_num = game)





#Make copies of Stockfish, if they don't already exist
for i in range(parallel_size):
    if not os.path.exists(stockfish_path + str(i)):
        shutil.copy(stockfish_path, stockfish_path + str(i))


if __name__ == '__main__':
    pool = Pool(parallel_size)
    pool.map(process_multiple_games, [(sf_num) for sf_num in range(parallel_size)])
