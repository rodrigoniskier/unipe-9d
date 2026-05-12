import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Avaliação Matriz 9D", layout="wide", initial_sidebar_state="expanded")

# ──────────────────────────────────────────────────────────────
# BASE DE DADOS COM DETALHAMENTO PEDAGÓGICO (EXTRAÍDO DO DOCX)
# ──────────────────────────────────────────────────────────────
DOM_A = [
    {"title": "1.1 Identificação formal na matriz",
     "guidance": "**Verifique se constam:** nome oficial, código, período/semestre, carga horária, eixo ou núcleo curricular e modalidade.\n\n⚠️ **Se faltar algum item:** inadequação estrutural imediata.",
     "evidence": "PPC, matriz oficial, catálogo do curso"},
    {"title": "1.2 Identidade pedagógica claramente distinta",
     "guidance": "**Pergunte:** Este componente tem propósito próprio ou apenas repete conteúdo de outro?\n\n🔍 **Indicadores de problema:** nomes diferentes com mesma função, duplicação de conteúdos, redundância sem progressão cognitiva.",
     "evidence": "Ementas comparadas, plano de ensino"},
    {"title": "2.1 Vinculação explícita a dimensão formativa",
     "guidance": "**Exemplos válidos:** conhecimento biomédico, habilidades clínicas, comunicação, profissionalismo, gestão, atenção à saúde.\n\n❌ **Inadequado:** resposta vaga como \"ensina conteúdo médico\". A dimensão precisa ser explícita.",
     "evidence": "Aba 'Dimensões', matriz de vinculação"},
    {"title": "2.2 Coerência entre dimensão e prática pedagógica",
     "guidance": "**Teste de alinhamento:** Ex: Farmacologia clínica com dimensão \"liderança institucional\" = desalinhamento.\n\n💡 **Pergunte:** \"Existe coerência real entre a dimensão declarada e o que é ensinado?\"",
     "evidence": "Plano de ensino, atividades descritas"},
    {"title": "3.1 Competências com verbos de ação claros",
     "guidance": **Bons verbos:** interpretar, decidir, executar, comunicar, correlacionar, raciocinar, resolver.\n\n❌ **Fragilidade:** \"conhecer\", \"entender\", \"aprender\" (não descrevem desempenho observável).",
     "evidence": "Aba 'Competências', PPC"},
    {"title": "3.2 Competências mensuráveis e observáveis",
     "guidance": **Exemplo bom:** \"Interpretar exames laboratoriais no contexto clínico.\"\n❌ **Exemplo ruim:** \"Compreender medicina laboratorial.\"\n\n🔍 **Teste:** \"Como eu observaria objetivamente essa competência?\" Se não houver resposta clara → inadequação.",
     "evidence": "Rubricas, planos de avaliação"},
    {"title": "3.3 Progressão de complexidade compatível",
     "guidance": **Inadequado:** 1º período exigindo decisão terapêutica complexa ou manejo de UTI.\n❌ **Inadequado:** 10º período com exigência cognitiva superficial.\n\n💡 Verifique se a demanda cognitiva acompanha o estágio formativo do aluno.",
     "evidence": "Sequência curricular, taxonomia de Bloom"},
    {"title": "4.1 Conteúdos servem às competências",
     "guidance": **Teste:** Para cada conteúdo, pergunte: \"Por que este conteúdo existe?\"\n❌ **Inadequado:** \"Porque sempre esteve no currículo\" ou lista temática desconectada de desempenho.",
     "evidence": "Aba 'Conteúdos', plano de ensino"},
    {"title": "4.2 Ausência de conteúdo irrelevante/ornamental",
     "guidance": **Sinais:** excesso enciclopédico, detalhe sem aplicação clínica, informação sem utilidade formativa.\n\n💡 **Pergunta-chave:** \"Se este conteúdo for removido, a competência continua sendo atingida?\" Se SIM → provável excesso.",
     "evidence": "Cronograma, carga horária por tópico"},
    {"title": "4.3 Cobertura de conteúdos essenciais (sem lacunas)",
     "guidance": **Teste:** Para atingir a competência proposta, falta algum conteúdo essencial?\n❌ **Exemplo:** Competência de interpretação clínica sem valores de referência, sensibilidade/especificidade ou interferentes.",
     "evidence": "Diretrizes nacionais, literatura de referência"},
    {"title": "5.1 Objetivos explícitos e mensuráveis",
     "guidance": **Devem responder:** \"Ao final, o estudante será capaz de quê?\"\n❌ **Inadequado:** \"Ampliar conhecimentos\", \"favorecer aprendizado\", \"apresentar visão geral\".",
     "evidence": "Aba 'Articulação', PPC"},
    {"title": "5.2 Alinhamento objetivo × conteúdo × competência",
     "guidance": **Teste de triangulação:** Objetivo diz X, conteúdo ensina Y, avaliação cobra Z?\n❌ **Se SIM:** desalinhamento pedagógico grave.",
     "evidence": "Matriz de cruzamento operacional"}
]

