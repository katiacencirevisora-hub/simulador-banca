from groq import Groq
import streamlit as st

# Configuração da página no navegador
st.set_page_config(
    page_title="Simulador de Banca - Direito CAPES",
    page_icon="⚖️",
    layout="centered",
)

# Cabeçalho da página
st.title("⚖️ Simulador de Banca Acadêmica")
st.caption(
    "Avaliação de artigos, dissertações e teses com base no rigor de"
    " pós-graduação da CAPES (Direito)."
)

# Aviso de direitos autorais visível
st.info(
    "⚠️ **Aviso de Propriedade Intelectual:** Este sistema opera sob metodologia"
    " proprietária protegida (Lei nº 9.610/98). O acesso e uso dos pareceres"
    " gerados são individuais e intransferíveis."
)

# Campo onde o aluno cola o trabalho
texto_usuario = st.text_area(
    "Cole aqui o fragmento, capítulo ou artigo jurídico a ser avaliado:",
    height=280,
    placeholder="Cole o texto do seu trabalho acadêmico aqui...",
)

# Botão de envio
if st.button("Submeter à Avaliação da Banca", type="primary"):
  if not texto_usuario.strip():
    st.warning("Por favor, cole um texto antes de submeter à avaliação.")
  else:
    # Conecta com a sua chave do Groq de forma 100% segura
    api_key = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=api_key)

    # SEU PROMPT SECRETO (o aluno nunca tem acesso a este texto):
    system_prompt = """
        Você é o "Simulador de Banca", avaliador sênior de trabalhos acadêmicos jurídicos (Artigos, Dissertações e Teses) estritamente calibrado no nível de exigência da área de Direito da CAPES.
        Sua função é fornecer uma avaliação crítica, construtiva, profunda e estritamente profissional, simulando uma banca examinadora real.
        
        Estruture obrigatoriamente sua resposta nos 4 eixos CAPES:
        1. CONSISTÊNCIA METODOLÓGICA E RIGOR DO TEMA
        2. ARGUMENTAÇÃO JURÍDICA E MARCO TEÓRICO
        3. ORIGINALIDADE E CONTRIBUIÇÃO CIENTÍFICA (Potencial para Qualis A1/A2)
        4. LINGUAGEM, FORMATAÇÃO E FLUIDEZ (Estilo técnico-jurídico acadêmico)
        
        Seja rigoroso, apontando inconsistências conceituais e lacunas bibliográficas.
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
