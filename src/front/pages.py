import os
from abc import abstractmethod, ABCMeta
from typing import Optional

import plotly.graph_objects as go
import requests
import streamlit as st

import utils


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
            with open(os.path.join('front', 'markdown', lang, self.markdown_name), 'r', encoding='utf8') as f:
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

    def __init__(self, backend: str, binary_model_threshold: float = 0.5, *args, **kwargs):
        """
        Streamlit page with models inference
        :param eurygaster_models: EurygasterModels class
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.backend = backend
        self.binary_model_threshold = binary_model_threshold
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

    def post_predict(self, file) -> dict:
        return requests.post(self.backend,
                             files={"file": (f"{file.name};type=image/jpeg", file.getvalue()),
                                    "name": (None, file.name),
                                    }

                             ).json()

    def make_barplot(self, multiclass_output: dict) -> None:
        """
        Make a barplot for multiclass confidence values
        :param multiclass_output: output of the multiclass model
        :return:
        """
        sorted_output = sorted(multiclass_output.items(), key=lambda x: x[1], reverse=True)
        class_names, class_confidence = (x[0] for x in sorted_output), (float(x[1]) for x in sorted_output)
        fig = go.Figure([go.Bar(x=tuple(class_names), y=tuple(class_confidence))])
        fig.update_layout(yaxis_title='Class confidence', xaxis_title='Species')
        fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
        st.plotly_chart(fig, use_container_width=True)

    def write(self, lang: str) -> None:
        with st.spinner(f"Loading {self.title} ..."):
            self.set_title()
            msg = self.messages[lang]
            file = st.file_uploader(msg[0], type=["jpg", "jpeg"])
            if file:
                pil_image = utils.open_image(file)
                if pil_image:
                    st.image(pil_image, use_column_width=True)
                    res = self.post_predict(file)
                    st.write(msg[1])
                    st.write(res['binary'])
                    if float(res['binary']['Eurygaster']) > self.binary_model_threshold:
                        if float(res['binary']['Eurygaster']) > self.binary_model_threshold:
                            st.write(msg[2])
                            st.write(res['multiclass'])
                            self.make_barplot(res['multiclass'])

                else:
                    st.write(msg[3])
            else:
                st.text(msg[4])
            self.hide_style()
