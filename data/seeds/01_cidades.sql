-- ============================================
-- Seed: Cidades
-- ============================================

INSERT INTO cidades (nome, estado, latitude, longitude) VALUES
('São Paulo', 'SP', -23.5505, -46.6333),
('Rio de Janeiro', 'RJ', -22.9068, -43.1729),
('Belo Horizonte', 'MG', -19.9203, -43.9345),
('Brasília', 'DF', -15.8267, -47.8822),
('Salvador', 'BA', -12.9714, -38.5014)
ON CONFLICT (nome) DO NOTHING;
