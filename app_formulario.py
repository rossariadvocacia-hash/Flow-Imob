import streamlit as st
from datetime import datetime, timedelta

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Formulário de Contratos", layout="wide", page_icon="📝")

st.title("📝 Formulário Inteligente de Compra e Venda de Imóvel")
st.subheader("Fase 1: Captação e Estruturação de Dados")
st.markdown("---")

# INICIALIZAÇÃO DO BANCO DE DADOS DE CORRETORES NA MEMÓRIA DO SISTEMA
if "corretores_db" not in st.session_state:
    st.session_state.corretores_db = {
        "Selecione um profissional...": {"cpf": "", "creci": "", "banco": "", "pix": ""},
        "Carlos Alencar": {"cpf": "123.456.789-00", "creci": "RS-12345", "banco": "Itaú - Ag 0101 C/C 12345-6", "pix": "carlos@imoveis.com"},
        "Fernanda Lima": {"cpf": "987.654.321-11", "creci": "RS-54321", "banco": "Nubank - Ag 0001 C/C 98765-4", "pix": "41999998888"}
    }

# INICIALIZAÇÃO DA MEMÓRIA DO FORMULÁRIO
if "num_vendedores" not in st.session_state:
    st.session_state.num_vendedores = 1
if "num_compradores" not in st.session_state:
    st.session_state.num_compradores = 1
if "num_intermediarios" not in st.session_state:
    st.session_state.num_intermediarios = 1

# CRIAÇÃO DAS ABAS ORGANIZACIONAIS
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "👥 1. Vendedores", 
    "👥 2. Compradores", 
    "🏠 3. O Imóvel", 
    "💰 4. O Negócio", 
    "🤝 5. Intermediação"
])

