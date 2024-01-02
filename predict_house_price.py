import pickle


def predict_house_price(area, region_id, building_year):
    with open('regression_model.pkl', 'rb') as model_file:
        regression_model = pickle.load(model_file)

    input_features = [area, region_id, building_year]
    predicted_price = regression_model.predict([input_features])
    return predicted_price
