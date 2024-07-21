import json
import math

from app.customer import Customer
from app.shop import Shop
from app.car import Car


def shop_trip() -> None:
    with open("app/config.json", "r") as f:
        data = json.load(f)
    fuel_price = data["FUEL_PRICE"]
    customers = data["customers"]
    shops = [Shop(**shop) for shop in data["shops"]]
    for people in customers:
        customer = Customer(
            people["name"],
            people["product_cart"],
            people["location"],
            people["money"],
            Car(people["car"]["brand"],
                people["car"]["fuel_consumption"])
        )
        print(f"{customer.name} has {customer.money} dollars")
        prices = []
        for shop in shops:
            distance = math.dist(customer.location, shop.location)
            cost = round(shop.trip_cost(distance, fuel_price, customer), 2)
            prices.append(cost)
            print(f"{customer.name}'s trip to the {shop.name} costs {cost}")
        ride = False
        for price in prices:
            if price <= customer.money:
                ride = True
        if ride:
            current_shop = shops[prices.index(min(price for price in prices))]
            print(f"{customer.name} rides to {current_shop.name}\n")
            distance = math.dist(customer.location, current_shop.location)
            current_shop.print_receipt(customer)
            print(f"{customer.name} rides home")
            customer.money -= round(
                current_shop.trip_cost(distance, fuel_price, customer), 2
            )
            print(f"{customer.name} now has {customer.money} dollars\n")
            continue
        print(f"{customer.name} doesn't have enough "
              f"money to make a purchase in any shop")
