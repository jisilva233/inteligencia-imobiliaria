-- ============================================
-- Seed: Oportunidades de Prospecção
-- ============================================

INSERT INTO oportunidades_prospeccao (
  cidade_id, imobiliaria_id, tipo_lead, status, contato_nome, contato_email,
  contato_telefone, score_qualificacao, notas
)
SELECT
  c.id,
  (SELECT id FROM imobiliarias WHERE nome = 'Remax Premium SP' AND cidade_id = c.id LIMIT 1),
  'lead_frio',
  'qualificado',
  'João Pereira Teixeira',
  'joao@empresa.com.br',
  '(11) 98888-7777',
  7.5,
  'Interessado em imóvel para investimento em Pinheiros'
FROM cidades c WHERE c.nome = 'São Paulo'
UNION ALL
SELECT
  c.id,
  (SELECT id FROM imobiliarias WHERE nome = 'Remax Premium SP' AND cidade_id = c.id LIMIT 1),
  'qualificado',
  'em_contato',
  'Marina Silva Costa',
  'marina@email.com.br',
  '(11) 99999-1111',
  8.2,
  'Enviada proposta para imóvel Vila Olímpia'
FROM cidades c WHERE c.nome = 'São Paulo'
UNION ALL
SELECT
  c.id,
  (SELECT id FROM imobiliarias WHERE nome = 'Imobiliária São Paulo Plus' AND cidade_id = c.id LIMIT 1),
  'qualificado',
  'proposta_enviada',
  'Ricardo Gomes',
  'ricardo@business.com.br',
  '(11) 97777-5555',
  8.8,
  'Proposta de Mooca - aguardando resposta'
FROM cidades c WHERE c.nome = 'São Paulo'
UNION ALL
SELECT
  c.id,
  (SELECT id FROM imobiliarias WHERE nome = 'RJ Imóveis Copacabana' AND cidade_id = c.id LIMIT 1),
  'qualificado',
  'em_contato',
  'Ana Paula Rocha',
  'ana.paula@email.com.br',
  '(21) 98888-2222',
  7.8,
  'Interesse em Copacabana - visitará a propriedade na próxima semana'
FROM cidades c WHERE c.nome = 'Rio de Janeiro'
UNION ALL
SELECT
  c.id,
  (SELECT id FROM imobiliarias WHERE nome = 'Praia Empreendimentos' AND cidade_id = c.id LIMIT 1),
  'qualificado',
  'fechado',
  'Patricia Mendes',
  'patricia@empresa.com.br',
  '(21) 99555-1111',
  9.5,
  'Contrato assinado para Ipanema em fevereiro/2026'
FROM cidades c WHERE c.nome = 'Rio de Janeiro'
UNION ALL
SELECT
  c.id,
  (SELECT id FROM imobiliarias WHERE nome = 'BH Imóveis Savassi' AND cidade_id = c.id LIMIT 1),
  'lead_frio',
  'qualificado',
  'Marcelo Tavares',
  'marcelo.tavares@email.com.br',
  '(31) 98888-5555',
  6.5,
  'Lead novo - investigar interesse real'
FROM cidades c WHERE c.nome = 'Belo Horizonte'
ON CONFLICT DO NOTHING;
