import time
import os
from keycloak import KeycloakOpenID
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

class SentinelClient:
    def __init__(self):
        # Carregar as variáveis do arquivo .env
        self.auth_url = os.getenv('AUTH_URL')
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.realm_name = "main"
        
        if not all([self.auth_url, self.client_id, self.client_secret, self.realm_name]):
            raise ValueError("Check your .env file")
        
        self.token = None
        self.token_expiry_time = 0    # Timestamp de quando o token expira
        
        # Inicializa a instância do Keycloak
        self.keycloak_openid = KeycloakOpenID(server_url=self.auth_url,
                                              client_id=self.client_id,
                                              realm_name=self.realm_name,
                                              client_secret_key=self.client_secret)
    
    def _authenticate(self):
        """
        Faz a autenticação no Keycloak e armazena o token.
        """
        try:
            # Autentica e obtém o token
            token_data = self.keycloak_openid.token(grant_type="client_credentials")
            self.token = token_data['access_token']
            
            # Calcula o tempo de expiração com base no 'expires_in'
            self.token_expiry_time = time.time() + token_data['expires_in']
            
            print("Token obtido com sucesso.")
        
        except Exception as e:
            print(f"Erro ao autenticar no Keycloak: {str(e)}")
            self.token = None
    
    def get_valid_token(self) -> str:
        """
        Retorna um token válido. Se o token atual estiver expirado ou inválido,
        realiza uma nova autenticação para obter um novo token.
        """
        # Verifica se o token está presente e ainda não expirou
        if not self.token or time.time() >= self.token_expiry_time:
            print("Token expirado ou ausente, renovando...")
            self._authenticate()  # Renova o token
        
        return self.token
