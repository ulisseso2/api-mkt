-- VENDAS POR DIA E CATEGORIA — agregado (venda líquida = status Pago).
-- Parâmetros: :inicio, :fim (inclusivo), :escola (1=Degrau, 2=Central, 0=ambas)
-- Pedido com itens de várias categorias entra uma vez em cada (valor do pedido não é rateado:
-- para receita total use vendas_por_dia sem a coluna categoria, ou some valor_total em vendas.sql).
SELECT
    DATE(o.paid_at)                                  AS dia,
    CASE WHEN o.school_id = 1 THEN 'Degrau' ELSE 'Central' END AS empresa,
    COALESCE(pc.name, '(sem item)')                  AS categoria,
    COUNT(DISTINCT o.id)                             AS pedidos_pagos,
    SUM(oi.price * oi.quantity - COALESCE(oi.discount, 0)) AS valor_itens
FROM orders o
LEFT JOIN order_items oi        ON oi.order_id = o.id
LEFT JOIN product_categories pc ON pc.id = oi.product_category_id
WHERE o.paid_at >= :inicio
  AND o.paid_at <  DATE_ADD(:fim, INTERVAL 1 DAY)
  AND (:escola = 0 OR o.school_id = :escola)
  AND o.school_id IN (1, 2)
  AND o.order_status_id = 2
GROUP BY 1, 2, 3
ORDER BY dia, empresa, pedidos_pagos DESC
