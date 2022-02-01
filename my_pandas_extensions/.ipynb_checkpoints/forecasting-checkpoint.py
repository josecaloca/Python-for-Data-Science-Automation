import pandas as pd
import numpy as np

from sktime.forecasting.arima import AutoARIMA

from tqdm import tqdm

import pandas_flavor as pf

@pf.register_dataframe_method
def arima_forecast(
    data, h, sp, alpha = 0.05, 
    suppress_warnings = True, 
    *args, **kwargs
    ):

    # Checks

    # Handle Inputs ----
    df = data

    # FOR LOOP ----

    model_results_dict = {}
    for col in tqdm(df.columns, mininterval=0):

        # Series Extraction
        y = df[col]

        # Modeling
        forecaster = AutoARIMA(
            sp = sp, 
            suppress_warnings = suppress_warnings,
            *args, 
            **kwargs
        )

        forecaster.fit(y)

        # Predictions & Conf Intervals

        predictions, conf_int_df = forecaster.predict(
            fh              = np.arange(1, h+1),
            return_pred_int = True,
            alpha           = alpha 
        )

        # Combine into data frame
        ret = pd.concat([y, predictions, conf_int_df], axis=1)
        ret.columns = ["value", "prediction", "ci_lo", "ci_hi"]

        # Update Dictionary
        model_results_dict[col] = ret

    # Stack Each Dict Element on Top of Each Other
    model_results_df = pd.concat(
        model_results_dict, 
        axis=0
    )

    # Handle Names
    nms = [*df.columns.names, *df.index.names]
    model_results_df.index.names = nms

    # Reset Index
    ret = model_results_df.reset_index()

    # Drop columns containing "level"
    cols_to_keep = ~ret.columns.str.startswith("level_")

    ret = ret.iloc[:, cols_to_keep]

    return ret
