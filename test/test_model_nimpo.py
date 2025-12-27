import pandas as pd
from sklearn.linear_model import LinearRegression

def test_model_trains():
    df = pd.DataFrame({
        "points": [10, 20, 30],
        "age": [20, 30, 40]
    })
    X = df[["age"]]
    y = df["points"]

    model = LinearRegression()
    model.fit(X, y)

    assert model.coef_[0] != 0
