from pycoingecko import CoinGeckoAPI
from celery import Celery

cg = CoinGeckoAPI()
prices = cg.get_price(ids=["bitcoin", "litecoin", "ethereum"], vs_currencies="eur")
print(prices)

app = Celery()

app.conf.beat_schedule = {
    "add-every-30-seconds": {"task": "tasks.add", "schedule": 30.0, "args": (16, 16)},
}
app.conf.timezone = "UTC"


@app.task
def test(arg):
    print(arg)


@app.task
def add(x, y):
    z = x + y
    print(z)
