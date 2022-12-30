# -*- coding: utf-8 -*-
"""
Define a class AE31 facilitating work with Magee Scientific AE33 data.

@author: joerg.klausen@meteoswiss.ch
"""
# %%
import os
import matplotlib.pyplot as plt
import pandas as pd
# import doctest
import tarfile

# %%
class AE31:
    """Magee Scientific Aethalometer data as produced by mkndaq
    """

    def __init__(self):
        print("AE31 initialized.")


    def extract_file(self, file: str, sep=",", type=".tar.gz", filter="A11_", round="min") -> pd.DataFrame:
        """Read AE33 data file into a pd.DataFrame

        Args:
            file (str): full path to file
            sep (str, optional): field separator used in file. Defaults to "|".
            type (str, optional): Archive type. Defaults to ".tar.gz"
            filter (str, optional): Filter for file inside archive. Defaults to "A11_"
        Returns:
            pd.DataFrame: DataFrame with dtm and source columns added to data

        Usage:
        >>> file = r"~\Documents\git\magee\data\ae31\mkn_20200130T190013Z.tar.gz"
        >>> ae31 = AE31
        >>> df = ae31.read(file=file)
        >>> len(df)

        Shell command:
        $ python -m doctest -v ae31.py
        """
        try:
            cols = ["A11a", "STN", "EPOCH", "dtm", "Q_A11", "PCT_A11", 
                    "X1c_A11", "X2c_A11", "X3c_A11", "X4c_A11", "X5c_A11", "X6c_A11", "X7c_A11", 
                    "ZIr1_A11", "ZIr2_A11", "ZIr3_A11", "ZIr4_A11", "ZIr5_A11", "ZIr6_A11", "ZIr7_A11", 
                    "Ipz1_A11", "Ipz2_A11", "Ipz3_A11", "Ipz4_A11", "Ipz5_A11", "Ipz6_A11", "Ipz7_A11", 
                    "Ip1_A11", "Ip2_A11", "Ip3_A11", "Ip4_A11", "Ip5_A11", "Ip6_A11", "Ip7_A11", "Ifz1_A11", "Ifz2_A11", "Ifz3_A11", "Ifz4_A11", "Ifz5_A11", "Ifz6_A11", "Ifz7_A11", 
                    "If1_A11", "If2_A11", "If3_A11", "If4_A11", "If5_A11", "If6_A11", "If7_A11"]
            na_values = ["A11a", "ZZZ", "0", "9999-99-99T99:99:99Z", "0.00", "0.00", "000000", "000000", "000000", "000000", "000000", "000000", "000000", "000.000", "000.000", "000.000", "000.000", "000.000", "000.000", "000.000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000", "00.0000"]
            varfmt = ["A11a", "%s", "%u", "%04d-%02d-%02dT%02d:%02d:%02dZ", "*@01.2f", "*@01.2f", "*@06.0f", "*@06.0f", "*@06.0f", "*@06.0f", "*@06.0f", "*@06.0f", "*@06.0f", "*@03.3f", "*@03.3f", "*@03.3f", "*@03.3f", "*@03.3f", "*@03.3f", "*@03.3f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f", "*@02.4f"]

            with tarfile.open(file, "r:*") as tar:
                files = tar.getnames()
                fh = [s for s in files if "A11_" in s][0]
                df = pd.read_csv(tar.extractfile(fh), header=None, 
                                 skiprows=100, names=cols, sep=sep)
            
            df["dtm"] = pd.to_datetime(df["dtm"], utc=True)
            if round:
                df["dtm"] = df["dtm"].round(round)
            df['source'] = fh

            return df
        except Exception as err:
            print(err)


    def extract_files(self, path: str, type=".tar.gz", filter="A11_") -> pd.DataFrame:
        try:
            files = os.listdir(path)
            df = self.extract_file(file=os.path.join(path, files[0]))
            for file in files[1:]:
                df = pd.concat([df, self.extract_file(file=os.path.join(path, file))])
        
            return df
            
        except Exception as err:
            print(f"{file} : {err}")


    def remove_extremes(self, df: pd.DataFrame, q=0.01, index="dtm") -> pd.DataFrame:
        try:
            df.set_index(index, inplace=True)
            N = [1,2,3,4,5,6,7]
            for n in N:
                lower = df[f"X{n}c_A11"].quantile(q=q)
                upper = df[f"X{n}c_A11"].quantile(q=1-q)
                df.loc[(df[f"X{n}c_A11"] < lower) | (df[f"X{n}c_A11"] > upper), f"X{n}c_A11"] = None
            df.reset_index(inplace=True)
            return df

        except Exception as err:
            print(err)

    def plot(self, df: pd.DataFrame, index="dtm", path=None) -> None:
        try:
            fig, ax = plt.subplots()
            ax.set_title(f"AE31 [{df['dtm'].min().strftime('%Y-%m-%d %H:%M')} thru {df['dtm'].max().strftime('%Y-%m-%d %H:%M')}]")
            ax.set_ylabel("Xnc_A11 (ng/m3)")
            ax.plot(df["dtm"], df[["X1c_A11", "X2c_A11", "X3c_A11", "X4c_A11", "X5c_A11", "X6c_A11", "X7c_A11"]])

            if path:
                fig.savefig(fname=path, format="pdf")

        except Exception as err:
            print(err)
