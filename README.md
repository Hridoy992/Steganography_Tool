# Image Steganography Tool 🔐

A cybersecurity lab project: a web app that hides secret text messages inside
images using **LSB (Least Significant Bit) steganography**, with optional
password-based **XOR encryption** for extra security.

## Features
- Hide any text message inside a PNG/JPG/BMP image
- Reveal a hidden message from a stego image
- Optional password protection (XOR cipher) before embedding
- Shows image capacity (max characters it can hold)
- Clean, simple Streamlit web interface
- "How it works" tab explaining the concept (great for viva/demo)

## How to Run

1. **Install Python** (3.8 or newer) if you don't have it already.

2. **Install the required libraries.** Open a terminal in this folder and run:
   ```
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```
   streamlit run app.py
   ```

4. Your browser will automatically open at `http://localhost:8501` — that's
   the app.

## How to Use

### Hiding a message
1. Go to the **"Hide Message"** tab.
2. Upload a cover image (a plain photo works fine, PNG is best).
3. Type your secret message.
4. (Optional) Check "Protect with a password" and set a password.
5. Click **"Hide Message"**.
6. Download the resulting **stego image** (PNG) — this looks identical to
   the original but secretly contains your message.

### Revealing a message
1. Go to the **"Reveal Message"** tab.
2. Upload the stego image (the PNG you downloaded earlier — do NOT
   re-save it as JPG, that will destroy the hidden data).
3. If it was password-protected, check the box and enter the same password.
4. Click **"Reveal Message"**.

## Project Structure
```
stego_project/
├── app.py              # Main Streamlit application (all logic + UI)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Concepts Demonstrated (for your report/viva)
- **Steganography**: hiding data within other data (here: image pixels)
- **LSB technique**: modifying the least significant bit of each color
  channel value — invisible to the human eye, but reconstructible bit by bit
- **Symmetric encryption (XOR cipher)**: an extra security layer, showing
  how encryption and steganography can be combined (encrypt-then-hide)
- **Capacity limits**: why the size of the cover image limits how much data
  can be hidden (3 bits per pixel here)

## Notes
- Always download/save the stego image as **PNG**. JPEG compression is lossy
  and will destroy the hidden bits.
- This is an educational project — XOR encryption is simple and NOT meant
  for real-world secure communication (use AES/RSA for that in production).
