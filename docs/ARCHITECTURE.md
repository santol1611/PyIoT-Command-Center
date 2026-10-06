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

During Phase 3, do not add:

- PostgreSQL
- FastAPI
- Redis

unless requested.


## Current Implementation

Phase 3 currently implements this data path:

```text
Virtual Device
      |
      | Telemetry JSON over MQTT
      v
Eclipse Mosquitto
      |
      v
MQTT Subscriber
```

The simulator publishes telemetry from 10 virtual devices to topics in this
format:

```text
pyiot/devices/{device_id}/telemetry
```

Publishing uses QoS 1 and waits at most 5 seconds for confirmation. If the
broker becomes unavailable, the simulator pauses for 2 seconds between retries
while the Paho network loop reconnects in the background.

The broker host and port come from the `MQTT_HOST` and `MQTT_PORT`
operating-system environment variables, with defaults of `127.0.0.1` and
`1883`. The optional `MQTT_USERNAME` and `MQTT_PASSWORD` values provide the
credentials required by a protected broker. The simulator requires the two
credential values together and validates all settings before creating the MQTT
client. The current local Mosquitto setup rejects anonymous connections.

FastAPI, PostgreSQL, and the web dashboard remain future-phase components.
