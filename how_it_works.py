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
4. A special delimiter (`#####END#####`) marks where the hidden message ends,
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
