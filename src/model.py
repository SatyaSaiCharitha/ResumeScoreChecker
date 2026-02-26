from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import pickle

def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)

    print("MSE:", mse)
    print("RMSE:", rmse)
    print("R2 Score:", r2)

    return model


def save_model(model, path='resume_model.pkl'):
    with open(path, 'wb') as f:
        pickle.dump(model, f)


# 👇 THIS PART IS IMPORTANT
if __name__ == "__main__":
    print("This file contains model functions only.")
    print("Run main.py to train the model.")