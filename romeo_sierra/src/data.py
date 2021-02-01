import pandas as pd
from sklearn.decomposition import PCA
from enum import Enum, auto

from .data_fetch import get_historical_data, get_realtime_stream_data

class DataType(Enum):
    historical = auto()
    realtime = auto()
    PCA = auto()

class Data:
    """
    Class holding the data in both the raw format and the unmelted form.

    Attributes:
        data_type (DataType): String specifying whether the data is historical or realtime - realtime data will be the last 3 days of intra-day data.
        raw_data (pd.DataFrame): Dataframe containing the melted data (for future expandability - in case other functions added require it)
    """

    def __init__(self, data_type: DataType, data: pd.DataFrame=None) -> None:
        """
        Constructor for the Data class.

        Parameters:
            data_type (DataType): The type of data that the instance of the class contains.
            data (pd.DataFrame): The raw data, before melting, if available (not available for PCA data).
        """

        self.data_type = data_type
        self.data = data

    @classmethod
    def build_data(cls, stock_list: "List(str)", start_date: pd.Timestamp=None, end_date: pd.Timestamp=None, historical: bool=False) -> "Data":
        """
        Constructs an instance of the Data class by fetching historical or realtime data.

        Parameters:
            stock_list (list(str)): The list of stocks to be used
            start_date (pd.TimeStamp): The start date of the data, not required if realtime data is to be used
            end_date (pd.TimeStamp): The end date of the data, not required if realtime data is being used
            historical (bool): true if the data to fetch is historical, false if realtime data
        """

        data_type = DataType.historical if historical else DataType.realtime
        if historical:
            data = get_historical_data(start_date, end_date, stock_list)
            return Data(data_type, data)

    
    def PCA(self) -> "Data":
        """
        Function that carries out PCA on the data, tranforms the data to fit the PCA, and returns the PCA-calculated form of the data.

        Returns:
            Data: A Data object containing the transformed data.
        """

        pca = PCA(n_components=3)
        pca.fit(self.data)
        comps = pca.components_
        vals = pca.transform(self.data)
        pca_vals = vals @ comps + pca.mean_
        return Data(DataType.PCA, data=pd.DataFrame(pca_vals, index=self.data.index, columns=self.data.columns))