DOM_B = [
    {"title": "6.1 Competência associada a atividade concreta",
     "guidance": **Teste:** Escolha uma competência e pergunte: \"Onde exatamente o aluno desenvolve isso?\"\n✅ **Aceitável:** comunicar más notícias = simulação com paciente padronizado, OSCE, role-play.\n❌ **Inadequado:** apenas aula expositiva sobre comunicação.",
     "evidence": "Plano de aula, cronograma de atividades"},
    {"title": "6.2 Rastreabilidade Competência → Atividade → Espaço → Avaliação",
     "guidance": **Pergunta auditável:** \"Consigo provar onde esta competência é treinada?\"\n❌ Se não for possível mapear o caminho completo → desalinhamento sistêmico.",
     "evidence": "Planilhas de articulação, matriz 9D"},
    {"title": "6.3 Limitação da dependência exclusiva de aula expositiva",
     "guidance": **Pergunte:** Qual % do componente depende exclusivamente de aula tradicional/transmissão passiva?\n❌ Se competências práticas forem ensinadas apenas assim → problema metodológico.",
     "evidence": "Carga horária teórico-prática"},
    {"title": "6.4 Atividade pedagogicamente compatível",
     "guidance": **Exemplos:**\n✅ Competência: realizar exame físico → Atividade: prática supervisionada.\n❌ Competência: realizar exame físico → Atividade: leitura de capítulo.\n\n💡 Conhecimento sobre a competência ≠ competência desenvolvida.",
     "evidence": "Metodologias ativas descritas"},
    {"title": "7.1 Espaço educacional compatível com a atividade",
     "guidance": **Tabela de referência:** discussão clínica = sala tutorial | exame físico = ambulatório/lab | simulação = centro de simulação | habilidades cirúrgicas = lab técnico | APS = UBS.\n❌ Competência prática treinada apenas em sala teórica = inadequação.",
     "evidence": "Aba 'Espaços', alocação física"},
    {"title": "7.2 Diversidade de cenários formativos",
     "guidance": **Currículo robusto expõe o aluno a:** laboratório, ambulatório, hospital, APS, comunidade, simulação, discussão tutorial.\n\n💡 \"O componente ensina em um único ambiente quando deveria usar vários?\"",
     "evidence": "Mapa de cenários, termos de parceria"},
    {"title": "7.3 Espaço favorece autenticidade formativa",
     "guidance": **Pergunta crítica:** O aluno vivencia o contexto real da competência?\n❌ **Exemplo inadequado:** aprender relação médico-paciente apenas via slides ou estudos de caso teóricos.",
     "evidence": "Registros de prática, portfólios"},
    {"title": "8.1 Integração horizontal e vertical",
     "guidance": **Pergunte:** Este componente conversa com básico + clínico? Teoria + prática? Horizontalmente (mesmo período) e verticalmente (entre períodos)?\n❌ Se for isolado → fragmentação curricular.",
     "evidence": "Temas integradores, eixos estruturantes"},
    {"title": "8.2 Ausência de redundância improdutiva",
     "guidance": **Pergunte:** O mesmo conteúdo aparece repetidamente sem progressão?\n❌ **Exemplo:** Inflamação ensinada em Patologia, Imunologia, Clínica e Farmacologia sem integração ou novo foco.",
     "evidence": "Matriz de conteúdos cruzados"},
    {"title": "8.3 Progressão longitudinal clara",
     "guidance": **Boa progressão:** 1º ano: conceitos → 3º ano: aplicação clínica → 5º ano: decisão assistencial.\n❌ Componente terminal e desconectado do fluxo formativo = falha.",
     "evidence": "Sequência de competências por semestre"},
    {"title": "8.4 Integração interdisciplinar real",
     "guidance": **Não basta citar outras áreas.** Pergunte: Há atividades realmente integradas? (ex: microbio+infecto, anatomia+cirurgia, fisiologia+clínica).\n❌ Justaposição de disciplinas ≠ integração.",
     "evidence": "Projetos integradores, avaliações conjuntas"},
    {"title": "9.1 Toda atividade possui espaço definido",
     "guidance": **Sem espaço físico/virtual alocado = atividade abstrata.**\n💡 Verifique se cada linha da aba de articulação tem o campo \"Espaço\" preenchido e coerente.",
     "evidence": "Planilha 'CC x atividade x espaço'"},
    {"title": "9.2 Espaço tem justificativa pedagógica",
     "guidance": **Pergunte:** \"Por que essa atividade ocorre aqui?\"\n❌ **Resposta inadequada:** \"Porque é onde tem sala disponível\" ou \"Por logística administrativa\".",
     "evidence": "Justificativa metodológica no plano"},
    {"title": "9.3 Coerência Componente × Atividade × Espaço",
     "guidance": **Checklist:** Componente (o que ensina?) → Atividade (como ensina?) → Espaço (onde ensina?).\n❌ Se um elemento falhar ou não se sustentar → desalinhamento operacional.",
     "evidence": "Matriz 9D completa"},
    {"title": "10.1 Número de atividades realisticamente executável",
     "guidance": **Currículos às vezes planejam fantasia.** Pergunte: Cabe na CH? Cabe no calendário acadêmico? Cabe no número de docentes? Cabe na infraestrutura?\n❌ Planejamento irreal = inadimplemento curricular.",
     "evidence": "Grade horária, calendário acadêmico"},
    {"title": "10.2 Ausência de dependência de recursos indisponíveis",
     "guidance": **Exemplos de falha:** simulação sem centro de simulação ativo, ambulatório sem fluxo de pacientes, laboratório inexistente ou sem insumos.\n💡 Valide a viabilidade física e logística.",
     "evidence": "Inventário de infraestrutura, contratos"},
    {"title": "10.3 Sustentabilidade docente para operacionalização",
     "guidance": **Pergunte:** Os docentes conseguem operacionalizar isso sem colapso de carga horária ou turnover?\n❌ Sobrecarga não planejada = risco de descontinuidade.",
     "evidence": "Quadro de professores, carga didática"}
]

