-- ============================================
-- Seed: Imóveis
-- ============================================

-- São Paulo - Vila Madalena
INSERT INTO imoveis (
  cidade_id, bairro_id, imobiliaria_id, endereco, preco, area_m2, quartos, banheiros, estacionamentos,
  qtd_fotos, tem_video, tem_tour_virtual, descricao_marketing, tipo_empreendimento, em_construcao,
  latitude, longitude
)
SELECT
  c.id, b.id, im.id,
  'Rua Augusta 1250 - Vila Madalena', 1200000, 150, 3, 2, 1,
  3, FALSE, FALSE, 'Apto antigo', 'pronto', FALSE,
  -23.5568, -46.6802
FROM cidades c
JOIN bairros b ON c.id = b.cidade_id AND b.nome = 'Vila Madalena'
LEFT JOIN imobiliarias im ON c.id = im.cidade_id AND im.nome = 'Imobiliária São Paulo Plus'
WHERE c.nome = 'São Paulo'
UNION ALL
SELECT
  c.id, b.id, im.id,
  'Rua Henrique Schaumann 500 - Pinheiros', 1800000, 220, 4, 3, 2,
  12, TRUE, TRUE, 'Excelente apartamento com varanda e vista para a cidade. Próximo a metrô e comércios.', 'pronto', FALSE,
  -23.5633, -46.6973
FROM cidades c
JOIN bairros b ON c.id = b.cidade_id AND b.nome = 'Pinheiros'
LEFT JOIN imobiliarias im ON c.id = im.cidade_id AND im.nome = 'Remax Premium SP'
WHERE c.nome = 'São Paulo'
UNION ALL
SELECT
  c.id, b.id, im.id,
  'Avenida Paulista 2000 - Bela Vista', 950000, 120, 2, 2, 1,
  2, FALSE, FALSE, 'Apt', 'pronto', FALSE,
  -23.5633, -46.6550
FROM cidades c
JOIN bairros b ON c.id = b.cidade_id AND b.nome = 'Pinheiros'
LEFT JOIN imobiliarias im ON c.id = im.cidade_id AND im.nome = 'Lopes Imóveis'
WHERE c.nome = 'São Paulo';

-- São Paulo - Mooca
INSERT INTO imoveis (
  cidade_id, bairro_id, imobiliaria_id, endereco, preco, area_m2, quartos, banheiros, estacionamentos,
  qtd_fotos, tem_video, tem_tour_virtual, descricao_marketing, tipo_empreendimento, em_construcao,
  latitude, longitude
)
SELECT
  c.id, b.id, im.id,
  'Rua Vergueiro 3000 - Mooca', 680000, 100, 2, 1, 1,
  8, TRUE, FALSE, 'Apartamento bem localizado próximo a todas as facilidades', 'pronto', FALSE,
  -23.5582, -46.5942
FROM cidades c
JOIN bairros b ON c.id = b.cidade_id AND b.nome = 'Mooca'
LEFT JOIN imobiliarias im ON c.id = im.cidade_id AND im.nome = 'Lopes Imóveis'
WHERE c.nome = 'São Paulo'
UNION ALL
SELECT
  c.id, b.id, im.id,
  'Avenida Tatuapé 1500 - Tatuapé', 750000, 110, 2, 2, 1,
  4, FALSE, FALSE, 'Sem descrição', 'pronto', FALSE,
  -23.5548, -46.5722
FROM cidades c
JOIN bairros b ON c.id = b.cidade_id AND b.nome = 'Tatuapé'
LEFT JOIN imobiliarias im ON c.id = im.cidade_id AND im.nome = 'Vieira Empreendimentos'
WHERE c.nome = 'São Paulo';

-- São Paulo - Empreendimentos em construção
INSERT INTO imoveis (
  cidade_id, bairro_id, imobiliaria_id, endereco, preco, area_m2, quartos, banheiros, estacionamentos,
  qtd_fotos, tem_video, tem_tour_virtual, descricao_marketing, tipo_empreendimento, em_construcao, percentual_conclusao,
  latitude, longitude
)
SELECT
  c.id, b.id, im.id,
  'Avenida Berrini 4000 - Vila Olímpia', 2500000, 300, 4, 3, 2,
  15, TRUE, TRUE, 'Empreendimento moderno com excelentes acabamentos e localização privilegiada. Próximo a empresa.', 'estrutura', TRUE, 60,
  -23.5849, -46.6821
