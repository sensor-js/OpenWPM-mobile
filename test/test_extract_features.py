from openwpmtest import OpenWPMTest
from ..feature_extraction.extract_features import is_get_image_data_dimensions_too_small


class TestDependencies(OpenWPMTest):

    def test_is_get_image_data_dimensions_too_small(self):
        TEST_DATA = {
            '{"0":0,"1":0,"2":17,"3":17}': False,
            '{"0":0,"1":0,"2":0,"3":0}': True,
            '{"0":0,"1":0,"2":"null","3":"null"}': True
            }
        for args, expected in TEST_DATA.iteritems():
            assert expected == is_get_image_data_dimensions_too_small(args)
