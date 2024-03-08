"""
Filter out patients that are not oropharynx.
"""
import pandas as pd


if __name__ == "__main__":
    # Load data
    data = pd.read_csv("data/enhanced.csv", header=[0,1,2])

    # Filter
    is_oropharynx = data["tumor", "1", "subsite"].str.contains(r"^C(01|09|10)")
    has_nan_extension = data["tumor", "1", "extension"].isna()
    filtered_data = data[is_oropharynx & ~has_nan_extension]

    # Save
    filtered_data.to_csv("data/filtered.csv", index=False)
