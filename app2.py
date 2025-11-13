# app_direct_dropbox.py
import streamlit as st
import pandas as pd
from datetime import datetime, date
import dropbox
import io
import requests

# ================================
# Dropbox 設定（直接ハードコーディング）
# ================================
APP_KEY = "jl6ot0jkupqwj5o"  # ここに自分のApp Key
APP_SECRET = "7gt6s2j08hxwtc8"          # ここに自分のApp Secret
REFRESH_TOKEN = "HiSMjRKn0I0AAAAAAAAAAT47w1YQ5_Ke_d2MLkChV4k2o7-qz8heFrk1h2oScnSc"  # 取得したRefresh Token
DROPBOX_FOLDER = "/釣りアプリ"
CSV_PATH = f"{DROPBOX_FOLDER}/voyage_records.csv"

# ================================
# Dropbox クライアント作成
# ================================
def get_dropbox_client():
    resp = requests.post(
        "https://api.dropboxapi.com/oauth2/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": REFRESH_TOKEN,
            "client_id": APP_KEY,
            "client_secret": APP_SECRET
        }
    )
    if resp.status_code != 200:
        st.error(f"Dropbox認証エラー: {resp.status_code}")
        st.write(resp.text)
        st.stop()

    access_token = resp.json()["access_token"]
    return dropbox.Dropbox(access_token)

# アプリ起動時にDropboxクライアント作成
dbx = get_dropbox_client()

# ================================
# CSV 読み込み関数
# ================================
def load_csv_from_dropbox():
    try:
        metadata, res = dbx.files_download(CSV_PATH)
        df = pd.read_csv(io.BytesIO(res.content))
    except dropbox.exceptions.ApiError:
        df = pd.DataFrame(columns=[
            "出航日", "出航時刻", "帰港時刻",
            "釣果写真URL", "トラブル写真URL", "登録日時"
        ])
    return df

# ================================
# CSV 保存関数
# ================================
def save_csv_to_dropbox(df):
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    dbx.files_upload(csv_buffer.getvalue().encode("utf-8"), CSV_PATH, mode=dropbox.files.WriteMode.overwrite)

# ================================
# 写真アップロード関数
# ================================
def upload_to_dropbox(file):
    path = f"{DROPBOX_FOLDER}/{file.name}"
    dbx.files_upload(file.read(), path, mode=dropbox.files.WriteMode.overwrite)
    shared_link = dbx.sharing_create_shared_link_with_settings(path)
    return shared_link.url.replace("?dl=0", "?raw=1")

# ================================
# Streamlit UI
# ================================
st.set_page_config(page_title="操船手順書＆航海記録", layout="centered")
page = st.sidebar.radio("ページ選択", ["手順書", "航海記録入力", "航海記録閲覧"])
df = load_csv_from_dropbox()

# ページ①：手順書
if page == "手順書":
    st.title("🚤 船舶 操船時 手順書")
    st.markdown("出航前・帰港後の安全確認にご利用ください。")
    st.header("⚙️ 出航前チェック")
    start_steps = [
        "メインブレーカーを入れる","スクリューを降ろす","30分の暖機運転",
        "冷却水が出ているか確認","燃料残量を確認","ライト動作確認",
        "車のカギ確認","救命胴衣確認","係留ロープ・アンカーの状態確認",
        "天候・潮汐・波高の確認"
    ]
    for i, step in enumerate(start_steps, 1):
        st.markdown(f"**{i}. {step}**")

    st.header("⚓ 帰港後チェック")
    end_steps = [
        "エンジン停止後、冷却状態を確認","燃料漏れ・異音の有無を確認",
        "ブレーカーを降ろす","スクリューを降ろす",
        "係留ロープ・フェンダーの状態確認","備品回収・船内清掃"
    ]
    for i, step in enumerate(end_steps, 1):
        st.markdown(f"**{i}. {step}**")

    st.markdown("---")
    st.markdown("📍 **漁礁ポイント（Googleマップ）** [こちらを開く](https://www.google.com/maps/d/edit?mid=1h6m8fXg0UpW2BKKGzVcydgSmsGPf_Rk&usp=sharing)")
    st.caption("© 2025 操船安全管理マニュアル")

# ページ②：航海記録入力
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
            st.success("✅ 航海記録を Dropbox に保存しました！")

# ページ③：航海記録閲覧
elif page == "航海記録閲覧":
    st.title("📂 航海記録閲覧")
    tab1, tab2 = st.tabs(["記録一覧", "写真一覧"])

    with tab1:
        if df.empty:
            st.info("まだ航海記録はありません。")
        else:
            st.dataframe(df[["出航日","出航時刻","帰港時刻"]])
            st.subheader("❌ 記録削除")
            options = [f"{i+1}: {row['出航日']} {row['出航時刻']}" for i, row in df.iterrows()]
            selected_idx = st.selectbox("削除する記録を選択してください", options)
            if st.button("削除"):
                idx_to_delete = int(selected_idx.split(":")[0]) - 1
                df = df.drop(index=idx_to_delete).reset_index(drop=True)
                save_csv_to_dropbox(df)
                st.success(f"記録 {selected_idx} を削除しました！")
                st.experimental_rerun()

    with tab2:
        st.subheader("📸 Dropbox内の画像一覧")
        try:
            res = dbx.files_list_folder(DROPBOX_FOLDER)
            image_files = [entry for entry in res.entries
                           if isinstance(entry, dropbox.files.FileMetadata)
                           and entry.name.lower().endswith((".jpg",".jpeg",".png"))]
            if not image_files:
                st.info("フォルダ内に画像が見つかりません。")
            else:
                for file in image_files:
                    _, res_file = dbx.files_download(f"{DROPBOX_FOLDER}/{file.name}")
                    st.image(io.BytesIO(res_file.content), caption=file.name, use_container_width=True)
        except dropbox.exceptions.ApiError as e:
            st.error(f"画像取得に失敗しました: {e}")
