import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def AE_correlation_plot(df31, df33, index="dtm", path=None) -> str:
    try:
        df31.set_index(index, inplace=True)
        df33.set_index(index, inplace=True)
        df = pd.merge(df31, df33, on="dtm", how="inner")
        df.reset_index(inplace=True)
        df.dropna(inplace=True)

        fig, ax = plt.subplots()
        ax.set_title(f"Aethalometer Comparison {df['dtm'].min().strftime('%Y-%m-%d %H:%M')} thru {df['dtm'].max().strftime('%Y-%m-%d %H:%M')}")
        ax.set_xlabel("AE33 BCn (ng/m3)")
        ax.set_ylabel("AE31 Xnc_A11 (ng/m3)")

        N = [1,2,3,4,5,6,7]
        for n in N:
            ax.scatter(df[f"BC{n}"], df[f"X{n}c_A11"], marker=".")

            z = np.polyfit(df[f"BC{n}"], df[f"X{n}c_A11"], 1)
            p = np.poly1d(z)
            print(f"{n} : {p}")
            ax.plot(df[f"BC{n}"], p(df[f"BC{n}"]))

        if path:
            fig.savefig(fname=path, format="pdf")

    except Exception as err:
        print(err)
