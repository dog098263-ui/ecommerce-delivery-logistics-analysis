# Data Dictionary: E-Commerce Delivery & Logistics Analysis

This data dictionary outlines the tables, entities, fields, data types, descriptions, constraints, and relationships for the Olist E-Commerce Logistics dataset.

---

## 1. Table: `orders` (`olist_orders_dataset.csv`)
*Primary Key: `order_id`* | *Total Records: 99,441*  
Represents the core order transaction entity tracking the lifecycle milestones of every order from placement to customer delivery.

| Field Name | Raw Type | Parsed Type | Nullable | Description & Domain Rules |
| :--- | :--- | :--- | :---: | :--- |
| `order_id` | `VARCHAR(32)` | `string` | No | Unique alphanumeric identifier for each order (Primary Key). |
| `customer_id` | `VARCHAR(32)` | `string` | No | Key referencing the `customers` table (each order has a distinct customer transaction ID). |
| `order_status` | `VARCHAR(20)` | `string` | No | Current fulfillment status: `delivered` (96,478), `shipped` (1,107), `canceled` (625), `unavailable` (609), `invoiced` (314), `processing` (301), `created` (5), `approved` (2). |
| `order_purchase_timestamp` | `VARCHAR` | `datetime64[ns]` | No | Timestamp when the customer placed the order online. |
| `order_approved_at` | `VARCHAR` | `datetime64[ns]` | Yes (160) | Timestamp when payment clearance and fraud verification was completed. |
| `order_delivered_carrier_date` | `VARCHAR` | `datetime64[ns]` | Yes (1,783) | Timestamp when the order was handed over from seller/warehouse to the logistics carrier (dispatch). |
| `order_delivered_customer_date` | `VARCHAR` | `datetime64[ns]` | Yes (2,965) | Actual timestamp when the parcel was delivered to the recipient. Crucial for measuring transit duration. |
| `order_estimated_delivery_date` | `VARCHAR` | `datetime64[ns]` | No | Target/promised delivery date communicated to the customer at checkout. |

---

## 2. Table: `order_items` (`olist_order_items_dataset.csv`)
*Composite Primary Key: (`order_id`, `order_item_id`)* | *Total Records: 112,650*  
Line-item detail for items within each order, linking products, sellers, freight charges, and shipping deadlines.

| Field Name | Raw Type | Parsed Type | Nullable | Description |
| :--- | :--- | :--- | :---: | :--- |
| `order_id` | `VARCHAR(32)` | `string` | No | Foreign Key referencing `orders.order_id`. |
| `order_item_id` | `INT` | `int64` | No | Sequential number identifying line item count within the order (1, 2, 3...). |
| `product_id` | `VARCHAR(32)` | `string` | No | Foreign Key referencing `products.product_id`. |
| `seller_id` | `VARCHAR(32)` | `string` | No | Foreign Key referencing `sellers.seller_id`. |
| `shipping_limit_date` | `VARCHAR` | `datetime64[ns]` | No | Seller fulfillment deadline to hand the package to the logistics carrier. |
| `price` | `FLOAT` | `float64` | No | Item selling price in Brazilian Real (BRL / R$). |
| `freight_value` | `FLOAT` | `float64` | No | Shipping fee allocated to this item in BRL. |

---

## 3. Table: `order_reviews` (`olist_order_reviews_dataset.csv`)
*Primary Key: `review_id`* | *Foreign Key: `order_id`* | *Total Records: 99,224*  
Customer satisfaction feedback submitted after order placement/delivery.

| Field Name | Raw Type | Parsed Type | Nullable | Description |
| :--- | :--- | :--- | :---: | :--- |
| `review_id` | `VARCHAR(32)` | `string` | No | Unique identifier for each review. |
| `order_id` | `VARCHAR(32)` | `string` | No | Foreign Key referencing `orders.order_id`. Note: 551 orders have multiple reviews. |
| `review_score` | `INT` | `int64` | No | Rating integer from 1 (lowest / dissatisfied) to 5 (highest / satisfied). |
| `review_comment_title` | `VARCHAR` | `string` | Yes (87,656)| Optional headline text provided by the customer. |
| `review_comment_message`| `TEXT` | `string` | Yes (58,247)| Optional full review text. |
| `review_creation_date` | `VARCHAR` | `datetime64[ns]` | No | Date when the satisfaction survey was sent to the customer. |
| `review_answer_timestamp`| `VARCHAR` | `datetime64[ns]`| No | Timestamp when the customer completed the survey. |

