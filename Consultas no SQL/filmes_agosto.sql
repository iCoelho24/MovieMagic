SELECT DISTINCT
    customer.first_name as NOME,
    customer.last_name AS SOBRENOME,
    TO_CHAR(rental.rental_date, 'YYYY/MM/DD') AS data_aluguel
FROM customer 
LEFT JOIN rental 
ON customer.customer_id = rental.customer_id 
WHERE rental.rental_date BETWEEN '2022-08-01' AND '2022-08-31'
ORDER BY data_aluguel;
