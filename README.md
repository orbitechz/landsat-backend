# Landsat-Backend

Welcome to the **Landsat-Backend** repository! This is the backend service for the Landsat Notification and Visualization System, designed to track Landsat satellite overpasses, retrieve surface reflectance data, and support data analysis. The backend is built using a combination of Python libraries and APIs, including FastAPI, Google Earth Engine API, Skyfield, and N2YO API, to provide users with real-time satellite monitoring and environmental data insights.

## 📚 Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the Application](#running-the-application)
- [Technologies Used](#technologies-used)
- [Project Goals](#project-goals)
- [Contributing](#contributing)
- [License](#license)
- [Contact Information](#contact-information)

## 🌍 Project Overview

The **Landsat-Backend** is the core service that powers the Landsat Notification and Visualization System. It handles satellite tracking, data retrieval, and serves as the bridge between user requests and the external data sources. This service allows users to define a geographic location and receive notifications when a Landsat satellite is due to pass over that area. After the satellite has passed, it retrieves the corresponding Landsat Surface Reflectance (SR) data and provides it through structured API endpoints for visualization and analysis.

### 🎯 What Exactly Does It Do?
- Tracks Landsat satellite orbits and predicts when a pass will occur over a user-defined area.
- Retrieves satellite imagery data using the Google Earth Engine API.
- Sends real-time notifications of upcoming satellite passes through an external frontend service.
- Provides endpoints for accessing Surface Reflectance data, enabling comparison with ground-based observations.
- Supports educational and research use-cases by making remote sensing data more accessible and easier to interpret.

### 🛠️ How Does It Work?
1. **Target Location Input**: The backend receives geographic coordinates from the frontend.
2. **Satellite Overpass Tracking**: Using `Skyfield` and the `N2YO API`, it predicts when a Landsat satellite will pass over the specified coordinates.
3. **Surface Reflectance Data Retrieval**: Once a pass is detected, the backend retrieves corresponding SR data from the Google Earth Engine API using `earthengine-api`.
4. **Data Formatting**: The retrieved data is processed and formatted into a user-friendly JSON structure for frontend visualization and analysis.

### 💡 Benefits
- **Accurate Overpass Predictions**: Users receive precise timing for Landsat satellite overpasses, enhancing data collection planning.
- **Seamless Integration**: Interfaces directly with popular APIs for Earth observation and satellite tracking.
- **Data Accessibility**: Bridges the gap between satellite imagery and practical use, supporting both educational and research purposes.
- **Supports Environmental Analysis**: Enables users to compare satellite data with ground-based measurements, contributing to environmental research and monitoring efforts.

## ✨ Features
- **Real-Time Overpass Predictions** using `Skyfield` and `N2YO API`.
- **Surface Reflectance Data Retrieval** from the Google Earth Engine API.
- **Dynamic Location-Based Data Processing** for any geographic region.
- **User-Friendly API Endpoints** for frontend integration.
- **Data Preprocessing** for efficient storage and retrieval of satellite imagery.

## 🚀 Getting Started

Follow these steps to set up and run the backend service on your local environment.

### Prerequisites
- Python 3.8 or later
- Virtual Environment (recommended)
- Google Earth Engine Account (for accessing satellite data)
- N2YO API Key (for satellite tracking)
- FastAPI knowledge (for understanding the backend structure)

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/orbitechz/landsat-backend.git
   cd landsat-backend
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Configuration
1. **Set up environment variables**:
   Create a `.env` file in the project root with the following information:
   ```env
   GOOGLE_APPLICATION_CREDENTIALS="path_to_your_service_account_key.json"
   N2YO_API_KEY="your_n2yo_api_key"
   ```
   
2. **Google Earth Engine Authentication**:
   Follow the instructions [here](https://developers.google.com/earth-engine/guides/python_install) to authenticate your `earthengine-api` using a service account.

### Running the Application
1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

2. Open your browser and navigate to `http://localhost:8000/docs` to view the interactive API documentation.


## 💻 Technologies Used
- **Python** - Backend programming language.
- **FastAPI** - Framework for building the RESTful API.
- **Google Earth Engine API** - For retrieving satellite surface reflectance data.
- **Skyfield** - For calculating satellite orbits and overpass predictions.
- **N2YO API** - For real-time satellite tracking.
- **Uvicorn** - ASGI server for FastAPI.

## 🎯 Project Goals
- **Data Accessibility**: Make satellite and remote sensing data easier to access and analyze.
- **Research Support**: Provide tools for environmental monitoring and spectral analysis.
- **Educational Value**: Support learning about remote sensing, satellite tracking, and environmental science.

## 🤝 Contributing
We welcome contributions! Please follow the standard workflow:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

## 📧 Contact Information
For questions, suggestions, or feedback, feel free to reach out:
- **GitHub**: [orbitechz](https://github.com/orbitechz)

Thank you for exploring **Landsat-Backend**! We hope this service helps bridge the gap between satellite data and

 real-world environmental analysis.
