import datetime
import unittest
from unittest.mock import patch, MagicMock
from plugins.stock_service import SuperSimpleStock

class TestSuperSimpleStock(unittest.TestCase):
    """
    Test class for SuperSimpleStoc
    """
    def setUp(self):
        # Create an instance of SimpleStock with mock data
        self.stock = SuperSimpleStock("POP")

    def test_calculate_dividend_common(self):
        # Test calculate_dividend for Common stock type
        price = 20
        self.assertEqual(self.stock.calculate_dividend(price), 0.4) # last divindend is 0

    def test_calculate_dividend_preferred_type(self):
        # Test calculate_dividend with "Preferred" type
        self.stock.type = "Preferred"
        self.stock.fixed_dividend = 0.02
        self.stock.par_value = 100
        self.assertEqual(self.stock.calculate_dividend(10), 0.02 * 100 / 10)

    def test_calculate_dividend_zero_price(self):
        # Test calculate_dividend with price as zero
        price = 0
        expected_dividend = None  # Should return None when price is zero
        self.assertEqual(self.stock.calculate_dividend(price), expected_dividend)

    def test_get_pe_ratio_common(self):
        # Test P/E Ratio for Common stock type
        price = 20
        expected_pe_ratio = price / (8 / price)
        self.assertEqual(self.stock.calculate_pe_ratio(price), expected_pe_ratio)

    def test_get_pe_ratio_preferred(self):
        # Test P/E Ratio for Preferred stock type
        price = 50
        expected_pe_ratio = 312.5  # Because fixed_dividend is None for Preferred stock
        self.assertEqual(self.stock.calculate_pe_ratio(price), expected_pe_ratio)

    def test_get_pe_ratio_zero_price(self):
        # Test P/E Ratio with price as zero
        price = 0
        expected_pe_ratio = None  # Should return None when price is zero
        self.assertEqual(self.stock.calculate_pe_ratio(price), expected_pe_ratio)

    def test_get_pe_ratio_dividend_zero(self):
        # Test P/E Ratio when dividend is zero
        price = 10
        expected_pe_ratio = 12.5
        self.assertEqual(self.stock.calculate_pe_ratio(price), expected_pe_ratio)

    def test_record_trades_valid(self):
        # Test recording valid trades
        self.stock.record_trades(100, "buy", 20)
        self.stock.record_trades(50, "sell", 15)
        self.assertEqual(len(self.stock.trades), 2)  # Two trades should be recorded

    def test_record_trades_invalid_quantity(self):
        # Test recording trade with invalid quantity (negative quantity)
        with self.assertRaises(ValueError):
            self.stock.record_trades(-100, "buy", 20)

    def test_record_trades_invalid_order_type(self):
        # Test recording trade with invalid order type
        with self.assertRaises(ValueError):
            self.stock.record_trades(100, "invalid_type", 20)

    def test_record_trades_invalid_price(self):
        # Test recording trade with invalid price (zero price)
        with self.assertRaises(ValueError):
            self.stock.record_trades(100, "buy", 0)

    def test_get_volume_weighted_price_no_trades(self):
        # Test get_volume_weighted_price when there are no trades
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime.datetime(2023, 7, 25, 12, 0, 0)
            self.assertEqual(self.stock.calculate_volume_weighted_price(), 0)

    # def test_get_volume_weighted_price_no_matching_symbol(self):
    #     # Test get_volume_weighted_price when there are trades, but no matching symbol
    #     self.stock.record_trades(100, "buy", 20)
    #     self.stock.record_trades(50, "sell", 15)
    #     with patch('datetime.datetime') as mock_datetime:
    #         mock_datetime.now.return_value = datetime.datetime(2023, 7, 25, 12, 0, 0)
    #         self.assertEqual(self.stock.calculate_volume_weighted_price(), 0)

    # @patch("plugins.stock_service.datetime")  # Mock the datetime module in your_module
    # def test_get_volume_weighted_price_with_trades(self, mock_datetime):
    #     self.stock.trades = [
    #         {"timestamp": datetime.datetime.now().timestamp(), "symbol": "TEA", "quantity": 10, "price": 15},
    #         {"timestamp": (datetime.datetime.now() - datetime.timedelta(minutes=20)).timestamp(), "symbol": "TEA", "quantity": 20, "price": 20},
    #         {"timestamp": (datetime.datetime.now() - datetime.timedelta(minutes=10)).timestamp(), "symbol": "TEA", "quantity": 15, "price": 25},
    #         {"timestamp": (datetime.datetime.now() - datetime.timedelta(minutes=5)).timestamp(), "symbol": "ABC", "quantity": 5, "price": 10},
    #     ]
    #     # Mock datetime.datetime.now() to return a fixed timestamp
    #     fixed_timestamp = datetime.datetime(2023, 7, 1, 12, 0, 0)
    #     mock_datetime.now.return_value = fixed_timestamp

    #     # Mock datetime.datetime.fromtimestamp() to return a datetime object
    #     def mock_fromtimestamp(ts):
    #         return fixed_timestamp

    #     mock_datetime.fromtimestamp.side_effect = mock_fromtimestamp

    #     # Test the function when there are trades for the symbol "TEA" in the past 15 minutes
    #     symbol = "TEA"
    #     past_fifteen_minutes = fixed_timestamp - datetime.timedelta(minutes=15)
  
    #     expected_result = (10 * 15 + 15 * 25) / (10 + 15)  # (Sum of (quantity * price)) / (Sum of quantities)
    #     self.assertEqual(self.stock.calculate_volume_weighted_price(), expected_result)

    # @patch("modules.stock_service.datetime") 
    # def test_get_volume_weighted_price_with_no_trades(self, mock_datetime):
    #     # Mock datetime.datetime.now() to return a fixed timestamp
    #     fixed_timestamp = datetime.datetime(2023, 7, 1, 12, 0, 0)
    #     mock_datetime.now.return_value = fixed_timestamp

    #     # Mock datetime.datetime.fromtimestamp() to return a datetime object
    #     def mock_fromtimestamp(ts):
    #         return fixed_timestamp

    #     mock_datetime.fromtimestamp.side_effect = mock_fromtimestamp

    #     # Test the function when there are no trades for the symbol "XYZ" in the past 15 minutes
    #     symbol = "XYZ"
    #     past_fifteen_minutes = fixed_timestamp - datetime.timedelta(minutes=15)
    #     self.assertEqual(self.stock.get_volume_weighted_price(symbol), 0)


    # def test_get_volume_weighted_price_with_matching_symbol(self):
    #     # Test get_volume_weighted_price with matching symbol
    #     self.stock.record_trades(100, "buy", 20)
    #     self.stock.record_trades(50, "sell", 15)

    #     # Mock the datetime.datetime.fromtimestamp method to return a fixed timestamp
    #     with patch('datetime.datetime') as mock_datetime:
    #         mock_datetime.now.return_value = datetime.datetime(2023, 7, 25, 12, 0, 0)
    #         with patch('datetime.datetime.fromtimestamp') as mock_fromtimestamp:
    #             mock_fromtimestamp.side_effect = lambda ts: datetime.datetime(2023, 7, 25, 11, 45, 0)
    #             # The trades are within the past 15 minutes, so the volume-weighted price should be calculated
    #             self.assertEqual(self.stock.calculate_volume_weighted_price(), (100 * 20 + 50 * 15) / (100 + 50))

    def test_get_gbce_all_share_index_no_trades(self):
        # Test get_gbce_all_share_index when there are no trades
        self.assertIsNone(self.stock.calculate_gbce_all_share_index())

    def test_get_gbce_all_share_index_with_trades(self):
        # Test get_gbce_all_share_index with trades
        self.stock.record_trades(100, "buy", 20)
        self.stock.record_trades(50, "sell", 15)
        self.stock.record_trades(75, "buy", 18)
        expected = 17.666666666666668
        self.assertEqual(self.stock.calculate_gbce_all_share_index(), expected)

# if __name__ == "__main__":
#     unittest.main()