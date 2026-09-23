DELIMITER = "#####END#####"  # marks the end of the hidden message


def xor_encrypt_decrypt(text: str, key: str) -> str:
    """Simple XOR cipher for password-based obfuscation (symmetric)."""
    if not key:
        return text
    key_bytes = key.encode("utf-8")
    text_bytes = text.encode("utf-8")
    result = bytearray()
    for i, b in enumerate(text_bytes):
        result.append(b ^ key_bytes[i % len(key_bytes)])
    # Represent as a hex string so it's safe to embed as text
    return result.hex()


def message_to_bits(message: str) -> str:
    """Convert a string into a string of '0'/'1' bits."""
    return "".join(format(ord(char), "08b") for char in message)


def get_max_capacity(image: Image.Image) -> int:
    """Maximum number of characters that can be hidden in the image."""
    width, height = image.size
    total_pixels = width * height
    # 3 usable bits per pixel (R, G, B) -> 1 char needs 8 bits
    return (total_pixels * 3) // 8


def encode_image(image: Image.Image, secret_message: str, password: str = "") -> Image.Image:
    """Hide secret_message inside image using LSB and return new image."""
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