DOM_C = [
    {"title": "11.1 Instrumento avaliativo compatível com competência",
     "guidance": **Tabela de referência:** Interpretar ECG = estação prática/caso clínico | Exame físico = OSCE | Comunicar más notícias = paciente padronizado.\n❌ **Inadequação clássica:** competência prática avaliada apenas por prova de múltipla escolha (mede memória, não performance).",
     "evidence": "Aba 'Instrumentos de avaliação', rubricas"},
    {"title": "11.2 Instrumento mede domínio correto",
     "guidance": **Categorias:** cognitivo, psicomotor, afetivo/profissional.\n❌ **Erro frequente:** medir atitude ou habilidade psicomotora com prova teórica escrita.",
     "evidence": "Especificações de avaliação"},
    {"title": "11.3 Congruência entre ensino e avaliação",
     "guidance": **Pergunta auditável:** \"O aluno foi treinado no formato exato em que será avaliado?\"\n❌ **Inadequado:** ensino via discussão tutorial, avaliação por checklist procedimental nunca praticado.",
     "evidence": "Planos de aula vs planos de prova"},
    {"title": "12.1 Todas as competências relevantes são avaliadas",
     "guidance": **Faça inventário:** Liste todas as competências do componente. Marque: avaliada? não avaliada?\n❌ **Regra de ouro:** Competência não avaliada = competência presumida (não existe pedagogicamente).",
     "evidence": "Matriz de avaliação por competência"},
    {"title": "12.2 Equilíbrio entre memória e performance",
     "guidance": **Pergunte:** O currículo privilegia decorar/reconhecer/repetir em detrimento de executar/decidir/comunicar/integrar?\n💡 Busque equilíbrio proporcional aos domínios da Matriz 9D.",
     "evidence": "Banco de questões, instrumentos aplicados"},
    {"title": "12.3 Ausência de redundância avaliativa inútil",
     "guidance": **Exemplo de falha:** cinco provas teóricas medindo exatamente o mesmo constructo cognitivo.\n❌ Sem ganho formativo ou diagnóstico = burocratização.",
     "evidence": "Calendário avaliativo, análise de itens"},
    {"title": "13.1 Evidência produzida é objetiva",
     "guidance": **Pergunte:** A avaliação gera dado observável e registrável?\n✅ **Objetivo:** checklist OSCE, rubrica pontuada.\n❌ **Fraco:** \"impressão subjetiva do docente\" ou \"participação em sala\".",
     "evidence": "Formulários de avaliação preenchidos"},
    {"title": "13.2 Avaliação é reprodutível",
     "guidance": **Teste de confiabilidade:** Outro avaliador treinado chegaria a uma conclusão semelhante?\n❌ Se NÃO → baixa confiabilidade, risco jurídico e pedagógico.",
     "evidence": "Calibração de avaliadores, kappa"},
    {"title": "13.3 Critérios explícitos de desempenho (rubricas)",
     "guidance": **Pergunte:** O que define claramente: aprovado? insuficiente? excelente?\n❌ Sem rubrica ou descritores → subjetividade excessiva e insegurança na decisão.",
     "evidence": "Rubricas validadas, critérios de corte"},
    {"title": "14.1 Feedback estruturado",
     "guidance": **Características obrigatórias:** imediato, específico, acionável.\n❌ **Feedback ruim:** \"estude mais\", \"melhore a comunicação\".",
     "evidence": "Relatórios de devolutiva, portfólios"},
    {"title": "14.2 Feedback corrige desempenho de forma clara",
     "guidance": **Exemplo bom:** \"Na anamnese você não explorou fatores de risco cardiovasculares; na próxima, inclua tabagismo, HAS e DM na família.\"\n💡 Deve apontar lacuna + direção de melhoria.",
     "evidence": "Registros de tutoria, feedbacks escritos"},
    {"title": "14.3 Oportunidade de melhoria após feedback",
     "guidance": **Pergunte:** Existe reavaliação, nova prática ou segunda tentativa?\n❌ Sem oportunidade de correção → feedback perde função pedagógica e vira punição.",
     "evidence": "Regulamento de recuperação, plano de mentoria"},
    {"title": "15.1 Rastreabilidade curricular completa",
     "guidance": **Pergunta de governança:** Consigo seguir o fluxo: competência → atividade → avaliação → resultado → melhoria?\n❌ Se NÃO → governança fraca, vulnerável em auditorias.",
     "evidence": "Sistemas acadêmicos, fluxogramas NDE"},
    {"title": "15.2 Indicadores de desempenho monitorados",
     "guidance": **Exemplos válidos:** taxa de aprovação, falhas recorrentes por competência, competências críticas deficitárias, satisfação discente, consistência entre turmas.\n💡 Indicadores devem ser coletados e analisados periodicamente.",
     "evidence": "Relatórios gerenciais, dashboards"},
    {"title": "15.3 Revisão periódica baseada em evidências",
     "guidance": **Pergunte:** Quando foi revisado pela última vez? Com base em quê?\n❌ **Inadequado:** revisão apenas por troca de docente ou \"achismo\". Deve usar dados, feedback e DCNs.",
     "evidence": "Atas de NDE, pareceres de revisão"},
    {"title": "15.4 Capacidade institucional de melhoria contínua",
     "guidance": **Se problemas forem detectados:** quem corrige? Coordenação? NDE? Colegiado? Comissão curricular?\n💡 Deve haver fluxo formal de ação corretiva.",
     "evidence": "Regimentos, fluxos de governança"},
    {"title": "16.1 Avaliação cabe na carga horária disponível",
     "guidance": **Problema comum:** planejamento com 12 OSCEs, múltiplos feedbacks e prática extensa… sem tempo real na CH declarada.\n❌ Subdimensionamento = inadimplemento ou sobrecarga.",
     "evidence": "Grade horária, cronograma de avaliações"},
    {"title": "16.2 Densidade avaliativa proporcional",
     "guidance": **Equilíbrio:** Nem excesso burocrático que engole o tempo de aprendizagem, nem avaliação insuficiente que mascara lacunas.\n💡 Proporção adequada ao nível de complexidade.",
     "evidence": "Plano de avaliação, carga horária avaliativa"},
    {"title": "17.1 Risco de currículo fictício",
     "guidance": **Pergunta brutal:** O que está descrito realmente acontece?\n❓ Essa atividade ocorre? Essa avaliação existe? Esse feedback acontece? Esse espaço é usado?\n💡 Separe o PPC do que é executado de fato.",
     "evidence": "Diários de classe, registros de presença"},
    {"title": "17.2 Existência de evidência documental",
     "guidance": **Verifique fisicamente/digitalmente:** cronogramas, checklists aplicados, atas de avaliação, relatórios de prática, rubricas assinadas, registros acadêmicos.\n❌ Sem documentação = currículo não auditável.",
     "evidence": "Acervo pedagógico, SEI, SIGAA, etc."}
]

