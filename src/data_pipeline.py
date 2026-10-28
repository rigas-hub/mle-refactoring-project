from pathlib import Path
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from transformers import FillingMissingValuesTransformer,\
      RebuildingSqftBasementTransformer, CalculateLastChangeTransformer, \
      DistToWealthCenterTransformer

import os

import skops.io as sio


def data_preperation_pipeline(data_path):
     
     kc_data = pd.read_csv(data_path)
     
     data_preperation_pipeline = Pipeline(
             [
                 ("filling_missing_values", FillingMissingValuesTransformer()),
                 ("rebuilding_sqft_basement", RebuildingSqftBasementTransformer()),
                 ("calculate_last_change", CalculateLastChangeTransformer()),
                 ("dist_to_wealth_center_feature", DistToWealthCenterTransformer()),
             ]
         )
     
     # Run pipeline
     kc_data = data_preperation_pipeline.fit_transform(kc_data)

     return kc_data

    

def main() -> None:
    
    data_path = (Path(__file__).resolve().parents[3]
              / "Repos"
              / "mle-refactoring-project"
              / "data"
              / "King_County_House_prices_dataset.csv"
    )

    kc_data = data_preperation_pipeline(data_path)

     # Remove columns that would cause data leakage or add no predictive value.
    drop_lst = [
        "price",
        "sqft_price",
        "date",
        "delta_lat",
        "delta_long",
    ]
    
    # Keep all remaining variables as candidate features.
    all_features = [x for x in kc_data.columns if x not in drop_lst]
    

    # `X` contains the descriptive variables defined above.
    X = kc_data[all_features]
        
    # Define `y` as the target variable.
    y = kc_data.price
        
    # Split the data into training and test sets. We reserve 30% for evaluation.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    # Instantiate the model.
    model_lin_reg = LinearRegression()

    # Train the model.
    model_lin_reg.fit(X_train, y_train)

    print(f"R^2: {round(model_lin_reg.score(X_test, y_test), 2)}")

    sample_input_feature = pd.DataFrame(
        [
            {
                "id": 1.77e9,
                "bedrooms": 2.0,
                "bathrooms": 1.75,
                "sqft_living": 1060.0,
                "sqft_lot": 16470.0,
                "floors": 1.0,
                "waterfront": 0.0,
                "view": 0.0,
                "condition": 3.0,
                "grade": 7.0,
                "sqft_above": 1060.0,
                "sqft_basement": 0.0,
                "zipcode": 98072.0,
                "lat": 47.7409,
                "long": -122.089,
                "sqft_living15": 1790.0,
                "sqft_lot15": 16748.0,
                "last_known_change": 1977.0,
                "center_distance": 17.03975,
                #"water_distance": 10.68189,
            }
        ]
    )

    predicted_price = model_lin_reg.predict(
         sample_input_feature)

    print(predicted_price)
    
    # Create the directory if it does not already exist.
    os.makedirs("model", exist_ok=True)
    with open("model/model.bin", "wb") as f_out:
        sio.dump(model_lin_reg, f_out)

if __name__ == "__main__":
        main()