# ESPHome Pressure Sensor External Component

ESPHome external component for DFRobot SEN0257 and compatible ADC pressure sensors.

Implements smart median-filtered multi-sample ADC reading with configurable calibration.
Publishes pressure (Pa) and optionally voltage (V).

Requires ESPHome with **ESP-IDF 5.0+ framework** (not Arduino). Tested on ESP32-C6, ESP32-S3, and ESP32 WROOM-32.

```yaml
esp32:
  board: <your-board>
  framework:
    type: esp-idf
    version: recommended
```

> **Classic ESP32 (WROOM-32) note:** ADC2 pins (GPIO0–GPIO15 area, varies by variant) are shared with the WiFi radio and cannot be used while WiFi is active. Use ADC1 pins: GPIO32–GPIO39.

## Usage

The component uses ESPHome's built-in `adc` sensor as its voltage source. Define the `adc` sensor first, then reference it via `source_id`.

```yaml
external_components:
  - source: github://your-username/ESPHomePressSensor@main
    components: [dfrobot_257]

sensor:
  - platform: adc
    id: pressure_adc
    pin: GPIO34        # ADC1 pin — avoid ADC2 pins when WiFi is active
    attenuation: 2.5db
    update_interval: never

  - platform: dfrobot_257
    source_id: pressure_adc
    pressure:
      name: "Water Pressure"
```

## Configuration

### `adc` sensor (pin and hardware config)

| Parameter | Notes |
|---|---|
| `pin` | GPIO pin connected to sensor signal. Use ADC1 pins (GPIO32–GPIO39 on classic ESP32). |
| `attenuation` | `0db`, `2.5db`, `6db`, `11db`. Use `2.5db` for DFRobot SEN0257. |
| `update_interval` | Set to `never` — `dfrobot_257` controls when to read. |

### `dfrobot_257` sensor (sampling and calibration)

| Parameter | Required | Default | Description |
|---|---|---|---|
| `source_id` | yes | — | ID of the `adc` sensor to read from |
| `zero_voltage` | no | `0.471` | Voltage at zero pressure (V) — calibration |
| `pa_per_volt` | no | `250000` | Pascals per volt conversion factor |
| `sample_count` | no | `50` | Samples per measurement (1–100) |
| `sample_interval` | no | `10ms` | Delay between samples |
| `outlier_threshold` | no | `10` | Max % deviation from median before sample is discarded |
| `update_interval` | no | `3s` | Measurement interval |
| `pressure` | yes | — | Pressure sensor sub-config (Pa) |
| `voltage` | no | — | Voltage sensor sub-config (V) |

## Full Example

```yaml
esphome:
  name: pressure-sensor
  friendly_name: Pressure Sensor

esp32:
  board: esp32-c6-devkitc-1
  framework:
    type: esp-idf

external_components:
  - source: github://your-username/ESPHomePressSensor@main
    components: [dfrobot_257]

logger:

wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

sensor:
  - platform: adc
    id: pressure_adc
    pin: GPIO34
    attenuation: 2.5db
    update_interval: never

  - platform: dfrobot_257
    source_id: pressure_adc
    zero_voltage: 0.471
    pa_per_volt: 250000
    sample_count: 50
    sample_interval: 10ms
    outlier_threshold: 10
    update_interval: 3s
    pressure:
      name: "Water Pressure"
    voltage:
      name: "Sensor Voltage"
```

## Wiring

Sensor powered from 5V. Signal output is ratiometric (typically 0.5–4.5V), which exceeds the ESP32 ADC input range (~1.25V at 2.5dB attenuation). A voltage divider is required to avoid damaging the ESP32.

All components mount at the ESP32 end (not at the sensor).

```
ESP 5V ──────────────────────────────────── 3m cable ──── Sensor VCC
         │
     [C3 100nF ceramic]   ← 5V rail decoupling at ESP
         │
ESP GND ─┴───────────────────────────────── 3m cable ──── Sensor GND
                                                │
                              3m cable ─────── Sensor OUT
                                                │
                                          [R1 30kΩ]
                                                │
                                ────────────────┴──── GPIO34 (ADC)
                                                │
                                          ┌─────┴─────┐
                                       [R2 10kΩ]  [C2 100nF]
                                          │            │
                                         GND ──────────┘
```

**Component values:**

| Part | Value | Purpose |
|------|-------|---------|
| R1 | 30kΩ | Voltage divider top — scales 5V → 1.25V |
| R2 | 10kΩ | Voltage divider bottom |
| C2 | 100nF ceramic | Low-pass filter at ADC input, fc ≈ 212 Hz |
| C3 | 100nF ceramic | Decoupling on 5V rail at ESP side |

Voltage divider ratio: R2 / (R1 + R2) = 10k / 40k = 0.25 → 4.5V maps to 1.125V.

RC filter cutoff: fc = 1 / (2π × (R1‖R2) × C2) = 1 / (2π × 7.5k × 100n) ≈ 212 Hz.

Default pin is GPIO34. Change with `pin:` in YAML.
Not all ESP32 GPIO pins support ADC — consult your variant's datasheet.

## Calibration

1. Leave the sensor open (not mounted in pipe or tank).
2. Check the `voltage` sensor reading in ESPHome logs or Home Assistant.
3. Set that voltage value as `adc_offset` in your YAML config.

## License

MIT — see [LICENSE](LICENSE).
