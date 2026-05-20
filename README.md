# CHARTH – Supervisão Varejo v6 Oficial

App Streamlit para avaliação de supervisão das lojas CHARTH, com login por perfil, formulário oficial, dashboard, histórico, plano de ação e cálculo de bonificação.

## 1. Como rodar no VS Code - Windows

1. Extraia o ZIP em uma pasta nova.
2. Abra a pasta no VS Code: **Arquivo > Abrir Pasta**.
3. Abra o terminal do VS Code.
4. Rode:

```powershell
.\install_windows.bat
```

5. Depois rode:

```powershell
.\run_windows.bat
```

Se preferir manualmente:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## 2. Como rodar no Mac/Linux

```bash
chmod +x install_mac_linux.sh run_mac_linux.sh
./install_mac_linux.sh
./run_mac_linux.sh
```

## 3. Logins de teste



Troque as senhas antes de publicar online.

## 4. Permissões

- Admin e supervisora: acesso completo.
- Gestoras: acesso somente a Dashboard, Histórico e Planos de Ação. Não conseguem criar avaliação.
- Em `src/config.py`, a constante `GESTORA_CAN_VIEW_ALL_STORES` controla se gestoras veem todas as lojas ou apenas a loja vinculada.

## 5. Formulário oficial

O app contém 11 seções:

1. Identificação
2. Equipe e Atendimento
3. Visual Merchandising
4. Estoque e Produto
5. Resultados e Indicadores
6. Experiência da Cliente
7. WhatsApp e Vendas Digitais
8. Gestão da Gerente
9. Estrutura da Loja
10. Experiência Premium
11. Perguntas Estratégicas

Perguntas avaliativas comuns usam escala de 1 a 10. Perguntas binárias usam Sim/Não e geram nota 10 ou 0 conforme a regra do briefing.

## 6. Cálculo da média ponderada oficial

A média ponderada principal segue exatamente:

```text
((Equipe x 1) + (VM x 1) + (Estoque x 1) + (Resultado x 2) + (Experiência x 1) + (Gestão x 2)) / 8
```

WhatsApp, Estrutura e Experiência Premium aparecem no formulário e dashboard, mas não entram na média ponderada principal.

## 7. Bonificação

As regras ficam em `src/config.py`, na constante `BONUS_CONFIG`.

Pontos configuráveis importantes:

- Valor da Prata, pois o briefing menciona duas versões: R$ 3.700 ou R$ 2.000.
- Valor do Bronze, pois o briefing cita valor mas não define todos os critérios.
- Critério mínimo de Bronze, definido como constante explícita.
- Percentuais do Fundo Ouro da equipe.

## 8. Dados e arquivos

- Banco SQLite local: `charth_supervisao_v6.db`
- Uploads de fotos: pasta `uploads/`
- Backups: pasta `backups/`
- Exportação: feita pelo botão de download no Dashboard.

## 9. Identidade visual

O CSS usa `font-family: SIMPLO` com fallback para fontes sem serifa elegantes. Para usar SIMPLO de fato, a fonte precisa estar instalada no computador que acessa o app. O projeto não inclui arquivos de fonte por questão de licença.

## 10. Observações de regra

Há uma inconsistência no briefing: gestoras devem ver todas as avaliações, mas também há controle por loja. O app implementa isso de forma configurável via `GESTORA_CAN_VIEW_ALL_STORES`.

Também há conflito controlado no modelo de bonificação: Prata aparece como R$ 3.700 ou R$ 2.000, e Bronze não possui critérios completos. Esses pontos foram colocados como constantes em `src/config.py`.

## Atualizacao v7 - Bonificacao

Esta versao inclui o menu **Bonificacao** com calculo trimestral por loja.

Se voce ja possui avaliacoes cadastradas na versao v6 e quer manter os dados, prefira usar o pacote `charth_supervisao_v6_atualizacao_bonificacao.zip` e substituir apenas os arquivos de codigo na pasta atual. Nao apague o banco `charth_supervisao_v6.db`.
