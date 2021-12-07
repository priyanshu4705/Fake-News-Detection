from flask import request, Blueprint, render_template
from app.scrapper import clean_data, scrape
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import pandas as pd

view = Blueprint('view', __name__)

tfvect = TfidfVectorizer(stop_words='english', max_df=0.7)
loaded_model = pickle.load(open('model.pkl', 'rb'))
dataframe = pd.read_csv('./news.csv')

dataframe = pd.read_csv('news.csv')
x = dataframe['text']
y = dataframe['label']
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=0)


def fake_news_det(news : str) -> str:
    '''
        prediction
    '''
    _ = tfvect.fit_transform(x_train)
    _ = tfvect.transform(x_test)
    input_data = [news]
    vectorized_input_data = tfvect.transform(input_data)
    prediction = loaded_model.predict(vectorized_input_data)
    return prediction


@view.get('/text')
def predict_from_text():
    '''
        predict from text from article
    '''
    text = str(request.args.get('text'))

    text = clean_data(text)
    pred = fake_news_det(text)
    return render_template('index.html', text=text, prediction=pred[0])


@ view.get('/url')
def predict_from_url():
    '''
        predict from url of the article
    '''
    url = str(request.args.get('url'))

    title, text = scrape(url)
    pred = fake_news_det(text)
    return render_template('index.html', title=title, text=text, prediction=pred[0])


@ view.get('/')
def index():
    '''
        Home Page of the site
    '''
    return render_template('index.html')
