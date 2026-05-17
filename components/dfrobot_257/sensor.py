import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor, voltage_sampler
from esphome.const import (
    CONF_ID,
    CONF_SOURCE_ID,
    DEVICE_CLASS_PRESSURE,
    STATE_CLASS_MEASUREMENT,
    UNIT_PASCAL,
    UNIT_VOLT,
)
from . import dfrobot_257_ns, DFRobot257Component

CONF_ZERO_VOLTAGE = "zero_voltage"
CONF_PA_PER_VOLT = "pa_per_volt"
CONF_SAMPLE_COUNT = "sample_count"
CONF_SAMPLE_INTERVAL = "sample_interval"
CONF_OUTLIER_THRESHOLD = "outlier_threshold"
CONF_PRESSURE = "pressure"
CONF_VOLTAGE = "voltage"

CONFIG_SCHEMA = cv.All(
    cv.Schema(
        {
            cv.GenerateID(): cv.declare_id(DFRobot257Component),
            cv.Required(CONF_SOURCE_ID): cv.use_id(voltage_sampler.VoltageSampler),
            cv.Optional(CONF_ZERO_VOLTAGE, default=0.471): cv.float_,
            cv.Optional(CONF_PA_PER_VOLT, default=250000): cv.positive_int,
            cv.Optional(CONF_SAMPLE_COUNT, default=50): cv.int_range(min=1, max=100),
            cv.Optional(
                CONF_SAMPLE_INTERVAL, default="10ms"
            ): cv.positive_time_period_milliseconds,
            cv.Optional(
                CONF_OUTLIER_THRESHOLD, default=10
            ): cv.int_range(min=1, max=100),
            cv.Required(CONF_PRESSURE): sensor.sensor_schema(
                unit_of_measurement=UNIT_PASCAL,
                accuracy_decimals=0,
                device_class=DEVICE_CLASS_PRESSURE,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
            cv.Optional(CONF_VOLTAGE): sensor.sensor_schema(
                unit_of_measurement=UNIT_VOLT,
                accuracy_decimals=3,
                state_class=STATE_CLASS_MEASUREMENT,
            ),
        }
    )
    .extend(cv.polling_component_schema("3s"))
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)

    source = await cg.get_variable(config[CONF_SOURCE_ID])
    cg.add(var.set_source(source))

    cg.add(var.set_zero_voltage(config[CONF_ZERO_VOLTAGE]))
    cg.add(var.set_pa_per_volt(config[CONF_PA_PER_VOLT]))
    cg.add(var.set_sample_count(config[CONF_SAMPLE_COUNT]))
    cg.add(var.set_sample_interval_ms(config[CONF_SAMPLE_INTERVAL].total_milliseconds))
    cg.add(var.set_outlier_threshold(config[CONF_OUTLIER_THRESHOLD]))

    pressure_sens = await sensor.new_sensor(config[CONF_PRESSURE])
    cg.add(var.set_pressure_sensor(pressure_sens))

    if CONF_VOLTAGE in config:
        voltage_sens = await sensor.new_sensor(config[CONF_VOLTAGE])
        cg.add(var.set_voltage_sensor(voltage_sens))
