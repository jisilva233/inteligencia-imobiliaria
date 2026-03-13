-- ============================================
-- Dashboard de Inteligência Imobiliária
-- Views Calculadas
-- ============================================

-- ============================================
-- VIEW: vw_imoveis_marketing_fraco
-- ============================================
-- Calcula score de fraqueza de marketing (0-100)
-- Baseado em: qtd_fotos, video, tour_virtual, descricao
--
-- Lógica:
-- - 0-4 fotos: +30 pontos (muito fraco)
-- - Sem video: +20 pontos
-- - Sem tour virtual: +15 pontos
-- - Descricao < 50 caracteres: +35 pontos
--
-- Score final: quanto maior, pior o marketing
-- ============================================
CREATE OR REPLACE VIEW vw_imoveis_marketing_fraco AS
SELECT
  i.id,
  i.endereco,
  i.preco,
  i.bairro_id,
  b.nome AS bairro_nome,
  i.qtd_fotos,
  i.tem_video,
  i.tem_tour_virtual,
  LENGTH(COALESCE(i.descricao_marketing, '')) AS descricao_length,
  (
    CASE
      WHEN i.qtd_fotos < 5 THEN 30
      WHEN i.qtd_fotos < 10 THEN 15
      WHEN i.qtd_fotos < 15 THEN 5
      ELSE 0
    END
    +
    CASE WHEN i.tem_video = FALSE THEN 20 ELSE 0 END
    +
    CASE WHEN i.tem_tour_virtual = FALSE THEN 15 ELSE 0 END
    +
    CASE
      WHEN LENGTH(COALESCE(i.descricao_marketing, '')) < 50 THEN 35
      WHEN LENGTH(COALESCE(i.descricao_marketing, '')) < 150 THEN 15
      ELSE 0
    END
  ) AS score_fraqueza_marketing,
  i.imobiliaria_id,
  im.nome AS imobiliaria_nome,
  i.created_at,
  i.updated_at
FROM imoveis i
LEFT JOIN bairros b ON i.bairro_id = b.id
LEFT JOIN imobiliarias im ON i.imobiliaria_id = im.id
ORDER BY score_fraqueza_marketing DESC, i.created_at DESC;

-- RLS para a view (herda das tabelas base)
ALTER TABLE vw_imoveis_marketing_fraco OWNER TO postgres;

-- ============================================
-- VIEW: vw_ranking_bairros
-- ============================================
-- Ranking composto de bairros
-- Score = (40% × valorizacao) + (35% × demanda) + (25% × oferta)
-- ============================================
CREATE OR REPLACE VIEW vw_ranking_bairros AS
SELECT
  b.id,
  b.cidade_id,
  c.nome AS cidade_nome,
  b.nome AS bairro_nome,
  b.latitude,
  b.longitude,
  b.score_valorizacao,
  b.score_demanda,
  b.score_oferta,
  ROUND(
    (b.score_valorizacao * 0.40) +
    (b.score_demanda * 0.35) +
    (b.score_oferta * 0.25)
  , 2) AS score_composto,
  DENSE_RANK() OVER (PARTITION BY b.cidade_id ORDER BY
    (b.score_valorizacao * 0.40) +
    (b.score_demanda * 0.35) +
    (b.score_oferta * 0.25) DESC
  ) AS ranking_na_cidade,
  COUNT(i.id) AS total_imoveis,
  ROUND(AVG(i.preco), 2) AS preco_medio
FROM bairros b
LEFT JOIN cidades c ON b.cidade_id = c.id
LEFT JOIN imoveis i ON b.id = i.bairro_id
GROUP BY b.id, b.cidade_id, c.nome, b.nome, b.latitude, b.longitude,
         b.score_valorizacao, b.score_demanda, b.score_oferta
ORDER BY b.cidade_id, ranking_na_cidade;

ALTER TABLE vw_ranking_bairros OWNER TO postgres;

