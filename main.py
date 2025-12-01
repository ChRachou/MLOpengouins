# import load_data from src.pengouins.data
# from load_data import src.pengouins.data
from src.pengouins.data import load_data
from src.pengouins.data import get_X_y
from src.pengouins.data import split_data
from src.pengouins.data import preprocess_data
from src.pengouins.data import train_model
from src.pengouins.data import evaluate_model
 

data = load_data("data/pingouins.csv")

X, y = get_X_y(data, 'species')

# print(f"X: {X}")
# print(f"X shape: {X.shape}")
# print(f"y: {y}")
# print(f"y shape: {y.shape}")
# x = get_X_y(data, 'species', False )

X_train, X_test, y_train, y_test = split_data(X, y)

# print(f"X_train shape: {X_train.shape}")
# print(f"X_test shape: {X_test.shape}")
# print(f"y_train shape: {y_train.shape}")
# print(f"y_test shape: {y_test.shape}")
# print(data.head())

X_train_preproc = preprocess_data(X_train)
X_test_preproc = preprocess_data(X_test)
# print(X_train_preproc)
# print(X_test)

logi_final = train_model(X_train_preproc, y_train)
# print(logi_final)
score = evaluate_model(logi_final, X_train_preproc, y_test)
print(score)
if __name__ == "__main__":
    print("je suis dans le main")