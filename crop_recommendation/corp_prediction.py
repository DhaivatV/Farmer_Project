import pickle
import numpy as np

def recommend_crop(data):
    crop_recommendation_model_path = r'C:\Users\dvipa\OneDrive\Desktop\Stuff\farmer_project\models\RandomForest.pkl'
    crop_recommendation_model = pickle.load(
        open(crop_recommendation_model_path, 'rb'))
    return crop_recommendation_model.predict(data)

# data =np.array([[12, 13, 14, 44, 10, 7.5, 9]])
#
# print(recommend_crop(data))