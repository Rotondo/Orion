# Projeto Órion - Protótipo MVP

Sistema Inteligente de Orquestração de Ecossistema de E-commerce

## 🎯 Visão Geral

O Projeto Órion é uma solução inovadora que transforma plataformas de e-commerce de meros provedores de infraestrutura em **orquestradores inteligentes de ecossistema**. Através de uma rede de agentes autônomos e motores de inteligência preditiva, o sistema otimiza proativamente a jornada de cada lojista.

## 🏗️ Arquitetura

### Componentes Principais

1. **DNA da Loja**: Modelo de dados que captura o perfil único de cada loja
2. **Sistema de Scoring**: Calcula compatibilidade e rentabilidade de recomendações
3. **Agentes Autônomos**: Rede de agentes especializados que analisam e recomendam
4. **Motor de Recomendações**: Gera sugestões personalizadas para cada loja
5. **Orquestrador Central**: Coordena todos os componentes do sistema

### Agentes Disponíveis

- **Agente Mestre da Loja**: Orquestrador central para cada loja
- **Agentes Especialistas**: Focados em áreas específicas da "Espinha de Peixe"
- **Agentes de Parceiros**: Representam conhecimento sobre soluções de parceiros
- **Agente de Inteligência de Mercado**: Analisa tendências e oportunidades

## 🚀 Como Executar

### Pré-requisitos

- Python 3.11+
- pip ou poetry

### Instalação Local

```bash
# Clone o repositório
cd orion_prototype

# Instale dependências
pip install -r requirements.txt

# Execute a API
python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
```

### Usando Docker

```bash
# Build da imagem
docker build -t orion-prototype .

# Execute o container
docker run -p 8000:8000 orion-prototype

# Ou use docker-compose
docker-compose up
```

### Acesso à API

- **API**: http://localhost:8000
- **Documentação**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📊 Exemplo de Uso

### 1. Popular Dados de Exemplo

```bash
curl -X POST "http://localhost:8000/seed-data"
```

### 2. Criar Nova Loja

```bash
curl -X POST "http://localhost:8000/stores" \
  -H "Content-Type: application/json" \
  -d '{
    "store_id": "minha_loja_001",
    "name": "Minha Loja de Roupas",
    "segment": "fashion",
    "size": "pequena",
    "monthly_revenue": 20000,
    "monthly_orders": 150,
    "conversion_rate": 0.025
  }'
```

### 3. Obter Recomendações

```bash
curl "http://localhost:8000/stores/minha_loja_001/recommendations"
```

### 4. Análise Completa da Loja

```bash
curl "http://localhost:8000/stores/minha_loja_001/analysis"
```

### 5. Dashboard do Ecossistema

```bash
curl "http://localhost:8000/ecosystem/dashboard"
```

## 🧪 Executando Testes

```bash
# Execute todos os testes
python -m pytest tests/ -v

# Execute testes específicos
python -m pytest tests/test_core.py::TestDNAService -v

# Com coverage
pip install pytest-cov
python -m pytest tests/ --cov=. --cov-report=html
```

## 📋 Endpoints da API

### Lojas
- `POST /stores` - Criar loja
- `GET /stores/{store_id}` - Obter loja
- `GET /stores/{store_id}/analysis` - Análise completa
- `GET /stores/{store_id}/recommendations` - Recomendações
- `GET /stores/{store_id}/gaps` - Identificar gaps

### Parceiros
- `POST /partners` - Criar parceiro
- `GET /partners/{partner_id}/analysis` - Análise do parceiro

### Ecossistema
- `GET /ecosystem/dashboard` - Dashboard geral
- `GET /market/opportunities` - Oportunidades de mercado

### Utilidades
- `GET /enums` - Enums disponíveis
- `POST /seed-data` - Popular dados de exemplo

## 🎨 Espinha de Peixe - Jornada do E-commerce

O sistema organiza soluções em 12 etapas principais:

1. **Atração & Marketing Digital**
2. **Infraestrutura & Plataformas**
3. **Navegação & Descoberta**
4. **Página de Produto & Conteúdo Rico**
5. **Carrinho & Checkout**
6. **Pós-Pagamento & Fulfillment**
7. **Entrega & Last Mile**
8. **Pós-Venda & Relacionamento**
9. **Analytics & Inteligência de Dados**
10. **Governança, Jurídico & Compliance**
11. **Modelos de Negócio Específicos**
12. **Talentos & Desenvolvimento Humano**

## 🔮 Funcionalidades Demonstradas

### ✅ Implementado no MVP

- [x] Sistema de DNA da Loja
- [x] Algoritmos de Scoring (Compatibilidade + Rentabilidade)
- [x] Rede de Agentes Autônomos
- [x] Motor de Recomendações Personalizadas
- [x] API REST completa
- [x] Análise de Gaps e Maturidade
- [x] Dashboard do Ecossistema
- [x] Dados de exemplo para demonstração

### 🚧 Próximas Implementações

- [ ] Interface Web (Frontend React/Vue)
- [ ] Sistema de Webhooks e Eventos
- [ ] Machine Learning para Scoring
- [ ] Integração com APIs de Parceiros
- [ ] Sistema de Notificações
- [ ] Analytics Avançados
- [ ] Banco de dados persistente

## 📊 Exemplo de Resultado

```json
{
  "success": true,
  "data": {
    "store_id": "loja_fashion_001",
    "current_recommendations": [
      {
        "partner_id": "partner_checkout_003",
        "final_score": 0.85,
        "priority": 1,
        "reasoning": [
          "Forte compatibilidade com segmento da loja",
          "Alto potencial de receita para a plataforma", 
          "Resolve pain points identificados"
        ],
        "estimated_roi": 90,
        "implementation_timeline": "2-4 semanas"
      }
    ]
  }
}
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🙋‍♂️ Suporte

Para dúvidas ou suporte, abra uma issue no repositório ou entre em contato.

---

**Projeto Órion** - Orquestrando o futuro do e-commerce inteligente 🚀
