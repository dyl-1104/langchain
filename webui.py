import sys
import streamlit as st
import streamlit_antd_components as sac
import yaml
import os

from chatchat import __version__
from chatchat.server.utils import api_address
from chatchat.webui_pages.dialogue.dialogue import dialogue_page
from chatchat.webui_pages.kb_chat import kb_chat
from chatchat.webui_pages.knowledge_base.knowledge_base import knowledge_base_page
from chatchat.webui_pages.utils import *

api = ApiRequest(base_url=api_address())

def yaml_management_page():
    """模型选择管理页面"""
    st.title("模型选择管理")
    yaml_file_path = r"D:\path\to\chatchat_data\model_settings.yaml"  # 假设 YAML 文件路径为 config.yaml

    # 检查文件是否存在，如果不存在则创建一个空的 YAML 文件
    if not os.path.exists(yaml_file_path):
        with open(yaml_file_path, "w", encoding='utf-8') as f:
            yaml.dump({}, f)

    # 读取 YAML 文件内容
    with open(yaml_file_path, "r", encoding='utf-8') as f:
        yaml_data = yaml.safe_load(f)

    # 提供修改特定字段的接口
    st.header("修改特定配置项")

    # 修改 api_base_url
    st.subheader("修改 API 基础地址")
    current_api_base_url = yaml_data.get("MODEL_PLATFORMS", [{}])[0].get("api_base_url", "")
    new_api_base_url = st.text_input("输入新的 API 基础地址", value=current_api_base_url)
    if st.button("保存 API 基础地址"):
        yaml_data["MODEL_PLATFORMS"][0]["api_base_url"] = new_api_base_url
        with open(yaml_file_path, "w") as f:
            yaml.dump(yaml_data, f)
        st.success("API 基础地址已更新，请刷新页面")

    # 修改 api_key
    st.subheader("修改 API 密钥")
    current_api_key = yaml_data.get("MODEL_PLATFORMS", [{}])[0].get("api_key", "")
    new_api_key = st.text_input("输入新的 API 密钥", value=current_api_key)
    if st.button("保存 API 密钥"):
        yaml_data["MODEL_PLATFORMS"][0]["api_key"] = new_api_key
        with open(yaml_file_path, "w") as f:
            yaml.dump(yaml_data, f)
        st.success("API 密钥已更新，请刷新页面")

    # 修改 llm_models
    st.subheader("修改 LLM 模型列表")
    current_llm_models = yaml_data.get("MODEL_PLATFORMS", [{}])[0].get("llm_models", [])
    new_llm_models = st.text_area("输入新的 LLM 模型列表（每行一个模型名称）", value="\n".join(current_llm_models))
    if st.button("保存 LLM 模型列表"):
        new_llm_models_list = [model.strip() for model in new_llm_models.split("\n") if model.strip()]
        yaml_data["MODEL_PLATFORMS"][0]["llm_models"] = new_llm_models_list
        with open(yaml_file_path, "w") as f:
            yaml.dump(yaml_data, f)
        st.success("LLM 模型列表已更新,请刷新页面")


if __name__ == "__main__":
    is_lite = "lite" in sys.argv  # TODO: remove lite mode

    st.set_page_config(
        "Langchain-Chatchat WebUI",
        get_img_base64("chatchat_icon_blue_square_v2.png"),
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com/chatchat-space/Langchain-Chatchat",
            "Report a bug": "https://github.com/chatchat-space/Langchain-Chatchat/issues",
            "About": f"""欢迎使用 Langchain-Chatchat WebUI {__version__}！""",
        },
        layout="centered",
    )

    st.markdown(
        """
        <style>
        [data-testid="stSidebarUserContent"] {
            padding-top: 20px;
        }
        .block-container {
            padding-top: 25px;
        }
        [data-testid="stBottomBlockContainer"] {
            padding-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.image(
            get_img_base64("logo-long-chatchat-trans-v2.png"), use_column_width=True
        )
        st.caption(
            f"""<p align="right">当前版本：{__version__}</p>""",
            unsafe_allow_html=True,
        )

        selected_page = sac.menu(
            [
                sac.MenuItem("多功能对话", icon="chat"),
                sac.MenuItem("RAG 对话", icon="database"),
                sac.MenuItem("知识库管理", icon="hdd-stack"),
                sac.MenuItem("模型选择管理", icon="file-earmark-code"),  # 新增 YAML 文件管理菜单项
            ],
            key="selected_page",
            open_index=0,
        )

        sac.divider()

    if selected_page == "知识库管理":
        knowledge_base_page(api=api, is_lite=is_lite)
    elif selected_page == "RAG 对话":
        kb_chat(api=api)
    elif selected_page == "多功能对话":
        dialogue_page(api=api, is_lite=is_lite)
    elif selected_page == "模型选择管理":  # 新增 YAML 文件管理页面
        yaml_management_page()