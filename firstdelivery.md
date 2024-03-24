# First Delivery

[Explicar a app]

## Features

- Save your cart for later
- Effortlessly buy merchandise from the LECI students center
- Make your opinion count and add a rating or comment to the products you buy or wish to buy
- Stay on top of your orders by simply checking your orders page, you can rebuy from any past order you have

[Fazer o resto das funcionalidades]

## Requisitos

[Apresentar os requisitos funcionais e não funcionais]

## Entidades

* carts
* emergency_codes
* orders
* products
* reviews
* users

## Relações

* users - orders [1:N]
* users - emergency_codes [N:M]
* users - carts [1:1]
* users - reviews [1:N]
* orders - products [N:M]
* carts - products [N:M]
* reviews - products [N:1]

## Atributos das Entidades

#### carts

* user_id **[PK] [FK]**
* product_id **[PK] [FK]**
* quantity **[FK]**

#### emergency_codes

* user_id **[PK] [FK]**
* emergency_code **[PK]**
* emergency_code_valid
* emergency_code_timestamp

#### orders

* order_id **[PK]**
* user_id **[PK] [FK]**
* product_id **[PK] [FK]**
* quantity
* total_price
* shipping_address
* order_date

#### products

* product_id **[PK]**
* product_name
* product_description
* price
* category
* stock
* available

#### reviews

* review_id **[PK]**
* product_id **[FK]**
* user_id **[FK]**
* review_text
* rating
* review_date

#### users

* user_id **[PK]**
* username
* hashed_password
* password_reset_token
* password_reset_token_timestamp
* email
* totp_secret_key
* totp_secret_key_timestamp
* admin_role

## DER

[Apresentar o DER]

## ER

[Apresentar o ER]
