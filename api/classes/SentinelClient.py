import time
import os
import json
from keycloak import KeycloakOpenID
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

TOKEN_FILE = 'api/utils/sentinel_token.json'

class SentinelClient:
    def __init__(self):
        self.auth_url = os.getenv('AUTH_URL')
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.realm_name = os.getenv('REALM_NAME')
        
        if not all([self.auth_url, self.client_id, self.client_secret, self.realm_name]):
            raise ValueError("Check your env file")
        
        self.token = None
        self.token_expiry_time = 0  
        
        self.keycloak_openid = KeycloakOpenID(server_url=self.auth_url,
                                              client_id=self.client_id,
                                              realm_name=self.realm_name,
                                              client_secret_key=self.client_secret)
        

    def _load_token_from_file(self):
      if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'r') as file:
                data = json.load(file)
                self.token = data.get('access_token')
                self.token_expiry_time = data.get('expiry_time', 0)
                
                if time.time() >= self.token_expiry_time:
                    print("Token expired, renovating...")
                    self._authenticate()

    def _save_token_to_file(self):
        data = {
            'access_token': self.token,
            'expiry_time': self.token_expiry_time
        }
        with open(TOKEN_FILE, 'w') as file:
            json.dump(data, file)

    def _authenticate(self):
        try:
            print(self.auth_url)
            print(self.client_id)
            print(self.client_secret)
            token_data = self.keycloak_openid.token(grant_type="client_credentials")
            self.token = token_data['access_token']
            self.token_expiry_time = time.time() + token_data['expires_in']
            self._save_token_to_file()
            
            print("Token obtained.")
        
        except Exception as e:
            print(f"Error while authenticating {str(e)}")
            self.token = None
    
    def get_valid_token(self) -> str:
        if not self.token or time.time() >= self.token_expiry_time:
            print("Token expired, renovating...")
            self._authenticate()
        
        return self.token
