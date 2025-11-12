# boat_checklist_manual.py
import streamlit as st

st.set_page_config(page_title="操船手順書", layout="centered")

st.title("🚤 船舶 操船時 手順書")

st.markdown("""
このページは操船時の「開始前」「終了後」チェックポイントをまとめた手順書です。  
出航前・帰港後の安全確認にご利用ください。
""")

# --- 開始前チェック ---
st.header("⚙️ 出航前チェック（START）")

start_steps = [
    "エンジンオイル量を確認",
    "冷却水量を確認",
    "燃料残量を確認",
    "航海計器（GPS・コンパス）動作確認",
    "無線機（通信）動作確認",
    "救命胴衣・救命具の搭載確認",
    "係留ロープ・アンカーの状態確認",
    "天候・潮汐・波高の確認",
]

for i, step in enumerate(start_steps, start=1):
    st.markdown(f"**{i}. {step}**")

st.divider()

# --- 終了後チェック ---
st.header("⚓ 帰港後チェック（END）")

end_steps = [
    "エンジン停止後、冷却状態を確認",
    "燃料漏れ・異音の有無を確認",
    "不要な電気機器をオフにする",
    "航海ログ（出航時刻・帰港時刻・燃料使用量など）を記入",
    "係留ロープ・フェンダーの状態確認",
    "乗員全員の下船確認",
    "備品回収・船内清掃",
]

for i, step in enumerate(end_steps, start=1):
    st.markdown(f"**{i}. {step}**")

st.divider()

# --- 注意事項 ---
st.header("📘 注意事項")
st.markdown("""
- 操船前には必ずエンジン周辺・燃料系統・電装系の目視確認を行うこと  
- 無線機の通信確認は他船または陸上局との短時間のテストで行う  
- 天候が急変した場合は直ちに帰港または安全な避難港へ  
- 操船記録は毎回残すこと（安全・メンテナンス管理のため）
""")

st.markdown("---")
st.caption("© 2025 操船安全管理マニュアル")
