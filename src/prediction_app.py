from pathlib import Path
import pandas as pd

import os

import skops.io as sio

def main() -> None:

    with open("model/model.bin", "rb") as f_out:
        model_lin_reg = sio.load(f_out)

    sample_input_feature = pd.DataFrame(
            [
                {
                    #"id": 1.77e9,
                    #"bedrooms": 2.0,
                    #"bathrooms": 1.75,
                    #"sqft_living": 1060.0,
                    #"sqft_lot": 16470.0,
                    #"floors": 1.0,
                    #"waterfront": 0.0,
                    #"view": 0.0,
                    #"condition": 3.0,
                    "grade": 7.0,
                    #"sqft_above": 1060.0,
                    #"sqft_basement": 0.0,
                    #"zipcode": 98072.0,
                    #"lat": 47.7409,
                    #"long": -122.089,
                    #"sqft_living15": 1790.0,
                    #"sqft_lot15": 16748.0,
                    "last_known_change": 1977.0,
                    "center_distance": 17.03975,
                    #"water_distance": 10.68189,
                }
            ]
        )

    predicted_price = model_lin_reg.predict(sample_input_feature)
    print(predicted_price)

if __name__ == "__main__":
        main()