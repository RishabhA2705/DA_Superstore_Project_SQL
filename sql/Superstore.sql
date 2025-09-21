use superstoredb;

select * from customers limit 10;
select * from orders where ShipMode = "Second Class";
select distinct category from products;
select count(*) as total_customers from customers;
select * from orders where year(OrderDate) = 2017;

-- Find the total sales and profit for each category.
select p.category , sum(od.Sales) as total_sales , sum(od.Profit) as total_profit from orderdetails od join products p on p.ProductID = od.ProductID
group by p.category;

-- Find the top 5 most profitable products.
select p.ProductName , sum(od.profit) as total_profit from products p join orderdetails od on p.ProductID = od.ProductID group by p.productName
order by total_profit Desc Limit 5;

-- Show the first 10 orders with customer name
select c.CustomerName , o.OrderID , o.OrderDate from Orders o inner join Customers c on c.CustomerID = o.CustomerID Limit 10;

-- Find total sales for each customer.
select sum(od.Sales) as total_sales , c.customerName from customers c inner join orders o on o.CustomerID = c.CustomerID inner join od 
on od.OrderID = o.OrderID group by c.customerName order by TotalSales Desc Limit 10;

-- Show all customers and their total sales (include customers with no orders).
select c.CustomerName, SUM(od.Sales) as Total_Sales from Customers c left join Orders o on c.customerID = o.customerID left join Orderdetails od
on o.OrderID = od.OrderID group by c.customerName order by Total_Sales desc;

-- List all products with their total quantity sold (include products never ordered).
select p.ProductName , coalesce(sum(od.Quantity) , 0) as total_quantity from products p left join OrderDetails od on p.ProductID = od.ProductID
group by p.ProductName order by	total_quantity desc Limit 10;

-- Show all orders and their customer names (even if some customers don’t exist in Customers).
select o.OrderID, o.OrderDate, c.CustomerName from Orders o right join Customers c ON o.CustomerID = c.CustomerID LIMIT 10;

-- Show all order details and product names (even if some products are missing in Products)
select od.OrderID, p.ProductName, od.Sales from OrderDetails od right join Products p on od.ProductID = p.ProductID limit 10;

-- Get all customers and their orders (include customers with no orders and orders without valid customers).
select c.CustomerName , o.OrderID from Customers c left join Orders o on c.CustomerID = o.CustomerID UNION
select c.CustomerName , o.OrderID from Customers c right join Orders o on c.CustomerID = o.CustomerID;

-- Find customers from the same city (customer pairs)
select c1.CustomerName as Customer1 , c2.CustomerName as Customer2 , c1.City from Customers c1 join Customers c2 on c1.City = c2.City
and c1.CustomerID < c2.CustomerID Limit 10;

-- Find orders placed on the same date (different customers).
select o1.OrderID as order1 , o2.OrderID as order2 , o1.OrderDate from orders o1 join orders o2 on o1.OrderDate = o2.OrderDate and o1.OrderID < o2.OrderID Limit 10;
