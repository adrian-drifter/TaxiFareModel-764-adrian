# imports
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import numpy as np
from TaxiFareModel.utils import compute_rmse
from sklearn.linear_model import LinearRegression
from TaxiFareModel.encoders import TimeFeaturesEncoder, DistanceTransformer
from TaxiFareModel.data import get_data, clean_data

from sklearn import set_config; set_config(display='diagram')


class Trainer():
    def __init__(self, X, y):
        """
            X: pandas DataFrame
            y: pandas Series
        """
        self.pipeline = None
        self.X = X
        self.y = y

    def set_pipeline(self):
        """defines the pipeline as a class attribute"""
        # create distance pipeline
        dist_pipe = Pipeline([('dist_trans', DistanceTransformer()),
        ('stdscaler', StandardScaler())
        ])

        time_pipe = Pipeline([('time_enc',
                               TimeFeaturesEncoder('pickup_datetime')),
                              ('ohe', OneHotEncoder(handle_unknown='ignore'))])

        preproc_pipe = ColumnTransformer([('distance', dist_pipe, [
            "pickup_latitude", "pickup_longitude", 'dropoff_latitude',
            'dropoff_longitude'
        ]), ('time', time_pipe, ['pickup_datetime'])],
                                         remainder="drop")
        self.pipeline = Pipeline([('preproc', preproc_pipe),
                         ('linear_model', LinearRegression())])

        return self.pipeline


    def run(self):
        """set and train the pipeline"""
        self.set_pipeline()

        self.pipeline.fit(self.X, self.y)



    def evaluate(self, X_test, y_test):
        """evaluates the pipeline on df_test and return the RMSE"""
        y_pred = self.pipeline.predict(X_test)

        rmse = compute_rmse(y_pred, y_test)
        print(rmse)
        return rmse


if __name__ == "__main__":
    # get data
    df = get_data()
    # clean data
    clean_df = clean_data(df)
    # set X and y
    y = clean_df['fare_amount']
    X = clean_df.drop(columns=['fare_amount'])
    # hold out

    # train
    # evaluate
    print('TODO')
