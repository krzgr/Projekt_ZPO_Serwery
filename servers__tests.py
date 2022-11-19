import unittest

from servers import ListServer, Product, Client, MapServer, TooManyProductsFoundError

server_types = (ListServer, MapServer)


class ServerTest(unittest.TestCase):

    def test_get_entries_returns_proper_entries1(self):
        products = [Product('P12', 1), Product('PP234', 2), Product('PP235', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(2)
            self.assertEqual([products[2], products[1]], entries)

    def test_get_entries_returns_proper_entries2(self):
        products = [Product('PPP12', 5), Product('PPP234', 2), Product('PP235', 1), Product('PPP112', 1)]
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(3)
            self.assertEqual([products[3], products[1], products[0]], entries)

    def test_get_entries_returns_proper_entries3(self):
        products = []
        for server_type in server_types:
            server = server_type(products)
            entries = server.get_entries(3)
            self.assertEqual([], entries)


class RaisingExceptionsTest(unittest.TestCase):

    def test_if_product_raised_proper_exception1(self):
        with self.assertRaises(ValueError):
            Product('111aaa', 15.0)

    def test_if_product_raised_proper_exception2(self):
        with self.assertRaises(ValueError):
            Product('111', 15.0)

    def test_if_each_server_raised_proper_exception1(self):
        products = [Product('PPP12', 1.5), Product('PPP34', 2.3), Product('PPP235', 1.2),
                    Product('PPP146', 3.9), Product('PPP928', 6.1), Product('PPP719', 6.2)]
        for server_type in server_types:
            server = server_type(products)
            with self.assertRaises(TooManyProductsFoundError):
                server.get_entries(3)

    def test_if_each_server_raised_proper_exception2(self):
        products = [Product('P12', 1.5), Product('P235', 1.2),
                    Product('P928', 6.1), Product('P719', 6.2)]
        for server_type in server_types:
            server = server_type(products)
            with self.assertRaises(TooManyProductsFoundError):
                server.get_entries(1)

    def test_if_each_server_raised_proper_exception3(self):
        products = [Product('P12', 1.5), Product('P34', 2.3), Product('PPP235', 1.2),
                    Product('PPP146', 3.9), Product('PPP928', 6.1), Product('PP719', 6.2),
                    Product('P10', 1), Product('P24', 3), Product('PPP635', 2),
                    Product('PP000', 6), Product('PP763', 18), Product('PP173', 2.1)]
        for server_type in server_types:
            server = server_type(products)
            with self.assertRaises(TooManyProductsFoundError):
                server.get_entries(3)
            with self.assertRaises(TooManyProductsFoundError):
                server.get_entries(1)


class ListServerTestSortResult(unittest.TestCase):

    def test_if_entries_are_sorted_properly1(self):
        products = [Product('PPP12', 1.5), Product('PPP34', 2.3), Product('PPP235', 1.2)]
        server = ListServer(products)
        entries = server.get_entries(3)
        self.assertEqual([entry.get_price() for entry in entries], [1.2, 1.5, 2.3])

    def test_if_entries_are_sorted_properly2(self):
        products = [Product('PPP12', 1.5), Product('PPP34', 2.3), Product('PPP235', 1.2), Product('PP111', 1.8)]
        server = ListServer(products)
        entries = server.get_entries(3)
        self.assertEqual([entry.get_price() for entry in entries], [1.2, 1.5, 2.3])

    def test_if_entries_are_sorted_properly3(self):
        products = [Product('PPP12', 1.5), Product('PPP34', 2.3), Product('PPP235', 1.5), Product('PP111', 1.8)]
        server = ListServer(products)
        entries = server.get_entries(3)
        self.assertEqual([entry.get_price() for entry in entries], [1.5, 1.5, 2.3])


class ClientTest(unittest.TestCase):

    def test_total_price_for_normal_execution1(self):
        products = [Product('PP234', 2), Product('PP235', 3)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(5, client.get_total_price(2))

    def test_total_price_for_normal_execution2(self):
        products = [Product('PPP234', 2), Product('PP235', 3), Product('P123', 4),
                    Product('PP923', 1), Product('P999', 15), Product('PPP128', 8)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(19, client.get_total_price(1))
            self.assertEqual(4, client.get_total_price(2))
            self.assertEqual(10, client.get_total_price(3))

    def test_total_price_sensitive_case1(self):
        products = []
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(2))

    def test_total_price_sensitive_case2(self):
        products = [Product('PPP12', 1.5), Product('PPP34', 2.3), Product('PPP235', 1.5), Product('PPP111', 1.8)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(2))

    def test_total_price_sensitive_case3(self):
        products = [Product('PPP12', 1.5), Product('PPP34', 2.3), Product('PPP235', 1.5), Product('PPP111', 1.8)]
        for server_type in server_types:
            server = server_type(products)
            client = Client(server)
            self.assertEqual(None, client.get_total_price(3))


if __name__ == '__main__':
    unittest.main()
