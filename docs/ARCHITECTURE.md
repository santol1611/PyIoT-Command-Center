# Architecture

## Target Architecture

The planned architecture is:

Virtual Sensor / ESP32
        |
        | MQTT
        v
Eclipse Mosquitto
        |
        v
FastAPI Backend
        |
        +---- PostgreSQL
        |
        +---- Automation Engine
        |
        +---- WebSocket
                 |
                 v
             Browser


## Development Strategy

The system is developed incrementally.

### Phase 1

Project Foundation

### Phase 2

Virtual Sensor Simulator

### Phase 3

MQTT

### Phase 4

FastAPI Backend

### Phase 5

PostgreSQL

### Phase 6

Web Dashboard

### Phase 7

WebSocket

### Phase 8

Device Control

### Phase 9

Automation Engine

### Phase 10

ESP32


## Important

Do not implement components from future phases unless explicitly requested.

For example:

During Phase 2, do not add:

- PostgreSQL
- FastAPI
- MQTT
- Redis

unless requested.