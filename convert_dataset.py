from typing import List
import csv
import os
import sys
from constants import *

csv.field_size_limit(sys.maxsize) # To deal with really long reviews

FILE_IN = os.path.join(DATASET_FOLDER, "steam_reviews_all.csv")
FILE_OUT = os.path.join(DATASET_FOLDER, "steam_reviews_all_filtered.csv")

APP_NAMES_OUT = os.path.join(DATASET_FOLDER, "app_names.csv")

REMOVE_HEADERS = ['', 'review', 'review_id']
remove_headers_indexes = [] # to be filled by the script

app_names = []
app_ids_set = {} # For fast lookup


def update_headers(headers: List[str]) -> List[str]:
    """
    Returns the updated header list without columns to be removed.
    """
    print(f"Original headers: {headers}")
    new_headers = []
    for i, header in enumerate(headers):
        if header in REMOVE_HEADERS:
            # If the column must be removed, store its index tofilter it out in entries' rows
            remove_headers_indexes.append(i)
        else:
            # Otherwise simply keep it
            new_headers.append(header)
    print(f'New headers: {new_headers}')
    return new_headers


def filter_row(row: List[str]) -> List[str]:
    """
    Returns the updated row by removing the indexes from removed columns
    """
    return [elem for idx,elem in enumerate(row) if idx not in remove_headers_indexes]


def update_apps(app_id, app_name):
    """
    Stores a new (app_id, app_name) pair, provided that no entry with the same app_id was previously found.
    """
    if app_id not in app_ids_set:
        app_names.append([app_id, app_name])

if __name__ == '__main__':
    # Open the in/out files and CSV handlers
    with open(FILE_IN, "r", newline='') as fin:
        reader = csv.reader(fin, delimiter=',', quotechar='"')
        with open(FILE_OUT, "w",) as fout:
            writer = csv.writer(fout, delimiter=',', quotechar='"')

            # Iterate over lines
            for line_num, row in enumerate(reader):
                # Special case for the headers line
                if line_num == 0:
                    headers = update_headers(row)
                    writer.writerow(headers)
                    continue

                app_id, app_name = row[1], row[2]
                update_apps(app_id, app_name)
                writer.writerow(filter_row(row))

                # Print something every 1M lines for progress feedback
                if line_num % 1000000 == 0:
                    print(f"{line_num} rows processed...")

    # Save the app_id to app_name mapping
    with open(APP_NAMES_OUT, "w") as fout:
        writer = csv.writer(fout, delimiter=',', quotechar='"')

        writer.writerow(["app_id,app_name"])
        writer.writerows(app_names)