FAILS = [
    "FAIL 1: Competências inexistentes ou não mensuráveis",
    "FAIL 2: Avaliação incompatível com competências",
    "FAIL 3: Ausência de rastreabilidade curricular",
    "FAIL 4: Atividades não operacionalizáveis",
    "FAIL 5: Espaços incompatíveis com as atividades",
    "FAIL 6: Componente curricular fictício (não executado)",
    "FAIL 7: Ausência de evidência documental",
    "FAIL 8: Desalinhamento objetivo–conteúdo–avaliação"
]

# ──────────────────────────────────────────────────────────────
# INTERFACE DO USUÁRIO
# ──────────────────────────────────────────────────────────────
st.title("📘 Instrumento de Adequação Curricular à Matriz 9D")
st.markdown("Preencha os dados do componente e avalie cada critério. Clique em **📖 Como avaliar?** para ver orientações detalhadas, exemplos e evidências esperadas.")

with st.sidebar:
    st.header("📋 Identificação do Componente")
    nome_comp = st.text_input("Nome do Componente")
    periodo = st.selectbox("Série/Semestre", range(1, 13))
    ch = st.number_input("Carga Horária (h)", min_value=1, value=40)
    responsavel = st.text_input("Coordenador/Responsável")
    data_avaliacao = st.date_input("Data da Avaliação", datetime.now())

    st.divider()
    st.info("💡 **Escala:** `0` = Não Conforme | `1` = Parcial | `2` = Conforme")
    st.markdown("🔍 Use os *expanders* para acessar o guia de verificação de cada item.")

