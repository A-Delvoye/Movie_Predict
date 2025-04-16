import os
import request
from dotenv import load_dotenv,set_key
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

BASE_URL = "http://localhost:8080"
ENV_FILE = ".env"

def login():
    username = os.getenv("API_USERNAME")
    password = os.getenv("API_PASSWORD")

    if not username or password:
        raise Exception("Please set API_USERNAME and API_PASSWORD in your .env file")
    
    login_data = {
        "username" : username,
        "password" : password,
    }

    response = request.post(f"{BASE_URL}/api/v1/login",json=login_data)
    if response.status_code ==200:
        token = response.json()["access_token"]
        set_key(ENV_FILE, "API_TOKEN", token)
        return token
    else:
        raise Exception("Failed to login")
    
def make_prediction(data:dict):
    token = os.getenv("API_TOKEN")
    headers = {
        "Authorization" : f"Bearer {token}"}
    
    response = request.post(
        f"{BASE_URL}/api/v1/predict",
        json = data,
        headers = headers
    )

    if response.status_code ==200:
        return response.json()
    
    elif response.status_code == 401:
        new_token = login()
        headers = {"Authorization" : f"Bearer{new_token}"}
        response = request.post(f"{BASE_URL}/api/v1/predict",
                                json = data,
                                headers = headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception("login or password incorrect")
        
    else:
        raise Exception("Failed to make a prediction")
    
# def main():
#     data = {
#         ""
#     }

#     response = make_prediction(data)
#     print(response)

