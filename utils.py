from collections import defaultdict
from datetime import datetime
from typing import Any, Callable, Dict, List, Union

import csv
import json

import matplotlib.pyplot as plt
import pandas as pd

from constants import *

import sys
import csv

csv.field_size_limit(sys.maxsize)

class Review():
    """Utility class to manage entries in the filtered dataset."""

    def __init__(self, data):
        self.app_id, self.app_name = int(data[0]), data[1]
        self.language = data[2]
        self.timestamp_created, self.timestamp_updated = datetime.fromtimestamp(int(data[3])), datetime.fromtimestamp(int(data[4]))
        self.recommended = data[5] == 'True'
        self.votes_helpful = int(data[6])
        self.votes_funny = int(data[7])
        self.weighted_vote_score = float(data[8])
        self.comment_count = int(data[9])
        self.steam_purchase = data[10] == 'True'
        self.received_for_free = data[11] == 'True'
        self.written_during_early_access = data[12] == 'True'
        self.author_steamid = data[13]
        self.author_num_games_owned = int(data[14])
        self.author_num_reviews = int(data[15])
        self.author_playtime_forever = float(data[16] or 0)
        self.author_playtime_last_two_weeks = float(data[17] or 0)
        self.author_playtime_at_review = float(data[18] or 0)
        self.author_last_played = float(data[19] or 0)

    def __str__(self):
        return json.dumps(self)


class DatasetIterator():
    """
    Utility class to deal comfortably with the dataset, since it isn't manageable to load it all in memory,
    with pandas thus having limited utility since some requests need aggregate data and a custom processing
    layer must be implemented anyway.
    Pandas may still be used on the aggregated results as a utility around plotting.
    """

    def __init__(self, dataset_path, limit, skip=0, verbose=False):
        self.dataset_path = dataset_path
        self.limit = limit # How many lines to read
        self.skip = skip
        self.verbose = verbose

    def apply(self, f: Callable[[Review], None], include_if: Callable[[Review], bool] = None) -> None:
        """
        Calls f on each entry in the dataset. f is meant to be able to read/write variables in its scope
        to return outputs.
        An optional predicate can be specified to only process a subset of all entries
        """
        with open(self.dataset_path, "r", newline='') as fin:
            reader = csv.reader(fin, delimiter=',', quotechar='"')
            for line_count, row in enumerate(reader):
                if line_count == 0 or line_count < self.skip:
                    continue

                try:
                    review = Review(row)
                    if (not include_if) or include_if(review):
                        f(review)
                except Exception as e:
                    pass # ignore possible malformed entries

                if self.verbose and line_count % 1e7 == 0:
                    print(f"{line_count} entries processed...")
                if self.limit and line_count == self.limit + self.skip:
                    return


def defaultdict0():
    """
    Utility for a defaultdict with 0 as its default argument, which will be used often.
    """
    return defaultdict(lambda: 0)


def mean(l: List) -> float:
    """
    Return the mean value of an array of numerical values.
    """
    return sum(l)/len(l)


def compute_means(sums: Dict, counts: Dict) -> Dict:
    """
    Given an accumulator and a counter dicts, computes the means for each key by dividing the sums by their counts.
    """
    return {
        k:sums[k]/counts[k] for k in counts
    }


def map_dict(d: Dict, f: Callable[[Any], Any]) -> Dict:
    """
    Given a dict, updates each value by applying a function to it
    """
    return {k: f(v) for k,v in d.items()}


def show_barplot_for_dict(
    d: Dict[str, Union[int, float]],
    title: str,
    xlabel: str,
    ylabel: str,
    column_name: str = "_unused",
) -> pd.DataFrame:
    """
    Given a dict mapping string keys to numerical values (e.g. for counters, averages, accumulators), plot it
    on a bar plot.

    :param d: the dict to plot
    :param title: the plot's title
    :param xlabel: the label for the X axis
    :param ylabel: the label for the Y label
    """
    df = pd.DataFrame(d.values(), columns=[column_name], index=d.keys())
    plt.show(df.nlargest(PLOT_LIMIT, column_name).plot.bar(
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
    ))
    return df