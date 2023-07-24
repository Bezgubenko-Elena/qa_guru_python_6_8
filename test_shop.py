"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product, Cart


@pytest.fixture
def book():
    return Product("book", 100, "This is a book", 1000)

@pytest.fixture
def notebook():
    return Product("notebook", 10.5 , "This is a notebook", 500)

@pytest.fixture
def my_cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, book):
        # TODO напишите проверки на метод check_quantity
        assert book.check_quantity(10)
        assert book.check_quantity(1000)
        assert not book.check_quantity(1001)

    def test_product_buy(self, book):
        # TODO напишите проверки на метод buy

        book.buy(10)
        assert book.quantity == 990

    def test_product_buy_more_than_available(self, book):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            book.buy(1001)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_init_empty_cart(self, my_cart):
        assert not len(my_cart.products)

    def test_add_product_first_addition(self, my_cart, book):
        my_cart.add_product(book, 10)
        assert my_cart.products[book] == 10

    def test_add_product_product_in_cart(self, my_cart, book):
        my_cart.add_product(book, 10)
        my_cart.add_product(book, 10)
        assert my_cart.products[book] == 20

    def test_add_product_one_addition(self, my_cart, book):
        my_cart.add_product(book)
        assert my_cart.products[book] == 1

    def test_remove_product_if_remove_count_None(self, my_cart, book):
        my_cart.add_product(book, 10)
        my_cart.remove_product(book)
        assert book not in my_cart.products

    def test_remove_product_remove_count_less_quantity(self, my_cart, book):
        my_cart.add_product(book, 10)
        my_cart.remove_product(book, 5)
        assert my_cart.products[book] == 5

    def test_remove_product_remove_count_more_quantity(self, my_cart, book):
        my_cart.add_product(book, 10)
        my_cart.remove_product(book, 15)
        assert book not in my_cart.products

    def test_clear_cart(self, my_cart, book):
        my_cart.add_product(book, 10)
        my_cart.clear()
        assert my_cart.products == {}

    def test_get_total_price(self, my_cart, book, notebook):
        my_cart.add_product(book, 10)
        my_cart.add_product(notebook, 10)
        total_price = my_cart.get_total_price()
        assert total_price == 1105

    def test_get_total_price_check_type_of_data(self, my_cart, book, notebook):
        my_cart.add_product(book, 10)
        my_cart.add_product(notebook, 10)
        total_price = my_cart.get_total_price()
        assert type(total_price) == float

    def test_buy_successful(self, my_cart, book, notebook):
        my_cart.add_product(book, 10)
        my_cart.add_product(notebook, 10)
        my_cart.buy()
        assert book.quantity == 990
        assert notebook.quantity == 490
        assert not len(my_cart.products)

    def test_buy_more_quantity_error(self, my_cart, book, notebook):
        my_cart.add_product(book, 10000)
        my_cart.add_product(notebook, 10)
        with pytest.raises(ValueError):
            my_cart.buy()