

# Create your tests here.
# portfolio/tests.py
from django.test import TestCase
from .models import Stock
from django.contrib.auth.models import User

class StockModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        Stock.objects.create(user=self.user, ticker='AAPL', name='Apple Inc', quantity=10, purchase_price=150)

    def test_stock_creation(self):
        stock = Stock.objects.get(ticker='AAPL')
        self.assertEqual(stock.name, 'Apple Inc')
users = User.objects.all() 
for user in users:
    print(user.username) 