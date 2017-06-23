import utilities
from openwpmtest import OpenWPMTest
from ..automation import TaskManager
from ..automation.utilities import db_utils
import json
# TODO: add test for setter instrumentation


class TestExtension(OpenWPMTest):
    NUM_BROWSERS = 1

    def get_config(self, data_dir=""):
        manager_params, browser_params = self.get_test_config(data_dir)
        browser_params[0]['js_instrument'] = True
        return manager_params, browser_params

    def test_sensor_probing(self, tmpdir):
        test_url = utilities.BASE_TEST_URL + '/sensors.html'
        db = self.visit(test_url, str(tmpdir))
        rows = db_utils.get_javascript_entries(db, all_columns=True)
        observed_sensor_apis = set()
        expected_apis = set(['deviceorientation', 'devicemotion',
                             'deviceproximity', 'devicelight'])
        for row in rows:
            if row[9] == "window.addEventListener":
                observed_sensor_apis.add(json.loads(row[12])["0"])
                assert row[3] == test_url
        assert observed_sensor_apis == expected_apis
