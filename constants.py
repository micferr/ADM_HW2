import os

# The number of lines to read from the dataset file
# Setting this value to None causes the notebook to load the whole dataset
NUM_ROWS_TO_LOAD = None

# The name of the folder where all datasets' files are stored
DATASET_FOLDER = "data"

# The nlimit parameter to be used in plots, selecting only the top elements for each query to prevent
# the plots from being unreadable
PLOT_LIMIT = 20

# Used to filter outliers (instances with too few occurrences to be relevant).
# Note that we limit outputs both by filtering outliers (by using this parameter) and by
# imposing an overall limit (the PLOT_LIMIT parameter)
MIN_COUNT = 1000

# Path to the complete dataset file (including bonuses), relative to the working directory
DATASET_PATH = os.path.join(DATASET_FOLDER, "steam_reviews_all_filtered.csv")

# Number of seconds in a day
SECONDS_IN_DAY = 60*60*24