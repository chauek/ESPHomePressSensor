import esphome.codegen as cg

CODEOWNERS = ["@your-github-username"]
DEPENDENCIES = ["sensor", "voltage_sampler"]

dfrobot_257_ns = cg.esphome_ns.namespace("dfrobot_257")
DFRobot257Component = dfrobot_257_ns.class_(
    "DFRobot257Component", cg.PollingComponent
)
