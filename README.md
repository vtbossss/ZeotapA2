
# Weather Monitoring System

This project is a **Real-Time Weather Monitoring System** that fetches weather data from the OpenWeatherMap API and processes it for various metrics such as temperature, humidity, and wind speed. The application includes daily weather rollups and allows for the visualization of this data. It also supports background task processing using Celery and Redis for daily summaries.

## Features
- Fetch weather data at regular intervals from the OpenWeatherMap API.
- Calculate dominant weather.
- Store weather data for further analysis.
- Calculate and store daily summaries (e.g., average, max, min temperature, humidity, wind speed).
- Visualize weather trends using Plotly.
- Background tasks using Celery and Redis for data processing and aggregation.
- Alerts based on weather condition or thershold values.

## Project Structure
```bash
ZeotapA2/
└── weather_monitoring/
    ├── Dockerfile               # Docker configuration file
    ├── docker-compose.yml       # Docker Compose configuration file
    ├── .env                     # Environment variables
    ├── manage.py                # Django management script
    ├── requirements.txt         # Project dependencies
    ├── db.sqlite3               # SQLite database file
    ├── celerybeat-schedule      # Celery Beat schedule file
    ├── templates/               # HTML templates
    │   ├── base.html
    │   ├── home.html
    │   ├── temp.html
    │   └── visualizations.html
    ├── weather/                 # Django app
    │   ├── admin.py             # Admin interface configuration
    │   ├── alerts.py            # Alerts logic
    │   ├── apps.py              # App configuration
    │   ├── models.py            # Database models
    │   ├── tasks.py             # Celery tasks
    │   ├── tests.py             # Tests for the app
    │   ├── urls.py              # URL routing for the app
    │   ├── utils.py             # Utility functions
    │   ├── views.py             # Views for handling requests
    │   └── visualizations.py     # Visualization logic
    └── weather_monitoring/      # Main project directory
        ├── asgi.py              # ASGI configuration
        ├── celery.py            # Celery configuration
        ├── settings.py          # Django settings
        ├── urls.py              # URL routing for the project
        └── wsgi.py              # WSGI configuration

```

## Build Instructions

### Prerequisites
- Docker and Docker Compose
- Git
- OpenWeatherMap API key
- Secret key(django)

### Dependencies
The project uses the following major dependencies:
- **Django**: Web framework used to build the application.
- **Celery**: For background task processing.
- **Redis**: As a message broker for Celery.
- **Plotly**: For data visualization.

### Build and Run the Application

1. Clone the repository:
   ```bash
   git clone https://github.com/vtbossss/ZeotapA2
   
   cd ZeotapA2
   
   cd weather_monitoring
   ```

2. Create a `.env` file in the project root and add the following variables:
   ```bash
   SECRET_KEY=your_secret_key
   OPENWEATHER_API_KEY=your_openweathermap_api_key
   ```

3. Build and start the application using Docker Compose(make sure u are in project directory where docker-compose.yml is available):
   ```bash
   docker-compose build
   
   docker-compose up
   ```

   This will start the following services:
   - **Django** app running on `http://localhost:8000`.
   - **Redis** service running on `localhost:6379`.
   - **Celery** worker and beat to handle periodic tasks.

5. Access the application in your browser at `http://localhost:8000`.

### Usage

- The **Home Page** displays real-time weather data fetched from the OpenWeatherMap API, with updates occurring every minute along with daily summaries.
- The **Visualizations Page** provides graphical representations of weather data trends, allowing users to analyze patterns visually.
- Background tasks for generating daily summaries run at **11:59 PM** (configurable in Celery), ensuring the latest data is processed and stored in Sqlite database present in project directory(db.sqlite3).
- **Dominant Weather Condition**: This is determined by analyzing the weather conditions recorded for the day. The application counts the occurrences of each weather condition (from the `main` field) and identifies the condition with the highest count. 
- **check for alerts(current_temp, weather_condition, city_name)**:
  - Checks if the current temperature exceeds a predefined threshold (35°C) or if the weather condition is among those that trigger alerts (e.g., Rain, Thunderstorm).
  - Generates alerts based on these conditions.



### Visualizations

The app uses **Plotly** to display weather trends, such as daily average temperature. You can access the visualizations at `/visualizations/`.

### Design Choices

- **Django** is used for the backend, leveraging its ORM for database interaction.
- **Celery** with **Redis** is used for task queuing and periodic tasks.
- **Docker** containers ensure consistency across environments and simplify deployment.
- **SQLite** is used for local development; you can replace it with PostgreSQL or any other RDBMS in production.
- **Redis** is used as message broker for celery.
- **SSE(server side events)** is used for updating weather data on frontend without reloading the page.

### How to Extend

- Add more detailed metrics (e.g., pressure, visibility) by extending the `WeatherData` model.
- Implement user-defined weather alerts based on thresholds (e.g., temperature spikes).
- Integrate additional APIs for air quality monitoring or severe weather alerts.



