import numpy as np
from flask import Flask, request
from crop_recommendation.corp_prediction import recommend_crop
from crop_recommendation.weather import weather_fetch
from disease_classifier.classify_disease import predict_image
from fertilizier_predict.crop_type_encoder import encode_crop_type
from fertilizier_predict.decode_fertilizer import decode_fertilizer
from fertilizier_predict.fertilizer_report import generate_fertilizer_report
from fertilizier_predict.min_max import min_max
from fertilizier_predict.predict_fertilier import recommend_fertilizer
from fertilizier_predict.soil_type_encoder import encode_soil_type
from localization.translator import translate_text_to_language
from utils import response_payload

app = Flask(__name__)


@app.route("/", methods=["GET"])
def test():
    return response_payload(True, "Hello World")


@app.route('/crop-recommedation', methods=["POST"])
def crop_recommedation():
    try:
        print('hello')
        data = request.get_json()
        print(data)
        N = data["N"]
        P = data["P"]
        K = data["K"]
        ph = data["ph"]
        rainfall = data["rainfall"]
        humidity = data["humidity"]
        temperature = data["temperature"]
        lang = 'en'

        # try:
        #     city_info = weather_fetch(city)
        # except Exception:
        #     return response_payload(False, msg="Unable to get the city information. Please try again")
        #
        # if city_info != None:
        #     temperature, humidity = city_info
        data = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
        print(data)
        my_prediction = str(recommend_crop(data)[0])
        print(my_prediction, "------------------")
        recommendation_result = {
              "prediction": my_prediction
            }
        return response_payload(True,recommendation_result, "Success search")


    except Exception:
        return response_payload(False, msg="Request body is not valid")


@app.route('/fertilizer-predict', methods=["POST"])
def predict_fertilizer():
    try:
        soil_type = str(input())
        crop_type = str(input())
        moisture = input()
        N = int(input())
        P = int(input())
        K = int(input())
        city = input()
        lang = input()
        if lang == None:
            lang = "en"

        soil_type = translate_text_to_language(soil_type, "en", lang)
        crop_type = translate_text_to_language(crop_type, "en", lang)
        city = translate_text_to_language(city, "en", lang)
        try:
            city_info = weather_fetch(city)
        except Exception:
            return response_payload(False, msg="Unable to get the city information. Please try again")

        encoded_soil_type = encode_soil_type(soil_type)
        encoded_crop_type = encode_crop_type(crop_type)

        if (encoded_soil_type == None and encoded_crop_type == None):
            return response_payload(False, msg="Invalid soil type or crop type")

        if city_info != None:
            temperature, humidity = city_info
            data = np.array([[temperature, humidity, moisture, encoded_soil_type, encoded_crop_type, N, P, K]])

            try:
                data = min_max(data)
                print('Data ', data)
            except  Exception as e:
                print('Error')
                print(e)

            try:
                my_prediction = recommend_fertilizer(data)
            except  Exception as e:
                print('Error')
                print(e)
                my_prediction = "Error"

            prediction = decode_fertilizer(my_prediction[0])
            recommendation_result = {
                "prediction": prediction,
                "info": generate_fertilizer_report(prediction, lang)
            }
            return response_payload(True, recommendation_result, "Success prediction")
        else:
            return response_payload(False, 'Please try again')

    except Exception as e:
        print(e)
        return response_payload(False, msg="Request body is not valid")


@app.route('/disease-predict/<lang>', methods=['GET', 'POST'])
def disease_prediction(lang):
    if request.method == 'POST':
        if lang == None:
            lang = "en"

        if 'file' not in request.files:
            return response_payload(False, 'Please select a file')
        file = request.files.get('file')
        if not file:
            return response_payload(False, 'Please select a file. Make sure there is  file')
        try:
            img = file.read()

            prediction = predict_image(img)
            recommendation_result = {
                "prediction": translate_text_to_language(prediction, lang, "en"),
            }
            return response_payload(True, recommendation_result, "Success prediction")

        except Exception as e:
            print(e)
            pass
    return response_payload(False, 'Please try again')


if __name__ == '__main__':

    app.run()
