import pytest
import utilities
from openwpmtest import OpenWPMTest
from ..automation import TaskManager
from ..automation import CommandSequence
from ..automation.utilities import db_utils


class TestTriggerSensorEvents(OpenWPMTest):
    """Make sure that we trigger fake sensor events."""

    def get_config(self, data_dir=""):
        return self.get_test_config(data_dir)

    def test_trigger_sensor_events(self):
        manager_params, browser_params = self.get_config()
        browser_params[0]['trigger_sensor_events'] = True
        manager = TaskManager.TaskManager(manager_params, browser_params)
        test_url = utilities.BASE_TEST_URL + '/sensor_value_test.html'

        def get_text_from_el(driver, element_id):
            js_str = 'return document.getElementById("%s").innerHTML' %\
                element_id
            return driver.execute_script(js_str)

        def check_trigger_sensor_events(**kwargs):
            """Check if we find the sensor values on the page"""
            driver = kwargs['driver']

            device_light_str = get_text_from_el(driver, "DeviceLight")
            assert "AmbientLight current Value: " in device_light_str
            assert "Max:" in device_light_str
            assert "Min:" in device_light_str

            device_proximity_str = get_text_from_el(driver, "DeviceProximity")
            assert "DeviceProximity current Value: " in device_proximity_str
            assert "Max:" in device_proximity_str
            assert "Min:" in device_proximity_str

            user_proximity_str = get_text_from_el(driver, "UserProximity")
            assert user_proximity_str == "UserProximity: true"

            batt_in_charge_str = get_text_from_el(driver, "in-charge")
            assert batt_in_charge_str != "unavailable"

            batt_charging_time_str = get_text_from_el(driver, "charging-time")
            assert batt_charging_time_str != "unavailable"

            batt_discharging_time_str = get_text_from_el(driver,
                                                         "discharging-time")
            assert batt_discharging_time_str != "unavailable"

            batt_level_str = get_text_from_el(driver, "battery-level")
            assert batt_level_str != "unavailable"

            assert "Z-axis: " in get_text_from_el(driver, "Orientation_a")
            assert "X-axis: " in get_text_from_el(driver, "Orientation_b")
            assert "Y-axis: " in get_text_from_el(driver, "Orientation_g")

            assert "AccelerometerIncludingGravity X-axis:" in\
                get_text_from_el(driver, "Accelerometer_gx")
            assert "AccelerometerIncludingGravity Y-axis:" in\
                get_text_from_el(driver, "Accelerometer_gy")
            assert "AccelerometerIncludingGravity Z-axis:" in\
                get_text_from_el(driver, "Accelerometer_gz")

            assert "Accelerometer X-axis: " in\
                get_text_from_el(driver, "Accelerometer_x")
            assert "Accelerometer Y-axis: " in\
                get_text_from_el(driver, "Accelerometer_y")
            assert "Accelerometer Z-axis: " in\
                get_text_from_el(driver, "Accelerometer_z")
            assert "Data Interval: " in\
                get_text_from_el(driver, "Accelerometer_i")

            assert "Gyro X-axis: " in\
                get_text_from_el(driver, "Gyro_x")
            assert "Gyro Y-axis: " in\
                get_text_from_el(driver, "Gyro_y")
            assert "Gyro Z-axis: " in\
                get_text_from_el(driver, "Gyro_z")

        cs = CommandSequence.CommandSequence(test_url, blocking=True)
        cs.get(sleep=5, timeout=60)
        cs.run_custom_function(check_trigger_sensor_events)
        manager.execute_command_sequence(cs)
        manager.close()
        assert not db_utils.any_command_failed(manager_params['db'])
