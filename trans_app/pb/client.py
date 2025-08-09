# client.py
import grpc
import pgw_pb2
import pgw_pb2_grpc

def run():
    # サーバーへの接続を作成（今回はローカルホストの50051番ポート）
    with grpc.insecure_channel('172.20.20.2:50051') as channel:
        # サーバーと通信するための「スタブ」を作成
        stub = pgw_pb2_grpc.SNMPStub(channel)

        # サーバーに送るリクエストメッセージを作成
        # このIPアドレスは、SNMPポーリングの「最終的なターゲット」
        request_message = pgw_pb2.SNMPRequest(
            ip="srl1", # ContainerLabのSNMP対応ルータ名
            oid="1.3.6.1.2.1.1.5.0", # sysName.0 (ホスト名)
            community="public",
            version=2
        )

        print("--- SNMP Pollリクエストを送信します ---")
        # サーバーのPollメソッドを呼び出し、レスポンスを受け取る
        response = stub.Poll(request_message)

        print("--- サーバーからのレスポンス ---")
        print(f"ステータス: {response.status}")
        print(f"取得した値: {response.value}")

if __name__ == '__main__':
    run()
