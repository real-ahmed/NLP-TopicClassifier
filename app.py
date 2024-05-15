from flask import Flask, request, jsonify ,render_template
import joblib
import sklearn
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import json


app = Flask(__name__)



#load models
svm_model = joblib.load('svm_model.pkl')
nb_model = joblib.load('nb_model.pkl')
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')

#get category name
with open('category_mapping.json', 'r') as f:
    category_names = json.load(f)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    match data['modelType']:
        case "svm":
            model = svm_model
        case "nb":
            model = nb_model
        case _:
            model = svm_model

    # preprocessing the input
    text = data['text']
    text = str(text).lower()
    text = text.replace('[^\w\s]', ' ')
    tokens = nltk.word_tokenize(text)

    stemmer = nltk.PorterStemmer()
    stemmed_tokens = [stemmer.stem(token) for token in tokens]

    stemmed_text = ' '.join(stemmed_tokens)
    features = tfidf_vectorizer.transform([stemmed_text])

    prediction = model.predict(features)
    return jsonify({'prediction': category_names.get(str(prediction.tolist()[0]))})


if __name__ == '__main__':
    app.run()
