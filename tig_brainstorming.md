# TIG Stack Brainstorming

This document outlines the plan for setting up a TIG (Telegraf, InfluxDB, Grafana) stack for monitoring and data analysis of the license plate system.

## 1. Goal

The primary goal is to collect, analyze, and visualize service health stats and real-time data from the database. This includes:
-   Daily car count
-   A map showing the origins of cars
-   Historical data analytics

## 2. Monitoring Stack Setup

The monitoring stack will be integrated into the existing `docker-compose.dev.yaml`.

-   **Services to add**:
    -   `influxdb:2.7`
    -   `grafana/grafana:10.2.0`
    -   `telegraf:1.29`
-   **Configuration**:
    -   The services will be configured using environment variables defined in the `.env` file.
    -   A `telegraf/telegraf.conf` file will be created to define the metrics collection.
    -   Volumes will be created for InfluxDB and Grafana to persist data.
-   **Plugins**:
    -   Grafana will be started with `grafana-clock-panel` and `grafana-worldmap-panel` plugins.

## 3. Metrics Collection (Telegraf)

Telegraf will be configured to collect the following metrics:

-   **System Metrics**:
    -   Use the `inputs.docker` plugin to collect CPU and memory metrics for all running containers.
-   **Database Metrics**:
    -   Use the `inputs.postgresql` plugin to collect metrics from the PostgreSQL database. This will be used for business-level metrics like "daily car count".
-   **Application Metrics**:
    -   The Python services will be instrumented to expose a Prometheus endpoint.
    -   Telegraf will use the `inputs.prometheus` plugin to scrape these metrics.

## 4. Data Visualization (Grafana)

Grafana will be used to visualize the data stored in InfluxDB.

-   **Data Source**: InfluxDB will be configured as the data source.
-   **Dashboards**:
    -   **Car Count Dashboard**: A dashboard to show the daily count of cars, with historical trends.
    -   **Geomap Dashboard**: A map to visualize the origin of the cars based on their `country_code` and `municipality`.

## 5. Geocoding for Map Visualization

To display the car origins on a map, we need to convert the `municipality` and `country_code` from the database into geographical coordinates (latitude and longitude).

-   **Approach**: We will use a local dataset to perform the geocoding. This avoids external dependencies and potential costs.
-   **Dataset**: A promising dataset has been found on GitHub: [GeoJSON and TopoJSON for Austria](https://github.com/ginseng666/GeoJSON-TopoJSON-Austria). This repository contains GeoJSON files for Austrian municipalities, districts, and states, which include the necessary geometries to derive coordinates.
-   **Implementation Plan**:
    1.  Download the relevant GeoJSON file (e.g., for municipalities/districts).
    2.  Store the file in the `shared-data` directory.
    3.  Modify the `data-collection-service` to:
        a.  Load the GeoJSON data on startup.
        b.  When a new vehicle observation is processed, look up the coordinates for the given `municipality` code.
        c.  Store the latitude and longitude in the municipality lookup file.