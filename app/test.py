import requests

main_url = "http://127.0.0.1:8000/"

users = {
    "arber": {
        "username": "arberbiljali",
        "email": "arberbiljali@gmail.com",
        "password": "admin1234"
    },
    "hamza": {
        "username": "hamzaiseni",
        "email": "hamzaiseni@gmail.com",
        "password": "admin1234"
        
    },
    "lorik": {
        "username": "loriklimani",
        "email": "loriklimani@gmail.com",
        "password": "admin1234"
    },
    "hejfa": {
        "username": "hejfayahya",
        "email": "hejfayahya@gmail.com",
        "password": "admin1234"
    },
    "alejna": {
        "username": "alejnarexhepi",
        "email": "alejnarexhepi@gmail.com",
        "password": "admin1234"
    },
    "astrit": {
        "username": "astritterstena",
        "email": "astritterstena@gmail.com",
        "password": "admin1234"
    },
    "visar": {
        "username": "visaragushi",
        "email": "visaragushi@gmail.com",
        "password": "admin1234"
    }
}

categories = {
    "Computer & Laptops": {
        "category_name": "Computer & Laptops",
        "category_description": "Computers and Laptops for everyone"
    },
    "Phones": {
        "category_name": "Phones",
        "category_description": "Phones for everyone"
    },
    "TVs": {
        "category_name": "TVs",
        "category_description": "TVs for everyone"
    },
    "Gaming": {
        "category_name": "Gaming",
        "category_description": "Gaming accessories for everyone"
    },
    "Smart": {
        "category_name": "Smart",
        "category_description": "Smart gadgets for everyone"
    },
    "Accessories": {
        "category_name": "Accessories",
        "category_description": "Accessories for everyone"
    },
    "Computer Parts": {
        "category_name": "Computer Parts",
        "category_description": "Parts for every laptop and computer"
    }
}

products = {
    "Macbook Pro 16": {
        "title": "Macbook Pro 16",
        "description": "Macbook Pro 16 2019",
        "price": 2000,
        "image": "https://www.google.com/imgres?imgurl=https%3A%2F%2Fm.media-amazon.com%2Fimages%2FI%2F71-AXXlyd7L.jpg&tbnid=vgfERxrnXcQ8YM&vet=12ahUKEwirt7TDsY7_AhWMCewKHRIgAngQMygFegUIARDqAQ..i&imgrefurl=https%3A%2F%2Fwww.amazon.com%2FApple-MacBook-Touch-2-4GHz-Renewed%2Fdp%2FB09TCQLY4Y&docid=5zNlEm345H8KpM&w=2560&h=1676&q=Macbook%20Pro%2016%202019&client=ubuntu&ved=2ahUKEwirt7TDsY7_AhWMCewKHRIgAngQMygFegUIARDqAQ",
        "category_id": 1,
        
    },
    "Macbook Pro 13": {
        "title": "Macbook Pro 13",
        "description": "Macbook Pro 13 2019",
        "price": 1500,
        "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzpa9x4oIKppWA7rU1xv4Xxh2rydcT_vGUR19gSuoNrYIGErpzg5biZWS6no8N2k_PLrc&usqp=CAU",
        "category_id": 1,
    },
    "Macbook Air 13": {
        "title": "Macbook Air 13",
        "description": "Macbook Air 13 2019",
        "price": 1000,
        "image": "https://support.apple.com/library/APPLE/APPLECARE_ALLGEOS/SP798/mba-2019.jpg",
        "category_id": 1,
    },
    "Samsung UE43AU7092UXXH crystal uhd smart 4K Ultra HD": {
        "title": "Samsung UE43AU7092UXXH crystal uhd smart 4K Ultra HD",
        "description": "SAMSUNG LED TV UE43AU7092UXXH, 4K, SMART 43 (109 cm), rezolucija 3 ,840 x 2,160, UHD zatamljenje, LED, Smart TV, HDR 10+, PQI 2000, Crystal Processor",
        "price": 2000,
        "image": "https://img.ep-cdn.com/i/500/500/mv/mvdbwnargehzxpkqcofu/samsung-ue43au7092uxxh-crystal-uhd-smart-4k-ultra-hd-televizor-cene.webp",
        "category_id": 3,
    },
    
}

def create_user(data: dict):
    
    url = main_url + "users"
    
    response = requests.post(url, json=data)
    
    print(response.status_code)


def login_user(data: dict):
    
    url = main_url + "login"
    
    headers =  {"Content-Type":"application/json"}
    
    payload = {
        "username": data["email"],
        "password": data["password"]
    }
    
    
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        return "Bearer " + response.json()["access_token"]
    
def logout_user(token: str):
    pass

def create_category(data: dict, token: str):
    
    url = main_url + "categories"
    
    headers = {"Authorization": token}
    
    response = requests.post(url, headers=headers, json=data)
    
    print(response.status_code)
    
def get_categories(token: str):
        
    url = main_url + "categories"
    
    headers = {"Authorization": token}
    
    response = requests.get(url, headers=headers)
    
    print(response.status_code)
    print(response.json())

def create_product(data: dict, token: str):
        
    url = main_url + "products"
    
    headers = {"Authorization": token}
    
    response = requests.post(url, headers=headers, json=data)
    
    print(response.status_code)
    print(response.json())
    
def get_products(token: str):
            
    url = main_url + "products"
    
    headers = {"Authorization": token}
    
    response = requests.get(url, headers=headers)
    
    print(response.status_code)
    print(response.json())

def get_product_by_id(token: str, id: int):
                    
    url = main_url + "products/" + str(id)
    
    headers = {"Authorization": token}
    
    response = requests.get(url, headers=headers)
    
    print(response.status_code)
    print(response.json())

def get_product_by_category(token: str, category_id: int):
    
    url = main_url + "products/category=" + str(category_id)
    
    headers = {"Authorization": token}
    
    response = requests.get(url, headers=headers)
    
    print(response.status_code)
    print(response.json())
    
def create_cart(token: str):
    
    url = main_url + "carts/"
    
    headers = {"Authorization": token}
    
    response  = requests.post(url, headers=headers)#, json=data)
    
    print(response.status_code)
    print(response.json())
    
    return response

def get_carts(token: str):
    
    url = main_url + "carts/"
    
    headers = {"Authorization": token}
    
    response = requests.get(url, headers=headers)
    
    print(response.json())
    print(response.status_code)

def add_product_to_cart(token: str, cart_id: int, product_id: int):
    
    url = main_url + "carts/" + str(cart_id) + "/"
    
    headers = {"Authorization": token}
    
    response = requests.post(url, headers=headers, json={"product_id": product_id})
    
    print(response.status_code)
    print(response.json())
    
    
############################################
# Main part of the script
############################################

FILL_DB = False

if FILL_DB:
    for user in users:
        create_user(users[user])
    
    token = login_user(users["arber"])
    
    for category in categories:
        create_category(categories[category], token)
        
    # for product in products:
    #     create_product(products[product], token)
    
token = login_user(users["arber"])

# for category in categories:
#     create_category(categories[category], token)

# get_categories(token)
# for product in products:
#     create_product(products[product], token)

# get_products(token)
# get_product_by_category(token, 1)

add_product_to_cart(token, 1, 4)

print("DEBUG!")
# get_products(token)
# get_carts(token)

print("Done!")