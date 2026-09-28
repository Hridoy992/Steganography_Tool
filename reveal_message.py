def xor_decrypt_from_hex(hex_text: str, key: str) -> str:
    """Reverse of xor_encrypt_decrypt when data was hex-encoded."""
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


def bits_to_message(bits: str) -> str:
    """Convert a string of '0'/'1' bits back into text."""
    chars = [bits[i : i + 8] for i in range(0, len(bits), 8)]
    message = ""
    for byte in chars:
        if len(byte) < 8:
            break
        message += chr(int(byte, 2))
    return message


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
