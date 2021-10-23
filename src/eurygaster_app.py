import streamlit as st
from PIL import Image
import model_inference


def app() -> None:
    st.write("""
             # Eurygaster spp. classification
             """
             )
    file = st.file_uploader("Please, upload an image file", type=["jpg", "jpeg"])
    if file:
        pil_image = Image.open(file)
        st.image(pil_image, use_column_width=True)
        bin_result, eurg_result = model_inference.do_inference(pil_image=pil_image)

        st.write('Confidence that this is the picture of Eurygaster spp.:')
        st.write(bin_result)
        st.write('Confidence distribution of species if Eurygaster is in the picture:')
        st.write(eurg_result)
    else:
        st.text("No image input")


if __name__ == '__main__':
    app()
