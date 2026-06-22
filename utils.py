import pandas as pd

from config import CSV_FILE


def load_dataset():
    """
    Loads the sales dataset.
    """

    return pd.read_csv(CSV_FILE)