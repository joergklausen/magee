# -*- coding: utf-8 -*-
"""
Define a class AE33 facilitating work with Magee Scientific AE33 datat.

@author: joerg.klausen@meteoswiss.ch
"""
import matplotlib.pyplot as plt
import pandas as pd
import doctest

class AE33:
    """Magee Scientific Aethalometer data as produced by mkndaq
    """

    def __init__(self):
        print("AE33 initialized.")


    def extract_file(self, file: str, sep="|", round="min") -> pd.DataFrame:
        """Read AE33 data file into a pd.DataFrame

        Args:
            file (str): full path to file
            sep (str, optional): field separator used in file. Defaults to "|".

        Returns:
            pd.DataFrame: DataFrame with dtm and source columns added to data

        Usage:
        >>> file = r"~\Documents\git\magee\data\ae33\data\ae33-202212111300.zip"
        >>> df = read(file=file)
        >>> len(df)

        """
        try:
            cols = ["Inst_SN", "row_id", "dtm_1", 
                    "dtm", "unclear", "dtm_2", 
                    "RefCh1", "Sen1Ch1", "Sen2Ch1", 
                    "RefCh2", "Sen1Ch2", "Sen2Ch2", 
                    "RefCh3", "Sen1Ch3", "Sen2Ch3", 
                    "RefCh4", "Sen1Ch4", "Sen2Ch4", 
                    "RefCh5", "Sen1Ch5", "Sen2Ch5", 
                    "RefCh6", "Sen1Ch6", "Sen2Ch6", 
                    "RefCh7", "Sen1Ch7", "Sen2Ch7", 
                    "BC11", "BC12", "BC1", 
                    "BC21", "BC22", "BC2", 
                    "BC31", "BC32", "BC3", 
                    "BC41", "BC42", "BC4", 
                    "BC51", "BC52", "BC5", 
                    "BC61", "BC62", "BC6", 
                    "BC71", "BC72", "BC7", 
                    "K1", "K2", "K3", "K4", "K5", "K6", "K7", 
                    "unclear_2", # "BB"
                    "Pres", "Temp", 
                    "Flow1", "Flow2", "FlowC", 
                    "Temp_1", "Temp_2","Temp_3",
                    # "ContTemp", "SupplyTemp", "LedTemp",
                    "Stat_1", "Stat_2", "Stat_3", "Stat_4", "Stat_5", 
                    # "Status", "ContStatus", "DetectStatus", "LedStatus", "ValveStatus", 
                    "TapeAdvCount", "unknown_2", "unknown_3", "unknown_4", "unknown_5"
                    # "ID_com1", "ID_com2", "ID_com3", "fields_i"
                    ]

            df = pd.read_csv(file, sep=sep, header=None, names=cols)
            df["dtm"] = pd.to_datetime(df["dtm"], utc=True)
            # remove all data prior to the deployment date of instrument
            df.drop(df[df["dtm"] < pd.to_datetime("2022-12-09", utc=True)].index, inplace=True)

            df["dtm"] = df["dtm"].round(round)

            df["dtm_1"] = pd.to_datetime(df["dtm_1"])
            df["dtm_2"] = pd.to_datetime(df["dtm_2"])
            
            return df
        except Exception as err:
            print(err)


    def remove_extremes(self, df: pd.DataFrame, q=0.01, index="dtm") -> pd.DataFrame:
        try:
            df.set_index(index, inplace=True)
            N = [1,2,3,4,5,6,7]
            for n in N:
                lower = df.quantile(q, numeric_only=True)
                upper = df.quantile(1-q, numeric_only=True)
                df.loc[(df[f"BC{n}"] < lower[f"BC{n}"]) | (df[f"BC{n}"] > upper[f"BC{n}"]), f"BC{n}"] = None
            df.reset_index(inplace=True)        
            return df

        except Exception as err:
            print(err)


    def plot(self, df: pd.DataFrame, path=None) -> None:
        try:
            fig, ax = plt.subplots()
            ax.set_title(f"AE33 [{df['dtm'].min().strftime('%Y-%m-%d %H:%M')} thru {df['dtm'].max().strftime('%Y-%m-%d %H:%M')}]")
            ax.set_ylabel("BCn (ng/m3)")
            ax.plot(df["dtm"], df[["BC1", "BC2", "BC3", "BC4", "BC5", "BC6", "BC7"]])

            if path:
                fig.savefig(fname=path, format="pdf")

        except Exception as err:
            print(err)


