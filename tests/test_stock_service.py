import datetime
import unittest
from unittest.mock import patch, MagicMock, mock_open
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
        data = SuperSimpleStock.get_all_trades_record()
        self.assertGreaterEqual(len(data), 2)  # Two trades should be recorded

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

    @patch("plugins.stock_service.SuperSimpleStock.get_all_trades_record")
    def test_get_volume_weighted_price_no_trades(self, mock_get_all_trades_record):
        # Test get_volume_weighted_price when there are no trades
        mock_get_all_trades_record.return_value = []
        with patch('datetime.datetime') as mock_datetime:
            mock_datetime.now.return_value = datetime.datetime(2023, 7, 25, 12, 0, 0)
            self.assertEqual(self.stock.calculate_volume_weighted_price(), 0)

    def test_calculate_volume_weighted_price(self):
        self.stock.calculate_volume_weighted_price()

    @patch("plugins.stock_service.SuperSimpleStock.get_all_trades_record")
    def test_calculate_gbce_all_share_index(self, mock_get_all_trades_record):
        # Mock the trades data returned by get_all_trades_record
        mock_get_all_trades_record.return_value = [
            {"traded_price": 10},
            {"traded_price": 20},
            {"traded_price": 30},
        ]

        # Call the calculate_gbce_all_share_index function
        result = SuperSimpleStock.calculate_gbce_all_share_index()

        # Assert that the result is calculated correctly
        self.assertEqual(result, 20)  # geometric mean of traded prices (60 / 3)

        # Assert that the mock functions were called with the correct arguments
        mock_get_all_trades_record.assert_called_once()
    
    @patch("plugins.stock_service.open", new_callable=mock_open, read_data="")  # Mock 'open' to return an empty file
    @patch("plugins.stock_service.pickle.dump")  # Mock 'pickle.dump'
    @patch("plugins.stock_service.pickle.load")  # Mock 'pickle.dump'
    def test_store_trade_data(self, mock_load, mock_pickle_dump, mock_open):

        # Call the method with some sample trade data
        sample_trade = {"symbol": "AAPL", "quantity": 10, "price": 150}
        SuperSimpleStock.store_trade_data(sample_trade)

        # Check if 'open' was called twice with the correct file name and mode
        mock_open.assert_called_with("trades.pickle", "wb")
        self.assertEqual(mock_open.call_count, 2)  # Ensure it's called twice (once for reading, once for writing)

        # Check if 'pickle.dump' was called once with the correct arguments
        mock_pickle_dump.assert_called()

    @patch("plugins.stock_service.open", new_callable=mock_open, read_data="")
    @patch("plugins.stock_service.pickle.load")
    def test_get_all_trades_record(self, mock_pickle_load, mock_open):
        # Prepare a mock trades data to be returned by pickle.load
        mock_trades_data = [{"symbol": "AAPL", "quantity": 10, "price": 150},
                            {"symbol": "GOOG", "quantity": 5, "price": 250}]

        # Mock 'open' to return an empty file-like object
        mock_open.return_value.__enter__.return_value = mock_open()
        
        # Mock 'pickle.load' to return the mock_trades_data
        mock_pickle_load.return_value = mock_trades_data

        # Call the method
        result = SuperSimpleStock.get_all_trades_record()

        # Check if 'open' was called once with the correct file name and mode
        mock_open.assert_called_with("trades.pickle", "rb")

        # Check if 'pickle.load' was called once
        mock_pickle_load.assert_called_once()

        # Check if the result matches the expected mock_trades_data
        self.assertEqual(result, mock_trades_data)

    @patch("plugins.stock_service.open", new_callable=mock_open, read_data='{"key": "value"}')  # Replace with sample JSON data
    @patch("plugins.stock_service.json.load")
    def test_get_gbce_data(self, mock_json_load, mock_open):
        # Prepare the mock data to be returned by json.load
        mock_data = {"key": "value"}

        # Mock 'open' to return an empty file-like object
        mock_open.return_value.__enter__.return_value = mock_open()
        
        # Mock 'json.load' to return the mock_data
        mock_json_load.return_value = mock_data

        # Call the method
        result = SuperSimpleStock.get_gbce_data()

        # Check if 'open' was called once with the correct file name and mode
        mock_open.assert_called_with('plugins/gbce_data.json', 'r', encoding="utf-8")

        # Check if 'json.load' was called once
        mock_json_load.assert_called_once()

        # Check if the result matches the expected mock_data
        self.assertEqual(result, mock_data)

# if __name__ == "__main__":
#     unittest.main()