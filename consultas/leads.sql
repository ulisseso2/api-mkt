-- LEADS (oportunidades) do período — 1 linha por lead, SEM dados pessoais.
-- Parâmetros: :inicio e :fim (AAAA-MM-DD, fim inclusivo), :escola (1=Degrau, 2=Central, 0=ambas)
-- Base: SQL_OPORTUNIDADES do DashboardController (seducar-dashboard), com as mesmas regras.
-- Exclui origem 14 (Upsell Passaport): não é lead novo, é venda adicional para aluno.
SELECT
    i.id                                            AS lead_id,
    CASE WHEN i.school_id = 1 THEN 'Degrau' ELSE 'Central' END AS empresa,
    i.created_at                                    AS criado_em,
    DATE(i.created_at)                              AS dia,
    o.name                                          AS origem,
    i.utm_source, i.utm_medium, i.utm_campaign, i.utm_content,
    (i.gclid IS NOT NULL AND i.gclid <> '')         AS tem_gclid,
    (i.fbclid IS NOT NULL AND i.fbclid <> '')       AS tem_fbclid,
    i.page_title                                    AS pagina,
    i.page_type                                     AS tipo_pagina,
    f.name                                          AS concurso,
    a.name                                          AS area,
    s.name                                          AS etapa,
    CASE WHEN i.opportunity_step_id IN (12, 20) THEN 1 ELSE 0 END AS etapa_vendido,
    CASE WHEN i.opportunity_step_id IN (11, 19) THEN 1 ELSE 0 END AS etapa_perdido,
    d.full_name                                     AS dono,
    i.prelead,
    CASE
        WHEN (l.name IS NULL OR l.name = '') AND i.opportunity_modality_id IN (2, 5) THEN 'EAD'
        WHEN (l.name IS NULL OR l.name = '') AND i.opportunity_modality_id IN (3, 6) THEN 'LIVE'
        WHEN (l.name IS NULL OR l.name = '') AND i.opportunity_modality_id IN (1, 4) THEN 'Presencial/Indefinido'
        WHEN (l.name IS NULL OR l.name = '') AND i.opportunity_modality_id IS NULL THEN 'Indefinida'
        ELSE l.name
    END                                             AS unidade,
    CASE
        WHEN (m.name IS NULL OR m.name = '') AND i.unit_id IN (22, 24) THEN 'Live'
        WHEN (m.name IS NULL OR m.name = '') AND i.unit_id IN (23, 25) THEN 'Online'
        WHEN (m.name IS NULL OR m.name = '') AND i.unit_id BETWEEN 1 AND 21 THEN 'Presencial'
        WHEN (m.name IS NULL OR m.name = '') AND i.unit_id IN (26, 27) THEN 'Smart'
        WHEN (m.name IS NULL OR m.name = '') AND i.unit_id IS NULL THEN 'Indefinida'
        ELSE m.name
    END                                             AS modalidade,
    ip.tier,
    ip.total_score                                  AS score_total,
    ip.p1_score, ip.p2_score,
    pa1.text                                        AS p1_resposta,
    CASE WHEN ip.p2_answer = 'aluno' THEN 'Já é aluno' ELSE pa2.text END AS p2_resposta
FROM interesteds i
LEFT JOIN opportunity_steps s       ON s.id = i.opportunity_step_id
LEFT JOIN opportunity_origins o     ON o.id = i.opportunity_origin_id
LEFT JOIN opportunity_modalities m  ON m.id = i.opportunity_modality_id
LEFT JOIN units l                   ON l.id = i.unit_id
LEFT JOIN areas a                   ON a.id = i.area_id
LEFT JOIN sales_force f             ON f.id = i.sales_force_id
LEFT JOIN users d                   ON d.id = i.owner_id
-- pontuação mais recente do lead (há leads com mais de uma linha)
LEFT JOIN interested_pontuations ip ON ip.id = (
    SELECT MAX(ip2.id) FROM interested_pontuations ip2 WHERE ip2.interested_id = i.id
)
LEFT JOIN interested_pontuations_answers pa1
       ON pa1.school_id = ip.school_id AND pa1.question = 1 AND pa1.question_number = ip.p1_answer
LEFT JOIN interested_pontuations_answers pa2
       ON pa2.school_id = ip.school_id AND pa2.question = 2 AND ip.p2_answer REGEXP '^[0-9]+$'
      AND pa2.question_number = ip.p2_answer
WHERE i.created_at >= :inicio
  AND i.created_at <  DATE_ADD(:fim, INTERVAL 1 DAY)
  AND (:escola = 0 OR i.school_id = :escola)
  AND i.school_id IN (1, 2)
  AND (i.opportunity_origin_id IS NULL OR i.opportunity_origin_id <> 14)
ORDER BY i.created_at DESC
