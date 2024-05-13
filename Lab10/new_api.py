from fastapi import FastAPI
import uvicorn
from datetime import datetime

app = FastAPI()

class Controller:
    def __init__(self):
        self.__customer_account_list = []
        self.__rider_account_list = []
        self.__restaurant_account_list = []
        self.__order_list = []
        self.__central_pocket = None
        
    @property
    def central_pocket(self):
        return self.__central_pocket
    
    @central_pocket.setter
    def central_pocket(self, central_pocket):
        self.__central_pocket = central_pocket 
        
    def add_customer_account_list(self, customer_account):
        self.__customer_account_list.append(customer_account)
        
    def add_rider_account_list(self, rider_account):
        self.__rider_account_list.append(rider_account)
        
    def add_restaurant_account_list(self, restaurant_account):
        self.__restaurant_account_list.append(restaurant_account)
        
    def add_order_list(self, order):
        self.__order_list.append(order)
        
    def remove_customer_account_list(self, customer_account):
        self.__customer_account_list.remove(customer_account)
        del customer_account
        
    def remove_rider_account_list(self, rider_account):
        self.__rider_account_list.remove(rider_account)
        del rider_account
        
    def remove_restaurant_account_list(self, restaurant_account):
        self.__restaurant_account_list.remove(restaurant_account)
        del restaurant_account
        
    def remove_order_list(self, order):
        self.__order_list.remove(order)
        del order
        
    def search_customer_account_by_id(self, customer_id):
        for customer in self.__customer_account_list:
            if customer.account_id == customer_id: return customer
        return None
    
    def search_rider_account_by_id(self, rider_id):
        for rider in self.__rider_account_list:
            if rider.account_id == rider_id: return rider
        return None
    
    def search_restaurant_account_by_id(self, restaurant_owner_id):
        for restaurant_owner in self.__restaurant_account_list:
            if restaurant_owner.account_id == restaurant_owner_id: return restaurant_owner
        return None
    
    def search_restaurant_by_id(self, restaurant_id):
        for restaurant in self.__restaurant_list:
            if restaurant.restaurant_id == restaurant_id: return restaurant
        return None
    
    def search_order_by_id(self, order_id):
        for order in self.__order_list:
            if order.order_id == order_id: return order
        return None
    
    def show_order_in_system(self):
        return [order.show_order_detail() for order in self.__order_list]

    # Customer actions
    
    def show_customer_order_cart(self, customer_id):
        customer = self.search_customer_by_id(customer_id)
        if customer == None: return f"customer_id : {customer_id} not found"
        return [order.show_order_detail() for order in customer.order_cart]
    
    def show_customer_order_by_id(self, customer_id, order_id):
        customer = self.search_customer_by_id(customer_id)
        if customer == None: return f"customer_id : {customer_id} not found"
        order = customer.search_order_by_id(order_id)
        if order == None: return f"order_id : {order_id} not found"
        return order.show_order_detail()
        
    def add_order_into_cart(self, customer_id, order_id):
        customer = self.search_customer_by_id(customer_id)
        if customer == None: return f"customer_id : {customer_id} not found"
        order = self.search_order_by_id(order_id)
        if order == None: return f"order_id : {order_id} not found"
        if order in customer.order_cart:
            return f"order_id : {order.order_id} already in cart"
        customer.add_order_into_cart(order)
        return f"order_id : {order.order_id} added into cart"
        
    def remove_order_from_cart(self, customer_id, order_id):
        customer = self.search_customer_by_id(customer_id)
        if customer == None: return f"customer_id : {customer_id} not found"
        order = customer.search_order_by_id(order_id)
        if order == None: return f"order_id : {order_id} not found"
        customer.remove_order_from_cart(order)
        return f"order_id : {order.order_id} removed from cart"
        
    def confirm_customer_order(self, customer_id, order_id):
        customer = self.search_customer_by_id(customer_id)
        if customer == None: return f"customer_id : {customer_id} not found"
        order = customer.search_order_by_id(order_id)
        if order == None: return f"order_id : {order_id} not found"
        amount = sum(food.food_price for food in order.order_food_list)
        if customer.pocket.balance < amount:
            return "Insufficient balance"
        customer.pocket.pay_out(amount)
        payment_time = datetime.now()
        payment = Payment("paid", payment_time.strftime("%c"), amount)
        order.order_state = "confirmed"
        order.order_payment = payment
        # customer.pocket.add_payment_list(payment)
        return f"order_id : {order.order_id} confirmed, amount : {amount}"
    
    # Rider actions
    
    def show_requested_rider_order(self, rider_id):
        rider = self.search_rider_by_id(rider_id)
        if rider == None: return f"rider_id : {rider_id} not found"
        return [order.show_order_detail() for order in rider.requested_order]
    
    def view_confirmed_customer_order(self, rider_id):
        rider = self.search_rider_by_id(rider_id)
        if rider == None: return f"rider_id : {rider_id} not found"
        return [{"customer_id" : customer.account_id, "order_id" : order.order_id} for customer in self.__customer_account_list for order in customer.order_cart if order.order_state == "confirmed"]
        
    def receive_confirmed_customer_order(self, rider_id, customer_id, order_id):
        rider = self.search_rider_by_id(rider_id)
        if rider == None: return f"rider_id : {rider_id} not found"
        customer = self.search_customer_by_id(customer_id)
        if customer == None: return f"customer_id : {customer_id} not found"
        order = customer.search_order_by_id(order_id)
        if order == None: return f"order_id : {order_id} not found"
        restaurant = self.search_restaurant_by_id(order.order_restaurant)
        if restaurant == None: return f"restaurant_id : {order.order_restaurant} not found"
        if order.order_state == "confirmed":
            order.order_state = "received"
            order.order_rider = rider.account_id
            rider.add_requested_order(order)
            restaurant.add_requested_order_list(order)
            # customer.pocket.add_payment_list(order.order_payment)
            return f"order_id : {order_id} requested by {rider.account_id}"
        
    def cancel_received_customer_order(self, rider_id, order_id):
        rider = self.search_rider_by_id(rider_id)
        if rider == None: return f"rider_id : {rider_id} not found"
        order = rider.search_requested_order_by_id(order_id)
        if order == None: return f"order_id : {order_id} not found"
        if order.order_state == "received":
            order.order_state = "confirmed"
            order.order_rider = None
            rider.remove_requested_order(order)
            restaurant = self.search_restaurant_by_id(order.order_restaurant)
            restaurant.remove_requested_order_list(order)
            # customer = self.search_customer_by_id(order.order_customer)
            # customer.pocket.remove_payment_list(order.order_payment)
            return f"order_id : {order_id} canceled by {rider.account_id}"
        
    def receive_finished_restaurant_order(self, rider_id, restaurant_owner_id, restaurant_id, order_id):
        rider = self.search_rider_by_id(rider_id)
        if rider == None: return f"rider_id : {rider_id} not found"
        restaurant_owner = self.search_restaurant_owner_by_id(restaurant_owner_id)
        if restaurant_owner == None: return f"restaurant_owner_id : {restaurant_owner_id} not found"
        restaurant = restaurant_owner.search_restaurant_by_id(restaurant_id)
        if restaurant == None: return f"restaurant_id : {restaurant_id} not found"
        order = restaurant.search_finished_order_by_id(order_id)
        if order == None: return f"order_id : {order_id} not found"
        target_rider_order = rider.search_requested_order_by_id(order_id)
        if target_rider_order == None: return f"order_id : {order_id} not found"
        if target_rider_order.order_id == order.order_id:
            order.order_state = "delivering"
            rider.remove_requested_order(target_rider_order)
            rider.add_holding_order(target_rider_order)
            restaurant.remove_finished_order_list(order)        
            return f"order_id : {order_id} received by {rider.account_id}"
        
    def deliver_finished_restaurant_order(self, rider_id, order_id):
        rider = self.search_rider_by_id(rider_id)
        if rider == None: return f"rider_id : {rider_id} not found"
        order = rider.search_holding_order_by_id(order_id)
        if order == None: return f"order_id : {order_id} not found"
        customer = self.search_customer_by_id(order.order_customer)
        if customer == None: return f"customer_id : {order.order_customer} not found"
        restaurant = self.search_restaurant_by_id(order.order_restaurant)
        if restaurant == None: return f"restaurant_id : {order.order_restaurant} not found"
        restaurant_owner = self.search_restaurant_owner_by_id(restaurant.restaurant_owner.account_id)
        if restaurant_owner == None: return f"restaurant_owner_id : {restaurant.restaurant_owner.account_id} not found"
        if order.order_state == "delivering":
            order.order_staet = "completed"
            amount = order.order_payment.payment_amount
            amount_paid_rider = amount * 0.2
            amount_paid_restaurant = amount * 0.6
            amount_paid_application = amount * 0.2
            rider.pocket.deposite(amount_paid_rider)
            restaurant_owner.pocket.deposite(amount_paid_restaurant)
            self.central_money.deposite(amount_paid_application)
            customer.pocket.add_payment_list(order.order_payment)
            rider.remove_holding_order(order)
            customer.remove_order_from_cart(order)
            return f"order_id : {order_id} delivered by {rider.account_id}"
        
    #Restaurant actions
        
    def add_food_into_restaurant_menu(self, restaurant_owner_id, restaurant_id, food):
        restaurant_owner = self.search_restaurant_owner_by_id(restaurant_owner_id)
        restaurant = restaurant_owner.search_restaurant_by_id(restaurant_id)
        restaurant.add_food_into_menu(food)
        return f"food_id : {food.food_id} added into menu at {restaurant.restaurant_name}"
    
    def show_requested_order_list(self, restaurant_owner_id, restaurant_id):
        restaurant_owner = self.search_restaurant_owner_by_id(restaurant_owner_id)
        if restaurant_owner == None: return f"restaurant_owner_id : {restaurant_owner_id} not found"
        restaurant = restaurant_owner.search_restaurant_by_id(restaurant_id)
        if restaurant == None: return f"restaurant_id : {restaurant_id} not found"
        return [order.show_order_detail() for order in restaurant.requested_order_list]
    
    def show_finished_order_list(self, restaurant_owner_id, restaurant_id):
        restaurant_owner = self.search_restaurant_owner_by_id(restaurant_owner_id)
        if restaurant_owner == None: return f"restaurant_owner_id : {restaurant_owner_id} not found"
        restaurant = restaurant_owner.search_restaurant_by_id(restaurant_id)
        if restaurant == None: return f"restaurant_id : {restaurant_id} not found"
        return [order.show_order_detail() for order in restaurant.finished_order_list]
    
    def finish_cooking_requested_order(self, restaurant_owner_id, restaurant_id, order_id):
        restaurant_owner = self.search_restaurant_owner_by_id(restaurant_owner_id)
        if restaurant_owner == None: return f"restaurant_owner_id : {restaurant_owner_id} not found"
        restaurant = restaurant_owner.search_restaurant_by_id(restaurant_id)
        if restaurant == None: return f"restaurant_id : {restaurant_id} not found"
        order = restaurant.search_requested_order_by_id(order_id)
        if order == None: return f"order_id : {order_id} not found"
        if order.order_state == "received":
            order.order_state = "finished"
            restaurant.remove_requested_order_list(order)
            restaurant.add_finished_order_list(order)
            return f"order_id : {order_id} finished by {restaurant_owner.account_id}"
        
