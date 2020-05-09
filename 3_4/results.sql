use test
set names utf8;

-- 1. Выбрать все товары (все поля)
select * from product;

-- 2. Выбрать названия всех автоматизированных складов
select name from store where is_automated=1;

-- 3. Посчитать общую сумму в деньгах всех продаж
select sum(total) from sale;

-- 4. Получить уникальные store_id всех складов, с которых была хоть одна продажа
select distinct(store_id) from store right join sale using (store_id);


-- 5. Получить уникальные store_id всех складов, с которых не было ни одной продажи
select distinct(store_id) from store left join sale using (store_id) where sale_id is null;

-- 6. Получить для каждого товара название и среднюю стоимость единицы товара avg(total/quantity), если товар не продавался, он не попадает в отчет.
select name, avg(total/quantity) from product left join sale using (product_id) where sale_id is not null group by name;

-- 7. Получить названия всех продуктов, которые продавались только с единственного склада
select tab2.name from 
(select tab.name, count(*) co from 
(select p.name, s.store_id
from product as p left join sale as s using (product_id) where store_id is not null
group by name, store_id) as tab
group by tab.name having co=1) as tab2;

-- 8. Получить названия всех складов, с которых продавался только один продукт
select tab2.name from 
(select tab.name, count(*) co from
(select p.name, s.product_id
from store as p left join sale as s using (store_id) where product_id is not null
group by p.name, s.product_id) as tab
group by tab.name having co=1) as tab2;

-- 9. Выберите все ряды (все поля) из продаж, в которых сумма продажи (total) максимальна (равна максимальной из всех встречающихся)
SELECT * FROM sale as s where s.total in 
(
SELECT max(total) FROM sale
)

-- 10. Выведите дату самых максимальных продаж, если таких дат несколько, то самую раннюю из них
select tab.date from 
(SELECT date, sum(quantity) as summa FROM test.sale group by date order by summa desc limit 1) as tab;

