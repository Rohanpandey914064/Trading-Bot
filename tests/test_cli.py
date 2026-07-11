import unittest
from unittest.mock import patch

from cli import parse_arguments



class ParseArgumentsTests(unittest.TestCase):
    def test_accepts_order_type_alias(self) -> None:
        with patch("sys.argv", [
            "cli.py",
            "--symbol",
            "BTCUSDT",
            "--side",
            "BUY",
            "--order-type",
            "MARKET",
            "--quantity",
            "0.01",
        ]):
            args = parse_arguments()

        self.assertEqual(args.order_type, "MARKET")
        self.assertEqual(args.symbol, "BTCUSDT")
        self.assertEqual(args.quantity, "0.01")


if __name__ == "__main__":
    unittest.main()
