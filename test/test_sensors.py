import pytest # NOQA
import os
import utilities
import expected
from openwpmtest import OpenWPMTest
from ..automation import TaskManager
# TODO: add test for setter instrumentation


class TestExtension(OpenWPMTest):
    NUM_BROWSERS = 1

    def get_config(self, data_dir):
        manager_params, browser_params = TaskManager.load_default_params(self.NUM_BROWSERS)
        manager_params['data_directory'] = data_dir
        manager_params['log_directory'] = data_dir
        browser_params[0]['headless'] = False
        browser_params[0]['extension']['enabled'] = True
        browser_params[0]['extension']['jsInstrument'] = True
        manager_params['db'] = os.path.join(manager_params['data_directory'],
                                            manager_params['database_name'])
        return manager_params, browser_params

    def test_sensor_probing(self, tmpdir):
        test_url = utilities.BASE_TEST_URL + '/sensors.html'
        db = self.visit(test_url, str(tmpdir))
        rows = utilities.get_javascript_entries(db, True)
        observed_sensor_apis = set()
        expected_apis = set(['deviceorientation', 'devicemotion',
                             'deviceproximity', 'devicelight'])
        for row in rows:
            if row[10] == 0:
                observed_sensor_apis.add(row[11])
                assert row[3] == test_url
        assert observed_sensor_apis == expected_apis
