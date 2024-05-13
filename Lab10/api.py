from typing import Union
import uvicorn
from fastapi import FastAPI

app = FastAPI()

class Controller():
    def __init__(self):
        self.__customer_account_list = []
        self.__rider_account_list = []
        self.__restaurant_list = []
        self.__approval_list = []

    def get_customer_account_list(self):
        return self.__customer_account_list
    def set_customer_account_list(self, customer):
        self.__customer_account_list = customer
    
    def get_rider_account_list(self):
        return self.__rider_account_list
    def set_rider_account_list(self, rider):
        self.__rider_account_list = rider    
    
    def get_restaurant_list(self):
        return self.__restaurant_list
    def set_restaurant_list(self, restaurant):
        self.__restaurant_list = restaurant
    
    def add_customer_account(self, new_customer):
        self.__customer_account_list.append(new_customer)
    def add_rider_account(self, new_rider):
        self.__rider_account_list.append(new_rider)
    def add_restaurant(self, new_restaurant):
        self.__restaurant_list.append(new_restaurant)

    def remove_customer_account(self, customer):
        self.__customer_account_list.remove(customer)
        del customer
    def remove_rider_account(self, rider):
        self.__rider_account_list.remove(rider)
        del rider
    def remove_restaurant(self, restaurant):
        self.__restaurant_account_list.remove(restaurant)
        del restaurant
        
    def search_customer_by_id(self, customer_id):
        for customer in self.get_customer_account_list():
            if customer.get_account_id() == customer_id:
                return customer
    def search_rider_by_id(self, rider_id):
        for rider in self.__rider_account_list:
            if rider.get_account_id() == rider_id: 
                return rider
    def search_restaurant_by_id(self, restaurant_id):
        for restaurant in self.__restaurant_list:
            if restaurant.get_account_id() == restaurant_id : 
                return restaurant

    def show_order_state_list(self, customer_id):
        customer = self.search_customer_by_id(customer_id)
        return [[order.get_order_id(), order.get_order_state()] for order in customer.get_current_order_list()]

    def confirm_order(self, customer_id, order_id):
        customer = self.search_customer_by_id(customer_id)
        order = customer.search_order_by_id(order_id)
        amount = 0
        for food in order.get_food_list():
            amount += food.get_price()
        payment = Payment(amount, "Paid")
        order.set_payment(payment)
        customer.get_profile().pay_out(amount)
        order.set_order_state("confirmed")
        return str(order.get_order_id()) + " " + str(order.get_order_state()) + " " + str(order.get_payment().get_payment_status())

    def rider_recieve_order(self, rider_id, customer_id, order_id):
        rider = self.search_rider_by_id(rider_id)
        customer = self.search_customer_by_id(customer_id)
        order = customer.search_order_by_id(order_id)
        if order.get_order_state() == "confirmed":
            order.set_order_state("recieved")
            order.get_restaurant().add_requested_order(order)
            return str(order.get_order_id()) + "-" + str(order.get_order_state())

class Account():
    def __init__(self, type=None, account_id=None, password=None, profile=None):
        self.__type = type
        self.__account_id = account_id
        self.__password = password
        self.__profile = profile
        
    def get_type(self):
        return self.__type

    def get_account_id(self):
        return self.__account_id
        
    def get_password(self):
        return self.__password
    def set_password(self, password):
        self.__password = password
        
    def get_profile(self):
        return self.__profile
    def set_profile(self, profile):
        self.__profile = profile
              
class Profile:
    def __init__(self,username = None, name = None, email = None, phone = None,balance = 0):
        self.__username = username
        self.__name = name
        self.__email = email
        self.__phone = phone
        self.__balance = balance

    def get_username(self):
        return self.__username
    def set_username(self, username: str):
        self.__username = username
        
    def get_balance(self):
        return self.__balance
    def set_balance(self, balance: int):
        self.__balance = balance
        
    def top_up(self, amount: int):
        self.__balance += amount
    def pay_out(self, amount: int):
        self.__balance -= amount 
                