FROM cidades c
JOIN bairros b ON c.id = b.cidade_id AND b.nome = 'Vila Olímpia'
LEFT JOIN imobiliarias im ON c.id = im.cidade_id AND im.nome = 'Remax Premium SP'
WHERE c.nome = 'São Paulo';

-- Rio de Janeiro - Copacabana
INSERT INTO imoveis (
  cidade_id, bairro_id, imobiliaria_id, endereco, preco, area_m2, quartos, banheiros, estacionamentos,
  qtd_fotos, tem_video, tem_tour_virtual, descricao_marketing, tipo_empreendimento, em_construcao,
  latitude, longitude
)
SELECT
  c.id, b.id, im.id,
  'Avenida Atlântica 1500 - Copacabana', 2000000, 180, 3, 2, 1,
  10, TRUE, FALSE, 'Apartamento com vista para o mar, excelente oportunidade de investimento', 'pronto', FALSE,
  -22.9829, -43.1936
FROM cidades c
JOIN bairros b ON c.id = b.cidade_id AND b.nome = 'Copacabana'
LEFT JOIN imobiliarias im ON c.id = im.cidade_id AND im.nome = 'RJ Imóveis Copacabana'
WHERE c.nome = 'Rio de Janeiro'
UNION ALL
SELECT
  c.id, b.id, im.id,
  'Rua Figueiredo Magalhães 800 - Copacabana', 1500000, 140, 2, 2, 1,
  3, FALSE, FALSE, 'Bom', 'pronto', FALSE,
  -22.9850, -43.1950
FROM cidades c
JOIN bairros b ON c.id = b.cidade_id AND b.nome = 'Copacabana'
LEFT JOIN imobiliarias im ON c.id = im.cidade_id AND im.nome = 'RJ Imóveis Copacabana'
WHERE c.nome = 'Rio de Janeiro';

-- Rio de Janeiro - Ipanema
INSERT INTO imoveis (
  cidade_id, bairro_id, imobiliaria_id, endereco, preco, area_m2, quartos, banheiros, estacionamentos,
  qtd_fotos, tem_video, tem_tour_virtual, descricao_marketing, tipo_empreendimento, em_construcao,
  latitude, longitude
)
SELECT
  c.id, b.id, im.id,
  'Rua Visconde de Pirajá 500 - Ipanema', 3500000, 250, 4, 3, 2,
  18, TRUE, TRUE, 'Luxuoso apartamento em Ipanema com piscina, academia e concierge 24h. Melhor endereço do Rio.', 'pronto', FALSE,
  -22.9869, -43.2006
FROM cidades c
JOIN bairros b ON c.id = b.cidade_id AND b.nome = 'Ipanema'
LEFT JOIN imobiliarias im ON c.id = im.cidade_id AND im.nome = 'Praia Empreendimentos'
WHERE c.nome = 'Rio de Janeiro';

-- Belo Horizonte - Savassi
INSERT INTO imoveis (
  cidade_id, bairro_id, imobiliaria_id, endereco, preco, area_m2, quartos, banheiros, estacionamentos,
  qtd_fotos, tem_video, tem_tour_virtual, descricao_marketing, tipo_empreendimento, em_construcao,
  latitude, longitude
)
SELECT
  c.id, b.id, im.id,
  'Avenida Getúlio Vargas 1000 - Savassi', 850000, 130, 3, 2, 1,
  9, TRUE, FALSE, 'Apartamento bem localizado na melhor avenida de Belo Horizonte, prédio com infraestrutura completa', 'pronto', FALSE,
  -19.9289, -43.9383
FROM cidades c
JOIN bairros b ON c.id = b.cidade_id AND b.nome = 'Savassi'
LEFT JOIN imobiliarias im ON c.id = im.cidade_id AND im.nome = 'BH Imóveis Savassi'
WHERE c.nome = 'Belo Horizonte';
