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
        {"key": "acuracidade_estoque_5_itens", "label": "A conferência de 5 itens aleatórios apresentou acuracidade entre estoque físico e sistema?", "type": "binary"},
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
# Biblioteca de sugestões para Planos de Ação
# Cada pergunta que gerar pendência recebe uma orientação prática para a gestora.
# A função action_plan_recommendation usa a regra específica da pergunta quando
# existir e, quando não existir, usa um padrão por bloco.
# -----------------------------------------------------------------------------
ACTION_PLAN_SECTION_DEFAULTS = {
    "Equipe e Atendimento": {
        "problem": "Ponto de atendimento abaixo do padrão esperado.",
        "impact": "Pode reduzir conversão, vínculo com a cliente, venda adicional e consistência da experiência em loja.",
        "recommended_action": "Realizar alinhamento com a equipe, observar atendimentos reais no salão e reforçar o comportamento esperado no início de cada turno.",
        "validation": "Validar por observação direta da gerente ou supervisora e registrar evidências de melhoria no próximo acompanhamento.",
        "deadline_days": 7,
    },
    "Visual Merchandising": {
        "problem": "Execução visual abaixo do padrão esperado.",
        "impact": "Compromete leitura de produto, desejo de compra e percepção de cuidado da loja.",
        "recommended_action": "Reorganizar o ponto identificado conforme orientação de VM, priorizando clareza visual, exposição comercial e padrão premium.",
        "validation": "Enviar foto da correção ou validar na próxima visita de supervisão.",
        "deadline_days": 2,
    },
    "Estoque e Produto": {
        "problem": "Rotina de estoque/produto abaixo do padrão esperado.",
        "impact": "Pode afetar venda, reposição, transferências, disponibilidade de produto e confiança da equipe nas informações do estoque.",
        "recommended_action": "Revisar a causa do desvio, organizar a rotina com a gerente e registrar os ajustes necessários para correção.",
        "validation": "Conferir novamente o ponto na próxima visita ou por evidência enviada pela loja.",
        "deadline_days": 3,
    },
    "Resultados e Indicadores": {
        "problem": "Rotina comercial ou acompanhamento de indicadores abaixo do padrão.",
        "impact": "Reduz velocidade de reação da loja e pode comprometer meta, PA, ticket médio e conversão.",
        "recommended_action": "Definir plano comercial objetivo com meta do dia, foco de venda, acompanhamento por vendedora e ação de recuperação quando necessário.",
        "validation": "Verificar registro do plano e evolução dos indicadores nos dias seguintes.",
        "deadline_days": 2,
    },
    "Experiência da Cliente e Padrão Premium": {
        "problem": "Entrega da experiência da cliente ou padrão premium abaixo do esperado.",
        "impact": "Pode reduzir encantamento, percepção de exclusividade e consistência do DNA CHARTH.",
        "recommended_action": "Reforçar com a equipe o ritual de atendimento, conferir disponibilidade dos itens de experiência e garantir execução durante o atendimento.",
        "validation": "Validar por observação do atendimento, evidência física ou nova checagem na próxima visita.",
        "deadline_days": 3,
    },
    "WhatsApp e Vendas Digitais": {
        "problem": "Rotina de WhatsApp/vendas digitais abaixo do padrão esperado.",
        "impact": "Pode reduzir conversão digital, relacionamento com cliente e recuperação de oportunidades de venda.",
        "recommended_action": "Definir responsável por turno, rotina de checagem, busca ativa e acompanhamento das conversas pendentes.",
        "validation": "Conferir amostra de conversas, tempo de resposta, contatos ativos e vendas geradas pelo canal.",
        "deadline_days": 7,
    },
    "Gestão da Gerente": {
        "problem": "Rotina de liderança ou gestão abaixo do padrão esperado.",
        "impact": "Afeta disciplina operacional, execução da equipe, reação aos resultados e consistência da cultura de loja.",
        "recommended_action": "Alinhar com a gerente uma rotina clara de reunião, acompanhamento, registro de ações e cobrança dos combinados.",
        "validation": "Conferir registros, evidências de acompanhamento e evolução do comportamento da equipe.",
        "deadline_days": 7,
    },
    "Estrutura da Loja": {
        "problem": "Estrutura física ou ambiente da loja fora do padrão esperado.",
        "impact": "Pode comprometer experiência da cliente, segurança, operação e percepção premium da marca.",
        "recommended_action": "Registrar o ponto com evidência, acionar o responsável pela correção e acompanhar até a solução final.",
        "validation": "Validar por foto, ordem de manutenção concluída ou nova checagem presencial.",
        "deadline_days": 7,
    },
}

