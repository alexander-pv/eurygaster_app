import streamlit as st

import config as conf
import model_inference
import utils


def app() -> None:
    utils.download_weights()
    eurygaster_models = model_inference.EurygasterModels(models_config=(conf.bm_conf, conf.mm_conf))

    st.write("""
             # Eurygaster spp. classification
             """
             )
    file = st.file_uploader("Please, upload an image file", type=["jpg", "jpeg"])
    if file:

        pil_image = utils.open_image(file)

        if pil_image:
            st.image(pil_image, use_column_width=True)
            bin_result, eurg_result = eurygaster_models(pil_image=pil_image)

            st.write("Confidence that this is the picture of Eurygaster spp.:")
            st.write(bin_result)
            st.write("Confidence distribution of species if Eurygaster is in the picture:")
            st.write(eurg_result)

            if conf.gen_config.upload_images:
                utils.image_upload(file)

        else:
            st.write("The input contains undefined data. Perhaps it is a masked file of another data type.")
    else:
        st.text("No image input")


if __name__ == '__main__':
    app()
