import streamlit as st

import constants as const
import model_inference
import utils


def app() -> None:
    utils.download_weights()
    st.write("""
             # Eurygaster spp. classification
             """
             )
    file = st.file_uploader("Please, upload an image file", type=["jpg", "jpeg"])
    if file:

        pil_image = utils.open_image(file)

        if pil_image:
            st.image(pil_image, use_column_width=True)
            bin_result, eurg_result = model_inference.do_inference(pil_image=pil_image)

            st.write("Confidence that this is the picture of Eurygaster spp.:")
            st.write(bin_result)
            st.write("Confidence distribution of species if Eurygaster is in the picture:")
            st.write(eurg_result)

            if const.upload_images:
                utils.image_upload(file)

        else:
            st.write("The input contains undefined data. Perhaps it is a masked file of another data type.")
    else:
        st.text("No image input")


if __name__ == '__main__':
    app()