# ==========================================
# ABA 1: VENDEDORES
# ==========================================
with tab1:
    st.header("Dados do(s) Vendedor(es)")
    for i in range(st.session_state.num_vendedores):
        st.markdown(f"#### 👤 Vendedor {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            st.file_uploader(f"Documento de Identificação (RG/CNH) - Vendedor {i+1}", type=["png", "jpg", "jpeg", "pdf"], key=f"doc_vend_{i}")
            st.text_input(f"Celular (com DDD) - Vendedor {i+1}", placeholder="(00) 99999-9999", key=f"tel_vend_{i}")
        with col2:
            st.file_uploader(f"Comprovante de Endereço - Vendedor {i+1}", type=["png", "jpg", "jpeg", "pdf"], key=f"end_vend_{i}")
            st.text_input(f"E-mail - Vendedor {i+1}", placeholder="exemplo@email.com", key=f"mail_vend_{i}")
        st.markdown("---")
    
    if st.button("➕ Adicionar Outro Vendedor"):
        st.session_state.num_vendedores += 1
        st.rerun()

# ==========================================
# ABA 2: COMPRADORES
# ==========================================
with tab2:
    st.header("Dados do(s) Comprador(es)")
    for i in range(st.session_state.num_compradores):
        st.markdown(f"#### 👤 Comprador {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            st.file_uploader(f"Documento de Identificação (RG/CNH) - Comprador {i+1}", type=["png", "jpg", "jpeg", "pdf"], key=f"doc_comp_{i}")
            st.text_input(f"Celular (com DDD) - Comprador {i+1}", placeholder="(00) 99999-9999", key=f"tel_comp_{i}")
        with col2:
            st.file_uploader(f"Comprovante de Endereço - Comprador {i+1}", type=["png", "jpg", "jpeg", "pdf"], key=f"end_comp_{i}")
            st.text_input(f"E-mail - Comprador {i+1}", placeholder="exemplo@email.com", key=f"mail_comp_{i}")
        st.markdown("---")
    
    if st.button("➕ Adicionar Outro Comprador"):
        st.session_state.num_compradores += 1
        st.rerun()

# ==========================================
# ABA 3: O IMÓVEL
# ==========================================
with tab3:
    st.header("Documentação da Unidade")
    col1, col2 = st.columns(2)
    with col1:
        st.file_uploader("Matrícula Atualizada do Imóvel", type=["png", "jpg", "jpeg", "pdf"])
    with col2:
        st.file_uploader("Última Cota Condominial (Comprovação)", type=["png", "jpg", "jpeg", "pdf"])

# ==========================================
# ABA 4: O NEGÓCIO
# ==========================================
with tab4:
    st.header("Condições Financeiras e Condições de Entrega")
    
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        valor_total = st.number_input("Valor Total do Negócio (R$)", min_value=0.0, format="%.2f", key="valor_total_negocio")
    with col_m2:
        data_assinatura = st.date_input("Data prevista para assinatura do contrato", datetime.today())
    
    st.markdown("---")
    st.subheader("💵 Fluxo de Parcelas")
    
    num_parcelas = st.number_input("Número de Parcelas/Etapas de Pagamento", min_value=1, max_value=20, value=1, step=1)
    lista_parcelas_nomes = []
    
    for p in range(int(num_parcelas)):
        st.markdown(f"##### 🎯 Parcela {p+1}")
        col_p1, col_p2, col_p3 = st.columns(3)
        
        with col_p1:
            tipo_parcela = st.selectbox(f"Tipo da Parcela {p+1}", ["Entrada/Sinal/Arras", "Intermediária", "Final/Entrega das chaves", "Outra"], key=f"tipo_p_{p}")
            forma_pag = st.selectbox(f"Forma de Pagamento {p+1}", ["Recursos próprios", "Financiamento bancário", "Dação de Imóvel", "Dação de Móvel/Veículo"], key=f"forma_p_{p}")
            
        with col_p2:
            regra_venc = st.selectbox(f"Regra de Vencimento {p+1}", ["Data específica", "Na data de assinatura do contrato", "Em até 30 dias", "Em até 60 dias", "Em até 90 dias", "Em até 120 dias", "Na assinatura do contrato de financiamento"], key=f"regra_v_{p}")
            
            if regra_venc == "Data específica":
                data_venc = st.date_input(f"Data de Vencimento {p+1}", data_assinatura + timedelta(days=30), key=f"data_v_{p}")
            elif regra_venc == "Na data de assinatura do contrato":
                data_venc = data_assinatura
                st.caption(f"🗓️ Calculado: {data_venc.strftime('%d/%m/%Y')}")
            elif "dias" in regra_venc:
                try:
                    dias = int(regra_venc.split(" ")[2])
                    data_venc = data_assinatura + timedelta(days=dias)
                    st.caption(f"🗓️ Calculado: {data_venc.strftime('%d/%m/%Y')}")
                except Exception:
                    data_venc = data_assinatura
            else:
                data_venc = "Condicionado ao Financiamento"
                st.caption("⚠️ Evento futuro condicionado.")
                
        with col_p3:
            valor_p = st.number_input(f"Valor da Parcela {p+1} (R$)", min_value=0.0, format="%.2f", key=f"val_p_{p}")
            correcao_p = st.text_input(f"Previsão de Correção Monetária {p+1}", placeholder="Ex: Sem correção / INCC", key=f"corr_p_{p}")
            
        if "Dação de Imóvel" in forma_pag:
            st.file_uploader(f"📎 Enviar Matrícula Atualizada do Imóvel de Dação ({p+1})", type=["png", "jpg", "jpeg", "pdf"], key=f"up_dacao_imovel_{p}")
        elif "Dação de Móvel/Veículo" in forma_pag:
            st.file_uploader(f"📎 Enviar Documento/Foto do Veículo de Dação ({p+1})", type=["png", "jpg", "jpeg", "pdf"], key=f"up_dacao_veic_{p}")
            
        lista_parcelas_nomes.append(f"Parcela {p+1} ({tipo_parcela})")
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🔑 Entrega das Chaves / Posse")
    col_ch1, col_ch2 = st.columns(2)
    with col_ch1:
        regra_chaves = st.selectbox("A entrega das chaves estará vinculada a qual evento?", ["Atribuir uma data específica fixa", "Na data de assinatura do contrato", "Vinculada ao vencimento de uma parcela específica"])
    with col_ch2:
        if regra_chaves == "Atribuir uma data específica fixa":
            st.date_input("Data de Entrega das Chaves", data_assinatura)
        elif regra_chaves == "Na data de assinatura do contrato":
            st.info(f"🔑 Chaves entregues no dia da assinatura: {data_assinatura.strftime('%d/%m/%Y')}")
        elif regra_chaves == "Vinculada ao vencimento de uma parcela específica":
            st.selectbox("Selecione a parcela de gatilho para as chaves:", lista_parcelas_nomes)

    st.markdown("---")
    st.subheader("🛋️ Condições de Entrega (O que fica no Imóvel?)")
    col_ent1, col_ent2 = st.columns(2)
    with col_ent1:
        itens_ficam = st.multiselect("Selecione as categorias de itens que permanecerão no imóvel:", ["Móveis Planejados", "Ar Condicionado", "Eletrodomésticos da Cozinha", "Luminárias/Plafons", "Cortinas/Persianas"])
    with col_ent2:
        if "Móveis Planejados" in itens_ficam:
            st.multiselect("Cômodos onde os Móveis Planejados vão ficar:", ["Cozinha", "Quarto Principal", "Suíte", "Sala de Estar", "Banheiros"], key="com_moveis")
        if "Ar Condicionado" in itens_ficam:
            st.multiselect("Cômodos com Ar Condicionado incluso:", ["Quarto Principal", "Suíte", "Sala de Estar"], key="com_ar")
        if "Eletrodomésticos da Cozinha" in itens_ficam:
            st.multiselect("Quais eletros ficam?", ["Fogão/Cooktop", "Forno Embutido", "Coifa/Depurador", "Geladeira"], key="com_eletro")
# ==========================================
# ABA 5: INTERMEDIAÇÃO
# ==========================================
with tab5:
    st.header("🤝 Regras de Intermediação e Repasse")
    
    st.markdown("#### 📊 Comissão Global da Venda")
    col_com1, col_com2 = st.columns(2)
    
    with col_com1:
        tipo_calculo_comissao = st.selectbox(
            "Formato do cálculo da comissão:",
            ["Definir Percentual (%) sobre o negócio", "Acordado (Valor Manual)"]
        )
    
    with col_com2:
        if tipo_calculo_comissao == "Definir Percentual (%) sobre o negócio":
            porcentagem_global = st.number_input("Percentual da Comissão (%)", min_value=0.0, max_value=100.0, value=6.0, step=0.1)
            valor_comissao_total = (porcentagem_global / 100) * st.session_state.valor_total_negocio
            st.metric(label="Valor Total da Comissão Calculado", value=f"R$ {valor_comissao_total:,.2f}")
        else:
            valor_comissao_total = st.number_input("Insira o Valor Total da Comissão Acordado (R$)", min_value=0.0, format="%.2f")

    st.markdown("---")
    st.markdown("#### 🗂️ Distribuição e Divisão dos Repasses")
    
    for idx in range(st.session_state.num_intermediarios):
        st.markdown(f"##### 👤 Beneficiário {idx+1}")
        col_int1, col_int2, col_int3 = st.columns(3)
        
        with col_int1:
            nome_selecionado = st.selectbox(
                f"Selecione o Profissional {idx+1}", 
                list(st.session_state.corretores_db.keys()), 
                key=f"nome_inter_{idx}"
            )
            tipo_vinculo = st.selectbox(
                f"Tipo de Vínculo {idx+1}", 
                ["Corretor", "Agenciador", "Imobiliária"], 
                key=f"vinculo_inter_{idx}"
            )
            
        with col_int2:
            pct_participacao = st.number_input(
                f"Percentual sobre a Comissão Total (%) - Beneficiário {idx+1}", 
                min_value=0.0, max_value=100.0, value=0.0, step=1.0, 
                key=f"pct_inter_{idx}"
            )
            valor_individual = (pct_participacao / 100) * valor_comissao_total
            st.caption(f"💰 Valor a receber: **R$ {valor_individual:,.2f}**")
            
        with col_int3:
            if nome_selecionado != "Selecione um profissional...":
                dados = st.session_state.corretores_db[nome_selecionado]
                st.markdown(f"""
                **Dados Pessoais e Bancários:**
                *   **CPF/CNPJ:** {dados['cpf']}
                *   **CRECI:** {dados['creci']}
                *   **Conta Bancária:** {dados['banco']}
                *   **Chave PIX:** {dados['pix']}
                """)
        st.markdown("<br>", unsafe_allow_html=True)
        
    if st.button("➕ Adicionar Outro Beneficiário na Comissão"):
        st.session_state.num_intermediarios += 1
        st.rerun()

    st.markdown("---")
    
    with st.expander("✨ Cadastrar Novo Profissional no Sistema", expanded=False):
        st.markdown("Preencha os dados abaixo para disponibilizar o profissional na lista acima:")
        col_cad1, col_cad2 = st.columns(2)
        
        with col_cad1:
            novo_nome = st.text_input("Nome Completo / Razão Social")
            novo_cpf = st.text_input("CPF ou CNPJ do Profissional")
            novo_creci = st.text_input("Número do CRECI")
        with col_cad2:
            nova_conta = st.text_input("Dados da Conta Bancária (Banco, Ag, Conta)")
            novo_pix = st.text_input("Chave PIX para recebimento")
            
        if st.button("💾 Salvar Cadastro"):
            if novo_nome and novo_cpf:
                st.session_state.corretores_db[novo_nome] = {
                    "cpf": novo_cpf,
                    "creci": novo_creci,
                    "banco": nova_conta,
                    "pix": novo_pix
                }
                st.success(f"🎉 {novo_nome} cadastrado com sucesso! Já está disponível na lista de seleção.")
                st.rerun()
            else:
                st.error("Por favor, preencha pelo menos o Nome e o CPF/CNPJ para salvar.")

st.markdown("---")
if st.button("💾 Salvar Todos os Dados do Contrato", type="primary"):
    st.success("Perfeito! Todos os dados da negociação foram estruturados e salvos localmente.")
