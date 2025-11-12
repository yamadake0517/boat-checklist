# boat_checklist_dropbox_v4.py
import streamlit as st
import pandas as pd
from datetime import datetime, date
import dropbox
from io import BytesIO

# -----------------------
# Dropbox 設定
# -----------------------
DROPBOX_TOKEN = "sl.u.AGHzs4C-L4fVJPfn951Z21Wg4J98jJgpZq9fOPp84vfulXXJogNCJGPA968WxOuwR4qo_nsEYj_XAtNeCom2P3xgD0AQPmWiTMAl-r31yCPkB-GnTL4prmkyQRubJNYiS4p9FY-a99haFqOWkJ7HvKvV9z-rhYD-CjO_ji5yZCVpb0nZ6hE94oacCJnGUKouM6AARVtW2ezUgvs4Nrbq8dcf7RvqfyiGfWW6NjAc7RpxuEIs7quU5flVgQHcSQvYC21nJp-01E85BUHyvARuv_um83fAKMc70_mBgiQwZZgxmPOE1DIbWS1MuN68d_0Bi1B9p2V0xpX9F4-Z_y33G6avuEe5-5bqHdNWuWVuciN9sNp_ICpvqIg4D6ea7lQO_H788JOAftoGDo-s0uKGlwA7UVlM_uSjs5tN2K55nrzJOcLgWnMfeCflTqIVeXX84cR7Q-aVD5FJB2qnq6WMsPuNZxJ7eVqb5NAEoM3esm4i_T5PoyTR5rW98FMDVaWyIu0MbgGWP1_DTLDsjBQ9Z8zlqmg0Sxa7Oa0ES6Oop3r3Lcch3Ia0IDZyWgcwdOCcF02pFJ786wr5y8Q-OoEw08dyMj8WWfv7DlPR7Ki3uls6LJ_eAGBltYv_bgN6fRFXe4jdeKVPm7Vi-0s2JjeQEXF-PXa2QXcZ4tA-Nj19Nr6FzsX3lmsTtUo7apXGhUvvMqCJmgPZiEJbwKw7XLlrf9cmlFYqWWOi_jY4KGcAefw1yeSfg83gQmvO4Bm14Wf3YGXaSLwpogY2H843xhneCYbwCDLXO4gIighSFUNehpupRhxzpVnCSe2Q962PozXQ31ZUQNXBMKZPU0MNvP_8UbJQAdX3gbjfnhXthysCw-o3XEaiRMcau4Lsij0CQRV9iyUkBHxOFNn91R6xUdbRRPYVgzDSiK9R5I8eGaZzjX9Ufc9hAxE2wL1GTsmNqodQyHJdrE2DX45uy78y61tAdo-j6nMzF2wQyikkDZaVvlF2wVqSBmaim18qLg1pMvr7H3SJlmHZHxHnhigQx6MKDvmtRSlq9IwoRi-xlure0KjRBWb7ViBleEYvgMyk3N80jjT3GQYDwUuaB55eQDQVMwWGDW2F9G63Zjd3j-612ibOkDFDHl_QygB8fzt05vsM-esE_eTlA_ev3xIaXCdZHIMnckNiB5F2t_6bcXoHpx_9K9M_YtwRGEHlpNBSJywOuHDAAgAWs2eyf8Fq2rXfHqw6vXxI4Iez9GDWz4kPTmQpszaBz-jPNKu3US900cWJ1yU"  # 新しいトークンに置き換える
DROPBOX_FOLDER = "/釣りアプリ"
DROPBOX_CSV_PATH = f"{DROPBOX_FOLDER}/voyage_records.csv"
dbx = dropbox.Dropbox(DROPBOX_TOKEN)

# -----------------------
# Streamlit 設定
# -----------------------
st.set_page_config(page_title="操船手順書＆航海記録", layout="centered")
page = st.sidebar.radio("ページ選択", ["手順書", "航海記録入力", "航海記録閲覧"])

# -----------------------
# CSV読み込み関数
# -----------------------
def load_csv_from_dropbox():
    try:
        _, res = dbx.files_download(DROPBOX_CSV_PATH)
        df = pd.read_csv(BytesIO(res.content))
        df = df.fillna("")  # NaNを空文字に置換
        return df
    except:
        return pd.DataFrame(columns=[
            "出航日", "出航時刻", "帰港時刻",
            "釣果写真URL", "トラブル写真URL", "登録日時"
        ])

# CSV読み込み
df = load_csv_from_dropbox()

# -----------------------
# CSV保存関数
# -----------------------
def save_csv_to_dropbox(df):
    with BytesIO() as f:
        df.to_csv(f, index=False)
        f.seek(0)
        dbx.files_upload(f.read(), DROPBOX_CSV_PATH, mode=dropbox.files.WriteMode.overwrite)

