### Konfigruacja 
Aplikacja FortiFraud musi działać.

AUTH_LOGIN: a
Login którym będą się przedstawiać żadania predykcji.

AUTH_PASSWORD: a
Hasło którym będą się przedstawiać żadania predykcji.

PREDICTION_ADDRESS: http://host.docker.internal:8000/predict
Adres endpoint usługi predict w FortiFraud

Przykład docker-compose_example.yml

### Budowa obrazu:
docker-compose build
 
### Start aplikacji
docker-compose up 

