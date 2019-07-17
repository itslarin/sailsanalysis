--total quantity of orders - 
select count(*) from public.order



--average order price, total order price and total order quantity by months
select 
date_part('year',order_datetime) as year, 
LPAD(date_part('month',order_datetime)::text, 2, '0') as month, 
concat(date_part('year',order_datetime)::text,LPAD(date_part('month',order_datetime)::text, 2, '0')) as yearmonth,
ceil(sum(order_price)) as total_order_price, 
ceil(avg(order_price)) as avg_order_price, 
count(order_id) as total_orders 
from public.order 
group by year, month 
order by year desc, month desc



--average volume of order (positions quantity) by months
select 
date_part('year',order_datetime) as year, 
LPAD(date_part('month',order_datetime)::text, 2, '0') as month, 
concat(date_part('year',order_datetime)::text,LPAD(date_part('month',order_datetime)::text, 2, '0')) as yearmonth,
count(torderproduct.orderproduct_id) as total_orderproducts,
count(distinct(torderproduct.order_id)) as total_orders,
round(count(torderproduct.orderproduct_id)::decimal / count(distinct(torderproduct.order_id)),2) as avg_orderproducts
from public.orderproduct as torderproduct
left outer join public.order as torder on torderproduct.order_id = torder.order_id
group by year, month 
order by year desc, month desc 
