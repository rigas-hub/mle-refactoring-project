import pytest
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal

from src.data_preperation import fill_missings_view_wf

@pytest.mark.parametrize(
    "input_frame, expected_result",
    [
        (
            pd.DataFrame(
                {
                    "price": [100, 200, 150, 300],
                    "view": [1., np.nan, 4., np.nan],
                    "waterfront": [0, 1., np.nan, np.nan],
                }
            ),
            pd.DataFrame(
                {
                    "price": [100, 200, 150, 300],
                    "view": [1., 0, 4., 0],
                    "waterfront": [0, 1., 0, 0],
                }
            )
        )
    ],
)
def test_get_sum_score_by_brand_and_gender(input_frame, expected_result):
    # This check compares a grouped DataFrame, not just a single column.
    output_frame = fill_missings_view_wf(input_frame)
    assert_frame_equal(output_frame, expected_result)
    assert isinstance(output_frame, pd.DataFrame)