# Função auxiliar para renderizar critérios com guia
def render_critérios(titulo_domínio, lista_critérios, prefixo_key):
    st.subheader(titulo_domínio)
    scores = {}
    for i, crit in enumerate(lista_critérios):
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            st.markdown(f"**{crit['title']}**")
        with col2:
            scores[crit['title']] = st.radio(
                "", [0, 1, 2], index=0, horizontal=True, 
                key=f"{prefixo_key}_{i}", label_visibility="collapsed"
            )
        with st.expander("📖 Como avaliar?"):
            st.markdown(crit['guidance'])
            st.caption(f"📂 **Evidência esperada:** {crit['evidence']}")
        st.divider()
    return scores

# ──────────────────────────────────────────────────────────────
# FORMULÁRIO DE AVALIAÇÃO
# ──────────────────────────────────────────────────────────────
with st.form("form_avaliacao"):
    tab1, tab2, tab3 = st.tabs(["🏛️ Domínio A: Estrutura", "⚙️ Domínio B: Operacionalização", "📊 Domínio C: Avaliação & Governança"])
    
    with tab1:
        scores_a = render_critérios("Identidade e Alinhamento Estrutural", DOM_A, "A")
    with tab2:
        scores_b = render_critérios("Operacionalização Pedagógica", DOM_B, "B")
    with tab3:
        scores_c = render_critérios("Avaliação, Evidência e Governança", DOM_C, "C")

    st.divider()
    st.subheader("🚨 Critérios de Reprovação Automática (FAIL CRÍTICO)")
    st.markdown("Marque qualquer item que se aplique. **Um único `FAIL` invalida o score final**, independentemente da pontuação acumulada.")
    fails_checked = {}
    for f in FAILS:
        fails_checked[f] = st.checkbox(f, key=f"fail_{f}")

    submitted = st.form_submit_button("📊 Gerar Diagnóstico Final", type="primary")

