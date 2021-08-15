from pyrebase4 import pyrebase
config = {
    "apiKey": "AIzaSyABkXEzTPWinL_hSo1ye0BVyJ0cbsHJK6E",
    "authDomain": "job-search-fastapi.firebaseapp.com",
    "databaseURL": "https://imgapi-144fe.firebaseio.com",
    "projectId": "job-search-fastapi",
    "storageBucket": "job-search-fastapi.appspot.com",
    "messagingSenderId": "1043351657546",
    "appId": "1:1043351657546:web:9b96d247bb077168c4dab3",
    "measurementId": "G-8RK49FRH5L"
}
firebase= pyrebase.initialize_app(config)
storage= firebase.storage()