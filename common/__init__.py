# %%
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def AE_plot_correlation(df31: pd.DataFrame, df33: pd.DataFrame) -> str:
    try:
        fig, ax = plt.subplots()
        ax.set_title(f"Aethalometer Comparison {df['dtm'].min().strftime('%Y-%m-%d %H:%M')} thru {df['dtm'].max().strftime('%Y-%m-%d %H:%M')}")
        ax.set_xlim(-500, 1000)
        ax.set_ylim(-500, 1000)
        ax.set_xlabel("AE33 BCn (ng/m3)")
        ax.set_ylabel("AE31 Xnc_A11 (ng/m3)")

        N = [1,2,3,4,5,6,7]
        
        for n in N:
            ax.scatter(df[f"BC{n}"], df[f"X{n}c_A11"], marker=".")

        # ax.scatter(df["BC1"], df["X1c_A11"], marker=".")
        # ax.scatter(df["BC2"], df["X2c_A11"], marker=".")
        # ax.scatter(df["BC3"], df["X3c_A11"], marker=".")
        # ax.scatter(df["BC4"], df["X4c_A11"], marker=".")
        # ax.scatter(df["BC5"], df["X5c_A11"], marker=".")
        # ax.scatter(df["BC6"], df["X6c_A11"], marker=".")
        # ax.scatter(df["BC7"], df["X7c_A11"], marker=".")

        # import numpy as np
        # z = np.polyfit(df["BC1"], df["X1c_A11"], 1)
        # p = np.poly1d(z)
        # ax.plot(df["BC1"], p(df["BC1"]))


    except Exception as err:
        print(err)

