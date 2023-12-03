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

### Query to product code, product name and stock balance

SELECT productCode, productName, sum(iif(inOut == 0, quantity, -quantity)) as stockBalance
FROM stock_in_out as sio, stock_in_out_detail as siod, product as p
WHERE sio.id = siod.stockInOutId and p.id = siod.productId
GROUP BY productName

### Query to get detail of stock of one product

SELECT productCode, productName, batchCode, batchDate, iif(inOut == 0, quantity, -quantity) as stockBalance
FROM stock_in_out as sio, stock_in_out_detail as siod, product as p
WHERE siod.productId = 1 and sio.id = siod.stockInOutId and p.id = siod.productId

SELECT id, batchCode, batchDate, CASE inOut WHEN 0 THEN "Batch In" ELSE "Batch Out" END AS "batchDirection"
FROM stock_in_out

SELECT productId, productCode, productName, quantity
FROM stock_in_out_detail AS siod, product AS p
WHERE siod.productId = p.id
AND stockInOutId = 1