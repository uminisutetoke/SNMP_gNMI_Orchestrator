import asyncio
from pygnmi.client import gNMIclient

# --- 監視対象の情報をここに書く ---
TARGET_HOST = "srl1"  # ContainerLabでのコンテナ名
TARGET_PORT = 57400
TARGET_USER = "admin"
TARGET_PASS = "admin"
# ------------------------------------

async def check_device():
    """指定した機器にgNMIで接続できるか試す"""
    print(f"--- {TARGET_HOST}への接続テストを開始します ---")

    # 接続情報を作成
    target = (TARGET_HOST, TARGET_PORT)

    try:
        # gNMIクライアントの部品を作成
        client = gNMIclient(target=target,
                              username=TARGET_USER,
                              password=TARGET_PASS,
                              insecure=True)

        # client部品を使って、capabilities()という機能をお願いする
        # この瞬間に接続とリクエストが行われます
        response = await client.capabilities()

        print("✅ 接続成功！")
        print(f"gNMIバージョン: {response.gNMI_version}")

    except Exception as e:
        # 接続に失敗した場合
        print(f"❌ 接続失敗...")
        print(f"エラー内容: {e}")

# --- プログラムの実行 ---
if __name__ == "__main__":
    asyncio.run(check_device())
