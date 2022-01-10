import os
from abc import abstractmethod, ABCMeta
from typing import Optional

import streamlit as st

import config as conf
import utils
from model_inference import EurygasterModels


class Page(metaclass=ABCMeta):
    def __init__(self, title: str, markdown_name: Optional[str] = None):
        """
        Abstract class for streamlit pages
        :param title:         str, page title
        :param markdown_name: Optional[str], name of the markdown file to write
        """
        self.title = title
        self.markdown_name = markdown_name
        self.markdown_text = self.load_markdown()

    def load_markdown(self, lang: str = "ru") -> str:
        """
        Load markdown file
        :param lang: directory of the text for a specific language
        :return: str
        """
        if self.markdown_name:
            with open(os.path.join('markdown', lang, self.markdown_name), 'r', encoding='utf8') as f:
                text = ''.join(f.readlines())
        else:
            text = None
        return text

    def set_title(self) -> None:
        """
        Set title for a streamlit page
        :return: None
        """
        st.write(f"## Eurygaster spp. classification - {self.title}")

    @staticmethod
    def hide_style() -> None:
        """
        Hide streamlit style
        :return: None
        """
        hide_streamlit_style = """
                    <style>
                    #MainMenu {visibility: hidden;}
                    footer {visibility: hidden;}
                    </style>
                    """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    @abstractmethod
    def write(self, lang: str) -> None:
        """
        Write page
        :param lang: str, language of the text
        :return: None
        """
        return


class PlainTextPage(Page):

    def __init__(self, *args, **kwargs):
        """
        Streamlit page with text information about the project
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)

    def write(self, lang: str) -> None:
        with st.spinner(f"Loading {self.title} ..."):
            self.markdown_text = self.load_markdown(lang=lang)
            self.set_title()
            if self.markdown_text:
                st.markdown(self.markdown_text, unsafe_allow_html=True)
            self.hide_style()


class ModelPage(Page):

    def __init__(self, eurygaster_models: EurygasterModels, *args, **kwargs):
        """
        Streamlit page with models inference
        :param eurygaster_models: EurygasterModels class
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.eurygaster_models = eurygaster_models
        self.messages = {'ru': ("Пожалуйста, загрузите фотографию",
                                "Вероятность, что на фотографии Eurygaster spp.:",
                                "Распределение вероятностей принадлежности к каждому из видов Eurygaster:",
                                "На вход поданы некорректные данные.",
                                "Изображение не загружено"
                                ),
                         'en': ("Please, upload an image file",
                                "Confidence that this is the picture of Eurygaster spp.:",
                                "Confidence distribution of species if Eurygaster is in the picture:",
                                "The input contains undefined data. Perhaps it is a masked file of another data type.",
                                "No image input",
                                )
                         }

    def write(self, lang: str) -> None:
        with st.spinner(f"Loading {self.title} ..."):
            self.set_title()
            msg = self.messages[lang]

            file = st.file_uploader(msg[0], type=["jpg", "jpeg"])
            if file:
                pil_image = utils.open_image(file)
                if pil_image:
                    st.image(pil_image, use_column_width=True)
                    bin_result, eurg_result = self.eurygaster_models(pil_image=pil_image)

                    st.write(msg[1])
                    st.write(bin_result)
                    st.write(msg[2])
                    st.write(eurg_result)

                    if conf.gen_config.upload_images:
                        utils.image_upload(file)

                else:
                    st.write(msg[3])
            else:
                st.text(msg[4])
            self.hide_style()
