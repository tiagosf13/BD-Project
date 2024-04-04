# BD: Trabalho Prático Loja (?)

**Grupo**: P2G3

- Tiago Fonseca, MEC: 107266
- João Gaspar, MEC: 114514

## Introduction

Online merchandising shop that implements a database, interactable through the front-end.
There will be one main entity, the `Users`:

* After a `User` creates an account, in order to protect the account in case the he looses access to the account or to the 2-step authentication, he can recover the account using one of the N associated `emergency_codes` that will verify that the `User` is indeed the owner of the account
* `Users` will have one `cart` that is `User` specific.
* Each `cart` contains N `products` and each `products` can be in `carts` from M different `Users`.
* After a `User` buys products from a cart, an `order` will be placed. Each `order` is associated to a `User` and N `products`
* `Users` will also be able to make N `reviews` on one `product`, each `review` will have only one writer.

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
  * Provide 2FA and Emergency Codes for Users, securing the Authentication process and the respective accounts
* Performance
  * The shop must be quick and have a short response time
* Reliability
  * It must persist during and after issues, maintaining the integrity of critical information
* Ease-of-Use
  * It should be intuitive and accessible for everyone to use

## Entities

* carts
* emergency_codes
* orders
* products
* reviews
* users

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
* user_id **[FK]**
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

![DER](DER.png)

## ER

![ER](ER.png)