class Account:
    def __init__(self, account_id, password, profile: object = None, pocket: object = None):
        self.__account_id = account_id
        self.__password = password
        self.__profile = profile
        self.__pocket = pocket
    
    @property
    def account_id(self):
        return self.__account_id
    
    @property
    def account_password(self):
        return self.__password
    
    @property
    def profile(self):
        return self.__profile
    
    @profile.setter
    def profile(self, new_profile):
        self.__profile = new_profile
        
    @property
    def pocket(self):
        return self.__pocket
    
    @pocket.setter
    def pocket(self, new_pocket):
        self.__pocket = new_pocket

class Profile:
    def __init__(self, username, fullname, email, phone):
        self.__username = username
        self.__fullname = fullname
        self.__email = email
        self.__phone = phone
        
    @property
    def username(self):
        return self.__username
    
    @username.setter
    def username(self, new_username):
        self.__username = new_username
    
    @property
    def fullname(self):
        return self.__fullname
    
    @fullname.setter
    def fullname(self, new_fullname):
        self.__fullname = new_fullname
        
    def view_profile(self):
        return {'username' : self.__username, 
                'fullname' : self.__fullname, 
                'email' : self.__email, 
                'phone' : self.__phone}
    
class Pocket: 
    def __init__(self, balance):
        self.__balance = balance
        self.__payment_list = []
    
    @property    
    def balance(self):
        return self.__balance
    
    @property
    def payment_list(self):
        return self.__payment_list
    
    def add_payment_list(self, new_payment):
        self.__payment_list.append(new_payment)
        
    def remove_payment_list(self, payment):
        self.__payment_list.remove(payment)
        
    def view_pocket_list(self):
        return {"balance" : self.__balance,
                "payment_list" : [payment.show_payment_detail() for payment in self.__payment_list]}
        
    def top_up(self, amount):
        self.__balance += amount
        
    def pay_out(self, amount):
        self.__balance -= amount
    
    def deposite(self, amount):
        self.__balance += amount
        self.__payment_list.append(Payment("deposite", datetime.now(), amount))
        
    def withdraw(self, amount):
        self.__balance -= amount
        self.__payment_list.append(Payment("withdraw", datetime.now(), amount))
        