# ──────────────────────────────────────────────────────────────
# LÓGICA DE CÁLCULO E RELATÓRIO
# ──────────────────────────────────────────────────────────────
if submitted:
    total_a = sum(scores_a.values())
    total_b = sum(scores_b.values())
    total_c = sum(scores_c.values())
    total_raw = total_a + total_b + total_c
    max_possible = len(DOM_A) + len(DOM_B) + len(DOM_C) * 2  # Cada item vale no máximo 2
    
    # Normaliza para a escala oficial do documento (máx 84 pontos)
    total_scaled = round((total_raw / max_possible) * 84)
    
    # Verifica Fail Crítico
    has_fail = any(fails_checked.values())
    fail_list = [f for f, val in fails_checked.items() if val]
    
    # Diagnóstico por bandas
    if has_fail:
        diag = "❌ REPROVADO (FAIL CRÍTICO)"
        color = "red"
    elif total_scaled >= 75:
        diag = "✅ EXCELENTE ADEQUAÇÃO 9D"
        color = "green"
    elif total_scaled >= 60:
        diag = "🟡 ADEQUAÇÃO SATISFATÓRIA COM AJUSTES"
        color = "orange"
    elif total_scaled >= 45:
        diag = "🟠 ADEQUAÇÃO LIMITADA"
        color = "darkorange"
    elif total_scaled >= 30:
        diag = "🔴 INADEQUAÇÃO IMPORTANTE"
        color = "red"
    else:
        diag = "⚫ NÃO ADERENTE À MATRIZ 9D"
        color = "gray"

    # Exibição do Relatório
    st.divider()
    st.header("📄 DIAGNÓSTICO FINAL PADRONIZADO")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Domínio A (Estrutura)", f"{total_a}/{len(DOM_A)*2}")
    col2.metric("Domínio B (Operacionalização)", f"{total_b}/{len(DOM_B)*2}")
    col3.metric("Domínio C (Avaliação/Gov)", f"{total_c}/{len(DOM_C)*2}")
    
    st.markdown(f"### 🎯 Score Total: `{total_scaled}/84`")
    st.markdown(f"### 🏷️ Classificação: **<span style='color:{color}'>{diag}</span>**", unsafe_allow_html=True)
    
    if has_fail:
        st.error("⚠️ **FAIL CRÍTICO DETECTADO:**\n" + "\n".join([f"• {f}" for f in fail_list]))
    else:
        st.success("✅ Nenhum critério de reprovação automática acionado.")

    # Lista de não conformidades (score < 2)
    nc = []
    for d, score_dict, lista in [("A", scores_a, DOM_A), ("B", scores_b, DOM_B), ("C", scores_c, DOM_C)]:
        for crit in lista:
            if score_dict[crit['title']] < 2:
                nc.append(f"[Domínio {d}] {crit['title']}")
    
    st.subheader("📌 Principais Não Conformidades")
    if nc:
        for i, item in enumerate(nc, 1):
            st.write(f"{i}. {item}")
    else:
        st.write("Nenhuma não conformidade identificada. Componente plenamente alinhado.")

    # Plano Corretivo Interativo
    st.subheader("🛠️ Plano Corretivo (Editável)")
    max_items = min(len(nc), 5)
    df_plan = pd.DataFrame({
        "Problema Identificado": nc[:max_items], 
        "Ação Proposta": [""]*max_items, 
        "Prioridade": ["Alta"]*max_items, 
        "Prazo": [""]*max_items
    })
    edited_df = st.data_editor(df_plan, num_rows="dynamic", use_container_width=True)

    # Botão de Exportação
    csv_export = (
        f"COMPONENTE;{nome_comp}\n"
        f"PERÍODO;{periodo}\n"
        f"CH;{ch}\n"
        f"RESPONSÁVEL;{responsavel}\n"
        f"DATA;{data_avaliacao}\n"
        f"SCORE A;{total_a}/{len(DOM_A)*2}\n"
        f"SCORE B;{total_b}/{len(DOM_B)*2}\n"
        f"SCORE C;{total_c}/{len(DOM_C)*2}\n"
        f"SCORE TOTAL;{total_scaled}/84\n"
        f"DIAGNÓSTICO;{diag}\n"
        f"FAILS CRÍTICOS;{', '.join(fail_list) if has_fail else 'Nenhum'}\n"
        f"NÃO CONFORMIDADES;{' | '.join(nc)}\n"
        f"PLANO CORRETIVO;{' | '.join([f\"{row['Problema Identificado']} -> {row['Ação Proposta']} ({row['Prioridade']})\" for _, row in edited_df.iterrows()])}\n\n"
        f"Relatório gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')} conforme Instrumento de Adequação à Matriz 9D."
    )
    st.download_button(
        label="📥 Baixar Relatório em CSV",
        data=csv_export,
        file_name=f"Relatorio_Matriz9D_{nome_comp.replace(' ','_')}.csv",
        mime="text/csv"
    )
