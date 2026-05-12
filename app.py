import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Avaliação Matriz 9D", layout="wide", initial_sidebar_state="expanded")

# ──────────────────────────────────────────────────────────────
# BASE DE DADOS DO INSTRUMENTO (EXTRAÍDA DO SEU DOCX)
# ──────────────────────────────────────────────────────────────
DOM_A = [
    "1.1 Identificação formal na matriz",
    "1.2 Identidade pedagógica distinta",
    "2.1 Vinculação a dimensão formativa explícita",
    "2.2 Coerência entre dimensão e prática pedagógica",
    "3.1 Competências claramente definidas (verbos de ação)",
    "3.2 Competências mensuráveis e observáveis",
    "3.3 Progressão de complexidade compatível com o período",
    "4.1 Conteúdos servem às competências (não são apenas listas)",
    "4.2 Ausência de conteúdo irrelevante/ornamental",
    "4.3 Cobertura de conteúdos essenciais (sem lacunas)",
    "5.1 Objetivos explícitos e mensuráveis",
    "5.2 Alinhamento objetivo × conteúdo × competência"
]

DOM_B = [
    "6.1 Cada competência associada a atividade concreta",
    "6.2 Rastreabilidade Competência → Atividade → Espaço → Avaliação",
    "6.3 Limitação da dependência exclusiva de aula expositiva",
    "6.4 Atividade pedagogicamente compatível com a competência",
    "7.1 Espaço educacional compatível com a atividade",
    "7.2 Diversidade de cenários formativos",
    "7.3 Espaço favorece autenticidade formativa",
    "8.1 Integração horizontal e vertical com outros componentes",
    "8.2 Ausência de redundância improdutiva",
    "8.3 Progressão longitudinal clara",
    "8.4 Integração interdisciplinar real",
    "9.1 Toda atividade possui espaço definido",
    "9.2 Espaço tem justificativa pedagógica",
    "9.3 Coerência Componente × Atividade × Espaço",
    "10.1 Número de atividades realisticamente executável",
    "10.2 Ausência de dependência de recursos indisponíveis",
    "10.3 Sustentabilidade docente para operacionalização"
]

DOM_C = [
    "11.1 Cada competência possui instrumento avaliativo compatível",
    "11.2 Instrumento mede domínio correto (cognitivo/psicomotor/afetivo)",
    "11.3 Congruência entre ensino e avaliação",
    "12.1 Todas as competências relevantes são avaliadas",
    "12.2 Equilíbrio entre avaliação de memória e performance",
    "12.3 Ausência de redundância avaliativa inútil",
    "13.1 Evidência produzida é objetiva",
    "13.2 Avaliação é reprodutível (confiabilidade interavaliadores)",
    "13.3 Critérios explícitos de desempenho (rubricas)",
    "14.1 Feedback estruturado (imediato, específico, acionável)",
    "14.2 Feedback corrige desempenho de forma clara",
    "14.3 Oportunidade de melhoria/remediação após feedback",
    "15.1 Rastreabilidade curricular completa",
    "15.2 Indicadores de desempenho do componente monitorados",
    "15.3 Revisão periódica baseada em evidências",
    "15.4 Capacidade institucional de melhoria contínua",
    "16.1 Avaliação cabe na carga horária disponível",
    "16.2 Densidade avaliativa proporcional",
    "17.1 O que está descrito realmente acontece (currículo fictício?)",
    "17.2 Existência de evidência documental"
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
st.markdown("Preencha os dados do componente e avalie cada critério. O score e o diagnóstico serão calculados automaticamente.")

with st.sidebar:
    st.header("📋 Identificação do Componente")
    nome_comp = st.text_input("Nome do Componente")
    periodo = st.selectbox("Série/Semestre", range(1, 13))
    ch = st.number_input("Carga Horária (h)", min_value=1, value=40)
    responsavel = st.text_input("Coordenador/Responsável")
    data_avaliacao = st.date_input("Data da Avaliação", datetime.now())

    st.divider()
    st.markdown("💡 **Escala:** `0` = Não Conforme | `1` = Parcial | `2` = Conforme")

# ──────────────────────────────────────────────────────────────
# FORMULÁRIO DE AVALIAÇÃO
# ──────────────────────────────────────────────────────────────
with st.form("form_avaliacao"):
    tab1, tab2, tab3 = st.tabs(["🏛️ Domínio A: Estrutura", "⚙️ Domínio B: Operacionalização", "📊 Domínio C: Avaliação & Governança"])
    
    scores_a = {}
    with tab1:
        for q in DOM_A:
            scores_a[q] = st.radio(q, [0, 1, 2], index=0, horizontal=True, key=f"a_{q}")
            
    scores_b = {}
    with tab2:
        for q in DOM_B:
            scores_b[q] = st.radio(q, [0, 1, 2], index=0, horizontal=True, key=f"b_{q}")
            
    scores_c = {}
    with tab3:
        for q in DOM_C:
            scores_c[q] = st.radio(q, [0, 1, 2], index=0, horizontal=True, key=f"c_{q}")

    st.divider()
    st.subheader("🚨 Critérios de Reprovação Automática (FAIL CRÍTICO)")
    st.markdown("Marque qualquer item que se aplique. Um único `FAIL` invalida o score final.")
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
        st.error("⚠️ **FAIL CRÍTICO DETECTADO:**\n" + "\n".join(fail_list))
    else:
        st.success("Nenhum critério de reprovação automática acionado.")

    # Lista de não conformidades (score < 2)
    nc = []
    for d, score_dict in [("A", scores_a), ("B", scores_b), ("C", scores_c)]:
        for q, s in score_dict.items():
            if s < 2:
                nc.append(f"[Domínio {d}] {q}")
    
    st.subheader("📌 Principais Não Conformidades")
    if nc:
        for i, item in enumerate(nc, 1):
            st.write(f"{i}. {item}")
    else:
        st.write("Nenhuma não conformidade identificada.")

    # Plano Corretivo Interativo
    st.subheader("🛠️ Plano Corretivo (Editável)")
    df_plan = pd.DataFrame({"Problema Identificado": nc[:5], "Ação Proposta": [""]*len(nc[:5]), "Prioridade": ["Alta", "Média", "Baixa", "Média", "Alta"], "Prazo": [""]*len(nc[:5])})
    edited_df = st.data_editor(df_plan, num_rows="dynamic")

    # Botão de Exportação
    st.download_button(
        label="📥 Baixar Relatório em CSV",
        data=f"Componente;{nome_comp}\nPeríodo;{periodo}\nCH;{ch}\nResponsável;{responsavel}\nData;{data_avaliacao}\nScore Total;{total_scaled}/84\nDiagnóstico;{diag}\nFails Críticos;{', '.join(fail_list) if has_fail else 'Nenhum'}\n\nRelatório completo gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        file_name=f"Relatorio_Matriz9D_{nome_comp.replace(' ','_')}.csv",
        mime="text/csv"
    )
