import requests
from decimal import Decimal
from currency import convert

# correct = Decimal('3754.8057')
# result = convert(Decimal("1000.1000"), 'RUR', 'JPY', "17/02/2005", requests)
# correct = Decimal('12.8540')
# result = convert(Decimal(str(10 ** 3)), 'RUR', 'USD', "26/01/2016", requests)
correct = Decimal('1051.8006')
result = convert(Decimal(str(10 ** 3)), 'EUR', 'USD', "26/02/2017", requests)
if result == correct:
    print("Correct")
else:
    print("Incorrect: %s != %s" % (result, correct))