class Customer(Account):
    def __init__(self, type="Customer", account_id=None, password=None, profile=None):
        super().__init__(type, account_id, password, profile)
        self.__current_order_list = []
        self.__address_list = []
        self.__reviewed_list = []
        self.__transcipt_list = []
        
    def get_current_order_list(self):
        return self.__current_order_list
    def get_address_list(self):
        return self.__address_list
    
    def add_current_order_list(self, order):
        self.__current_order_list.append(order)
    def remove_current_order_list(self, order):
        self.__address_list.remove(order)
        
    def add_address(self, address: str):
        self.__address_list.append(address)
    def remove_address(self, address: str):
        self.__address_list.remove(address)
    
    def search_order_by_id(self, chosen_order_id):
        for order in self.__current_order_list:
            if order.get_order_id() == chosen_order_id:
                return order
        return "Order is not found"
    
    def show_current_order_list(self):
        order_data = []
        for order in self.get_current_order_list():
            order_data.append([order.get_order_id(), order.get_order_state(), 
                               ("Payment", [order.get_payment().get_payment_id(), 
                                            order.get_payment().get_amount(), 
                                            order.get_payment().get_payment_status()])])
        return order_data
    
class Rider(Account):
    def __init__(self, type="Rider", account_id=None, password=None, profile=None):
        super().__init__(type, account_id, password, profile)
        self.__recieved_order_list = []
        self.__reviewed_list = []
    
    def add_recieved_order(self, order):
        self.__recieved_order_list.append(order)
    def remove_recieved_order(self, order):
        self.__reviewed_list.remove(order)
        
class Restaurant(Account):
    def __init__(self, type="Restaurant", account_id=None, password=None, profile=None):
        super().__init__(type, account_id, password, profile)
        self.__restaurant_name = None
        self.__address = None
        self.__food_list = []
        self.__requested_order_list = []
        self.__finished_order_list = []
        self.__reviewed_list = []
        
    def get_restaurant_name(self):
        return self.__restaurant_name
    def set_restaurant_name(self, name: str):
        self.__restaurant_name = name
        
    def get_address(self):
        return self.__address
    def set_address(self, address: str):
        self.__address = address
        
    def get_food_list(self):
        return self.__food_list
    
    def get_requested_order_list(self):
        return self.__requested_order_list
    
    def get_finished_order_list(self):
        return self.__finished_order_list
    
    def get_reviewed_list(self):
        return self.__reviewed_list
        
    def add_food_list(self, food):
        self.__food_list.append(food)
    def remove_food_list(self, food):
        self.__food_list.remove(food)
        
    def add_requested_order(self, order):
        self.__requested_order_list.append(order)
    def remove_requested_order(self, order):
        self.__requested_order_list.remove(order)
    
    def add_finished_order(self, order):
        self.__finished_order_list.append(order)
    def remove_finished_order(self, order):
        self.__finished_order_list.remove(order)
        
    def add_reviewed(self, review):
        self.__reviewed_list.append(review)
    def remove_reviewed(self, review):
        self.__reviewed_list.remove(review)
        
    def search_requested_order_by_id(self, chosen_order_id):
        for order in self.__requested_order_list:
            if order.get_order_id() == chosen_order_id:
                return order
        return "Order is not found"
    def search_finished_order_by_id(self, chosen_order_id):
        for order in self.__finished_order_list:
            if order.get_order_id() == chosen_order_id:
                return order
        return "Order is not found"
        
