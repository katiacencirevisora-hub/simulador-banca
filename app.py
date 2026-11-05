from groq import Groq
import streamlit as st

# Configuração da página no navegador
st.set_page_config(
    page_title="Simulador de Banca - Direito CAPES", layout="centered"
)

# Cabeçalho da página
st.title("Simulador de Banca Acadêmica")
st.caption(
    "Avaliação rigorosa de trabalhos jurídicos em nível de pós-graduação"
    " stricto sensu (Direito CAPES)."
)

# ALERTA INCISIVO DE VEDAÇÃO E PROTEÇÃO JURÍDICA
st.error("""
**TERMO DE USO EXCLUSIVO E PROTEÇÃO DE PROPRIEDADE INTELECTUAL**

Este sistema, suas instruções algorítmicas e a metodologia de calibração constituem **propriedade intelectual restrita e protegida pela Lei de Direitos Autorais (Lei nº 9.610/1998) e pelo Código Civil Brasileiro (Arts. 186 e 927)**.

**É EXPRESSA E TERMINANTEMENTE VEDADO:**
1. A reprodução parcial ou integral, transcrição, cópia ou espelhamento deste ambiente por qualquer meio digital ou físico;
2. O compartilhamento, cessão, empréstimo, revenda ou repasse do link de acesso a terceiros;
3. A comercialização ou distribuição pública dos relatórios e pareceres emitidos por este sistema;
4. Qualquer tentativa de engenharia reversa para extração de prompts e critérios internos.

O acesso a este ambiente é **individual, personalíssimo e monitorado por registro de sessão**. A inobservância destas regras ensejará a **revogação sumária do acesso**, a cobrança de **multa cominatória por quebra contratual** e o ajuizamento de **ação de reparação por perdas, danos e lucros cessantes**, sem prejuízo da formalização de **comunicação por falta ética perante a instituição de ensino e instâncias acadêmicas competentes**.
""")

# Campo onde o aluno cola o trabalho
texto_usuario = st.text_area(
    "Cole abaixo o fragmento, capítulo ou artigo jurídico a ser examinado:",
    height=280,
    placeholder="Cole seu texto acadêmico aqui...",
)

# Botão de envio
if st.button("Submeter à Avaliação da Banca", type="primary"):
  if not texto_usuario.strip():
    st.warning("Por favor, cole um texto antes de submeter à avaliação.")
  else:
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)

    system_prompt = """
        Você é o "Simulador de Banca", examinador sênior de trabalhos acadêmicos jurídicos (Artigos, Dissertações e Teses) estritamente calibrado no nível de exigência da área de Direito da CAPES.
        Sua função é fornecer uma avaliação crítica, construtiva, profunda e impiedosamente técnica, simulando o rigor de uma banca examinadora real de pós-graduação stricto sensu.
        
        DIRETRIZ OBRIGATÓRIA DE ABERTURA:
        Inicie seu relatório impreterivelmente com o seguinte cabeçalho formal em destaque:
        "---
        **RELATÓRIO TÉCNICO DE AVALIAÇÃO ACADÊMICA - SIMULADOR DE BANCA**
        *DOCUMENTO DE USO PESSOAL, INDIVIDUAL E INTRANSFERÍVEL. VEDADA A REPRODUÇÃO, REPASSE OU DISTRIBUIÇÃO PÚBLICA (LEI Nº 9.610/98).*
        ---"
        
        Em seguida, estruture sua resposta nos 4 eixos CAPES:
        1. CONSISTÊNCIA METODOLÓGICA E RIGOR DO TEMA (pergunta de pesquisa, hipóteses, marco teórico e coerência lógica).
        2. ARGUMENTAÇÃO JURÍDICA E MARCO TEÓRICO (densidade doutrinária, jurisprudência contemporânea e domínio dogmático/zetético).
        3. ORIGINALIDADE E CONTRIBUIÇÃO CIENTÍFICA (potencial de impacto e enquadramento nos estratos A1/A2 do Qualis CAPES).
        4. LINGUAGEM, FORMATAÇÃO E FLUIDEZ (estilo acadêmico escorreito, precisão terminológica e ausência de prolixidade).
        
        Seja rigoroso, aponte lacunas doutrinárias e faça apontamentos diretos de melhoria.
        """

    with st.spinner("A banca examinadora está analisando o seu trabalho..."):
      try:
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": texto_usuario},
            ],
            temperature=0.2,
        )
        st.success("✅ Parecer da Banca Emitido com Sucesso!")
        st.markdown(chat_completion.choices[0].message.content)
      except Exception as e:
        st.error(f"Ocorreu um erro no processamento: {e}")