class Customer(Account):
    customer_id = 10001
    def __init__(self, password):
        super().__init__(str(Customer.customer_id), password)
        self.__order_cart = []
        self.__order_currently = []
        self.__address_list = []
        self.__reviewed_list = []
        Customer.customer_id += 1
        
    @property
    def order_cart(self):
        return self.__order_cart
    
    @property
    def order_currently(self):
        return self.__order_currently
    
    def add_order_into_cart(self, order):
        self.__order_cart.append(order)
        
    def remove_order_from_cart(self, order):
        self.__order_cart.remove(order)
        
    def add_address_list(self, address):
        self.__address_list.append(address)
        
    def remove_address_list(self, address):
        self.__address_list.remove(address)
        
    def search_order_by_id(self, order_id):
        for order in self.__order_cart:
            if order.order_id == order_id: return order
        return None
    
class Rider(Account):
    rider_id = 20001
    def __init__(self, password):
        super().__init__(str(Rider.rider_id), password)
        self.__requested_order = []
        self.__holding_order = []
        self.__reviewed_list = []
        Rider.rider_id += 1
        
    @property
    def requested_order(self):
        return self.__requested_order
    
    @property
    def holding_order(self):
        return self.__holding_order
        
    def add_requested_order(self, order):
        self.__requested_order.append(order)
        
    def remove_requested_order(self, order):
        self.__requested_order.remove(order)
        
    def add_holding_order(self, order):
        self.__holding_order.append(order)
        
    def remove_holding_order(self, order):
        self.__holding_order.remove(order)
        
    def search_requested_order_by_id(self, order_id):
        for order in self.__requested_order:
            if order.order_id == order_id: return order
        return None
    
    def search_holding_order_by_id(self, order_id):
        for order in self.__holding_order:
            if order.order_id == order_id: return order
        return None

