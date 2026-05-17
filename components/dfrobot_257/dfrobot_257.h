#pragma once

#include "esphome/core/component.h"
#include "esphome/components/sensor/sensor.h"
#include "esphome/components/voltage_sampler/voltage_sampler.h"

namespace esphome {
namespace dfrobot_257 {

class DFRobot257Component : public PollingComponent {
 public:
  void set_source(voltage_sampler::VoltageSampler *s) { source_ = s; }
  void set_zero_voltage(float v) { zero_voltage_ = v; }
  void set_pa_per_volt(uint32_t p) { pa_per_volt_ = p; }
  void set_sample_count(uint16_t count) { sample_count_ = count; }
  void set_sample_interval_ms(uint32_t ms) { sample_interval_ms_ = ms; }
  void set_outlier_threshold(uint16_t pct) { outlier_threshold_pct_ = pct; }

  void set_pressure_sensor(sensor::Sensor *s) { pressure_sensor_ = s; }
  void set_voltage_sensor(sensor::Sensor *s) { voltage_sensor_ = s; }

  void setup() override;
  void update() override;
  float get_setup_priority() const override { return setup_priority::DATA; }

 protected:
  float sample_voltage_();

  voltage_sampler::VoltageSampler *source_{nullptr};
  float zero_voltage_{0.471f};
  uint32_t pa_per_volt_{250000};
  uint16_t sample_count_{50};
  uint32_t sample_interval_ms_{10};
  uint16_t outlier_threshold_pct_{10};

  sensor::Sensor *pressure_sensor_{nullptr};
  sensor::Sensor *voltage_sensor_{nullptr};
};

}  // namespace dfrobot_257
}  // namespace esphome
