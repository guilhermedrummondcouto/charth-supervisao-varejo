from __future__ import annotations

APP_NAME = "CHARTH – Supervisão Varejo"
DB_PATH = "charth_supervisao_v6.db"
UPLOAD_DIR = "uploads"

STORES = ["Cidade Jardim", "Vila da Serra", "Diamond", "Barigui"]

# Perfis
ROLE_ADMIN = "admin"
ROLE_SUPERVISORA = "supervisora"
ROLE_GESTORA = "gestora"
GESTORA_CAN_VIEW_ALL_STORES = True  # altere para False se quiser limitar cada gestora à própria loja

DEFAULT_USERS = [
    {"username": "admin", "password": "charth123", "role": ROLE_ADMIN, "store": None, "name": "Admin CHARTH"},
    {"username": "supervisora", "password": "charth123", "role": ROLE_SUPERVISORA, "store": None, "name": "Supervisora"},
    {"username": "gestora_cidade", "password": "charth123", "role": ROLE_GESTORA, "store": "Cidade Jardim", "name": "Gestora Cidade Jardim"},
    {"username": "gestora_vila", "password": "charth123", "role": ROLE_GESTORA, "store": "Vila da Serra", "name": "Gestora Vila da Serra"},
    {"username": "gestora_diamond", "password": "charth123", "role": ROLE_GESTORA, "store": "Diamond", "name": "Gestora Diamond"},
    {"username": "gestora_barigui", "password": "charth123", "role": ROLE_GESTORA, "store": "Barigui", "name": "Gestora Barigui"},
]

WEIGHTS = {
    "Equipe e Atendimento": 1,
    "Visual Merchandising": 1,
    "Estoque e Produto": 1,
    "Resultados e Indicadores": 2,
    "Experiência da Cliente": 1,
    "Gestão da Gerente": 2,
}

# Seções fora da média ponderada principal, mas mantidas no formulário e dashboard.
NON_WEIGHTED_SECTIONS = ["WhatsApp e Vendas Digitais", "Estrutura da Loja", "Experiência Premium"]

# Regras de bonificação configuráveis.
BONUS_CONFIG = {
    "silver_manager_value_option": 2000.0,  # briefing menciona 3700 ou 2000; altere aqui se optar por 3700.
    "bronze_manager_value_option": 2000.0,
    "gold_team_fund_percent": 0.01,
    "gold_sales_team_percent": 0.75,
    "gold_support_team_percent": 0.25,
    "gold_sales_equal_percent": 0.40,
    "gold_sales_individual_sales_percent": 0.60,
    "bronze_min_weighted_score": 7.50,  # critério não definido no briefing; mantido como constante explícita.
    "gold": {
        "min_weighted_score": 8.50,
        "min_results": 8.80,
        "min_management": 8.50,
        "min_block": 8.00,
        "requires_no_grave_disciplinary_issue": True,
    },
    "silver": {
        "min_weighted_score": 8.00,
        "min_results": 8.30,
        "min_management": 8.00,
        "min_block": 7.50,
        "manager_value": 2000.0,
    },
}

