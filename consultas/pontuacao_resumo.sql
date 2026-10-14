-- QUALIFICAÇÃO DO BOT (P1/P2/tier) — como os leads responderam e quanto cada faixa converte.
-- Parâmetros: :inicio, :fim (inclusivo), :escola (1=Degrau, 2=Central, 0=ambas)
-- Só existe pontuação para leads a partir de 16/06/2026.
SELECT
    CASE WHEN i.school_id = 1 THEN 'Degrau' ELSE 'Central' END AS empresa,
    COALESCE(ip.tier, '(sem tier)')                   AS tier,
    COALESCE(pa1.text, 'Sem resposta')                AS p1_urgencia,
    CASE
        WHEN ip.p2_answer = 'aluno' THEN 'Já é aluno'
        WHEN pa2.text IS NOT NULL THEN pa2.text
        ELSE 'Sem resposta'
    END                                               AS p2_investimento,
    CASE
        WHEN ip.p2_answered_at IS NOT NULL AND ip.p2_timed_out_at IS NOT NULL THEN 'Respondeu fora do prazo'
        WHEN ip.p2_answered_at IS NOT NULL THEN 'Respondeu no prazo'
        WHEN ip.p2_timed_out_at IS NOT NULL THEN 'Não respondeu (timeout)'
        ELSE 'Aguardando P2'
    END                                               AS p2_status,
    COUNT(*)                                          AS leads,
    ROUND(AVG(ip.total_score), 1)                     AS score_medio,
    SUM(i.opportunity_step_id IN (12, 20))            AS vendidos,
    ROUND(100 * SUM(i.opportunity_step_id IN (12, 20)) / COUNT(*), 2) AS taxa_conversao_pct
FROM interested_pontuations ip
JOIN interesteds i ON i.id = ip.interested_id
LEFT JOIN interested_pontuations_answers pa1
       ON pa1.school_id = ip.school_id AND pa1.question = 1 AND pa1.question_number = ip.p1_answer
LEFT JOIN interested_pontuations_answers pa2
       ON pa2.school_id = ip.school_id AND pa2.question = 2 AND ip.p2_answer REGEXP '^[0-9]+$'
      AND pa2.question_number = ip.p2_answer
WHERE ip.id = (SELECT MAX(ip2.id) FROM interested_pontuations ip2 WHERE ip2.interested_id = ip.interested_id)
  AND i.created_at >= :inicio
  AND i.created_at <  DATE_ADD(:fim, INTERVAL 1 DAY)
  AND (:escola = 0 OR i.school_id = :escola)
  AND i.school_id IN (1, 2)
GROUP BY 1, 2, 3, 4, 5
ORDER BY empresa, tier, leads DESC
