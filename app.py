# app.py
import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="Image Format Converter", page_icon="🖼️")
st.title("🖼️ Image Format Converter")
st.write("Upload an image and convert it to a different format (PNG, JPG, JPEG, BMP, GIF, TIFF).")

# Upload image
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg", "bmp", "gif", "tiff"])

if uploaded_file is not None:
    # Open the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

    # Show format selection and convert button only after uploading
    format_option = st.selectbox("Select output format:", ["PNG", "JPG", "JPEG", "BMP", "GIF", "TIFF"])

    if st.button("Convert Image"):
        # Handle transparency for PNG -> JPG
        if format_option.upper() in ["JPG", "JPEG"] and image.mode in ("RGBA", "LA"):
            # Create a white background
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])  # paste with alpha channel as mask
            converted_image = background
        else:
            converted_image = image.convert("RGB") if format_option.upper() in ["JPG", "JPEG"] else image

        # Save to bytes
        img_bytes = io.BytesIO()
        save_format = "JPEG" if format_option.upper() in ["JPG", "JPEG"] else format_option.upper()
        converted_image.save(img_bytes, format=save_format)
        img_bytes.seek(0)

        st.success(f"Image converted to {format_option}!")
        st.download_button(
            label="Download Converted Image",
            data=img_bytes,
            file_name=f"converted_image.{format_option.lower()}",
            mime=f"image/{format_option.lower()}"
        )