class Restaurant_Owner(Account):
    restaurant_owner_id = 30001
    def __init__(self, password):
        super().__init__(str(Restaurant_Owner.restaurant_owner_id), password)
        self.__restaurant_list = []
        Restaurant_Owner.restaurant_owner_id += 1
        
    def add_restaurant_into_list(self, restaurant):
        self.__restaurant_list.append(restaurant)
        
    def remove_restaurant_from_list(self, restaurant):
        self.__restaurant_list.remove(restaurant)
        
    def search_restaurant_by_id(self, restaurant_id):
        for restaurant in self.__restaurant_list:
            if restaurant.restaurant_id == restaurant_id: return restaurant
        return None
        
class Restaurant:
    id = 40001
    def __init__(self, restaurant_owner, restaurant_name, restaurant_address, restaurant_phone = None, restaurant_email = None):
        self.__restaurant_id = str(Restaurant.id)
        self.__restaurant_owner = restaurant_owner
        self.__restaurant_name = restaurant_name
        self.__restaurant_address = restaurant_address
        self.__restaurant_phone = restaurant_phone
        self.__restaurant_email = restaurant_email
        self.__restaurant_menu = []
        self.__requested_order_list = []
        self.__finished_order_list = []
        self.__reviewed_list = []
        Restaurant.id += 1
        
    @property
    def restaurant_id(self):
        return self.__restaurant_id
    
    @property
    def restaurant_owner(self):
        return self.__restaurant_owner
    
    @property
    def restaurant_name(self):
        return self.__restaurant_name
    
    @property
    def restaurant_address(self):
        return self.__restaurant_address
    
    @property
    def restaurant_phone(self):
        return self.__restaurant_phone
    
    @property
    def restaurant_email(self):
        return self.__restaurant_email
    
    @property
    def restaurant_menu(self):
        return self.__restaurant_menu
    
    @property
    def requested_order_list(self):
        return self.__requested_order_list
    
    @property
    def finished_order_list(self):
        return self.__finished_order_list
    
    def add_food_into_menu(self, food):
        self.__restaurant_menu.append(food)
        
    def remove_food_into_menu(self, food):
        self.__restaurant_menu.remove(food)
        
    def add_requested_order_list(self, requested_order):
        self.__requested_order_list.append(requested_order)
        
    def remove_requested_order_list(self, requested_order):
        self.__requested_order_list.remove(requested_order)
        
    def add_finished_order_list(self, finished_order):
        self.__finished_order_list.append(finished_order)
        
    def remove_finished_order_list(self, finished_order):
        self.__finished_order_list.remove(finished_order)
        
    def search_requested_order_by_id(self, order_id):
        for order in self.__requested_order_list:
            if order.order_id == order_id: return order
        return None
    
    def search_finished_order_by_id(self, order_id):
        for order in self.__finished_order_list:
            if order.order_id == order_id: return order
        return None
        
