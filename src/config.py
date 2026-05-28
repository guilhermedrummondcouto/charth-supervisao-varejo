from __future__ import annotations

APP_NAME = "CHARTH – Supervisão Varejo"
DB_PATH = "charth_supervisao_v6.db"
UPLOAD_DIR = "uploads"

STORES = ["Cidade Jardim", "Vila da Serra", "Diamond", "Barigui"]
MANAGERS = ["Natasha", "Jéssica", "Ingrid", "Fernanda"]

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

# Média ponderada principal.
# Experiência da Cliente e Experiência Premium foram unificadas em uma seção única.
WEIGHTS = {
    "Equipe e Atendimento": 1,
    "Visual Merchandising": 1,
    "Estoque e Produto": 1,
    "Resultados e Indicadores": 2,
    "Experiência da Cliente e Padrão Premium": 1,
    "Gestão da Gerente": 2,
}

# Seções fora da média ponderada principal, mas mantidas no formulário e dashboard.
NON_WEIGHTED_SECTIONS = ["WhatsApp e Vendas Digitais", "Estrutura da Loja"]

# Regras de bonificação configuráveis.
BONUS_CONFIG = {
    "silver_manager_value_option": 2000.0,
    "bronze_manager_value_option": 2000.0,
    "gold_team_fund_percent": 0.01,
    "gold_sales_team_percent": 0.75,
    "gold_support_team_percent": 0.25,
    "gold_sales_equal_percent": 0.40,
    "gold_sales_individual_sales_percent": 0.60,
    "bronze_min_weighted_score": 7.50,
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

# Campos do formulário. type = score (1-10), binary (Sim=10/Não=0), binary_inverse (Não=10/Sim=0).
FORM_SECTIONS = [
    {
        "name": "Equipe e Atendimento",
        "observation_key": "observacoes_equipe_atendimento",
        "questions": [
            {"key": "postura_uniforme_apresentacao", "label": "A equipe está com postura, uniforme e apresentação pessoal adequados?", "type": "score"},
            {"key": "atendimento_consultivo", "label": "A equipe pratica atendimento consultivo, com escuta ativa e solução?", "type": "score"},
            {"key": "oferecem_look_completo", "label": "A equipe oferece look completo, estimulando venda adicional?", "type": "score"},
            {"key": "atendimento_personalizado", "label": "A equipe realiza atendimento personalizado, chamando a cliente pelo nome?", "type": "score"},
            {"key": "senso_de_dono", "label": "A equipe demonstra senso de dono na rotina da loja?", "type": "score"},
            {"key": "equipe_engajada_salao", "label": "A equipe está engajada no salão, com energia ativa?", "type": "score"},
            {"key": "clima_organizacional", "label": "O clima entre a equipe favorece colaboração, respeito e boa convivência?", "type": "score"},
        ],
    },
    {
        "name": "Visual Merchandising",
        "observation_key": "observacoes_vm",
        "photo_key": "foto_vm",
        "questions": [
            {"key": "pecas_semana_evidenciadas", "label": "As peças da semana estão evidenciadas?", "type": "binary"},
            {"key": "preco_visivel_sem_poluicao", "label": "Os preços estão visíveis, sem poluição visual?", "type": "binary"},
            {"key": "manequins_bem_montados", "label": "Os manequins estão bem montados, com styling estratégico?", "type": "binary"},
            {"key": "vitrine_gera_desejo", "label": "A vitrine gera desejo real de compra?", "type": "binary"},
            {"key": "pecas_passadas_repostas", "label": "As peças estão bem passadas e repostas?", "type": "binary"},
            {"key": "araras_penteadas", "label": "As araras estão penteadas?", "type": "binary"},
        ],
    },
    {
        "name": "Estoque e Produto",
        "observation_key": "observacoes_estoque_produto",
        "photo_key": "foto_estoque_produto",
        "questions": [
            {"key": "estoque_organizado_limpo", "label": "O estoque está organizado e limpo?", "type": "binary"},
            {"key": "reposicao_agil_salao", "label": "A reposição no salão está sendo feita com agilidade?", "type": "binary"},
            {"key": "ruptura_best_sellers", "label": "A loja está sem ruptura de best sellers?", "type": "binary"},
            {"key": "pecas_defeito_separadas", "label": "As peças com defeito estão separadas corretamente?", "type": "binary"},
            {"key": "transferencias_solicitadas_em_dia", "label": "As transferências solicitadas estão em dia?", "type": "binary"},
        ],
    },
    {
        "name": "Resultados e Indicadores",
        "observation_key": "observacoes_resultados",
        "questions": [
            {"key": "time_conhece_meta_diaria", "label": "A equipe conhece a meta diária?", "type": "binary"},
            {"key": "meta_semanal_acompanhada", "label": "A meta semanal é acompanhada diariamente?", "type": "binary"},
            {"key": "gerente_plano_acao_abaixo_meta", "label": "A gerente apresenta plano de ação quando a loja está abaixo da meta?", "type": "binary"},
            {"key": "ticket_medio_meta", "label": "O ticket médio está dentro da meta?", "type": "binary"},
            {"key": "pa_meta", "label": "O produto por atendimento (PA) está dentro da meta?", "type": "binary"},
            {"key": "conversao_monitorada", "label": "A conversão é monitorada diariamente?", "type": "binary"},
        ],
    },
    {
        "name": "Experiência da Cliente e Padrão Premium",
        "observation_key": "observacoes_experiencia_cliente_premium",
        "questions": [
            {"key": "loja_limpa", "label": "A loja está limpa, incluindo salão, provadores e caixa?", "type": "binary"},
            {"key": "provadores_impecaveis", "label": "Os provadores estão impecáveis?", "type": "binary"},
            {"key": "cliente_sugestao_look", "label": "A cliente recebe sugestão de look completo?", "type": "binary"},
            {"key": "cliente_sugestao_variedade_cor", "label": "A cliente recebe sugestão de variedade de cor?", "type": "binary"},
            {"key": "embalagem_padrao_charth", "label": "A embalagem está alinhada ao padrão Charth?", "type": "binary"},
            {"key": "bala_charth_disponivel", "label": "A bala Charth está disponível?", "type": "binary"},
            {"key": "brigadeiro_charth_disponivel", "label": "O brigadeiro Charth está disponível?", "type": "binary"},
            {"key": "bebidas_personalizadas_disponiveis", "label": "As bebidas personalizadas estão disponíveis?", "type": "binary"},
            {"key": "personalizados_armazenados", "label": "Os personalizados estão armazenados corretamente?", "type": "binary"},
            {"key": "itens_oferecidos_ativamente", "label": "Os itens de experiência são oferecidos ativamente?", "type": "binary"},
            {"key": "servico_elegancia", "label": "O serviço é feito com elegância, usando bandeja ou apresentação adequada?", "type": "binary"},
            {"key": "experiencia_exclusividade", "label": "A experiência transmite exclusividade?", "type": "binary"},
            {"key": "insumos_adequados", "label": "Todos os insumos estão adequados?", "type": "binary"},
        ],
    },
    {
        "name": "WhatsApp e Vendas Digitais",
        "observation_key": "observacoes_whatsapp",
        "questions": [
            {"key": "responde_ate_10_min", "label": "As mensagens são respondidas em até 10 minutos?", "type": "binary"},
            {"key": "responsavel_turno_whatsapp", "label": "Existe responsável definido por turno para o WhatsApp?", "type": "binary"},
            {"key": "conversas_organizadas", "label": "As conversas estão organizadas e acompanhadas?", "type": "binary"},
            {"key": "fotos_padrao_charth", "label": "As fotos seguem o padrão Charth?", "type": "binary"},
            {"key": "busca_ativa_whatsapp", "label": "A loja realiza busca ativa via WhatsApp?", "type": "binary"},
            {"key": "novidades_semanais", "label": "A loja envia novidades semanalmente?", "type": "binary"},
            {"key": "pos_venda_whatsapp_24h", "label": "O pós-venda via WhatsApp é feito em até 24h?", "type": "binary"},
            {"key": "recupera_negociacoes", "label": "A loja recupera negociações não fechadas?", "type": "binary"},
        ],
    },
    {
        "name": "Gestão da Gerente",
        "observation_key": "observacoes_gestao_gerente",
        "questions": [
            {"key": "reuniao_diaria_registrada", "label": "A reunião diária é realizada e registrada?", "type": "binary"},
            {"key": "feedback_individual_mes", "label": "O feedback individual foi realizado no mês?", "type": "binary"},
            {"key": "plano_acao_documentado", "label": "O plano de ação está documentado?", "type": "binary"},
            {"key": "escala_organizada", "label": "A escala está organizada estrategicamente?", "type": "binary"},
            {"key": "lideranca_inspira", "label": "A liderança inspira respeito e resultado?", "type": "binary"},
            {"key": "gerente_acompanha_vendas", "label": "A gerente acompanha as vendas no salão?", "type": "binary"},
            {"key": "amostragem_livro_fiscal", "label": "A amostragem de lançamento do livro fiscal está correta?", "type": "binary"},
        ],
    },
    {
        "name": "Estrutura da Loja",
        "observation_key": "observacoes_estrutura_loja",
        "questions": [
            {"key": "lampadas_queimadas", "label": "Existem lâmpadas queimadas?", "type": "binary_inverse"},
            {"key": "moveis_equipamentos_danificados", "label": "Existem móveis ou equipamentos quebrados/danificados?", "type": "binary_inverse"},
            {"key": "pintura_acabamentos_conservados", "label": "A pintura e os acabamentos estão conservados?", "type": "binary"},
            {"key": "ar_condicionado_funcionando", "label": "O ar-condicionado está funcionando?", "type": "binary"},
            {"key": "som_ambiente_adequado", "label": "O som ambiente está adequado?", "type": "binary"},
            {"key": "fachada_limpa_cuidada", "label": "A fachada está limpa e bem cuidada?", "type": "binary"},
            {"key": "comunicacao_visual_sem_danos", "label": "A comunicação visual está sem danos?", "type": "binary"},
            {"key": "loucas_personalizadas_perfeitas", "label": "As louças personalizadas estão em perfeito estado?", "type": "binary"},
            {"key": "mascaras_provadores", "label": "Há máscaras em todos os provadores?", "type": "binary"},
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
    "default_gold_rule": "gold_strict",
    "min_block_scope": "all_sections",
    "team_fund_percent": 0.01,
    "team_sales_percent": 0.75,
    "team_support_percent": 0.25,
}
