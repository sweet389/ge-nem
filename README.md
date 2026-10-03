# Frontend — Gerador de Simulados ENEM (Flask/Jinja)

Somente apresentação. **Toda a lógica (cálculos, validação, seleção de questões, correção, datas) fica no backend.**
Os templates só exibem o que recebem; o JS cuida apenas de interface (mostrar/ocultar campos, navegar entre questões, cronômetro).

## Estrutura
templates/ base, dashboard, gerar_simulado, simulado, resultado
static/    css/style.css, js/app.js

## Rotas usadas nos `url_for()`
GET  /                 dashboard
GET  /simulado/gerar   gerar_simulado   (exibe o formulário)
POST /simulado/gerar   gerar_simulado   (recebe o formulário)
GET  /simulado/<id>    simulado
GET  /api/simulados/<id>  JSON do simulado carregado pelo JavaScript
POST /simulado/finalizar  finalizar_simulado
GET  /resultado/<id>   resultado

## Variáveis que cada template espera

**dashboard.html**
- `subjects`: lista de `{name, accuracy, errors, change}`. Sem histórico: `accuracy=None`. Sem tentativa anterior: `change=None`
- `last_attempt`, `days_to_enem`, `enem_year`, `enem_dates_label`, `redacao_url`

**gerar_simulado.html** — nenhuma. Campos enviados no POST:
`ano`, `dia` (1|2), `modo` (estatisticas|limite), e só os do dia escolhido: `linguagens`, `humanas` | `natureza`, `matematica`

**simulado.html** — recebe `simulado_id` e `redacao_url`. O JavaScript busca as questões em `/api/simulados/<id>` e monta a prova na tela a partir do JSON gerado pelo backend.
POST enviado: `simulado_id`, `tempo_segundos`, `questao_<id>=<letra>` (questões em branco não são enviadas)

**resultado.html** — `resultado`: `{acertos, erros, total, percentual, materias:[{nome, acertos, erros, total, percentual}]}`

## Cuidados
- `q.enunciado|safe` assume HTML confiável; sanitize no backend se necessário
- Com Flask-WTF, descomente a linha `csrf_token` nos formulários
