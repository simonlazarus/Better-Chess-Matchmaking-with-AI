# Summary
In this project, we create models aimed at better matchmaking for new players on online chess platforms.  Our primary innovation, as compared to existing player rating / matchmaking systems like Elo and Glicko, is to look at not only the *outcomes* of players' games but also the *moves* that the players made during their games.  We use the chess engine [Stockfish](https://github.com/official-stockfish/Stockfish) to evaluate players' moves and positions, then we feed these evaluations, along with other metadata about the players and their games, to a neural network model.

Considering the 2-week timeframe of this project and the heavy computational resources required, our production model is a proof-of-concept aimed at solving a simple instance of the general problem of better predictions of game outcomes for new players.  We task ourselves with predicting the outcome of a new player's *2nd-ever game* on [Lichess](https://lichess.org/) using only data from that player's *1st game* along with metadata about the upcoming game and about the new player's opponent's last game.

Our production model makes significant improvements upon widely-used existing models.  Its prediction accuracy is (PUT NUMBERS HERE) which improves upon the widely used Glicko and Elo models - used by Lichess, the International Chess Federation, and other organizations - by (PUT NUMBERS HERE).  More importantly, our model's *probabilistic* predictions have lower Binary Cross-Entropy (BCE) loss than those made by the Elo model and a simple variant of the Glicko model[^1]: (PUT NUMBERS HERE).  Since the aim of good chess matchmaking is to pair together players into matches where neither player has an overwhelming probability of winning, getting *probabilistic* predictions with low BCE loss is essential.


[^1]: It was not possible to precisely reconstruct the probabilistic predictions of Lichess's Glicko model with the data they provide, so our comparison is to a simpler Glicko-like model's probabilistic predictions.  If the necessary data were available to incorporate into a Glicko model, we could also incorporate these data into a better production model and would likely still see an improvement.



# Background
[Deloitte/FIDE Chess Rating Challenge](https://www.kaggle.com/c/ChessRatings2/overview/custom)



# Instructions to Replicate this Project
After forking and cloning this repository, do the following:
1. Install the [Stockfish App](https://github.com/official-stockfish/Stockfish).  This can be installed on Mac with the terminal command `brew install stockfish`.
2. Install the `stockfish` [Python API wrapper](https://pypi.org/project/stockfish/).  This can be installed with `pip install stockfish`.
3. Install the `chess` Python library with `pip install chess`.
4. Inside the `data` folder in this repository, create subfolders called `processed` and `sf_evals`.  In each of the two folders "processed" and "sf_evals", create three subfolders named `train`, `test` and `val`.

The following steps replicate our data collection and processing.  To skip any number of these steps, you can simply download our already-processed data from the [Google Drive data folder](https://drive.google.com/drive/folders/1Y2fCb8YP5Xd3ju7e0uTGtohQA_94pU-w?usp=sharing) for this project.  The fully-processed datasets used for training our neural network models are the pickled dictionaries `train.pcl`, `test.pcl` and `val.pcl` in the `sf_evals` subfolder (or equivalently, the corresponding `.txt` files).  The prcoessed `.csv` datasets, which we use for our baseline modeling, are the files in the `processed/train`, `processed/test` and `processed/val` folders.  Each folder contains three `.csv` files, named "1st", "2nd" and "opp".  If skipping steps 5-9, make sure to download all of these files to the same directories in which they appear on the Google Drive.

5. Download the dataset of [all the games played on Lichess.org in July of 2016](https://www.kaggle.com/datasets/arevel/chess-games).  Put it in the "data" folder.
6. Run notebooks [01](./code/01_data_processing.ipynb) and [02](./code/02_data_preparing.ipynb) in the "code" folder.
7. Using your own machine or ideally a virtual machine with many cores, open the [script to parallel-compute the Stockfish scores for all of the games](./code/parallelizing.py).  Follow the instructions written in the comments at the top of that script; you will have to edit indicated parameters.  Run the script on your (vitrual) machine.  (Our project used a virtual machine with 94 cores and this step took a little over 24 hours.)
8. Move the outputted `.txt` files from your (virtual) machine into the "sf_evals" folder, filing them into the "train", "test" and "val" subfolders as appropriate.
9. Run the notebook [03](./code/03_stockfish_processing.ipynb) in the "code" folder.

After this, all of the files mentioned above will have been created.

10. Run the remaining notebooks in the `code` folder (in order).  You may need to install PyTorch with `pip install torch`.