class Food:
    id = 50001
    def __init__(self, food_name, food_type, food_size, food_price):
        self.__food_id = str(Food.id)
        self.__food_name = food_name
        self.__food_type = food_type
        self.__food_size = food_size
        self.__food_price = food_price
        Food.id += 1
        
    @property
    def food_id(self):
        return self.__food_id
    
    @property
    def food_name(self):
        return self.__food_name
    
    @property
    def food_type(self):
        return self.__food_type
    
    @property
    def food_size(self):
        return self.__food_size
    
    @property
    def food_price(self):
        return self.__food_price
        
class Order:
    id = 60001
    def __init__(self, order_customer, order_restaurant, order_food_list):
        self.__order_id = str(Order.id)
        self.__order_state = "non-actived"
        self.__order_payment = None
        self.__order_customer = order_customer
        self.__order_rider = None
        self.__order_restaurant = order_restaurant
        self.__order_food_list = order_food_list
        Order.id += 1
        
    @property
    def order_id(self):
        return self.__order_id
    
    @property
    def order_state(self):
        return self.__order_state
    
    @order_state.setter
    def order_state(self, state):
        self.__order_state = state
        
    @property
    def order_payment(self):
        return self.__order_payment
    
    @order_payment.setter
    def order_payment(self, payment):
        self.__order_payment = payment
        
    @property
    def order_customer(self):
        return self.__order_customer
    
    @order_customer.setter
    def order_customer(self, customer):
        self.__order_customer = customer
        
    @property
    def order_rider(self):
        return self.__order_rider
    
    @order_rider.setter
    def order_rider(self, rider):
        self.__order_rider = rider
        
    @property
    def order_restaurant(self):
        return self.__order_restaurant
    
    @order_restaurant.setter
    def order_restaurant(self, restaurant):
        self.__order_restaurant = restaurant
        
    @property
    def order_food_list(self):
        return self.__order_food_list
    
    @order_food_list.setter
    def order_food_list(self, food_list):
        self.__order_food_list = food_list
        
    def show_food_list(self):
        return [{"food_name": food.food_name, 
                 "food_type": food.food_type, 
                 "food_size": food.food_size, 
                 "food_price": food.food_price} for food in self.__order_food_list]
        
    def show_order_detail(self):
        return {'order_id' : self.__order_id, 
                'order_state' : self.__order_state, 
                'order_payment' : self.__order_payment.show_payment_detail() if self.__order_payment != None else None, 
                'order_customer' : self.__order_customer, 
                'order_rider' : self.__order_rider, 
                'order_restaurant' : self.__order_restaurant, 
                'order_food_list' : self.show_food_list()}