# ==========================
# ページ①：手順書
# ==========================
if page == "手順書":
    st.title("🚤 船舶 操船時 手順書")
    st.markdown("""
このページは操船時の「開始前」「終了後」チェックポイントをまとめた手順書です。  
出航前・帰港後の安全確認にご利用ください。
""")
    st.header("⚙️ 出航前チェック（START）")
    start_steps = [
        "メインブレーカーを入れる",
        "スクリューを降ろす",
        "30分の暖機運転",
        "冷却水が出ているか確認",
        "燃料残量を確認",
        "ライト動作確認",
        "車のカギ確認",
        "救命胴衣確認",
        "係留ロープ・アンカーの状態確認",
        "天候・潮汐・波高の確認",
    ]
    for i, step in enumerate(start_steps, start=1):
        st.markdown(f"**{i}. {step}**")

    st.divider()
    st.header("⚓ 帰港後チェック（END）")
    end_steps = [
        "エンジン停止後、冷却状態を確認",
        "燃料漏れ・異音の有無を確認",
        "ブレーカーを降ろす",
        "スクリューを降ろす",
        "係留ロープ・フェンダーの状態確認",
        "備品回収・船内清掃",
    ]
    for i, step in enumerate(end_steps, start=1):
        st.markdown(f"**{i}. {step}**")

    st.divider()
    st.header("📘 注意事項")
    st.markdown("""
- 操船前には必ずエンジン周辺・燃料系統・電装系の目視確認を行うこと  
- 無線機の通信確認は他船または陸上局との短時間のテストで行う  
- 天候が急変した場合は直ちに帰港または安全な避難港へ  
- 操船記録は毎回残すこと（安全・メンテナンス管理のため）
""")
    st.markdown("---")
    st.markdown("📍 **漁礁ポイント（Googleマップ）** [こちらを開く](https://www.google.com/maps/d/edit?mid=1h6m8fXg0UpW2BKKGzVcydgSmsGPf_Rk&usp=sharing)")
    st.caption("© 2025 操船安全管理マニュアル")

# ==========================
# ページ②：航海記録入力
# ==========================
elif page == "航海記録入力":
    st.title("📝 航海記録入力")

    with st.form("voyage_form"):
        depart_date = st.date_input("出航日", date.today())
        depart_time = st.time_input("出航時刻", datetime.now().time())
        return_time = st.time_input("帰港時刻", datetime.now().time())
        catch_photo = st.file_uploader("釣果写真", type=["jpg","png","jpeg"])
        trouble_photo = st.file_uploader("トラブル写真", type=["jpg","png","jpeg"])
        submitted = st.form_submit_button("記録保存")

        if submitted:
            # Dropbox にアップロードして共有リンクを生成
            def upload_to_dropbox(file):
                path = f"{DROPBOX_FOLDER}/{file.name}"
                dbx.files_upload(file.read(), path, mode=dropbox.files.WriteMode.overwrite)
                shared_link = dbx.sharing_create_shared_link_with_settings(path)
                return shared_link.url.replace("?dl=0", "?dl=1")

            catch_url = upload_to_dropbox(catch_photo) if catch_photo else ""
            trouble_url = upload_to_dropbox(trouble_photo) if trouble_photo else ""

            new_record = {
                "出航日": depart_date.strftime("%Y-%m-%d"),
                "出航時刻": depart_time.strftime("%H:%M"),
                "帰港時刻": return_time.strftime("%H:%M"),
                "釣果写真URL": catch_url,
                "トラブル写真URL": trouble_url,
                "登録日時": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            df = pd.concat([df, pd.DataFrame([new_record])], ignore_index=True)
            save_csv_to_dropbox(df)
            st.success("航海記録を Dropbox に保存しました！")

# ==========================
# ページ③：航海記録閲覧
# ==========================
elif page == "航海記録閲覧":
    st.title("📂 航海記録一覧")
    df = load_csv_from_dropbox()  # 最新データをDropboxから取得

    if df.empty:
        st.info("まだ航海記録はありません。")
    else:
        # 表示用コピーを作成（写真はリンク化）
        df_display = df.copy()
        df_display["釣果写真"] = df_display["釣果写真URL"].apply(
            lambda x: f"[リンク]({x})" if isinstance(x, str) and x else ""
        )
        df_display["トラブル写真"] = df_display["トラブル写真URL"].apply(
            lambda x: f"[リンク]({x})" if isinstance(x, str) and x else ""
        )
        df_display = df_display.drop(columns=["釣果写真URL", "トラブル写真URL"])

        st.dataframe(df_display)

        st.markdown("---")
        st.subheader("❌ 航海記録の削除")

        # 削除対象の選択
        options = [f"{i+1}: {row['出航日']} {row['出航時刻']}" for i, row in df.iterrows()]
        selected_idx = st.selectbox("削除する記録を選択してください", options)

        if st.button("削除"):
            idx_to_delete = int(selected_idx.split(":")[0]) - 1
            # 画像も削除したい場合はここで dbx.files_delete_v2() を呼ぶことも可能
            df = df.drop(index=idx_to_delete).reset_index(drop=True)
            save_csv_to_dropbox(df)
            st.success(f"記録 {selected_idx} を削除しました！")
            st.experimental_rerun()  # ページをリロードして反映


