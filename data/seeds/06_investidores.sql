-- ============================================
-- Seed: Investidores Detectados
-- ============================================

INSERT INTO investidores_detectados (
  cidade_id, nome, email, telefone, qtd_imoveis, valor_total_investido,
  bairro_preferido, tipo_propriedade_preferida
)
SELECT
  id, 'Carlos Silva Santos', 'carlos.silva@email.com', '(11) 98765-4321', 3, 3500000,
  'Pinheiros', 'residencial'
FROM cidades WHERE nome = 'São Paulo'
UNION ALL
SELECT
  id, 'Fernanda Oliveira Costa', 'fernanda.oliveira@email.com', '(11) 99999-8888', 5, 7200000,
  'Vila Olímpia', 'comercial'
FROM cidades WHERE nome = 'São Paulo'
UNION ALL
SELECT
  id, 'Roberto Mendes', 'roberto.mendes@email.com', '(21) 98888-7777', 2, 4500000,
  'Copacabana', 'residencial'
FROM cidades WHERE nome = 'Rio de Janeiro'
UNION ALL
SELECT
  id, 'Beatriz Ferreira', 'beatriz.ferreira@email.com', '(21) 99555-3333', 4, 12000000,
  'Ipanema', 'misto'
FROM cidades WHERE nome = 'Rio de Janeiro'
UNION ALL
SELECT
  id, 'Alexandre Costa', 'alexandre.costa@email.com', '(31) 98888-1111', 2, 2200000,
  'Savassi', 'residencial'
FROM cidades WHERE nome = 'Belo Horizonte'
ON CONFLICT (email) DO NOTHING;

-- Nota: investidores_imoveis será preenchido via aplicação
-- pois requer IDs específicos de imoveis que devem ser reais
