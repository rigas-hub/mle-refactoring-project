from pathlib import Path
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from data_preperation import fill_missings_view_wf, \
    sqft_basement, calculate_last_change
from feature_engineering import dist_to_center_of_wealth, dist_to_water

class FillingMissingValuesTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.is_fitted_ = True
        return self

    def transform(self, X, y=None):        
        X_transformed = fill_missings_view_wf(X)
        return X_transformed

class RebuildingSqftBasementTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.is_fitted_ = True
        return self

    def transform(self, X, y=None):        
        X_transformed = sqft_basement(X)
        return X_transformed

class CalculateLastChangeTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.is_fitted_ = True
        return self

    def transform(self, X, y=None):        
        X_transformed = calculate_last_change(X)
        return X_transformed

class DistToWealthCenterTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.is_fitted_ = True
        return self

    def transform(self, X, y=None):        
        X_transformed = dist_to_center_of_wealth(X)
        return X_transformed

class DistToWaterTransformer(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.is_fitted_ = True
        return self

    def transform(self, X, y=None):        
        X_transformed = dist_to_water(X)
        return X_transformed
    

def main() -> None:

    data_path = (
        Path(__file__).resolve().parents[3]
        / "Repos"
        / "mle-refactoring-project"
        / "data"
        / "King_County_House_prices_dataset.csv"
    )
    kc_df = pd.read_csv(data_path)

    filling_missing_values_transformer = FillingMissingValuesTransformer()

    print(f"Missing `view`: {int(kc_df['view'].isna().sum())}")
    print(f"Missing `waterfront`: {int(kc_df['waterfront'].isna().sum())}")
    kc_df = filling_missing_values_transformer.fit_transform(kc_df)
    print(f"Missing `view`: {int(kc_df['view'].isna().sum())}")
    print(f"Missing `waterfront`: {int(kc_df['waterfront'].isna().sum())}")

    rebuilding_sqft_basement_transformer = RebuildingSqftBasementTransformer()
    kc_df = rebuilding_sqft_basement_transformer.fit_transform(kc_df)

    calculate_last_change_transformer = CalculateLastChangeTransformer()
    kc_df = calculate_last_change_transformer.fit_transform(kc_df)
    


if __name__ == "__main__":
        main()