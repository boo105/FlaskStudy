from flask import Flask
from flask_restx import Api, Resource
from service.api import Todo
from service.test import Good

print(Todo)

app = Flask(__name__)
api = Api(
    app, 
    version='1.0', 
    title='공부용 API', 
    description='공부용입니다.',
    terms_url="/",
    contact="minho@kakao.com",
    license="MIT") # API 만든다

api.add_namespace(Todo,"/api")
api.add_namespace(Good,"/good")

if __name__ == "__main__" :
    app.run(port="3000",debug=True)