class Payment:
    id = 70001
    def __init__(self, payment_status, payment_date, payment_amount):
        self.__payment_id = str(Payment.id)
        self.__payment_status = payment_status
        self.__payment_date = payment_date
        self.__payment_amount = payment_amount
        self.__payment_customer = None
        self.__payment_rider = None
        self.__payment_restaurant = None
        self.__payment_food_list = []
        Payment.id += 1
        
    @property
    def payment_id(self):
        return self.__payment_id
    
    @property
    def payment_status(self):
        return self.__payment_status
    
    @payment_status.setter
    def payment_status(self, new_status):
        self.__payment_status = new_status

    @property
    def payment_date(self):
        return self.__payment_date

    @property
    def payment_amount(self):
        return self.__payment_amount
    
    def show_payment_detail(self):
        return {'payment_id' : self.__payment_id, 
                'payment_status' : self.__payment_status, 
                'payment_date' : self.__payment_date, 
                'payment_amount' : self.__payment_amount}
    
class Review:
    id = 80001
    def __init__(self, reviewed_id, reviewed_into, reviewed_rate, reviewed_date, reviewed_comment):
        self.__reviewed_id = str(Review.id)
        self.__reviewed_into = reviewed_into
        self.__reviewed_rate = reviewed_rate
        self.__reviewed_date = reviewed_date
        self.__reviewed_comment = reviewed_comment
        self.__reviewed_customer = None
        self.__reviewed_rider = None
        self.__reviewed_restaurant = None
        Review.id += 1
        
controller = Controller()
system_balance = Pocket(5000000)
controller.central_money = system_balance

customer01 = Customer("555001")
customer02 = Customer("555002")
customer03 = Customer("555003")
profile01 = Profile("Proxy", "Proxeos Maximaz", "055-055-0551", "customer_01@gmail.com")
profile02 = Profile("Jingliu", "Jing Xiaoyu", "055-055-0552", "customer_02@gmail.com")
profile03 = Profile("Itachi", "Uchiha Itachi", "055-055-0553", "customer_03@gmail.com")
pocket01 = Pocket(6000)
pocket02 = Pocket(7500)
pocket03 = Pocket(9000)
customer01.profile = profile01
customer02.profile = profile02
customer03.profile = profile03
customer01.pocket = pocket01
customer02.pocket = pocket02
customer03.pocket = pocket03

controller.add_customer_account_list(customer01)
controller.add_customer_account_list(customer02)
controller.add_customer_account_list(customer03)

restaurant_owner_01 = Restaurant_Owner("666001")
restaurant_owner_02 = Restaurant_Owner("666002")
profile_owner_01 = Profile("Maco", "Maco Maximus", "066-066-0661", "restaurant_owner_01@gmail.com")
profile_owner_02 = Profile("Kira", "Kira Yoshikage", "066-066-0662", "restaurant_owner_02@gmail.com")
pocket_owner_01 = Pocket(60000)
pocket_owner_02 = Pocket(72000)
restaurant_owner_01.profile = profile_owner_01
restaurant_owner_02.profile = profile_owner_02
restaurant_owner_01.pocket = pocket_owner_01
restaurant_owner_02.pocket = pocket_owner_02

controller.add_restaurant_owner_account_list(restaurant_owner_01)
controller.add_restaurant_owner_account_list(restaurant_owner_02)

food_101 = Food("Fried Chicken", "dished", "medium", 150)
food_102 = Food("Italian Spaghetti", "dished", "medium", 200)
food_103 = Food("Pizza Hug", "fast-food", "medium", 250)
food_104 = Food("Burger Cheese", "fast-food", "medium", 150)

food_201 = Food("Shabu Shabu", "hot-pot", "medium", 300)
food_202 = Food("Sushi Set", "sushi", "medium", 250)
food_203 = Food("Ramen", "noodle", "medium", 200)
food_204 = Food("Sashimi", "sushi", "medium", 300)

restaurant01 = Restaurant(restaurant_owner_01, "KFC", "Bangkok")
restaurant02 = Restaurant(restaurant_owner_02, "Sushi Hana", "LadKraBang")

restaurant_owner_01.add_restaurant_into_list(restaurant01)
restaurant_owner_02.add_restaurant_into_list(restaurant02)