-- ============================================
-- VIEW: vw_investidores_resumo
-- ============================================
-- Resumo de investidores com agg de dados
-- ============================================
CREATE OR REPLACE VIEW vw_investidores_resumo AS
SELECT
  inv.id,
  inv.nome,
  inv.email,
  inv.telefone,
  inv.qtd_imoveis,
  inv.valor_total_investido,
  inv.bairro_preferido,
  inv.tipo_propriedade_preferida,
  c.nome AS cidade_nome,
  COUNT(ii.id) AS imoveis_count_verificado,
  ROUND(AVG(i.preco), 2) AS preco_medio_imoveis,
  MIN(i.preco) AS menor_imovel,
  MAX(i.preco) AS maior_imovel
FROM investidores_detectados inv
LEFT JOIN cidades c ON inv.cidade_id = c.id
LEFT JOIN investidores_imoveis ii ON inv.id = ii.investidor_id
LEFT JOIN imoveis i ON ii.imovel_id = i.id
GROUP BY inv.id, inv.nome, inv.email, inv.telefone, inv.qtd_imoveis,
         inv.valor_total_investido, inv.bairro_preferido, inv.tipo_propriedade_preferida,
         c.nome
ORDER BY inv.qtd_imoveis DESC;

ALTER TABLE vw_investidores_resumo OWNER TO postgres;

-- ============================================
-- VIEW: vw_oportunidades_qualificadas
-- ============================================
-- Pipeline de prospecção filtrado por status
-- ============================================
CREATE OR REPLACE VIEW vw_oportunidades_qualificadas AS
SELECT
  op.id,
  op.status,
  op.tipo_lead,
  op.contato_nome,
  op.contato_email,
  op.contato_telefone,
  op.score_qualificacao,
  op.data_deteccao,
  op.data_proxima_acao,
  im.nome AS imobiliaria_nome,
  i.endereco,
  i.preco,
  c.nome AS cidade_nome,
  CASE
    WHEN op.status = 'fechado' THEN 'success'
    WHEN op.status = 'proposta_enviada' THEN 'warning'
    WHEN op.status = 'em_contato' THEN 'info'
    WHEN op.status = 'qualificado' THEN 'primary'
    ELSE 'secondary'
  END AS status_badge,
  DATEDIFF(CURRENT_DATE, op.data_deteccao) AS dias_prospeccao
FROM oportunidades_prospeccao op
LEFT JOIN imobiliarias im ON op.imobiliaria_id = im.id
LEFT JOIN imoveis i ON op.imovel_id = i.id
LEFT JOIN cidades c ON op.cidade_id = c.id
ORDER BY op.score_qualificacao DESC, op.data_deteccao DESC;

ALTER TABLE vw_oportunidades_qualificadas OWNER TO postgres;

-- ============================================
-- VIEW: vw_imobiliarias_performance
-- ============================================
-- Performance de imobiliárias em vendas
-- ============================================
CREATE OR REPLACE VIEW vw_imobiliarias_performance AS
SELECT
  im.id,
  im.nome,
  im.email,
  im.telefone,
  im.score_oportunidade,
  c.nome AS cidade_nome,
  COUNT(DISTINCT i.id) AS total_imoveis_anunciados,
  COUNT(DISTINCT ii.investidor_id) AS total_compradores,
  ROUND(AVG(i.preco), 2) AS preco_medio,
  ROUND(AVG(i.score_fraqueza_marketing), 2) AS marketing_medio,
  COUNT(DISTINCT CASE WHEN i.score_fraqueza_marketing > 60 THEN i.id END) AS imoveis_marketing_fraco
FROM imobiliarias im
LEFT JOIN cidades c ON im.cidade_id = c.id
LEFT JOIN imoveis i ON im.id = i.imobiliaria_id
LEFT JOIN investidores_imoveis ii ON i.id = ii.imovel_id
GROUP BY im.id, im.nome, im.email, im.telefone, im.score_oportunidade, c.nome
ORDER BY im.score_oportunidade DESC;

ALTER TABLE vw_imobiliarias_performance OWNER TO postgres;
