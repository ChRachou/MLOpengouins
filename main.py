
from pengouins.data import load_data, get_X_y, split_data, preprocess_data
from pengouins.model import train_model, evaluate_model
from pengouins.registry import save_model, load_model

def initial_train():
    # Load data
    df = load_data("penguins")

    # Prepare features and target
    X, y = get_X_y(df, target_column="species")

    # Split data
    X_train, X_test, y_train, y_test = split_data(X, y)

    # Preprocess data
    preprocessor, X_train_preproc = preprocess_data(X_train, preprocessor=None)
    _, X_test_preproc = preprocess_data(X_test, preprocessor=preprocessor)

    # Train model
    model = train_model(X_train_preproc, y_train)

    # Evaluate model
    accuracy = evaluate_model(model, X_test_preproc, y_test)
    print(f"Model accuracy: {accuracy}")


def make_pred():
    # Load data
    df = load_data("penguins")

    # Prepare features and target
    X, y = get_X_y(df, target_column="species")

    # Preprocess data
    preprocessor = load_model(model_name="preprocessor")
    _, X_preproc = preprocess_data(X, preprocessor=preprocessor)

    # Load model
    model = load_model(model_name="pengouin_classifier")

    # Make predictions
    predictions = model.predict(X_preproc)
    print("Predictions:", predictions)


if __name__ == "__main__" : 
    initial_train()
    make_pred()