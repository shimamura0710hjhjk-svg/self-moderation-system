import streamlit as st
import json
import os
import random
import pandas as pd

# --- 0. セッション状態の初期化 ---
if 'history' not in st.session_state:
    st.session_state.history = {} 
if 'random_images' not in st.session_state:
    st.session_state.random_images = {} 

# 1. ページ設定
st.set_page_config(page_title="Self-Moderation System", layout="centered")

# --- 📱 画面制御 & レイアウトCSS ---
st.markdown("""
    <script>
        // 画面遷移（再描画）時に強制的に最上部へスクロールさせるJS
        window.parent.document.querySelector(".main").scrollTo(0,0);
    </script>
    <style>
    .block-container { max-width: 500px; padding-top: 1rem; }
    .banned-text { color: #ff4b4b; font-weight: bold; }
    .approved-text { color: #29b045; font-weight: bold; }
    /* ボタンの余白調整 */
    .stButton > button { margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ MODERATION CONSOLE")

# パス設定
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, 'contents_id.json')
IMG_EXTS = ('.png', '.jpg', '.jpeg', '.webp')
VID_EXTS = ('.mp4', '.mov', '.webm')

def load_data():
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"assets": []}

data = load_data()

# 規制理由
REASON_OPTIONS = ["--- 理由を選択してください ---", "性的コンテンツの混入", "未認証個体:深海鮟子（ふかみあんこ）の検知", "現実世界(Real)への過度な執着", "規律:Standard_Regulation_710 抵触", "その他（自由記述）"]

# --- 3. メインロジック ---
pending_assets = [a for a in data['assets'] if a['id'] not in st.session_state.history]

if pending_assets:
    # 進行状況
    progress = len(st.session_state.history) / len(data['assets'])
    st.progress(progress)
    
    # ターゲット選出ロジック (30個対応：ASSET-LOG-030を最後に固定)
    FINAL_ID = "ASSET-LOG-030"
    
    if 'current_target_id' not in st.session_state or st.session_state.current_target_id not in [a['id'] for a in pending_assets]:
        normal_pool = [a for a in pending_assets if a['id'] != FINAL_ID]
        if normal_pool:
            st.session_state.current_target_id = random.choice(normal_pool)['id']
        else:
            st.session_state.current_target_id = FINAL_ID
    
    asset = next(a for a in pending_assets if a['id'] == st.session_state.current_target_id)
    
    # IDとラベル
    st.subheader(f"ID: {asset['id']}")
    st.caption(f"CATEGORY: {asset.get('category')}")
    st.write(f"**LABEL:** {asset.get('label', 'N/A')}")

    # メディア表示
    rel_path = asset.get('folder_path', '')
    full_path = os.path.join(current_dir, rel_path.replace('/', os.sep))

    if asset['id'] not in st.session_state.random_images:
        try:
            if os.path.isdir(full_path):
                files = [f for f in os.listdir(full_path) if f.lower().endswith(IMG_EXTS + VID_EXTS)]
                if files:
                    st.session_state.random_images[asset['id']] = os.path.join(full_path, random.choice(files))
        except: pass

    target_file = st.session_state.random_images.get(asset['id'])
    if target_file and os.path.exists(target_file):
        ext = os.path.splitext(target_file)[1].lower()
        if ext in IMG_EXTS: st.image(target_file, use_column_width=True)
        elif ext in VID_EXTS: st.video(target_file)
    else:
        st.warning("⚠️ ASSET NOT FOUND")

    # 操作エリア
    st.write("---")
    selected_reason = st.selectbox("REGULATION REASON", options=REASON_OPTIONS, key=f"sel_{asset['id']}")
    final_reason = selected_reason
    if selected_reason == "その他（自由記述）":
        custom_reason = st.text_area("違反詳細", placeholder="記述...")
        final_reason = f"その他: {custom_reason}"

    c1, c2 = st.columns(2)
    with c1:
        can_ban = (selected_reason != REASON_OPTIONS[0]) and (not (selected_reason == "その他（自由記述）" and not custom_reason))
        if st.button("🔴 BAN", use_container_width=True, disabled=not can_ban):
            st.session_state.history[asset['id']] = {"result": "BANNED", "reason": final_reason}
            st.rerun()
    with c2:
        if st.button("🟢 APPROVE", use_container_width=True):
            st.session_state.history[asset['id']] = {"result": "APPROVED", "reason": "N/A (Approved)"}
            st.rerun()

else:
    # 4. 完了画面
    st.balloons()
    st.success("🏁 全アセット執行完了")
    results_df = pd.DataFrame([{"ID": k, "Res": v['result'], "Reason": v['reason']} for k, v in st.session_state.history.items()])
    
    st.subheader("Final Execution Log")
    for _, row in results_df.iterrows():
        res_style = "banned-text" if row['Res'] == "BANNED" else "approved-text"
        st.markdown(f"**{row['ID']}**: <span class='{res_style}'>{row['Res']}</span><br><small>{row['Reason']}</small>", unsafe_allow_html=True)

    if st.sidebar.button("REBOOT"):
        st.session_state.history = {}
        st.session_state.random_images = {}
        if 'current_target_id' in st.session_state: del st.session_state.current_target_id
        st.rerun()