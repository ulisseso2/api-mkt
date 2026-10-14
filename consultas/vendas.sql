-- VENDAS (pedidos) do período — 1 linha por pedido, SEM dados pessoais.
-- Parâmetros: :inicio, :fim (inclusivo), :escola (1=Degrau, 2=Central, 0=ambas)
-- Data da venda = paid_at (mesmo critério do seducar-dashboard).
-- Traz TODOS os status: filtre depois. Venda líquida = status_id 2 (Pago).
-- Venda bruta (padrão das telas de vendas) = status_id IN (2, 3, 10, 14, 15).
SELECT
    o.id                                            AS pedido_id,
    CASE WHEN o.school_id = 1 THEN 'Degrau' ELSE 'Central' END AS empresa,
    o.paid_at                                       AS data_venda,
    DATE(o.paid_at)                                 AS dia,
    os.id                                           AS status_id,
    os.name                                         AS status,
    o.total                                         AS valor_total,
    o.total_discount                                AS desconto,
    o.total_refund                                  AS estorno,
    pm.name                                         AS forma_pagamento,
    CASE WHEN o.owner_id IS NULL THEN 'Site' ELSE 'Time' END AS canal_venda,
    IFNULL(ow.full_name, IFNULL(v.full_name, 'Indefinido')) AS vendedor,
    it.produto, it.categoria, it.curso, it.curso_venda, it.turma, it.turno, it.unidade,
    o.opportunity_id                                AS lead_id_vinculado,
    o.customer_id                                   AS cliente_id,
    att.utm_source, att.utm_medium, att.utm_campaign, att.origem AS origem_atribuicao
FROM orders o
LEFT JOIN order_status os     ON os.id = o.order_status_id
LEFT JOIN payment_methods pm  ON pm.id = o.payment_method_id
LEFT JOIN users v             ON v.id  = o.user_id
LEFT JOIN users ow            ON ow.id = o.owner_id
LEFT JOIN order_attributions att ON att.order_id = o.id
-- itens agregados por pedido (evita duplicar linhas)
LEFT JOIN (
    SELECT
        oi.order_id,
        GROUP_CONCAT(DISTINCT p.title  SEPARATOR ', ') AS produto,
        GROUP_CONCAT(DISTINCT pc.name  SEPARATOR ', ') AS categoria,
        GROUP_CONCAT(DISTINCT t.name   SEPARATOR ', ') AS turma,
        GROUP_CONCAT(DISTINCT sh.name  SEPARATOR ', ') AS turno,
        GROUP_CONCAT(DISTINCT CASE
            WHEN cu.title IS NULL AND oi.product_category_id = 7  THEN 'Passaporte'
            WHEN cu.title IS NULL AND oi.product_category_id = 10 AND o2.school_id = 1 THEN 'Degrau Smart'
            WHEN cu.title IS NULL AND oi.product_category_id = 10 AND o2.school_id = 2 THEN 'Central Smart'
            ELSE cu.title END SEPARATOR ', ')            AS curso,
        GROUP_CONCAT(DISTINCT CASE
            WHEN cs.name  IS NULL AND oi.product_category_id = 7  THEN 'Passaporte'
            WHEN cu.title IS NULL AND oi.product_category_id = 10 AND o2.school_id = 1 THEN 'Degrau Smart'
            WHEN cu.title IS NULL AND oi.product_category_id = 10 AND o2.school_id = 2 THEN 'Central Smart'
            ELSE cs.name END SEPARATOR ', ')             AS curso_venda,
        COALESCE(MAX(u.name), CASE
            WHEN MAX(pc.id) = 3  THEN 'Live'
            WHEN MAX(pc.id) = 10 THEN 'Smart'
            WHEN MAX(pc.id) = 2  THEN 'EAD'
            WHEN MAX(pc.id) = 7  THEN COALESCE(MAX(u3.name), 'Indefinido')
            ELSE 'Indefinido' END)                       AS unidade
    FROM order_items oi
    JOIN orders o2               ON o2.id = oi.order_id
    LEFT JOIN products p         ON p.id  = oi.product_id
    LEFT JOIN product_categories pc ON pc.id = oi.product_category_id
    LEFT JOIN classrooms t       ON t.id  = oi.classroom_id
    LEFT JOIN shifts sh          ON sh.id = t.shift_id
    LEFT JOIN units u            ON u.id  = t.unit_id
    LEFT JOIN units u3           ON u3.id = o2.unit_id
    LEFT JOIN courses cu         ON cu.id = t.course_id
    LEFT JOIN course_sales cs    ON cs.id = cu.course_sale_id
    WHERE o2.paid_at >= :inicio
      AND o2.paid_at <  DATE_ADD(:fim, INTERVAL 1 DAY)
    GROUP BY oi.order_id
) it ON it.order_id = o.id
WHERE o.paid_at >= :inicio
  AND o.paid_at <  DATE_ADD(:fim, INTERVAL 1 DAY)
  AND (:escola = 0 OR o.school_id = :escola)
  AND o.school_id IN (1, 2)
ORDER BY o.paid_at DESC
