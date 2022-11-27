#!/usr/bin/python
# -*- coding: utf-8 -*-

from typing import Optional, List
from abc import ABC, abstractmethod
from copy import deepcopy
import re


class Product:
    def __init__(self, name: str = "test123", price: float = 0.0) -> None:
        self.set_name(name)
        self.set_price(price)

    def set_name(self, name: str):
        if isinstance(name, str) and re.fullmatch("^[a-zA-Z]+\d+$", name):
            self.name = name
        else:
            raise ValueError("Nazwa produktu musi być w postaci <ciąg_liter><ciąg cyfr>!")
    
    def set_price(self, price: float):
        if isinstance(price, (float, int)) and price >= 0:
            self.price = float(price)
        else:
            raise ValueError("Cena produktu nie może być ujemna!")

    def get_name(self):
        return self.name

    def get_price(self):
        return self.price

    def __eq__(self, other):
        if isinstance(other, Product):
            return other.name == self.name and other.price == self.price
        return False
    
    def __hash__(self):
        return hash((self.name, self.price))


class TooManyProductsFoundError(Exception):
    pass


class Server(ABC):
    n_max_returned_entries = 3

    @abstractmethod
    def __init__(self, products: List[Product] = []) -> None:
        pass
    
    @abstractmethod
    def add_product(self, product: Product) -> None:
        pass

    @abstractmethod
    def get_entries(self, n_letters: int) -> List[Product]:
        pass


class ListServer(Server):
    def __init__(self, products: List[Product] = []) -> None:
        self.products = deepcopy(products)

    def add_product(self, product: Product) -> None:
        self.products.append(product)
    
    def get_entries(self, n_letters: int = 1) -> List[Product]:
        if isinstance(n_letters, int) and n_letters > 0:
            pattern = "^[a-zA-Z]{" + str(n_letters) + "}\d{2,3}$"
            result = [x for x in self.products if re.fullmatch(pattern, x.get_name())]
            if len(result) > self.n_max_returned_entries:
                raise TooManyProductsFoundError()
            result.sort(key=lambda a: a.get_price())
            return result


class MapServer(Server):
    def __init__(self, products: List[Product] = []) -> None:
        self.products = {x.get_name(): x for x in products}

    def add_product(self, product: Product) -> None:
        self.products[product.get_name()] = product
    
    def get_entries(self, n_letters: int = 1) -> List[Product]:
        if isinstance(n_letters, int) and n_letters > 0:
            pattern = "^[a-zA-Z]{" + str(n_letters) + "}\d{2,3}$"
            result = [self.products[key] for key in self.products.keys() if re.fullmatch(pattern, key)]
            if len(result) > self.n_max_returned_entries:
                raise TooManyProductsFoundError()
            result.sort(key=lambda a: a.get_price())
            return result


class Client:
    def __init__(self, server: Server) -> None:
        self.server = server
        
    def get_total_price(self, n_letters: Optional[int]) -> Optional[float]:
        try:
            tmp = self.server.get_entries(n_letters) if isinstance(n_letters, int) else self.server.get_entries()
            if len(tmp) == 0:
                return None
            result = 0
            for prod in tmp:
                result += prod.get_price()
            return result
        except Exception as e:
            return None
