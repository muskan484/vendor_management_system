This is a Vendor Management System developed using Django and Django REST Framework. The system allows you to manage vendor profiles, track purchase orders, and calculate vendor performance metrics.

## Installation

1. Clone the repository:

git clone "https://github.com/muskan484/vendor_management_system.git",

3. Commands to run the project
    - python3 -m venv <ENV_NAME>
    - source <ENV_NAME>/bin/activate
    - pip3 install -r requirements.txt
    - Migrations for database 
        python3 manage.py makemigrations
        python3 manage.py migrate
    - Run server:
        python3 manage.py runserver

   
    or use the start.sh file to run the project
    neviagte to the root folder and run
    - sh start.sh

## Models
### Vendor Model
- name: Vendor's name.
- contact_details: Contact information of the vendor.
- address: Physical address of the vendor.
- vendor_code: A unique identifier for the vendor.
- on_time_delivery_rate: Tracks the percentage of on-time deliveries.
- quality_rating_avg:  Average rating of quality based on purchase orders.
- average_response_time: Average time taken to acknowledge purchase orders.
- fulfillment_rate: Percentage of purchase orders fulfilled successfully.

### Purchase Order Model
-  po_number: Unique number identifying the PO.
-  vendor: Link to the Vendor model.
-  order_date: Date when the order was placed.
-  delivery_date: Expected or actual delivery date of the order.
-  items: Details of items ordered.
-  quantity: Total quantity of items in the PO.
-  status: Current status of the PO (e.g., pending, completed, canceled).
-  quality_rating: Rating given to the vendor for this PO (nullable).
-  issue_date: Timestamp when the PO was issued to the vendor.
-  acknowledgment_date: Timestamp when the vendor acknowledged the PO(nullable).

### Historical Performance Model
- vendor: ForeignKey link to the Vendor model.
- date: Date of the performance record.
- on_time_delivery_rate: Historical record of the on-time delivery rate.
- quality_rating_avg: Historical record of the quality rating average.
- average_response_time: Historical record of the average response time.
- fulfillment_rate: Historical record of the fulfilment rate.

## Usage

### Vendor Profile Management

#### Create a new vendor

- POST /api/vendors/

Example request body:
```
{
    "name": "vansh dresses",
    "contact_details": "11223-33445",
    "address": "123, xyz street, mumbai, India",
    "vendor_code": "vansh123"
}
```

#### List all vendors

- GET /api/vendors/


#### Retrieve a specific vendor's details

- GET /api/vendors/{vendor_id}/


#### Update a vendor's details

- PUT /api/vendors/{vendor_id}/

Example request body:
```
{
    "name": "vansh dresses",
    "contact_details": "11223-33445",
    "address": "123, xyz street, mumbai, India",
    "vendor_code": "vansh001"
}
```


#### Delete a vendor

- DELETE /api/vendors/{vendor_id}/


### Purchase Order Tracking

#### Create a purchase order

- POST /api/purchase_orders/

Example request body:
```
{
    "po_number": "PO001",
    "vendor": 1,
    "order_date": "2022-01-01T00:00:00Z",
    "delivery_date": "2022-01-15T00:00:00Z",
    "items": [
        {
            "name": "Widget",
            "price": 9.99
        },
        {
            "name": "Gadget",
            "price": 19.99
        }
    ],
    "quantity": 15,
    "status": "pending"
}
```

#### List all purchase orders

- GET /api/purchase_orders/

#### Retrieve details of a specific purchase order

- GET /api/purchase_orders/{po_id}/

#### Update a purchase order

- PUT /api/purchase_orders/{po_id}/

Example request body:
```
{
    "po_number": "PO001",
    "vendor": 1,
    "order_date": "2022-01-01T00:00:00Z",
    "delivery_date": "2022-01-15T00:00:00Z",
    "items": [
        {
            "name": "Widget",
            "price": 9.99
        },
        {
            "name": "Gadget",
            "price": 19.99
        }
    ],
    "quantity": 15,
    "status": "completed",
    "quality_rating": 4.5,
    "issue_date": "2022-01-01T00:00:00Z",
    "acknowledgment_date": "2022-01-02T00:00:00Z"
}
```
#### Delete a purchase order

- DELETE /api/purchase_orders/{po_id}/


### Vendor Performance Evaluation

#### Retrieve a vendor's performance metrics

- GET /api/vendors/{vendor_id}/performance/

Example response body:
```
{
    "on_time_delivery_rate": 80.0,
    "quality_rating_avg": 4.5,
    "average_response_time": 30.0,
    "fulfillment_rate": 100.0
}
```
### Acknowledge a Purchase Order

#### Acknowledge a purchase order

- POST /api/purchase_orders/{po_id}/acknowledge/

Example response body:
```
{
    "message": "Purchase Order acknowledged successfully"
}
```
## Token Authentication

API endpoints are secured with JWT token-based authentication. To obtain an authentication token, send a POST request to the `/api/token/` endpoint with valid credentials. The response will contain an access token that can be used to authenticate subsequent requests.
