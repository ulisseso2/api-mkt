-- DISTRIBUIÇÃO DOS LEADS POR ETAPA DO CRM (pipeline) — leads criados no período.
-- Parâmetros: :inicio, :fim (inclusivo), :escola (1=Degrau, 2=Central, 0=ambas)
SELECT
    CASE WHEN i.school_id = 1 THEN 'Degrau' ELSE 'Central' END AS empresa,
    s.sort                                           AS ordem,
    COALESCE(s.name, '(sem etapa)')                  AS etapa,
    COUNT(*)                                         AS leads,
    ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY i.school_id), 2) AS pct_da_empresa
FROM interesteds i
LEFT JOIN opportunity_steps s ON s.id = i.opportunity_step_id
WHERE i.created_at >= :inicio
  AND i.created_at <  DATE_ADD(:fim, INTERVAL 1 DAY)
  AND (:escola = 0 OR i.school_id = :escola)
  AND i.school_id IN (1, 2)
  AND (i.opportunity_origin_id IS NULL OR i.opportunity_origin_id <> 14)
GROUP BY i.school_id, s.sort, s.name
ORDER BY empresa, ordem
