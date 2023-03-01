# Summary
In this project, we create models aimed at better matchmaking for new players on online chess platforms.  To achieve better matchmaking, models need to be able to make good *probabilistic* predictions of the outcomes of future games: if they can make good predictions, then a good match can be made by pairing two players such that the predicted probability of either one winning is close to 50%.

In addressing this problem, our primary innovation - as compared to existing player rating / matchmaking systems like Elo and Glicko - is to look at not only the *outcomes* of players' games but also the *moves* that the players made during their games.  We use the chess engine [Stockfish](https://github.com/official-stockfish/Stockfish) to evaluate players' moves and positions, then we feed these evaluations, along with other metadata about the players and their games, to a neural network model.

Considering the 2-week timeframe of this project and the heavy computational resources required, our production model is a proof-of-concept aimed at solving a simple instance of the general problem of better predictions of game outcomes for new players.  We task ourselves with predicting the outcome of a new player's *2nd-ever game* on the online chess platform [Lichess](https://lichess.org/) using only data from that player's *1st game* along with metadata about the upcoming game and about the new player's opponent's last game.

Our production model makes significant improvements upon widely-used existing models; see the "Results" section below for details.






# Background
The primary systems used to rate players and predict the outcomes of their games are [Elo](https://en.wikipedia.org/wiki/Elo_rating_system) and [Glicko](https://www.glicko.net/glicko.html).  The [International Chess Federation (FIDE)](https://www.fide.com/) uses the Elo to rate its players, while many chess websites (including Lichess.org) use variants of the more advanced [Glicko rating system](https://www.glicko.net/glicko.html).  For a good introduction to the most basic variant, Glicko-1, see [this document](https://www.glicko.net/glicko/glicko.pdf).

Both the Elo and Glicko systems model players' skill through a "rating" score in such a way that if two players P1 and P2 have ratings $r_1$ and $r_2$ prior to playing each other, then the expected probability that P1 defeats P2 is a logistic function of the ratings difference $r_1 - r_2$.  The Elo scoring system updates players' ratings based on who defeats whom, and the ratings of the players who won/lost.  The Glicko system also tracks each player's "ratings deviation" - a measure of our uncertainty about the player's true skill level, which decreases as the player plays more games - and updates players' ratings based on who defeated whom, the ratings of those players, and the ratings deviations of those players.

There have been several attempts at improving rating/prediction models.  The [Deloitte/FIDE Chess Rating Challenge](https://www.kaggle.com/c/ChessRatings2/overview/custom), for example, asked competitors to use game metadata to make low-BCE-loss probabilistic predictions of the outcomes of games.[^1]  However, to our knowledge no widely-used model employs *move data* to predict the outcomes of games.

[^1]: Technically it ranked models on the basis of their [Binomial Deviance](https://stats.stackexchange.com/questions/371476/calculate-binomial-deviance-binomial-log-likelihood-in-the-test-dataset) from the true outcomes, but this is just a constant times BCE loss.


# Data

We use [all the games played on Lichess.org in July of 2016](https://www.kaggle.com/datasets/arevel/chess-games).  From these data, we determine who the *new players* are by finding players whose rating at the start of their first game of the month was exactly 1500 (the starting rating on Lichess).  We perform various data-cleaning tasks described in notebook [01](./code/01_data_processing.ipynb), such as dropping games that last fewer than 10 moves (i.e. 5 moves per player).  Then for each new player, we extract the following games:

- That new player's 1st-ever game on Lichess,
- That player's 2nd-ever game on Lichess, and
- That player's 2nd-game opponent's most recent previous game (if it exists).

We perform a triple split on these data, reserving 1500 new players' worth of data as "test" data for selecting our best-performing models and another 1500 new players' worth of data as "validation" data to be used only for final comparisons of our models.  This leaves us with 20,420 new players' worth of data to use for training our models.

From each of the games mentioned above - 1st, 2nd, and opponent's previous - we extract "metadata" such as the players' ratings and the time controls used for that game.  Finally, from each new player's *1st game*, we extract the sequence of moves made in that game.  We feed these move data to Stockfish in order to obtain data that can be fed into a neural network model.  The computations we request from Stockfish require large computational resources; see the "Instructions to Replicate this Project" section below for details about replication.


# Metrics for Evaluating Models

We evaluate our models primarily on the basis of their probabilistic predictions' [binary cross-entropy (BCE)](https://en.wikipedia.org/wiki/Cross_entropy) with the true outcomes.  See notebook [04](./code/04_baseline_models.ipynb) for a discussion of why this is a good metric for evaluating models' predictions when one is interested in good matchmaking.  We also evaluate our models on the basis of their probabilistic predictions' mean absolute error (MAE) from the true outcomes and on the basis of the Accuracy score of their *discrete* predictions (among cases where the game to be predicted did not result in a draw).  In all cases, we compare models' performance using the untouched validation data.

# Results

Our production model represents a significant improvement over existing models.  Consider the "Glicko" model - we use quotation marks since we can't perfectly replicate its predictions with the available data.[^2]  This "Glicko" model represents a large improvement over the baseline "uninformed" model - the one that always predicts that either player has a 50% chance to win - in terms of BCE loss, MAE loss and accuracy score.  However, our production model achieves:

- An additional reduction in BCE loss that is 44.6% as large as the original improvement made by the "Glicko" model,
- An additional reduction in MAE loss that is 59.0% as large as the original improvement made by the "Glicko" model, and
- An additional incrase in Accuracy score that is 20.0% as large as the original improvement made by the Glicko model.[^3]

In this simple proof-of-concept project, the majority of our production model's improvements over existing models are achieved through the introduction of a neural network and *not* by looking at data on the *moves* a new player made in her 1st game.  Indeed, the analogous "additional improvements over Glicko" made by a baseline neural network model (that does not look at move data) are 34.6% for BCE, 35.7% for MAE, and 16.8% for accuracy.  However, with a more advanced production model that incorporates *multiple* games' worth of move data from new players, one might expect the production model to achieve larger improvements over the baseline neural network model.

[^2]: It was not possible to precisely reconstruct the *probabilistic* predictions of Lichess's Glicko model with the data they provide, so our comparison is to a simpler Glicko-like model's probabilistic predictions.  Our simpler "Glicko" model finds the optimal *average* ratings deviation to use as the ratings deviation for *all* players, rather than having access to per-player ratings deviation data.  If the data necessary to create a proper Glicko model were available, though, we could also incorporate these data into a better production model and would likely still see an improvement over the true Glicko model.

[^3]: This last mention of Glicko does not need quotation marks, as we *can* perfectly replicate the *binary* predictions made by the Glicko model used by Lichess.org.  Thus, this Accuracy improvement is one way in which our production model *definitively* improves upon a state-of-the-art model.

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

10. Run notebooks [04](./code/04_baseline_models.ipynb) and [05](./code/05_nn_modeling.ipynb).  You may need to install PyTorch with `pip install torch`.