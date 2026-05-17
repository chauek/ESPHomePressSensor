#include "dfrobot_257.h"
#include "esphome/core/log.h"
#include "esphome/core/helpers.h"
#include <algorithm>
#include <cmath>

namespace esphome {
namespace dfrobot_257 {

static const char *const TAG = "dfrobot_257";
static const uint16_t MAX_SAMPLES = 100;

void DFRobot257Component::setup() {
  if (source_ == nullptr) {
    ESP_LOGE(TAG, "source_id not configured");
    this->mark_failed();
  }
}

void DFRobot257Component::update() {
  float voltage = sample_voltage_();
  float pressure = (voltage - zero_voltage_) * static_cast<float>(pa_per_volt_);
  ESP_LOGD(TAG, "voltage=%.3fV  pressure=%.0fPa", voltage, pressure);
  if (pressure_sensor_ != nullptr)
    pressure_sensor_->publish_state(pressure);
  if (voltage_sensor_ != nullptr)
    voltage_sensor_->publish_state(voltage);
}

float DFRobot257Component::sample_voltage_() {
  float buf[MAX_SAMPLES];
  uint16_t n = std::min(sample_count_, MAX_SAMPLES);

  for (uint16_t i = 0; i < n; i++) {
    buf[i] = source_->sample();
    if (sample_interval_ms_ > 0)
      delay(sample_interval_ms_);
  }

  std::sort(buf, buf + n);
  float median = buf[n / 2];
  float limit = median * (outlier_threshold_pct_ / 100.0f);

  double sum = 0;
  uint16_t kept = 0;
  for (uint16_t i = 0; i < n; i++) {
    if (std::abs(buf[i] - median) <= limit) {
      sum += buf[i];
      kept++;
    }
  }

  return (kept > 0) ? static_cast<float>(sum / kept) : median;
}

}  // namespace dfrobot_257
}  // namespace esphome
