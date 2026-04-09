import streamlit as st
from src.services.agent.graph import graph as agent_app
from src.core.config import Config
from src.core.logger import logger

# --- СЛОВАРЬ ЛОКАЛИЗАЦИИ ---
LANG_DICT = {
    "EN": {
        "title": "📊 AI Data Analyst",
        "sidebar_title": "Settings",
        "model_label": "Model:",
        "sys_status": "System Status",
        "quick_queries": "Quick Queries",
        "clear_chat": "Clear Chat",
        "input_placeholder": "Ask something about your data...",
        "thinking": "Analysing database structure...",
        "log_title": "Execution Logs",
        "sql_label": "View Generated SQL",
        "error_msg": "System Error:",
        "btn_top_price": "Top 5 expensive items",
        "btn_payments": "Payment statistics",
        "system_lang": "Respond in English."
    },
    "RU": {
        "title": "📊 AI Аналитик БД",
        "sidebar_title": "Настройки",
        "model_label": "Модель:",
        "sys_status": "Состояние системы",
        "quick_queries": "Быстрые запросы",
        "clear_chat": "Очистить историю",
        "input_placeholder": "Задайте вопрос по данным...",
        "thinking": "Анализирую структуру БД...",
        "log_title": "Логи выполнения",
        "sql_label": "Показать SQL запрос",
        "error_msg": "Ошибка системы:",
        "btn_top_price": "Топ-5 дорогих товаров",
        "btn_payments": "Статистика платежей",
        "system_lang": "Отвечай строго на русском языке."
    }
}


st.set_page_config(
    page_title="InsightSQL",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


if "lang" not in st.session_state:
    st.session_state.lang = "EN"
if "messages" not in st.session_state:
    st.session_state.messages = []

L = LANG_DICT[st.session_state.lang]

with st.sidebar:
    st.title("⚙️ " + L["sidebar_title"])

    selected_lang = st.selectbox("🌐 Language / Язык", ["EN", "RU"],
                                 index=0 if st.session_state.lang == "EN" else 1)

    if selected_lang != st.session_state.lang:
        st.session_state.lang = selected_lang
        st.rerun()

    st.divider()

    model_name = getattr(Config, "MODEL_NAME", "qwen2.5-coder:3b")
    st.info(f"**{L['model_label']}** `{model_name}`")

    with st.expander(L["sys_status"], expanded=True):
        st.write("🟢 **DB:** Online")
        st.write("🟢 **Vector:** Active")

    st.markdown(f"### 💡 {L['quick_queries']}")
    if st.button(L["btn_top_price"], use_container_width=True):
        st.session_state.active_prompt = "Show 5 most expensive products" if st.session_state.lang == "EN" else "Покажи 5 самых дорогих товаров"
        st.rerun()

    if st.button(L["btn_payments"], use_container_width=True):
        st.session_state.active_prompt = "What are the most popular payment types?" if st.session_state.lang == "EN" else "Какие типы оплаты самые популярные?"
        st.rerun()

    st.divider()
    if st.button(L["clear_chat"], type="secondary", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- MAIN UI ---
st.title(L["title"])

# 1. Отрисовка истории сообщений
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sql"):
            with st.expander(L["sql_label"]):
                st.code(msg["sql"], language="sql")

# 2. Плейсхолдер для нового сообщения
chat_placeholder = st.container()


prompt = st.chat_input(L["input_placeholder"])


if "active_prompt" in st.session_state:
    prompt = st.session_state.pop("active_prompt")

# 4. ЛОГИКА ОБРАБОТКИ
if prompt:

    with chat_placeholder:
        with st.chat_message("user"):
            st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    with chat_placeholder:
        with st.chat_message("assistant"):
            with st.spinner(L["thinking"]):
                try:
                    query_with_lang = f"{L['system_lang']} Question: {prompt}"

                    result = agent_app.invoke({"question": query_with_lang})

                    answer = result.get("final_answer", "No response.")
                    sql = result.get("sql_query", "")

                    st.markdown(answer)
                    if sql:
                        with st.expander(L["sql_label"]):
                            st.code(sql, language="sql")

                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": answer,
                        "sql": sql
                    })
                except Exception as e:
                    error_msg = f"❌ {L['error_msg']} {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg})
                    logger.error(f"UI Error: {e}")

    # Финальная перезагрузка для очистки ввода и фиксации истории
    st.rerun()