controller.add_restaurant_list(restaurant01)
controller.add_restaurant_list(restaurant02)

rider01 = Rider("777001")
rider02 = Rider("777002")
profile_rider01 = Profile("Arith", "Arithemis Maximus", "077-077-0771", "rider01@gmail.com")
profile_rider02 = Profile("Killer", "Killer Queen", "077-077-0772", "rider02@gmail.com")
pocket_rider01 = Pocket(18000)
pocket_rider02 = Pocket(25000)
rider01.profile = profile_rider01
rider02.profile = profile_rider02
rider01.pocket = pocket_rider01
rider02.pocket = pocket_rider02

controller.add_rider_account_list(rider01)
controller.add_rider_account_list(rider02)

controller.add_food_into_restaurant_menu(restaurant_owner_01.account_id, restaurant01.restaurant_id, food_101)
controller.add_food_into_restaurant_menu(restaurant_owner_01.account_id, restaurant01.restaurant_id, food_102)
controller.add_food_into_restaurant_menu(restaurant_owner_01.account_id, restaurant01.restaurant_id, food_103)
controller.add_food_into_restaurant_menu(restaurant_owner_01.account_id, restaurant01.restaurant_id, food_104)

controller.add_food_into_restaurant_menu(restaurant_owner_01.account_id, restaurant01.restaurant_id, food_201)
controller.add_food_into_restaurant_menu(restaurant_owner_01.account_id, restaurant01.restaurant_id, food_202)
controller.add_food_into_restaurant_menu(restaurant_owner_01.account_id, restaurant01.restaurant_id, food_203)
controller.add_food_into_restaurant_menu(restaurant_owner_01.account_id, restaurant01.restaurant_id, food_204)

order01 = Order(customer01.account_id, restaurant01.restaurant_id, [food_101, food_102])
order02 = Order(customer01.account_id, restaurant01.restaurant_id, [food_103, food_104])
order03 = Order(customer02.account_id, restaurant02.restaurant_id, [food_201, food_202])
order04 = Order(customer02.account_id, restaurant02.restaurant_id, [food_203, food_204])
controller.add_order_list(order01)
controller.add_order_list(order02)
controller.add_order_list(order03)
controller.add_order_list(order04)

# Global actions

print(controller.add_order_into_cart(customer01.account_id, order01.order_id))
print(controller.add_order_into_cart(customer01.account_id, order02.order_id))

print(controller.show_customer_order_cart(customer01.account_id))

print(controller.confirm_customer_order(customer01.account_id, order01.order_id))
print(controller.confirm_customer_order(customer01.account_id, order02.order_id))

print(controller.search_customer_by_id(customer01.account_id).profile.view_profile())
print(controller.search_customer_by_id(customer02.account_id).profile.view_profile())
print(controller.search_customer_by_id(customer01.account_id).pocket.view_pocket_list())
print(controller.search_customer_by_id(customer02.account_id).pocket.view_pocket_list())

print(controller.view_confirmed_customer_order(rider01.account_id))
print(controller.view_confirmed_customer_order(rider02.account_id))

print(controller.receive_confirmed_customer_order(rider01.account_id, customer01.account_id, order01.order_id))
print(controller.receive_confirmed_customer_order(rider02.account_id, customer01.account_id, order02.order_id))

print(controller.finish_cooking_requested_order(restaurant_owner_01.account_id, restaurant01.restaurant_id, order01.order_id))
print(controller.finish_cooking_requested_order(restaurant_owner_01.account_id, restaurant01.restaurant_id, order02.order_id))
print(controller.receive_finished_restaurant_order(rider01.account_id, restaurant_owner_01.account_id, restaurant01.restaurant_id, order01.order_id))
print(controller.receive_finished_restaurant_order(rider02.account_id, restaurant_owner_01.account_id, restaurant01.restaurant_id, order02.order_id))
print(controller.deliver_finished_restaurant_order(rider01.account_id, order01.order_id))
print(controller.deliver_finished_restaurant_order(rider02.account_id, order02.order_id))

print(controller.show_customer_order_cart(customer01.account_id))

# if __name__ == "__main__":
#     uvicorn.run("new_api:app", host="127.0.0.1", port=8000, log_level="info")