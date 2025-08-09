import sys
sys.path.append('/opt/homebrew/lib/python3.11/site-packages')
import grpc
from concurrent import futures
import time

# 生成されたgRPCファイルをインポート
import pgw_pb2
import pgw_pb2_grpc

# pysnmpの必要な部品を、一つ一つ明示的にインポートします
# これが最も確実な書き方です
from pysnmp.hlapi import *

# pgw.protoで定義したサービスを実装するクラス
class SNMPServicer(pgw_pb2_grpc.SNMPServicer):

    # rpc Poll (SNMPRequest) returns (SNMPResponse); の部分を実装
    def Poll(self, request, context):
        """クライアントからのgRPCリクエストを処理し、SNMPポーリングを実行する"""
        print(f"受信リクエスト: ip={request.ip}, oid={request.oid}, community={request.community}")

        try:
            # pysnmpを使ってSNMP GETを実行
            iterator = getCmd(
                SnmpEngine(),
                CommunityData(request.community, mpModel=1), # mpModel=1はSNMPv2cを意味します
                UdpTransportTarget((request.ip, 161), timeout=2, retries=0),
                ContextData(),
                ObjectType(ObjectIdentity(request.oid))
            )

            errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

            # SNMPの結果に応じて、レスポンスを作成する
            if errorIndication:
                print(f"SNMPエラー: {errorIndication}")
                return pgw_pb2.SNMPResponse(value="", status=str(errorIndication))
            elif errorStatus:
                error_message = errorStatus.prettyPrint()
                print(f"SNMPエラー: {error_message}")
                return pgw_pb2.SNMPResponse(value="", status=error_message)
            else:
                # 成功した場合、取得した値をレスポンスに詰める
                result_value = varBinds[0][1].prettyPrint()
                print(f"SNMP成功: value={result_value}")
                return pgw_pb2.SNMPResponse(value=result_value, status="OK")

        except StopIteration:
            # タイムアウトなどで応答がなかった場合
            error_msg = "SNMPリクエストがタイムアウトしました。"
            print(f"エラー: {error_msg}")
            return pgw_pb2.SNMPResponse(value="", status=error_msg)
        except Exception as e:
            # その他の予期せぬエラー
            error_msg = f"サーバー内部で予期せぬエラーが発生しました: {e}"
            print(f"エラー: {error_msg}")
            # エラーの詳細をクライアントに伝える
            context.set_details(error_msg)
            context.set_code(grpc.StatusCode.INTERNAL)
            return pgw_pb2.SNMPResponse()

def serve():
    # gRPCサーバーを起動
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pgw_pb2_grpc.add_SNMPServicer_to_server(SNMPServicer(), server)
    server.add_insecure_port('[::]:50051') # 50051番ポートで待ち受ける
    server.start()
    print("gRPCサーバー起動完了。ポート50051で待機中...")
    try:
        # プログラムが終了しないように待機
        while True:
            time.sleep(86400) # 1日待機
    except KeyboardInterrupt:
        server.stop(0)
        print("gRPCサーバーを停止しました。")

if __name__ == '__main__':
    serve()

