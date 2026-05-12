import pandas as pd
import numpy as np

def load_data():

    np.random.seed(42)
    n = 500

    df = pd.DataFrame({
        "Time": pd.date_range("2024-01-01", periods=n, freq="h"),
        "value": np.sin(np.linspace(0, 20, n)) * 10 + np.random.randn(n)
    })

    threshold = df["value"].mean() - df["value"].std()
    df["fault"] = (df["value"] < threshold).astype(int)

    df["rul"] = df["value"].max() - df["value"]

    return df