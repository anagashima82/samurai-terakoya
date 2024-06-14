import streamlit as st
import debugpy

# デバッグサーバーの設定
if not debugpy.is_client_connected():
    try:
        debugpy.listen(("localhost", 5679))
        print("Waiting for debugger attach...")
        debugpy.wait_for_client()
        print("Debugger attached")
    except Exception as e:
        print(f"Debugger connection failed: {e}")

# 5つの領域とそのキーワードのリスト
domains = {
    "健康・生活": [],
    "運動・感覚": [],
    "認知・行動": [],
    "言語・コミュニケーション": [],
    "人間関係・社会性": []
}

# Streamlitアプリの設定
st.title("フィードバックテストアプリ")
st.write("以下に入力した「ねらい」または「支援内容」が、5つの領域のどれに該当するかを判定します。")

# ユーザー入力
user_input = st.text_area("ねらいまたは支援内容を入力してください:")

# セッション状態の初期化
if 'show_feedback' not in st.session_state:
    st.session_state['show_feedback'] = False

if 'classification_result' not in st.session_state:
    st.session_state['classification_result'] = ""

if 'display_buttons' not in st.session_state:
    st.session_state['display_buttons'] = False

st.button("判定2")

# 判定ボタンがクリックされた場合の処理
if st.button("判定"):
    if user_input:
        # 仮の判定結果を表示
        result = "健康・生活"  # 仮の結果
        st.session_state['classification_result'] = result
        st.write(f"入力された内容は「{result}」領域に該当します。")

        # フィードバックの提供
        st.write("この分類は正しいですか？")
        st.session_state['display_buttons'] = True

# 「はい」「いいえ」のボタン表示と処理
if st.session_state['display_buttons']:
    feedback = False
    col1, col2 = st.columns(2)
    with col1:
        if st.button("はい", key="yes"):
            st.write("フィードバックありがとうございます！")
            feedback = False
            st.session_state['display_buttons'] = False
    with col2:
        if st.button("いいえ", key="no"):
            feedback = True
    st.session_state['show_feedback'] = feedback

# フィードバックが表示される場合の処理
if st.session_state['show_feedback']:
    correct_label = st.selectbox("正しい領域を選択してください:", list(domains.keys()))
    if st.button("送信", key="submit"):
        if correct_label:
            st.write(f"フィードバックを反映しました。選択された領域は「{correct_label}」です。")
            st.session_state['show_feedback'] = False
            st.session_state['classification_result'] = correct_label