---

## 4. Table: `customers` (`olist_customers_dataset.csv`)
*Primary Key: `customer_id`* | *Total Records: 99,441*  
Destination customer details and geographic location.

| Field Name | Raw Type | Parsed Type | Nullable | Description |
| :--- | :--- | :--- | :---: | :--- |
| `customer_id` | `VARCHAR(32)` | `string` | No | Unique transaction-level customer ID (1:1 relationship with `orders`). |
| `customer_unique_id` | `VARCHAR(32)` | `string` | No | Persistent identifier for repeat buyers. |
| `customer_zip_code_prefix`| `INT` | `int64` | No | First 5 digits of the Brazilian postal code (CEP). |
| `customer_city` | `VARCHAR(100)`| `string` | No | Customer's city. |
| `customer_state` | `VARCHAR(2)` | `string` | No | Two-letter Brazilian federal state abbreviation (e.g., SP, RJ, MG, BA). |

---

## 5. Table: `sellers` (`olist_sellers_dataset.csv`)
*Primary Key: `seller_id`* | *Total Records: 3,095*  
Origin seller/warehouse locations.

| Field Name | Raw Type | Parsed Type | Nullable | Description |
| :--- | :--- | :--- | :---: | :--- |
| `seller_id` | `VARCHAR(32)` | `string` | No | Unique seller identifier. |
| `seller_zip_code_prefix` | `INT` | `int64` | No | First 5 digits of seller postal code. |
| `seller_city` | `VARCHAR(100)`| `string` | No | Seller dispatch city. |
| `seller_state` | `VARCHAR(2)` | `string` | No | Two-letter Brazilian state abbreviation for the origin warehouse/store. |

---

## 6. Table: `products` (`olist_products_dataset.csv`)
*Primary Key: `product_id`* | *Total Records: 32,951*  
Physical product attributes and category assignment.

| Field Name | Raw Type | Parsed Type | Nullable | Description |
| :--- | :--- | :--- | :---: | :--- |
| `product_id` | `VARCHAR(32)` | `string` | No | Unique product identifier. |
| `product_category_name` | `VARCHAR(100)`| `string` | Yes (610) | Category name in Portuguese. |
| `product_name_lenght` | `FLOAT` | `float64` | Yes (610) | Character length of product name. |
| `product_description_lenght`| `FLOAT` | `float64` | Yes (610) | Character length of description. |
| `product_photos_qty` | `FLOAT` | `float64` | Yes (610) | Count of published product photos. |
| `product_weight_g` | `FLOAT` | `float64` | Yes (2) | Product shipping weight in grams. |
| `product_length_cm` | `FLOAT` | `float64` | Yes (2) | Package length in centimeters. |
| `product_height_cm` | `FLOAT` | `float64` | Yes (2) | Package height in centimeters. |
| `product_width_cm` | `FLOAT` | `float64` | Yes (2) | Package width in centimeters. |

---

## 7. Table: `product_category_name_translation` (`product_category_name_translation.csv`)
*Primary Key: `product_category_name`* | *Total Records: 71*

| Field Name | Raw Type | Parsed Type | Nullable | Description |
| :--- | :--- | :--- | :---: | :--- |
| `product_category_name` | `VARCHAR(100)` | `string` | No | Original category name in Portuguese. |
| `product_category_name_english` | `VARCHAR(100)` | `string` | No | Clean English translation for reporting/dashboards. |

---

## 8. Relational Entity-Relationship Diagram (ERD)

```text
       [customers] (customer_id)
            │
            ▼ (1:1)
         [orders] (order_id)
         │       │
 (1:N)   ▼       ▼ (1:N)
   [order_items] [order_reviews]
   │          │
   ▼          ▼
[products]  [sellers]
```
