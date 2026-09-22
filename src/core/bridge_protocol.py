# file: ./src/core/bridge_protocol.py

class BridgeProtocol:

    @staticmethod
    def drive(tspeed: int, tangle: int) -> str:
        return f"Driver.Drive(speed:{tspeed}, steering:{tangle})" 

    @staticmethod
    def get_battery_level() -> str:
        return f"Battery.GetBatteryLevel()"

    @staticmethod
    def keep_alive() -> str:
        return f"SafetySupervisor.EnableTestMode()"

    @staticmethod
    def enable_test_mode() -> str:
        return f"SystemPower.KeepAlive()"
