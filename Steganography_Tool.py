

import streamlit as st
from PIL import Image
import numpy as np
import io



DELIMITER = "END"


def xor_encrypt_decrypt(text: str, key: str) -> str:

    if not key:
        return text
    key_bytes = key.encode("utf-8")
    text_bytes = text.encode("utf-8")
    result = bytearray()
    for i, b in enumerate(text_bytes):
        result.append(b ^ key_bytes[i % len(key_bytes)])

    return result.hex()


def xor_decrypt_from_hex(hex_text: str, key: str) -> str:

    if not key:
        return hex_text
    try:
        data = bytes.fromhex(hex_text)
    except ValueError:
        return ""
    key_bytes = key.encode("utf-8")
    result = bytearray()
    for i, b in enumerate(data):
        result.append(b ^ key_bytes[i % len(key_bytes)])
    return result.decode("utf-8", errors="ignore")


def message_to_bits(message: str) -> str:

    return "".join(format(ord(char), "08b") for char in message)


def bits_to_message(bits: str) -> str:

    chars = [bits[i : i + 8] for i in range(0, len(bits), 8)]
    message = ""
    for byte in chars:
        if len(byte) < 8:
            break
        message += chr(int(byte, 2))
    return message


def get_max_capacity(image: Image.Image) -> int:
    """Maximum number of characters that can be hidden in the image."""
    width, height = image.size
    total_pixels = width * height

    return (total_pixels * 3) // 8


def encode_image(image: Image.Image, secret_message: str, password: str = "") -> Image.Image:

    image = image.convert("RGB")
    img_array = np.array(image)

    if password:
        secret_message = xor_encrypt_decrypt(secret_message, password)

    full_message = secret_message + DELIMITER
    binary_message = message_to_bits(full_message)
    message_len = len(binary_message)

    capacity = get_max_capacity(image)
    if message_len > capacity * 8:
        raise ValueError(
            f"Message too long! Max capacity for this image is ~{capacity} characters."
        )

    flat_pixels = img_array.flatten()

    for i in range(message_len):
        flat_pixels[i] = (flat_pixels[i] & 0xFE) | int(binary_message[i])

    encoded_array = flat_pixels.reshape(img_array.shape).astype(np.uint8)
    return Image.fromarray(encoded_array, "RGB")


def decode_image(image: Image.Image, password: str = "") -> str:
    """Extract a hidden message from an image encoded with encode_image."""
    image = image.convert("RGB")
    img_array = np.array(image)
    flat_pixels = img_array.flatten()

    bits = "".join(str(pixel & 1) for pixel in flat_pixels)
    decoded_message = bits_to_message(bits)

    if DELIMITER in decoded_message:
        decoded_message = decoded_message.split(DELIMITER)[0]
    else:
        return "⚠️ No hidden message found (or wrong password/image)."

    if password:
        decoded_message = xor_decrypt_from_hex(decoded_message, password)

    return decoded_message



# Streamlit UI

