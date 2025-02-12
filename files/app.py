import streamlit as st
import qrcode
import qrcode.constants
from PIL import Image
import io

# Configuração da página Web
st.set_page_config(
    layout="centered",
    page_title="Gerador de QR Code",
    page_icon="icone.png"
)

st.title("Gerador de QR Code")  # Título da página

# Lista de cores disponíveis para o QR Code e o fundo
CORES_PRIMARIAS = {
    "Preto": "black",
    "Branco": "white",
    "Vermelho": "red",
    "Azul": "blue",
    "Amarelo": "yellow"
}

# Entrada da URL pelo usuário
url = st.text_input("Insira a URL neste espaço", placeholder="http://exemplo.com")

# Seleção de cores
col1, col2 = st.columns(2)
with col1:
    cor_qr = st.selectbox("Escolha a cor do QR Code", list(CORES_PRIMARIAS.keys()), index=0)
with col2:
    cor_fundo = st.selectbox("Escolha a cor do fundo", list(CORES_PRIMARIAS.keys()), index=1)

# Função para gerar o QR Code
def gerar_qrcode(url, cor_qr, cor_fundo):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=CORES_PRIMARIAS[cor_qr], back_color=CORES_PRIMARIAS[cor_fundo])
    return img.get_image()

# Verifica se o usuário inseriu uma URL válida
if url:
    if CORES_PRIMARIAS[cor_qr] == CORES_PRIMARIAS[cor_fundo]:
        st.warning("⚠️ Escolha cores diferentes para o QR Code e o fundo para garantir a leitura correta!")
    else:
        # Geração do QR Code
        pil_img = gerar_qrcode(url, cor_qr, cor_fundo)

        # Exibir o QR Code
        st.image(pil_img, caption="Seu QR Code", use_container_width=True)

        # Salvar a imagem para download
        buf = io.BytesIO()
        pil_img.save(buf, format="PNG")
        byte_im = buf.getvalue()

        # Botão para baixar o QR Code
        col1, col2, col3 = st.columns([1, 0.4, 1])
        with col2:
            st.download_button(
                label="Baixar QR Code",
                data=byte_im,
                file_name="qrcode.png",
                mime="image/png"
            )