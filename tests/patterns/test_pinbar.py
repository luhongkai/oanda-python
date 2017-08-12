import unittest
import patterns.pinbar as pinbar


class TestPinBar(unittest.TestCase):

    def test_get_pinbar_status(self):

        # open = 1.15334
        # close = 1.15354
        # low = 1.1529
        # high = 1.15389

        #data = dict(open=1.14953, close=1.14958, low=1.14921, high=1.14991)
        data = dict(open=1.15160, close=1.15165, low=1.15133, high=1.15170)

        pinbar_status = pinbar.get_pinbar_status(data['open'], data['high'], data['low'], data['close'])

        expected_pinbar_status = dict(is_valid=False, type=None)

        self.assertEqual(expected_pinbar_status, pinbar_status)
