# 🏠 Dashboard de Inteligência Imobiliária - SETUP

## ✅ Checklist de Configuração

### Fase 1: Configurar Supabase

1. **Criar projeto Supabase** (se não tiver)
   - Acesse: https://supabase.com
   - Crie novo projeto
   - Copie `SUPABASE_URL` e `SUPABASE_ANON_KEY`

2. **Executar SQL no Editor do Supabase**
   ```bash
   # Abrir Supabase SQL Editor
   # Copiar conteúdo de: sql/00_schema.sql
   # Colar e executar

   # Depois executar: sql/01_views.sql
   # Depois executar: data/seeds/*.sql (em ordem)
   ```

3. **Atualizar .env**
   ```bash
   SUPABASE_URL=https://seu-projeto.supabase.co
   SUPABASE_ANON_KEY=sua-anon-key
   MAPBOX_TOKEN=seu-token-mapbox  # Opcional
   ```

### Fase 2: Instalar Dependências

```bash
# 1. Criar ambiente virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Verificar instalação
pip list | grep streamlit
```

### Fase 3: Executar Dashboard

```bash
# Comando para iniciar
streamlit run app.py

# Ou com configurações específicas
streamlit run app.py --logger.level=debug
```

A aplicação abrirá em: **http://localhost:8501**

---

## 📋 Estrutura de Arquivos Criada

```
inteligencia-imobiliaria/
├── requirements.txt              # Dependências Python
├── app.py                        # Home page (MAIN)
├── config/
│   ├── __init__.py
│   └── settings.py               # Configurações (lê .env)
├── services/                     # Lógica de dados
│   ├── __init__.py
│   ├── supabase_client.py        # Cliente Supabase @st.cache_resource
│   ├── imobiliarias_service.py
│   ├── imoveis_service.py
│   ├── bairros_service.py
│   ├── investidores_service.py
│   └── prospeccao_service.py
├── components/                   # Componentes reutilizáveis
│   ├── __init__.py
│   ├── filtros_globais.py        # Sidebar com filtros
│   ├── metricas_header.py        # KPIs no header
│   └── tabela_exportavel.py      # Tabelas com export
├── utils/                        # Funções utilitárias
│   ├── __init__.py
│   ├── session_state.py          # Gerência de filtros
│   ├── formatters.py             # Formatação de dados
│   └── map_helpers.py            # Helpers para mapas
├── pages/                        # Páginas multipage Streamlit
│   ├── 1_Mapa_Imobiliarias.py
│   ├── 2_Marketing_Fraco.py
│   ├── 3_Novos_Empreendimentos.py
│   ├── 4_Investidores.py
│   ├── 5_Ranking_Bairros.py
│   └── 6_Prospeccao.py
├── sql/                          # Scripts SQL
│   ├── 00_schema.sql             # Schema + RLS
│   └── 01_views.sql              # Views calculadas
└── data/seeds/                   # Dados mock
    ├── 01_cidades.sql
    ├── 02_bairros.sql
    ├── 03_imobiliarias.sql
    ├── 04_imoveis.sql
    ├── 05_imoveis_fotos.sql
    ├── 06_investidores.sql
    └── 07_oportunidades.sql
```

---

## 🔐 Variáveis de Ambiente (.env)

```bash
# Supabase (OBRIGATÓRIO)
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_ANON_KEY=sua-chave-anon
SUPABASE_SERVICE_ROLE_KEY=sua-service-role-key

# Mapbox (OPCIONAL - necessário para mapas)
MAPBOX_TOKEN=pk.seu-token-mapbox

# Debug (OPCIONAL)
DEBUG=False
```

---

## 🧪 Teste da Aplicação

### 1. Home Page
```bash
streamlit run app.py
```
✅ Deve mostrar:
- Health check do Supabase
- Contagem: X cidades, Y bairros, Z imóveis
- Cards com as 6 seções

### 2. Sidebar de Filtros
✅ Deve aparecer em TODAS as páginas:
- Seletor de Cidade
- Seletor de Bairro (depende de cidade)
- Slider de Faixa de Preço
- Slider de Score de Marketing
- Multiselect de Status

### 3. Página 1: Mapa
```
Acessar: http://localhost:8501/1_Mapa_Imobiliarias
✅ Deve exibir:
- Mapa com pontos das imobiliárias
- Pontos coloridos por score (vermelho → amarelo → verde)
- Tabela com dados das imobiliárias
```

### 4. Página 5: Ranking
```
Acessar: http://localhost:8501/5_Ranking_Bairros
✅ Deve exibir:
- Top 3 bairros (🥇🥈🥉)
- Gráfico de barras com ranking
- Tabela detalhada com scores
```

### 5. Página 2: Marketing Fraco
```
Acessar: http://localhost:8501/2_Marketing_Fraco
✅ Deve exibir:
- Imóveis com score_fraqueza_marketing > 40
- Tabela com fotos, vídeo, descrição
```

### 6. Página 3: Empreendimentos
```
Acessar: http://localhost:8501/3_Novos_Empreendimentos
✅ Deve exibir:
- Abas por estágio: projeto, fundações, estrutura, acabamento, pronto
- Cards com detalhes de cada empreendimento
```

### 7. Página 4: Investidores
```
Acessar: http://localhost:8501/4_Investidores
✅ Deve exibir:
- Top 3 investidores (🥇🥈🥉)
- Gráfico de dispersão: Valor vs Quantidade
- Tabela com investidores
- Expandir para ver imóveis por investidor
```

### 8. Página 6: Prospecção
```
Acessar: http://localhost:8501/6_Prospeccao
✅ Deve exibir:
- KPIs: Total, Qualificado, Fechado, Taxa Conversão
- Gráfico de pizza com distribuição por status
- Tabela de oportunidades
- Próximas ações (7 dias)
```

---

## 🚀 Próximos Passos (Melhorias)

### Curto Prazo (Essencial)
- [ ] Adicionar autenticação de usuário (Supabase Auth)
- [ ] Implementar atualização de status em Prospecção
- [ ] Mapear cidade/bairro selecionados para IDs UUID

### Médio Prazo (Importante)
- [ ] Dashboard de performance (vendas, receita)
- [ ] Gráficos de tendências históricas
- [ ] Exportação de relatórios em PDF
- [ ] Notificações de ações urgentes

### Longo Prazo (Melhorias)
- [ ] Machine Learning para predição de preços
- [ ] Integração com APIs de terceiros
- [ ] App mobile (React Native)
- [ ] Analytics e rastreamento de cliques

---

## 🐛 Troubleshooting

### Erro: "SUPABASE_URL não configurada"
```bash
✅ Solução: Adicionar variáveis ao .env
```

### Erro: "Nenhuma imobiliária encontrada"
```bash
✅ Solução: Executar data/seeds/*.sql no Supabase SQL Editor
```

### Erro: "Mapa não carrega"
```bash
✅ Solução: Adicionar MAPBOX_TOKEN ao .env (mapas são opcionais)
```

### Erro: "ModuleNotFoundError: streamlit"
```bash
✅ Solução: pip install -r requirements.txt
```

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verificar logs do Streamlit (terminal)
2. Consultar Supabase Dashboard para erros de RLS
3. Validar credenciais no .env

---

**Desenvolvido com ❤️ usando Synkra AIOS Framework**
