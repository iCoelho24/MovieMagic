SELECT
    actor.actor_id as ID_ator,
    CONCAT(actor.first_name, ' ', actor.last_name) AS Nome_Completo,
    COUNT(film_actor.film_id) AS Numero_de_filmes
FROM
    actor
    JOIN film_actor ON actor.actor_id = film_actor.actor_id
GROUP BY
    actor.actor_id, Nome_Completo
HAVING
    COUNT(film_actor.film_id) >= 15
ORDER BY
    Numero_de_filmes DESC;