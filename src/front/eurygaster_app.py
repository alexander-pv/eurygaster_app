import argparse

import streamlit as st

from pages import PlainTextPage, ModelPage


def parse_cli_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='eurygaster_app argument parser')
    parser.add_argument('--server', metavar='server', type=str, default='localhost:15000',
                        help='str, inference server address, template: "ip:port", default:localhost:15000')
    return parser.parse_args()


def main(args: argparse.Namespace) -> None:
    pages = {
        'About': PlainTextPage(title='About', markdown_name='about.md'),
        'How to use': PlainTextPage(title='How to use', markdown_name='how_to_use.md'),
        'Getting accurate recognition': PlainTextPage(title='Getting accurate recognition',
                                                      markdown_name='best_photo.md'),
        'Model': ModelPage(title='Model', backend=f"http://{args.server}/predict/eurygaster")
    }

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Sections", list(pages.keys()))
    selected_page = pages[selection]
    selected_lang = st.sidebar.selectbox('Language', ['ru', 'en'])

    with st.spinner(f"Loading {selection} ..."):
        selected_page.write(lang=selected_lang)


if __name__ == '__main__':
    main(parse_cli_args())