st.set_page_config(page_title="Image Steganography Tool", page_icon="🔐", layout="centered")

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* Page background: deep navy-to-violet gradient with soft glow accents */
.stApp {
    background:
        radial-gradient(circle at 15% 20%, rgba(0, 217, 255, 0.12) 0%, transparent 40%),
        radial-gradient(circle at 85% 80%, rgba(255, 46, 151, 0.12) 0%, transparent 40%),
        linear-gradient(160deg, #0b0d2a 0%, #17123f 45%, #1a0e33 100%);
    color: #e8e8f4;
    font-family: 'Space Grotesk', sans-serif;
}

/* Title */
h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    background: linear-gradient(90deg, #00d9ff 0%, #7b5cff 50%, #ff2e97 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

h2, h3 { color: #f1f0ff; font-family: 'Space Grotesk', sans-serif; }

/* Caption under the title */
[data-testid="stCaptionContainer"], .stCaption {
    color: #9d9dc7 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}
.stTabs [data-baseweb="tab"] {
    background-color: rgba(255,255,255,0.03);
    border-radius: 10px 10px 0 0;
    color: #9d9dc7;
    padding: 8px 18px;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, rgba(0,217,255,0.15), rgba(255,46,151,0.15));
    color: #ffffff !important;
    border-bottom: 2px solid #00d9ff;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #00d9ff 0%, #7b5cff 60%, #ff2e97 100%);
    color: #0b0d2a;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 0.55em 1.4em;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    box-shadow: 0 4px 18px rgba(123, 92, 255, 0.35);
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 22px rgba(0, 217, 255, 0.45);
    color: #0b0d2a;
}

/* Text areas / text inputs */
.stTextArea textarea, .stTextInput input {
    background-color: rgba(255,255,255,0.04) !important;
    color: #f1f0ff !important;
    border: 1px solid rgba(123, 92, 255, 0.35) !important;
    border-radius: 8px !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border: 1px solid #00d9ff !important;
    box-shadow: 0 0 0 1px #00d9ff !important;
}

/* File uploader */
[data-testid="stFileUploaderDropzone"] {
    background-color: rgba(255,255,255,0.03);
    border: 1px dashed rgba(0, 217, 255, 0.4);
    border-radius: 12px;
}

/* Checkbox label */
.stCheckbox label p { color: #d8d8f0 !important; }

/* Alerts (info / success / warning / error) get a colorful left border */
div[data-testid="stAlert"] {
    border-radius: 10px;
    background-color: rgba(255,255,255,0.04);
}

/* Code / monospace accents used for the delimiter or capacity text */
code {
    color: #00d9ff;
    background: rgba(0, 217, 255, 0.08);
}

/* Horizontal divider */
hr { border-color: rgba(255,255,255,0.08); }

/* Footer caption */
.footer-note { color: #75759e; font-size: 0.85em; }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.title("🔐 Image Steganography Tool")
st.caption("Hide and reveal secret messages inside images using LSB steganography")

tab1, tab2, tab3 = st.tabs(["🙈 Hide Message", "🔍 Reveal Message", "ℹ️ How it works"])

# ---------------- Hide Message Tab ----------------
with tab1:
    st.subheader("Hide a secret message inside an image")

    uploaded_file = st.file_uploader(
        "Upload a cover image (PNG recommended)", type=["png", "jpg", "jpeg", "bmp"], key="encode_uploader"
    )

    secret_message = st.text_area("Secret message to hide", height=120)

    use_password_enc = st.checkbox("Protect with a password (XOR encryption)")
    password_enc = ""
    if use_password_enc:
        password_enc = st.text_input("Password", type="password", key="enc_pw")

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Cover Image Preview", use_container_width=True)

        capacity = get_max_capacity(image)
        st.info(f"📦 Estimated capacity of this image: ~{capacity} characters")

        if st.button("🙈 Hide Message", type="primary"):
            if not secret_message:
                st.warning("Please enter a message to hide.")
            elif use_password_enc and not password_enc:
                st.warning("Please enter a password, or uncheck the password option.")
            else:
                try:
                    encoded_image = encode_image(image, secret_message, password_enc)

                    buf = io.BytesIO()
                    encoded_image.save(buf, format="PNG")
                    buf.seek(0)

                    st.success("✅ Message hidden successfully! Download the image below.")
                    st.image(encoded_image, caption="Stego Image (contains hidden data)", use_container_width=True)

                    st.download_button(
                        label="⬇️ Download Stego Image",
                        data=buf,
                        file_name="stego_image.png",
                        mime="image/png",
                    )
                except ValueError as e:
                    st.error(str(e))

# ---------------- Reveal Message Tab ----------------
with tab2:
    st.subheader("Reveal a hidden message from an image")

    stego_file = st.file_uploader(
        "Upload a stego image (must be PNG, not re-compressed)", type=["png", "bmp"], key="decode_uploader"
    )

    use_password_dec = st.checkbox("This image is password-protected")
    password_dec = ""
    if use_password_dec:
        password_dec = st.text_input("Password", type="password", key="dec_pw")

    if stego_file is not None:
        stego_image = Image.open(stego_file)
        st.image(stego_image, caption="Uploaded Image", use_container_width=True)

        if st.button("🔍 Reveal Message", type="primary"):
            result = decode_image(stego_image, password_dec)
            st.success("Extraction complete:")
            st.text_area("Hidden Message", value=result, height=120)

# ---------------- How it works Tab ----------------
with tab3:
    st.markdown(
        """
### How LSB Steganography Works

1. Every pixel in an RGB image has 3 color channels (**R**, **G**, **B**),
   each stored as an 8-bit number (0–255).
2. Changing the **last bit** (Least Significant Bit) of a color value only
   changes it by at most 1 — a change invisible to the human eye.
3. To hide a message, we convert each character into 8 bits (its ASCII
   binary code) and store **one bit per color channel** across the image's
   pixels.
4. A special delimiter (`END`) marks where the hidden message ends,
   so the decoder knows when to stop reading.
5. Optionally, the message is first **XOR-encrypted** with a password before
   being embedded, adding a second layer of security — even if someone
   knows steganography was used, they can't read the message without the key.

### Why PNG?
PNG uses **lossless compression**, so the exact bit values we set are
preserved. JPEG uses lossy compression and would corrupt the hidden bits,
so always save/download the stego image as PNG.

### Security Note
This project is built for educational / cybersecurity lab demonstration
purposes to illustrate **data hiding (steganography)** and basic
**symmetric encryption (XOR cipher)** concepts.
        """
    )


