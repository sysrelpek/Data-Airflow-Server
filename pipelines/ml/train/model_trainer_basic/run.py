def run_pipeline():
    """Pure ML logic - no Airflow imports"""
    print("🚀 Starting model training pipeline...")

    data = load_data()
    features = build_features(data)
    model = train_model(features)
    save_model(model)

    print("✅ Model training pipeline finished")


def load_data():
    print("   Loading raw training data...")
    return {"samples": 10000}   # placeholder


def build_features(data):
    print("   Building features...")
    return {"features": "processed"}


def train_model(features):
    print("   Training model...")
    return {"model": "trained_model_v1"}


def save_model(model):
    print("   Saving model to models/ folder...")