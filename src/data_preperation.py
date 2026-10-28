from pathlib import Path

import pandas as pd


def fill_missings_view_wf(df: pd.DataFrame) -> pd.DataFrame:
    """Fill nullable visibility features with explicit zeros."""

    df = df.copy()
    try:
        df["view"] = df["view"].fillna(0)
    except KeyError as error:
        raise KeyError("Required column 'view' is missing") from error

    try:
        df["waterfront"] = df["waterfront"].fillna(0)
    except KeyError as error:
        raise KeyError("Required column 'waterfront' is missing") from error
    
    return df


def sqft_basement(df: pd.DataFrame) -> pd.DataFrame:
    """Rebuild basement size from more reliable source columns."""

    df = df.copy()
    # Recompute the feature from two columns that already carry the needed information.
    try:
        df["sqft_basement"] = df["sqft_living"] - df["sqft_above"]
    except KeyError as error:
        raise KeyError("Required column 'sqft_living' or 'sqft_above' is missing") from error 
    
    return df

def calculate_last_change(df: pd.DataFrame) -> pd.DataFrame:
    """Create one `last_known_change` column from build + renovation year columns."""

    df = df.copy()
    last_known_change = []
    for idx, yr_re in df["yr_renovated"].items():
        # Missing or zero renovation years mean "no known renovation",
        # so the build year becomes the last known change.
        if str(yr_re) == "nan" or yr_re == 0.0:
            last_known_change.append(df["yr_built"][idx])
        else:
            # Otherwise preserve the renovation year as the latest known change.
            last_known_change.append(int(yr_re))

    # Add the consolidated feature and remove the redundant source columns.
    df["last_known_change"] = last_known_change
    df.drop("yr_renovated", axis=1, inplace=True)
    df.drop("yr_built", axis=1, inplace=True)
    
    return df


def main() -> None:

    data_path = (
        Path(__file__).resolve().parents[3]
        / "Repos"
        / "mle-refactoring-project"
        / "data"
        / "King_County_House_prices_dataset.csv"
    )
    df = pd.read_csv(data_path)

    print("King County preprocessing running...")
    print("")
    print(f"Missing `view`: {int(df['view'].isna().sum())}")
    print(f"Missing `waterfront`: {int(df['waterfront'].isna().sum())}")
    print("")
    print("Calling function for filling missing values...")
    df = fill_missings_view_wf(df)
    print(f"Missing `view`: {int(df['view'].isna().sum())}")
    print(f"Missing `waterfront`: {int(df['waterfront'].isna().sum())}")
    print("")
    print(f"`last_known_change` present: {'last_known_change' in df.columns}")
    print(f"`yr_built` present: {'yr_built' in df.columns}")
    print(f"`yr_renovated` present: {'yr_renovated' in df.columns}")
    print("")
    print("Calling function for building new feature `last_known_change` "
    "and dropping the others...")
    df = calculate_last_change(df)
    print(f"`last_known_change` present: {'last_known_change' in df.columns}")
    print(f"`yr_built` present: {'yr_built' in df.columns}")
    print(f"`yr_renovated` present: {'yr_renovated' in df.columns}")
    print("")
    print(f"`sqft_basement` dtype: {df['sqft_basement'].dtype}")
    print("Calling function for calculating `sqft_basement` new...")
    print("")
    df = sqft_basement(df)
    print(f"`sqft_basement` dtype: {df['sqft_basement'].dtype}")


if __name__ == "__main__":
        main()