# Campos do formulário. type = score (1-10), binary (Sim=10/Não=0), note, text, select.
FORM_SECTIONS = [
    {
        "name": "Equipe e Atendimento",
        "observation_key": "observacoes_equipe_atendimento",
        "questions": [
            {"key": "postura_uniforme_apresentacao", "label": "Postura, uniforme e apresentação pessoal adequados?", "type": "score"},
            {"key": "atendimento_consultivo", "label": "Atendimento consultivo, escuta ativa e solução?", "type": "score"},
            {"key": "oferecem_look_completo", "label": "Oferecem look completo, venda adicional?", "type": "score"},
            {"key": "atendimento_personalizado", "label": "Atendimento personalizado, chama cliente pelo nome?", "type": "score"},
            {"key": "senso_de_dono", "label": "Time demonstra senso de dono?", "type": "score"},
            {"key": "equipe_engajada_salao", "label": "Equipe engajada no salão, energia ativa?", "type": "score"},
        ],
    },
    {
        "name": "Visual Merchandising",
        "observation_key": "observacoes_vm",
        "photo_key": "foto_vm",
        "questions": [
            {"key": "pecas_foco_evidenciadas", "label": "Peças foco da semana estão evidenciadas?", "type": "score"},
            {"key": "preco_visivel_sem_poluicao", "label": "Preço visível sem poluição visual?", "type": "score"},
            {"key": "iluminacao_valoriza_produtos", "label": "Iluminação valoriza os produtos?", "type": "score"},
            {"key": "manequins_bem_montados", "label": "Manequins bem montados, styling estratégico?", "type": "score"},
            {"key": "vitrine_gera_desejo", "label": "Vitrine gera desejo real?", "type": "score"},
            {"key": "pecas_passadas_repostas", "label": "As peças estão bem passadas e repostas?", "type": "score"},
        ],
    },
    {
        "name": "Estoque e Produto",
        "observation_key": "observacoes_estoque_produto",
        "questions": [
            {"key": "estoque_organizado_limpo", "label": "Estoque organizado e limpo?", "type": "score"},
            {"key": "reposicao_agil_salao", "label": "Reposição ágil no salão?", "type": "score"},
            {"key": "ruptura_best_sellers", "label": "Ruptura de best sellers?", "type": "score"},
            {"key": "pecas_defeito_separadas", "label": "Peças com defeito separadas corretamente?", "type": "score"},
            {"key": "estoque_remanejado_solicitacoes", "label": "Estoque foi remanejado com as solicitações?", "type": "score"},
        ],
    },
    {
        "name": "Resultados e Indicadores",
        "observation_key": "observacoes_resultados",
        "questions": [
            {"key": "time_conhece_meta_diaria", "label": "Time conhece a meta diária?", "type": "score"},
            {"key": "meta_semanal_acompanhada", "label": "Meta semanal é acompanhada diariamente?", "type": "score"},
            {"key": "gerente_plano_acao_abaixo_meta", "label": "Gerente apresenta plano de ação quando abaixo da meta?", "type": "score"},
            {"key": "ticket_medio_meta", "label": "Ticket médio está dentro da meta?", "type": "score"},
            {"key": "pa_meta", "label": "Produto por atendimento (PA) dentro da meta?", "type": "score"},
            {"key": "conversao_monitorada", "label": "Conversão é monitorada diariamente?", "type": "score"},
        ],
    },
    {
        "name": "Experiência da Cliente",
        "observation_key": "observacoes_experiencia_cliente",
        "questions": [
            {"key": "loja_limpa", "label": "Loja limpa, salão, provadores e caixa?", "type": "score"},
            {"key": "provadores_impecaveis", "label": "Provadores estão impecáveis?", "type": "score"},
            {"key": "cliente_sugestao_look", "label": "Cliente recebe sugestão de look completo?", "type": "score"},
            {"key": "embalagem_padrao_charth", "label": "Embalagem está alinhada ao padrão Charth?", "type": "score"},
            {"key": "posicionamento_muitocharth", "label": "A loja transmite posicionamento #MuitoCharth?", "type": "score"},
        ],
    },
    {
        "name": "WhatsApp e Vendas Digitais",
        "observation_key": "observacoes_whatsapp",
        "questions": [
            {"key": "responde_ate_10_min", "label": "Responde mensagens em até 10 minutos?", "type": "score"},
            {"key": "responsavel_turno_whatsapp", "label": "Existe responsável definido por turno?", "type": "score"},
            {"key": "conversas_organizadas", "label": "Conversas organizadas e acompanhadas?", "type": "score"},
            {"key": "fotos_padrao_charth", "label": "Fotos seguem padrão Charth?", "type": "score"},
            {"key": "busca_ativa_whatsapp", "label": "Busca ativa via WhatsApp?", "type": "score"},
            {"key": "novidades_semanais", "label": "Enviam novidades semanalmente?", "type": "score"},
            {"key": "pos_venda_whatsapp_24h", "label": "Pós-venda via WhatsApp em até 24h?", "type": "score"},
            {"key": "recupera_negociacoes", "label": "Recuperam negociações não fechadas?", "type": "score"},
        ],
    },
    {
        "name": "Gestão da Gerente",
        "observation_key": "observacoes_gestao_gerente",
        "questions": [
            {"key": "reuniao_diaria_registrada", "label": "Reunião diária realizada e registrada?", "type": "score"},
            {"key": "feedback_individual_mes", "label": "Feedback individual realizado no mês?", "type": "score"},
            {"key": "plano_acao_documentado", "label": "Plano de ação documentado?", "type": "score"},
            {"key": "escala_organizada", "label": "Escala organizada estrategicamente?", "type": "score"},
            {"key": "lideranca_inspira", "label": "Liderança inspira respeito e resultado?", "type": "score"},
            {"key": "gerente_acompanha_vendas", "label": "Gerente acompanha vendas no salão?", "type": "score"},
            {"key": "amostragem_livro_fiscal", "label": "Amostragem de lançamento do livro fiscal está correta?", "type": "binary"},
        ],
    },
    {
        "name": "Estrutura da Loja",
        "observation_key": "observacoes_estrutura_loja",
        "questions": [
            {"key": "lampadas_queimadas", "label": "Existem lâmpadas queimadas?", "type": "binary_inverse"},
            {"key": "moveis_equipamentos_danificados", "label": "Existem móveis ou equipamentos quebrados/danificados?", "type": "binary_inverse"},
            {"key": "pintura_acabamentos_conservados", "label": "Pintura e acabamentos conservados?", "type": "binary"},
            {"key": "ar_condicionado_funcionando", "label": "Ar-condicionado funcionando?", "type": "binary"},
            {"key": "som_ambiente_adequado", "label": "Som ambiente adequado?", "type": "binary"},
            {"key": "fachada_limpa_cuidada", "label": "Fachada limpa e bem cuidada?", "type": "binary"},
            {"key": "comunicacao_visual_sem_danos", "label": "Comunicação visual sem danos?", "type": "score"},
            {"key": "loucas_personalizadas_perfeitas", "label": "Louças personalizadas em perfeito estado?", "type": "binary"},
            {"key": "mascaras_provadores", "label": "Há máscaras em todos os provadores?", "type": "binary"},
        ],
    },
    {
        "name": "Experiência Premium",
        "observation_key": "observacoes_experiencia_premium",
        "questions": [
            {"key": "bala_charth_disponivel", "label": "Bala Charth disponível?", "type": "binary"},
            {"key": "brigadeiro_charth_disponivel", "label": "Brigadeiro Charth disponível?", "type": "binary"},
            {"key": "bebidas_personalizadas_disponiveis", "label": "Bebidas personalizadas disponíveis?", "type": "binary"},
            {"key": "personalizados_armazenados", "label": "Personalizados armazenados corretamente?", "type": "binary"},
            {"key": "itens_oferecidos_ativamente", "label": "Itens oferecidos ativamente?", "type": "score"},
            {"key": "servico_elegancia", "label": "Serviço com elegância, bandeja ou apresentação?", "type": "binary"},
            {"key": "experiencia_exclusividade", "label": "Experiência transmite exclusividade?", "type": "binary"},
            {"key": "insumos_adequados", "label": "Todos os insumos adequados?", "type": "binary"},
        ],
    },
]

