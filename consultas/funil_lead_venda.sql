-- FUNIL LEAD → VENDA por origem/UTM. Três formas de dizer "este lead virou venda":
--   vendido_etapa    : etapa do CRM = Vendido (o que o time marcou)
--   vendido_vinculo  : existe pedido pago com orders.opportunity_id = lead (vínculo direto)
--   cliente_comprou  : o mesmo cliente (customer_id) tem pedido pago em até :janela dias após o lead
--                      (paid_at está em UTC: desconta 3h para comparar com o created_at do lead)
-- Parâmetros: :inicio, :fim (inclusivo), :escola (1/2/0), :janela (dias, ex.: 30)
SELECT
    CASE WHEN i.school_id = 1 THEN 'Degrau' ELSE 'Central' END AS empresa,
    COALESCE(o.name, '(sem origem)')                 AS origem,
    COALESCE(NULLIF(i.utm_source, ''), '(sem utm)')  AS utm_source,
    COUNT(*)                                         AS leads,
    SUM(i.opportunity_step_id IN (12, 20))           AS vendido_etapa,
    SUM(EXISTS (SELECT 1 FROM orders v
                WHERE v.opportunity_id = i.id AND v.order_status_id = 2)) AS vendido_vinculo,
    SUM(i.customer_id IS NOT NULL AND EXISTS (
            SELECT 1 FROM orders v
            WHERE v.customer_id = i.customer_id AND v.order_status_id = 2
              AND DATE_SUB(v.paid_at, INTERVAL 3 HOUR) >= i.created_at
              AND DATE_SUB(v.paid_at, INTERVAL 3 HOUR) <  DATE_ADD(i.created_at, INTERVAL :janela DAY))) AS cliente_comprou
FROM interesteds i
LEFT JOIN opportunity_origins o ON o.id = i.opportunity_origin_id
WHERE i.created_at >= :inicio
  AND i.created_at <  DATE_ADD(:fim, INTERVAL 1 DAY)
  AND (:escola = 0 OR i.school_id = :escola)
  AND i.school_id IN (1, 2)
  AND (i.opportunity_origin_id IS NULL OR i.opportunity_origin_id <> 14)
GROUP BY 1, 2, 3
ORDER BY leads DESC
