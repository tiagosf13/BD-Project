# BD: Trabalho Prático Loja (?)

**Grupo**: P2G3

- Tiago Fonseca, MEC: 107266
- João Gaspar, MEC: 114514

## Introduction

Online merchandising shop that implements a database, interactable through the front-end. Users will be able to create accounts, add merchandising to their carts and buying the chosen merch by placing the order. While administrators will be able to add, remove and update the products sold in the app and even process the orders, they will also have utility tools to see diverse statistic, ultimately presenting shop success to the owner. 

## Features

- Save your cart for later
- Effortlessly buy merchandise from the LECI students center
- Make your opinion count and add a rating or comment to the products you buy or wish to buy
- Stay on top of your orders by simply checking your orders page, you can rebuy from any past order you have

## Requirements

### Functional

* #### Users

  * Create an account with a persistent cart
  * Add and remove products to cart
  * Complete orders
  * Edit account information
  * See previous orders
  * Review bought products
  * Filter and search for products
* #### Administrators

  * Add and remove products to the shop
  * Edit products data
  * See current selling products on shop
  * Process and/or delete orders
  * See shop statistics

### Non Functional

* Security
  * to complete
* Performance
  * to complete
* Reliability
  * to complete
* Ease-of-Use
  * to complete

## Entities

* carts
* emergency_codes
* orders
* products
* reviews
* users

## Relations

* users - orders [1:N]
* users - emergency_codes [1:N]
* users - carts [1:1]
* users - reviews [1:N]
* orders - products [N:M]
* carts - products [N:M]
* reviews - products [N:1]

## Entity attributes

#### carts

* user_id **[PK] [FK]**
* product_id **[PK] [FK]**
* quantity

#### emergency_codes

* user_id **[PK] [FK]**
* emergency_code **[PK]**
* emergency_code_valid
* emergency_code_timestamp

#### orders

* order_id **[PK]**
* user_id **[PK] [FK]**
* total_price
* shipping_address
* order_date

#### products_ordered

* order_id **[PK] [FK]**
* product_id **[PK] [FK]**
* quantity

#### products

* product_id **[PK]**
* product_name
* product_description
* price
* category
* stock
* available

#### reviews (NAO ESTA BEM NO ER)

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
* admin_role (FALTA NO ER)

## DER

![DER](DER.png)

## ER

![ER](ER.png)
