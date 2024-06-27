import numpy as np
import pandas as pd
from scipy.stats import shapiro

df = pd.read_csv('../../Data/Hepsiburada/3_ClassifiedData/version_1/analysed_hepsiburada.csv', sep=',')

cv = np.std(df['sentiment']) / np.mean(df['sentiment'])
print(f"Coefficient of Variation: {cv}")

df.dropna(subset=['sentiment'], inplace=True)
# Shapiro-Wilk test for normality (null hypothesis: Data is normally distributed)
_, p_value = shapiro(df['sentiment'])
print(f"Shapiro-Wilk test p-value: {p_value}")