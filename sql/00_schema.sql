-- ============================================
-- Dashboard de Inteligência Imobiliária
-- Schema Completo com RLS
-- ============================================

-- Extensões requeridas
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";

-- ============================================
-- 1. TABELA: cidades
-- ============================================
CREATE TABLE IF NOT EXISTS cidades (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  nome VARCHAR(255) NOT NULL UNIQUE,
  estado VARCHAR(2) NOT NULL,
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================
-- 2. TABELA: bairros
-- ============================================
CREATE TABLE IF NOT EXISTS bairros (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  cidade_id UUID NOT NULL REFERENCES cidades(id) ON DELETE CASCADE,
  nome VARCHAR(255) NOT NULL,
  score_valorizacao NUMERIC(5, 2) DEFAULT 5.0, -- 0-10
  score_demanda NUMERIC(5, 2) DEFAULT 5.0,      -- 0-10
  score_oferta NUMERIC(5, 2) DEFAULT 5.0,       -- 0-10
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(cidade_id, nome)
);

CREATE INDEX IF NOT EXISTS idx_bairros_cidade ON bairros(cidade_id);

-- ============================================
-- 3. TABELA: imobiliarias
-- ============================================
CREATE TABLE IF NOT EXISTS imobiliarias (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  cidade_id UUID NOT NULL REFERENCES cidades(id) ON DELETE CASCADE,
  nome VARCHAR(255) NOT NULL,
  latitude DECIMAL(10, 8) NOT NULL,
  longitude DECIMAL(11, 8) NOT NULL,
  email VARCHAR(255),
  telefone VARCHAR(20),
  qtd_imoveis_anunciados INT DEFAULT 0,
  score_oportunidade NUMERIC(5, 2) DEFAULT 5.0, -- 0-10
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_imobiliarias_cidade ON imobiliarias(cidade_id);
CREATE INDEX IF NOT EXISTS idx_imobiliarias_lat_lon ON imobiliarias(latitude, longitude);

-- ============================================
-- 4. TABELA: imoveis
-- ============================================
CREATE TABLE IF NOT EXISTS imoveis (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  cidade_id UUID NOT NULL REFERENCES cidades(id) ON DELETE CASCADE,
  bairro_id UUID NOT NULL REFERENCES bairros(id) ON DELETE CASCADE,
  imobiliaria_id UUID REFERENCES imobiliarias(id) ON DELETE SET NULL,
  endereco TEXT NOT NULL,
  preco NUMERIC(15, 2) NOT NULL,
  area_m2 NUMERIC(10, 2),
  quartos INT,
  banheiros INT,
  estacionamentos INT,

  -- Marketing fields
  qtd_fotos INT DEFAULT 0,
  tem_video BOOLEAN DEFAULT FALSE,
  tem_tour_virtual BOOLEAN DEFAULT FALSE,
  descricao_marketing TEXT,
  score_fraqueza_marketing NUMERIC(5, 2) DEFAULT 0, -- 0-100: quanto maior, pior o marketing

  -- Empreendimento fields
  tipo_empreendimento VARCHAR(50), -- 'projeto', 'fundações', 'estrutura', 'acabamento', 'pronto'
  em_construcao BOOLEAN DEFAULT FALSE,
  percentual_conclusao INT DEFAULT 0,
  data_lancamento DATE,

  -- Localização geográfica
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_imoveis_cidade ON imoveis(cidade_id);
CREATE INDEX IF NOT EXISTS idx_imoveis_bairro ON imoveis(bairro_id);
CREATE INDEX IF NOT EXISTS idx_imoveis_imobiliaria ON imoveis(imobiliaria_id);
CREATE INDEX IF NOT EXISTS idx_imoveis_preco ON imoveis(preco);
CREATE INDEX IF NOT EXISTS idx_imoveis_marketing_fraco ON imoveis(score_fraqueza_marketing)
  WHERE score_fraqueza_marketing > 40;

-- ============================================
-- 5. TABELA: imoveis_fotos
-- ============================================
CREATE TABLE IF NOT EXISTS imoveis_fotos (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  imovel_id UUID NOT NULL REFERENCES imoveis(id) ON DELETE CASCADE,
  url_foto TEXT NOT NULL,
  descricao VARCHAR(255),
  ordem INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_imoveis_fotos_imovel ON imoveis_fotos(imovel_id);

-- ============================================
-- 6. TABELA: investidores_detectados
-- ============================================
CREATE TABLE IF NOT EXISTS investidores_detectados (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  cidade_id UUID REFERENCES cidades(id) ON DELETE CASCADE,
  nome VARCHAR(255) NOT NULL,
  email VARCHAR(255),
  telefone VARCHAR(20),
  qtd_imoveis INT DEFAULT 0,
  valor_total_investido NUMERIC(15, 2) DEFAULT 0,
  bairro_preferido VARCHAR(255),
  tipo_propriedade_preferida VARCHAR(100), -- 'residencial', 'comercial', 'misto'
  criado_em TIMESTAMP DEFAULT NOW(),
  UNIQUE(email)
);

CREATE INDEX IF NOT EXISTS idx_investidores_cidade ON investidores_detectados(cidade_id);
CREATE INDEX IF NOT EXISTS idx_investidores_qtd_imoveis ON investidores_detectados(qtd_imoveis) DESC;

-- ============================================
-- 7. TABELA: investidores_imoveis
-- ============================================
CREATE TABLE IF NOT EXISTS investidores_imoveis (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  investidor_id UUID NOT NULL REFERENCES investidores_detectados(id) ON DELETE CASCADE,
  imovel_id UUID NOT NULL REFERENCES imoveis(id) ON DELETE CASCADE,
  data_compra DATE,
  preco_compra NUMERIC(15, 2),
  UNIQUE(investidor_id, imovel_id)
);

CREATE INDEX IF NOT EXISTS idx_investidores_imoveis_investidor ON investidores_imoveis(investidor_id);
CREATE INDEX IF NOT EXISTS idx_investidores_imoveis_imovel ON investidores_imoveis(imovel_id);

-- ============================================
-- 8. TABELA: oportunidades_prospeccao
-- ============================================
CREATE TABLE IF NOT EXISTS oportunidades_prospeccao (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  cidade_id UUID REFERENCES cidades(id) ON DELETE CASCADE,
  imobiliaria_id UUID REFERENCES imobiliarias(id) ON DELETE SET NULL,
  imovel_id UUID REFERENCES imoveis(id) ON DELETE SET NULL,
  tipo_lead VARCHAR(100), -- 'lead_frio', 'qualificado', 'proximo'
  status VARCHAR(50) DEFAULT 'lead_frio', -- 'lead_frio', 'qualificado', 'em_contato', 'proposta_enviada', 'fechado'
  contato_nome VARCHAR(255),
  contato_email VARCHAR(255),
  contato_telefone VARCHAR(20),
  data_deteccao TIMESTAMP DEFAULT NOW(),
  data_proxima_acao DATE,
  notas TEXT,
  score_qualificacao NUMERIC(5, 2) DEFAULT 0, -- 0-10
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_oportunidades_cidade ON oportunidades_prospeccao(cidade_id);
CREATE INDEX IF NOT EXISTS idx_oportunidades_status ON oportunidades_prospeccao(status);
CREATE INDEX IF NOT EXISTS idx_oportunidades_imobiliaria ON oportunidades_prospeccao(imobiliaria_id);

-- ============================================
-- RLS (Row Level Security)
-- ============================================

-- Habilitar RLS em todas as tabelas
ALTER TABLE cidades ENABLE ROW LEVEL SECURITY;
ALTER TABLE bairros ENABLE ROW LEVEL SECURITY;
ALTER TABLE imobiliarias ENABLE ROW LEVEL SECURITY;
ALTER TABLE imoveis ENABLE ROW LEVEL SECURITY;
ALTER TABLE imoveis_fotos ENABLE ROW LEVEL SECURITY;
ALTER TABLE investidores_detectados ENABLE ROW LEVEL SECURITY;
ALTER TABLE investidores_imoveis ENABLE ROW LEVEL SECURITY;
ALTER TABLE oportunidades_prospeccao ENABLE ROW LEVEL SECURITY;

-- Políticas de leitura pública (SELECT)
CREATE POLICY "cidades_select_public" ON cidades
  FOR SELECT
  USING (true);

CREATE POLICY "bairros_select_public" ON bairros
  FOR SELECT
  USING (true);

CREATE POLICY "imobiliarias_select_public" ON imobiliarias
  FOR SELECT
  USING (true);

CREATE POLICY "imoveis_select_public" ON imoveis
  FOR SELECT
  USING (true);

CREATE POLICY "imoveis_fotos_select_public" ON imoveis_fotos
  FOR SELECT
  USING (true);

CREATE POLICY "investidores_select_public" ON investidores_detectados
  FOR SELECT
  USING (true);

CREATE POLICY "investidores_imoveis_select_public" ON investidores_imoveis
  FOR SELECT
  USING (true);

CREATE POLICY "oportunidades_select_public" ON oportunidades_prospeccao
  FOR SELECT
  USING (true);

-- Políticas de escrita (INSERT/UPDATE/DELETE) apenas para service_role
CREATE POLICY "cidades_write_service" ON cidades
  FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "bairros_write_service" ON bairros
  FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "imobiliarias_write_service" ON imobiliarias
  FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "imoveis_write_service" ON imoveis
  FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "imoveis_fotos_write_service" ON imoveis_fotos
  FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "investidores_write_service" ON investidores_detectados
  FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "investidores_imoveis_write_service" ON investidores_imoveis
  FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

CREATE POLICY "oportunidades_write_service" ON oportunidades_prospeccao
  FOR ALL
  USING (auth.role() = 'service_role')
  WITH CHECK (auth.role() = 'service_role');

-- Índices para otimização de queries comuns
CREATE INDEX IF NOT EXISTS idx_imoveis_em_construcao
  ON imoveis(tipo_empreendimento)
  WHERE em_construcao = TRUE;

CREATE INDEX IF NOT EXISTS idx_imoveis_bairro_preco
  ON imoveis(bairro_id, preco);
