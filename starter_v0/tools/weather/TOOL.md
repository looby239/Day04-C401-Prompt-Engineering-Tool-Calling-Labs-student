---
name: weather
track: bonus
kind: live_api
provider: wttr.in
requires_env: []
inputs: [location]
outputs: [temperature_celsius, description, humidity_percent, wind_speed_kmh]
side_effect: false
---
# weather

Fetch the current weather condition of a specific city or location from wttr.in.