ACTION_PLAN_LIBRARY = {
    "atendimento_consultivo": {
        "problem": "Atendimento pouco consultivo ou sem escuta ativa suficiente.",
        "impact": "A cliente pode perceber o atendimento como operacional, reduzindo vínculo, conversão e venda adicional.",
        "recommended_action": "Realizar alinhamento com a equipe sobre abordagem consultiva, escuta ativa e perguntas-chave para entender ocasião de uso, preferência, necessidade e objeções da cliente.",
        "validation": "Observar atendimentos reais no salão e registrar se a equipe aplicou perguntas consultivas durante a venda.",
        "deadline_days": 7,
    },
    "oferecem_look_completo": {
        "problem": "A equipe não está oferecendo composição completa de look.",
        "impact": "Reduz PA, ticket médio e percepção de curadoria da marca.",
        "recommended_action": "Definir combinações de looks por coleção/semana e orientar a equipe a apresentar pelo menos uma peça complementar no atendimento.",
        "validation": "Acompanhar atendimentos e verificar se houve oferta de segunda peça, acessório ou variação de cor.",
        "deadline_days": 7,
    },
    "clima_organizacional": {
        "problem": "Clima da equipe não favorece colaboração, respeito ou boa convivência.",
        "impact": "Pode prejudicar energia de salão, atendimento, produtividade e retenção da equipe.",
        "recommended_action": "Realizar conversa estruturada com a gerente, identificar pontos de tensão e combinar ações objetivas de rotina, comunicação e postura entre a equipe.",
        "validation": "Reavaliar o clima em nova visita e observar se houve melhora na colaboração durante o atendimento.",
        "deadline_days": 7,
    },
    "pecas_semana_evidenciadas": {
        "problem": "Peças foco da semana não estão em destaque no salão.",
        "impact": "A loja perde força comercial nos produtos prioritários e reduz a conexão entre estratégia da semana e exposição visual.",
        "recommended_action": "Reposicionar as peças foco em pontos de maior visibilidade, como vitrine, mesa, araras de entrada ou manequins, conforme orientação de VM.",
        "validation": "Enviar foto da nova exposição e confirmar se as peças foco estão visíveis para a cliente.",
        "deadline_days": 2,
    },
    "araras_penteadas": {
        "problem": "Araras sem organização visual adequada.",
        "impact": "A desorganização reduz percepção de cuidado, dificulta leitura de produto e compromete o padrão premium da loja.",
        "recommended_action": "Reorganizar araras por categoria, cor, tamanho ou orientação de VM, garantindo espaçamento, alinhamento e leitura limpa.",
        "validation": "Validar por foto ou na próxima visita da supervisora.",
        "deadline_days": 2,
    },
    "vitrine_gera_desejo": {
        "problem": "Vitrine não está gerando desejo real de compra.",
        "impact": "Reduz atração de entrada, percepção de novidade e força comercial da loja.",
        "recommended_action": "Revisar composição da vitrine com foco em produto estratégico, styling, leitura de coleção e clareza visual.",
        "validation": "Registrar foto da vitrine após ajuste e acompanhar percepção da supervisora/gestora.",
        "deadline_days": 2,
    },
    "acuracidade_estoque_5_itens": {
        "problem": "Divergência de acuracidade entre estoque físico e sistema na conferência de 5 itens aleatórios.",
        "impact": "Afeta venda, transferência, reposição, inventário e confiança da equipe nas informações do estoque.",
        "recommended_action": "Recontar os itens divergentes, verificar possíveis causas como troca de referência, venda não baixada, transferência pendente ou peça em local incorreto, e solicitar ajuste quando necessário.",
        "validation": "Realizar nova conferência de 5 itens aleatórios e registrar se houve correção da divergência.",
        "deadline_days": 2,
    },
    "ruptura_best_sellers": {
        "problem": "Ruptura de produtos com alto potencial de venda.",
        "impact": "A loja perde oportunidade comercial e pode frustrar clientes com demanda ativa.",
        "recommended_action": "Listar os best sellers em ruptura, consultar disponibilidade em outras lojas/estoque central e solicitar reposição ou transferência.",
        "validation": "Confirmar chegada, exposição ou alternativa comercial para os itens críticos.",
        "deadline_days": 3,
    },
    "transferencias_solicitadas_em_dia": {
        "problem": "Transferências pendentes ou fora do prazo.",
        "impact": "Atrasos em transferência prejudicam reposição, atendimento à cliente e giro de produto entre lojas.",
        "recommended_action": "Revisar transferências abertas, identificar pendências, priorizar itens ligados a venda ou best sellers e alinhar envio/recebimento com a equipe responsável.",
        "validation": "Conferir se as transferências foram baixadas, enviadas ou recebidas corretamente.",
        "deadline_days": 3,
    },
    "time_conhece_meta_diaria": {
        "problem": "Equipe sem clareza da meta diária.",
        "impact": "Sem meta visível, a equipe perde referência de ritmo, foco e prioridade comercial.",
        "recommended_action": "Implantar rotina de abertura do dia com comunicação da meta diária, venda realizada, falta para meta e estratégia principal do dia.",
        "validation": "Perguntar à equipe a meta do dia e verificar se todas sabem responder.",
        "deadline_days": 2,
    },
    "gerente_plano_acao_abaixo_meta": {
        "problem": "Ausência de plano de reação quando a loja está abaixo da meta.",
        "impact": "A loja perde velocidade de correção e pode acumular desvio de resultado ao longo da semana.",
        "recommended_action": "Gerente deve registrar ações comerciais objetivas para recuperar performance, como carteira de clientes, WhatsApp ativo, foco em PA, looks estratégicos e acompanhamento por vendedora.",
        "validation": "Verificar plano escrito e acompanhar evolução dos indicadores após a ação.",
        "deadline_days": 2,
    },
    "cliente_sugestao_variedade_cor": {
        "problem": "A equipe não apresenta variações de cor durante o atendimento.",
        "impact": "Reduz possibilidade de escolha, venda adicional e percepção de curadoria personalizada.",
        "recommended_action": "Orientar a equipe a apresentar opções de cor quando houver disponibilidade, explicando ocasião de uso, combinação e diferença de proposta entre as variações.",
        "validation": "Observar atendimentos e verificar se a sugestão de cor passou a fazer parte da abordagem.",
        "deadline_days": 7,
    },
    "bala_charth_disponivel": {
        "problem": "Item de experiência premium indisponível ou não oferecido.",
        "impact": "A loja deixa de entregar elementos de hospitalidade que reforçam cuidado, encantamento e diferenciação da marca.",
        "recommended_action": "Conferir estoque dos itens de experiência, organizar armazenamento e orientar equipe sobre oferta ativa durante atendimento.",
        "validation": "Validar disponibilidade física e se a equipe oferece os itens à cliente.",
        "deadline_days": 2,
    },
    "brigadeiro_charth_disponivel": {
        "problem": "Item de experiência premium indisponível ou não oferecido.",
        "impact": "A loja deixa de entregar elementos de hospitalidade que reforçam cuidado, encantamento e diferenciação da marca.",
        "recommended_action": "Conferir estoque dos itens de experiência, organizar armazenamento e orientar equipe sobre oferta ativa durante atendimento.",
        "validation": "Validar disponibilidade física e se a equipe oferece os itens à cliente.",
        "deadline_days": 2,
    },
    "bebidas_personalizadas_disponiveis": {
        "problem": "Bebidas personalizadas indisponíveis ou não oferecidas.",
        "impact": "Reduz a percepção de hospitalidade e cuidado extra no atendimento.",
        "recommended_action": "Conferir disponibilidade, armazenamento e rotina de oferta das bebidas personalizadas durante o atendimento.",
        "validation": "Validar disponibilidade física e abordagem da equipe.",
        "deadline_days": 2,
    },
    "responde_ate_10_min": {
        "problem": "Tempo de resposta do WhatsApp acima do padrão esperado.",
        "impact": "A demora reduz conversão, enfraquece relacionamento e pode fazer a cliente comprar em outro canal.",
        "recommended_action": "Definir responsável por turno, acompanhar conversas pendentes e estabelecer rotina de checagem do WhatsApp em horários fixos.",
        "validation": "Verificar tempo médio de resposta e amostra de conversas recentes.",
        "deadline_days": 3,
    },
    "busca_ativa_whatsapp": {
        "problem": "Busca ativa insuficiente pelo WhatsApp.",
        "impact": "A loja deixa de gerar venda a partir da carteira de clientes e perde oportunidade de ativar relacionamento.",
        "recommended_action": "Criar rotina semanal de contatos com clientes, usando novidades, reposições, peças foco e oportunidades personalizadas.",
        "validation": "Conferir quantidade de contatos feitos, respostas recebidas e vendas geradas pelo canal.",
        "deadline_days": 7,
    },
    "reuniao_diaria_registrada": {
        "problem": "Rotina de reunião diária sem execução ou sem registro.",
        "impact": "A equipe perde alinhamento sobre meta, prioridades, foco comercial e combinados do dia.",
        "recommended_action": "Implantar reunião rápida diária com registro de meta, foco do dia, ponto de atenção e responsáveis por ação.",
        "validation": "Conferir registro da reunião e perguntar à equipe sobre os direcionamentos do dia.",
        "deadline_days": 2,
    },
    "plano_acao_documentado": {
        "problem": "Plano de ação não documentado.",
        "impact": "Sem registro, a correção depende de memória e não permite acompanhamento consistente.",
        "recommended_action": "Registrar plano com problema, ação, responsável, prazo e evidência esperada de conclusão.",
        "validation": "Supervisora confere plano registrado e evolução na próxima visita.",
        "deadline_days": 2,
    },
    "lampadas_queimadas": {
        "problem": "Lâmpadas queimadas ou iluminação fora do padrão.",
        "impact": "Compromete visual merchandising, percepção de cuidado e valorização dos produtos.",
        "recommended_action": "Registrar pontos com lâmpadas queimadas, acionar manutenção ou responsável interno e acompanhar substituição.",
        "validation": "Enviar foto após correção ou validar na próxima visita.",
        "deadline_days": 7,
    },
    "moveis_equipamentos_danificados": {
        "problem": "Móveis ou equipamentos danificados na loja.",
        "impact": "Afeta experiência da cliente, segurança, operação e percepção de padrão premium.",
        "recommended_action": "Registrar item danificado com foto, avaliar risco operacional e acionar manutenção, troca ou reparo.",
        "validation": "Confirmar reparo realizado ou previsão formal de solução.",
        "deadline_days": 7,
    },
}


def action_plan_recommendation(section_name: str, question_key: str, question_label: str) -> dict:
    section_default = ACTION_PLAN_SECTION_DEFAULTS.get(section_name, {})
    specific = ACTION_PLAN_LIBRARY.get(question_key, {})
    template = {**section_default, **specific}
    if not template:
        template = {
            "problem": f"Ponto abaixo do padrão: {question_label}",
            "impact": "Pode comprometer a operação, a experiência da cliente ou a execução do padrão CHARTH.",
            "recommended_action": "Analisar a causa com a gerente, definir ação objetiva, responsável e prazo para correção.",
            "validation": "Validar a correção na próxima visita ou por evidência enviada pela loja.",
            "deadline_days": 7,
        }
    return {
        "problem": template.get("problem") or f"Ponto abaixo do padrão: {question_label}",
        "impact": template.get("impact") or "Pode comprometer a operação, a experiência da cliente ou a execução do padrão CHARTH.",
        "recommended_action": template.get("recommended_action") or "Definir ação objetiva com responsável e prazo.",
        "validation": template.get("validation") or "Validar a correção na próxima visita.",
        "deadline_days": int(template.get("deadline_days") or 7),
    }

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