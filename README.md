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