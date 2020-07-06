import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from science.utils import constants as AUDIO_CONSTANTS

data_labeled = pd.read_excel(AUDIO_CONSTANTS.RESOURCES_PATH + "//pandas_chords.xlsx")
plt.figure(figsize=(8, 4))
sns.countplot(x='classID', data=data_labeled)
plt.show()
print("Finished")