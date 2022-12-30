# %%
import os
from ae31.ae31 import AE31
from ae33.ae33 import AE33
import common.common as common

ae31 = AE31()
ae33 = AE33()

# %%
path = r"~\Documents\git\magee\data\ae31"
df31 = ae31.extract_files(path=os.path.expanduser(path))
df31 = ae31.remove_extremes(df=df31, q=0.01)
path = os.path.join(os.path.expanduser(r"~\Documents\git\magee"), "figures", "AE31.pdf")
ae31.plot(df31, path=path)

# %%
file = r"~\Documents\git\magee\data\ae33\data\ae33-202212230940.zip"
df33 = ae33.extract_file(file=file)
df33 = ae33.remove_extremes(df=df33, q=0.01)
path = os.path.join(os.path.expanduser(r"~\Documents\git\magee"), "figures", "AE33.pdf")
ae33.plot(df33, path=path)

# %%
path = os.path.join(os.path.expanduser(r"~\Documents\git\magee"), "figures", "AE_correlation.pdf")
common.AE_correlation_plot(df31, df33, path=path)
# %%
