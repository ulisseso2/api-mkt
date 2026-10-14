-- LEADS POR CAMPANHA (UTM) — agregado, com qualidade (tier) e conversão (etapa Vendido).
-- Parâmetros: :inicio, :fim (inclusivo), :escola (1=Degrau, 2=Central, 0=ambas)
SELECT
    CASE WHEN i.school_id = 1 THEN 'Degrau' ELSE 'Central' END AS empresa,
    COALESCE(NULLIF(i.utm_source, ''), '(sem utm)')   AS utm_source,
    COALESCE(NULLIF(i.utm_medium, ''), '(sem utm)')   AS utm_medium,
    COALESCE(NULLIF(i.utm_campaign, ''), '(sem utm)') AS utm_campaign,
    COUNT(*)                                          AS leads,
    SUM(ip.id IS NOT NULL)                            AS leads_pontuados,
    SUM(ip.tier = 'A')                                AS tier_a,
    SUM(ip.tier = 'B')                                AS tier_b,
    SUM(ip.tier = 'C')                                AS tier_c,
    SUM(ip.tier = 'D')                                AS tier_d,
    ROUND(AVG(ip.total_score), 1)                     AS score_medio,
    SUM(i.opportunity_step_id IN (12, 20))            AS vendidos,
    ROUND(100 * SUM(i.opportunity_step_id IN (12, 20)) / COUNT(*), 2) AS taxa_conversao_pct
FROM interesteds i
LEFT JOIN interested_pontuations ip ON ip.id = (
    SELECT MAX(ip2.id) FROM interested_pontuations ip2 WHERE ip2.interested_id = i.id
)
WHERE i.created_at >= :inicio
  AND i.created_at <  DATE_ADD(:fim, INTERVAL 1 DAY)
  AND (:escola = 0 OR i.school_id = :escola)
  AND i.school_id IN (1, 2)
  AND (i.opportunity_origin_id IS NULL OR i.opportunity_origin_id <> 14)
GROUP BY 1, 2, 3, 4
ORDER BY leads DESC
