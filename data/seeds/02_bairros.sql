-- ============================================
-- Seed: Bairros
-- ============================================

-- São Paulo
INSERT INTO bairros (cidade_id, nome, score_valorizacao, score_demanda, score_oferta, latitude, longitude)
SELECT id, 'Vila Madalena', 8.5, 7.8, 6.2, -23.5568, -46.6802 FROM cidades WHERE nome = 'São Paulo'
UNION ALL
SELECT id, 'Pinheiros', 8.2, 8.0, 7.1, -23.5633, -46.6973 FROM cidades WHERE nome = 'São Paulo'
UNION ALL
SELECT id, 'Mooca', 7.5, 6.5, 5.8, -23.5582, -46.5942 FROM cidades WHERE nome = 'São Paulo'
UNION ALL
SELECT id, 'Tatuapé', 7.2, 6.8, 6.3, -23.5548, -46.5722 FROM cidades WHERE nome = 'São Paulo'
UNION ALL
SELECT id, 'Vila Olímpia', 8.8, 8.5, 7.9, -23.5849, -46.6821 FROM cidades WHERE nome = 'São Paulo'
ON CONFLICT (cidade_id, nome) DO NOTHING;

-- Rio de Janeiro
INSERT INTO bairros (cidade_id, nome, score_valorizacao, score_demanda, score_oferta, latitude, longitude)
SELECT id, 'Copacabana', 8.1, 9.0, 7.5, -22.9829, -43.1936 FROM cidades WHERE nome = 'Rio de Janeiro'
UNION ALL
SELECT id, 'Ipanema', 8.7, 9.2, 8.0, -22.9869, -43.2006 FROM cidades WHERE nome = 'Rio de Janeiro'
UNION ALL
SELECT id, 'Leblon', 8.5, 9.0, 7.8, -23.0100, -43.2275 FROM cidades WHERE nome = 'Rio de Janeiro'
UNION ALL
SELECT id, 'Barra da Tijuca', 7.8, 8.3, 8.5, -23.0277, -43.3664 FROM cidades WHERE nome = 'Rio de Janeiro'
UNION ALL
SELECT id, 'Centro', 6.2, 5.0, 6.8, -22.9028, -43.1729 FROM cidades WHERE nome = 'Rio de Janeiro'
ON CONFLICT (cidade_id, nome) DO NOTHING;

-- Belo Horizonte
INSERT INTO bairros (cidade_id, nome, score_valorizacao, score_demanda, score_oferta, latitude, longitude)
SELECT id, 'Savassi', 8.0, 7.5, 6.5, -19.9289, -43.9383 FROM cidades WHERE nome = 'Belo Horizonte'
UNION ALL
SELECT id, 'Lourdes', 7.8, 7.2, 6.0, -19.9338, -43.9399 FROM cidades WHERE nome = 'Belo Horizonte'
UNION ALL
SELECT id, 'Funcionários', 7.5, 6.8, 5.5, -19.9347, -43.9473 FROM cidades WHERE nome = 'Belo Horizonte'
UNION ALL
SELECT id, 'Pampulha', 6.8, 6.0, 5.2, -19.8809, -43.9715 FROM cidades WHERE nome = 'Belo Horizonte'
UNION ALL
SELECT id, 'Santa Lúcia', 7.2, 6.5, 5.8, -19.9489, -43.9473 FROM cidades WHERE nome = 'Belo Horizonte'
ON CONFLICT (cidade_id, nome) DO NOTHING;

-- Brasília
INSERT INTO bairros (cidade_id, nome, score_valorizacao, score_demanda, score_oferta, latitude, longitude)
SELECT id, 'Asa Sul', 7.5, 7.0, 6.5, -15.8267, -47.8822 FROM cidades WHERE nome = 'Brasília'
UNION ALL
SELECT id, 'Asa Norte', 7.3, 6.8, 6.2, -15.7939, -47.8822 FROM cidades WHERE nome = 'Brasília'
UNION ALL
SELECT id, 'Águas Claras', 7.8, 8.0, 7.5, -15.7733, -47.9293 FROM cidades WHERE nome = 'Brasília'
UNION ALL
SELECT id, 'Sudoeste', 6.5, 5.5, 4.8, -15.8583, -47.8975 FROM cidades WHERE nome = 'Brasília'
ON CONFLICT (cidade_id, nome) DO NOTHING;

-- Salvador
INSERT INTO bairros (cidade_id, nome, score_valorizacao, score_demanda, score_oferta, latitude, longitude)
SELECT id, 'Barra', 7.5, 7.2, 6.5, -13.0055, -38.5190 FROM cidades WHERE nome = 'Salvador'
UNION ALL
SELECT id, 'Vitória', 7.2, 6.8, 6.0, -12.9647, -38.5256 FROM cidades WHERE nome = 'Salvador'
UNION ALL
SELECT id, 'Periperi', 5.8, 4.5, 4.2, -13.0333, -38.4917 FROM cidades WHERE nome = 'Salvador'
UNION ALL
SELECT id, 'Itaigara', 7.8, 7.5, 6.8, -12.9947, -38.5017 FROM cidades WHERE nome = 'Salvador'
ON CONFLICT (cidade_id, nome) DO NOTHING;
