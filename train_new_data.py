import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
from models import RegressionModel, Session


def train_regression_model(csv_file):
    data_frame = pd.read_csv(csv_file)
    data_frame.dropna(inplace=True)
    data_frame = data_frame[data_frame['area'] < 1000]

    cdf = data_frame[['area', 'region_id', 'price', 'building_year']]

    outlier_columns = ["area"] + \
                      [col for col in cdf.columns if "price" in col]
    cdf = cdf[cdf["area"] < 400][outlier_columns]

    cdf.reset_index(drop=True, inplace=True)

    x = cdf[['area', 'region_id', 'building_year']]
    y = cdf[['price']]

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=45)

    st_x = StandardScaler()
    x_train_std = st_x.fit_transform(x_train)
    x_test_std = st_x.transform(x_test)

    regression_model = LinearRegression()
    regression_model.fit(x_train_std, y_train)

    session = Session()
    new_model = RegressionModel(model_pickle=pickle.dumps(regression_model))
    session.add(new_model)
    session.commit()

    return regression_model
