
# Weather Monitoring System

This project is a **Real-Time Weather Monitoring System** that fetches weather data from the OpenWeatherMap API and processes it for various metrics such as temperature, humidity, and wind speed. The application includes daily weather rollups and allows for the visualization of this data. It also supports background task processing using Celery and Redis for daily summaries.

## Features
- Fetch weather data at regular intervals from the OpenWeatherMap API.
- Store weather data for further analysis.
- Calculate and store daily summaries (e.g., average, max, min temperature, humidity, wind speed).
- Visualize weather trends using Plotly.
- Background tasks using Celery and Redis for data processing and aggregation.

## Project Structure
```bash
weather_monitoring/
├── weather_monitoring/
│   ├── settings.py
│   ├── urls.py
│   ├── celery.py
│   └── asgi.py
├── weather/
│   ├── models.py
│   ├── views.py
│   ├── tasks.py
│   ├── utils.py
│   └── templates/
│       ├── home.html
│       └── summaries.html
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## Setup Instructions

### Prerequisites
- Docker and Docker Compose
- OpenWeatherMap API key

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

3. Build and start the application using Docker Compose:
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

- The home page displays real-time weather data fetched from the OpenWeatherMap API along with daily summaries.
- The Visualizations Page in this project provides graphical representations of weather data trends.
- Background tasks for daily summaries run at 11:59 PM (configurable in Celery).

### Visualizations

The app uses **Plotly** to display weather trends, such as temperature changes and humidity levels. You can access the visualizations at `/visualizations/`.

### Design Choices

- **Django** is used for the backend, leveraging its ORM for database interaction.
- **Celery** with **Redis** is used for task queuing and periodic tasks.
- **Docker** containers ensure consistency across environments and simplify deployment.
- **SQLite** is used for local development; you can replace it with PostgreSQL or any other RDBMS in production.

### How to Extend

- Add more detailed metrics (e.g., pressure, visibility) by extending the `WeatherData` model.
- Implement user-defined weather alerts based on thresholds (e.g., temperature spikes).
- Integrate additional APIs for air quality monitoring or severe weather alerts.

### Deployment

You can deploy the application using Docker to any cloud service provider that supports Docker containers. Ensure that you configure environment variables for the production environment.

### License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
