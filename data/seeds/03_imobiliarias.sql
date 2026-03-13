-- ============================================
-- Seed: Imobiliárias
-- ============================================

-- São Paulo
INSERT INTO imobiliarias (cidade_id, nome, latitude, longitude, email, telefone, qtd_imoveis_anunciados, score_oportunidade)
SELECT id, 'Imobiliária São Paulo Plus', -23.5633, -46.6973, 'contato@spplus.com.br', '(11) 3000-0001', 45, 8.2
FROM cidades WHERE nome = 'São Paulo'
UNION ALL
SELECT id, 'Remax Premium SP', -23.5568, -46.6802, 'vendas@remaxsp.com.br', '(11) 3000-0002', 62, 8.5
FROM cidades WHERE nome = 'São Paulo'
UNION ALL
SELECT id, 'Lopes Imóveis', -23.5582, -46.5942, 'lopes@lopes.com.br', '(11) 3000-0003', 38, 7.8
FROM cidades WHERE nome = 'São Paulo'
UNION ALL
SELECT id, 'Vieira Empreendimentos', -23.5849, -46.6821, 'vieira@vieira.com.br', '(11) 3000-0004', 55, 7.5
FROM cidades WHERE nome = 'São Paulo'
ON CONFLICT DO NOTHING;

-- Rio de Janeiro
INSERT INTO imobiliarias (cidade_id, nome, latitude, longitude, email, telefone, qtd_imoveis_anunciados, score_oportunidade)
SELECT id, 'RJ Imóveis Copacabana', -22.9829, -43.1936, 'copacabana@rjimoveis.com.br', '(21) 3000-0001', 50, 8.6
FROM cidades WHERE nome = 'Rio de Janeiro'
UNION ALL
SELECT id, 'Praia Empreendimentos', -22.9869, -43.2006, 'ipanema@praia.com.br', '(21) 3000-0002', 68, 8.8
FROM cidades WHERE nome = 'Rio de Janeiro'
UNION ALL
SELECT id, 'Leblon Property', -23.0100, -43.2275, 'leblon@property.com.br', '(21) 3000-0003', 52, 8.4
FROM cidades WHERE nome = 'Rio de Janeiro'
ON CONFLICT DO NOTHING;

-- Belo Horizonte
INSERT INTO imobiliarias (cidade_id, nome, latitude, longitude, email, telefone, qtd_imoveis_anunciados, score_oportunidade)
SELECT id, 'BH Imóveis Savassi', -19.9289, -43.9383, 'savassi@bhimoveis.com.br', '(31) 3000-0001', 40, 7.9
FROM cidades WHERE nome = 'Belo Horizonte'
UNION ALL
SELECT id, 'Lourdes Corretora', -19.9338, -43.9399, 'lourdes@corretora.com.br', '(31) 3000-0002', 35, 7.6
FROM cidades WHERE nome = 'Belo Horizonte'
ON CONFLICT DO NOTHING;

-- Brasília
INSERT INTO imobiliarias (cidade_id, nome, latitude, longitude, email, telefone, qtd_imoveis_anunciados, score_oportunidade)
SELECT id, 'Brasília Imóveis', -15.8267, -47.8822, 'vendas@brasiliaimoveis.com.br', '(61) 3000-0001', 42, 7.7
FROM cidades WHERE nome = 'Brasília'
ON CONFLICT DO NOTHING;

-- Salvador
INSERT INTO imobiliarias (cidade_id, nome, latitude, longitude, email, telefone, qtd_imoveis_anunciados, score_oportunidade)
SELECT id, 'Bahia Corretora', -13.0055, -38.5190, 'barra@bahia.com.br', '(71) 3000-0001', 30, 7.2
FROM cidades WHERE nome = 'Salvador'
ON CONFLICT DO NOTHING;
