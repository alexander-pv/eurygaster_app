import streamlit as st

from backend import model_inference
from backend import utils
from backend import config as conf

from front.pages import PlainTextPage, ModelPage


def main() -> None:
    utils.download_weights()
    eurygaster_models = model_inference.EurygasterModels(models_config=(conf.bm_conf, conf.mm_conf))
    pages = {
        'About': PlainTextPage(title='About', markdown_name='about.md'),
        'How to use': PlainTextPage(title='How to use', markdown_name='how_to_use.md'),
        'Getting accurate recognition': PlainTextPage(title='Getting accurate recognition',
                                                      markdown_name='best_photo.md'),
        'Model': ModelPage(title='Model', eurygaster_models=eurygaster_models)
    }

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Sections", list(pages.keys()))
    selected_page = pages[selection]
    selected_lang = st.sidebar.selectbox('Language', ['ru', 'en'])

    with st.spinner(f"Loading {selection} ..."):
        selected_page.write(lang=selected_lang)


if __name__ == '__main__':
    main()
