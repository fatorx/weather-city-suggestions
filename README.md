# Weather City Suggestions

When you enter a city, a sentence is generated based on its current weather.

------

### Functionalities

- Check weather information for a given city.
- With the weather information, it generates a nice sentence based on the weather information.

------

### Technologies
- Python 3.12 with FastAPI
- Redis

------

### Requirements

To run the project, keys for the following services are required:

[Google Gemini](https://ai.google.dev/aistudio)

[OpenWeatherMap](https://home.openweathermap.org/users/sign_up)

------

### Quickstart - Docker and Tests

#### First time

Create a copy of .env.example and fill the variables with the values of your choice (i.e. your api keys, etc.)
```bash
cp .env.example .env 
```

Execute the docker command to build application

```bash
docker compose up -d --build
```

Run the tests to verify that the installation completed successfully.
```bash
docker exec -it weather_city-api pytest
```

#### Running after build 

```bash
docker compose up -d
```

------

#### Testing via CURL

```bash
curl -X 'GET' \
  'http://localhost:8004/api/v1/weather/?city=Caxias%20do%20Sul' \
  -H 'accept: application/json'
```

------

#### Access documentation

In the browser, access http://0.0.0.0:8004/docs, for access to API methods in OpenAPI format.

To details about architecture, access this [page](docs/architecture.md).

------

### Running tests

```bash
docker exec -it api pytest
```