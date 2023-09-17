SELECT
    film.title AS filme,
    SUM(payment.amount) AS receita_total
FROM
    rental
    JOIN payment ON rental.rental_id = payment.rental_id
    JOIN inventory ON rental.inventory_id = inventory.inventory_id
    JOIN film ON inventory.film_id = film.film_id
GROUP BY
    film.title
ORDER BY
    receita_total DESC;