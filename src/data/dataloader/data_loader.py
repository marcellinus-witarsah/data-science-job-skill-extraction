import pandas as pd
from types import NoneType
from typing import Union
from pathlib import Path


class DataLoader:
    @staticmethod
    def load_data(path: str) -> Union[NoneType, pd.DataFrame]:
        """Read data and return it as a Pandas DataFrame

        Args:
            path (str): path of the data

        Returns:
            NoneType, pd.DataFrame: return a Pandas DataFrame otherwise return NoneType
        """
        path = Path(path)  # convert the data from string to path
        assert path.exists() == True  # check if the path exists
        if path.suffix == ".csv":
            return pd.read_csv(path)
        return None