STRATEGIC_FIELDS = [
    {"key": "maior_risco", "label": "Maior risco da loja hoje"},
    {"key": "maior_oportunidade", "label": "Maior oportunidade de crescimento imediato"},
    {"key": "virar_ouro", "label": "O que precisa acontecer para virar Ouro"},
]
DNA_OPTIONS = ["Totalmente", "Parcialmente", "Não"]

# -----------------------------------------------------------------------------
# Bonificação trimestral - regra executiva CHARTH
# Mantém a regra antiga configurável e separa o cálculo trimestral do cálculo da avaliação.
# Ajuste aqui se a diretoria decidir trocar valores ou critérios.
# -----------------------------------------------------------------------------
BONUS_RULES = {
    "quarterly_manager_values": {
        "Ouro": 5000.0,
        "Prata": 3700.0,
        "Bronze": 2000.0,
        "Sem bônus": 0.0,
    },
    "consecutive_gold_extra": {
        1: 0.0,
        2: 1000.0,
        3: 2000.0,
        4: 3000.0,
    },
    "gold_strict": {
        "min_weighted_score": 8.8,
        "min_results": 9.0,
        "min_management": 8.5,
        "min_block": 8.0,
        "requires_no_grave_disciplinary_issue": True,
    },
    "gold_standard": {
        "min_weighted_score": 8.5,
        "min_results": 8.8,
        "min_management": 8.5,
        "min_block": 8.0,
        "requires_no_grave_disciplinary_issue": True,
    },
    "silver": {
        "min_weighted_score": 8.0,
        "min_results": 8.3,
        "min_management": 8.0,
        "min_block": 7.5,
    },
    "bronze": {
        "min_weighted_score": 7.5,
        "min_block": 7.0,
    },
    # Regra padrão selecionada no menu Bonificação.
    # Opções: "gold_strict" ou "gold_standard".
    "default_gold_rule": "gold_strict",
    # Escopo da menor nota de bloco para elegibilidade.
    # "all_sections" = considera todas as seções avaliativas.
    # "weighted_sections" = considera apenas Equipe, VM, Estoque, Resultado, Experiência e Gestão.
    "min_block_scope": "all_sections",
    "team_fund_percent": 0.01,
    "team_sales_percent": 0.75,
    "team_support_percent": 0.25,
}