class Order():
    id = 10001
    def __init__(self, customer=None, rider="Empty", restaurant=None, food_list=None, order_state="Empty", payment="Empty") :
        self.__order_id = str(Order.id)
        self.__customer = customer
        self.__rider = rider
        self.__restaurant = restaurant
        self.__food_list = food_list
        self.__order_state = order_state
        self.__payment = payment
        Order.id += 1

    def get_order_id(self):
        return self.__order_id
    def get_customer(self):
        return self.__customer
    def get_rider(self):
        return self.__rider
    def get_restaurant(self):
        return self.__restaurant
    def get_food_list(self):
        return self.__food_list
    def get_order_state(self):
        return self.__order_state
    def set_order_state(self, state):
        self.__order_state = state
    def get_payment(self):
        return self.__payment
    def set_payment(self, payment):
        self.__payment = payment
        
    def order_performance(self):
        return self.__order_id + "-" + self.__order_state + "-" + self.__payment.get_payment_status()
    
class Food:
    def __init__(self, name: str, type: str, size: str, price: int):
        self.__name = name
        self.__type = type
        self.__size = size
        self.__price = price
        
    def get_price(self):
        return self.__price
        
class Payment():
    id = 2501
    def __init__(self, food_list=[], restaurant=[], amount=0, payment_status="Paid"):
        self.__payment_id = str(Payment.id)
        self.__date_time = None
        # self.__food_list = food_list
        # self.__paid_restaurant = restaurant
        self.__amount = amount
        self.__payment_status = payment_status
        Payment.id += 1
        
    def get_payment_id(self):
        return self.__payment_id
    
    def get_amount(self):
        return self.__amount
    def set_amount(self, amount):
        self.__amount = amount
        
    def get_payment_status(self):
        return self.__payment_status
    def set_payment_status(self, status):
        self.__payment_status = status
        
    def payment_performance(self):
        return self.__payment_id + "-" + self.__payment_status + "-" + str(self.__amount)

# initial_infomation

controller = Controller()

profile01 = Profile("user01", "name01", "email01", 660001, 1500)
profile02 = Profile("user02", "name02", "email02", 660002, 2500)
customer01 = Customer("Customer", "3001", "3301")
customer02 = Customer("Customer", "3002", "3302")
customer01.set_profile(profile01)
customer02.set_profile(profile02)

restaurant01 = Restaurant("Restaurant", "5001", "5501")
restaurant01.set_restaurant_name("KFC")
restaurant01.set_address("Bangkok")
food01 = Food("BaoBao", "edible", "medium", 50)
food02 = Food("Breastable", "edible", "large", 150)
food03 = Food("SoraCora", "drink", "mini", 25)
food04 = Food("Orange", "drink", "large", 75)
restaurant01.add_food_list(food01)
restaurant01.add_food_list(food02)
restaurant01.add_food_list(food03)
restaurant01.add_food_list(food04)

controller.add_customer_account(customer01)
controller.add_customer_account(customer02)
controller.add_restaurant(restaurant01)

order01 = Order(customer01, None, restaurant01, [food01, food02])
order02 = Order(customer02, None, restaurant01, [food03])

rider01 = Rider("Rider", "6001", "6601")
rider02 = Rider("Rider", "6002", "6602")

controller.add_rider_account(rider01)
controller.add_rider_account(rider02)

customer01.add_current_order_list(order01)
customer01.add_current_order_list(order02)

@app.get("/show_order_list01", tags=["OrderList"])
async def read_order_state_list(customer_id) -> dict:
    return {"data": controller.show_order_state_list(customer_id)}

@app.get("/show_order_list02", tags=["OrderList"])
async def read_order_detail_list(customer_id) -> dict:
    return {"data": controller.search_customer_by_id(customer_id).show_current_order_list()}

@app.put("/method_order_list01", tags=["OrderList"])
async def confirm_order(customer_id, order_id) -> dict:
    return {"data": controller.confirm_order(customer_id, order_id)}

@app.put("/method_order_list02", tags=["OrderList"])
async def rider_recieve_order(rider_id, customer_id, order_id) -> dict:
    return {"data": controller.rider_recieve_order(rider_id, customer_id, order_id)}