# Notes

admin = $2b$12$dgtNmUp1CzzplcY0w0gLR.FwtxeKxyu1PCP0GFNE7g7DQafVjYJxO

## Dependencies

```pip install flask flask-login flask-sqlalchemy flask-bcrypt```

## Database tables

product
    product_id - int primary key
    product_code - text(12)
    description - text(100)
    rate - float

stock_in
    id - int auto-increment
    batch_code - text(10)
    batch_date - date

stock_in_detail
    stock_in_id int foreign key
    product_id int foreign key
    quantity

invoice
    id - int auto-increment
    customer - text(100)
    invoice_date - date
    total_amount - float

invoice_detail
    invoice_id - int foreign key
    product_id - int foreign key
    quantity - int
    rate - float
    amount - float
