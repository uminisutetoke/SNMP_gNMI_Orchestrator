# server.py
import grpc
from concurrent import futures
import time

# 生成されたgRPCファイルと、SNMPライブラリをインポート
import pgw_pb2
import pgw_pb2_grpc
from pysnmp.hlapi import *

# pgw.protoで定義したサービスを実装するクラス
class SNMPServicer(pgw_pb2_grpc.SNMPServicer):

    # rpc Poll (SNMPRequest) returns (SNMPResponse); の部分を実装
    def Poll(self, request, context):
        print(f"受信リクエスト: ip={request.ip}, oid={request.oid}, community={request.community}")

        # 以前作ったpysnmpのコードをここに組み込む
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(
                SnmpEngine(),
                CommunityData(request.community, mpModel=1), # v2c
                UdpTransportTarget((request.ip, 161), timeout=2, retries=0),
                ContextData(),
                ObjectType(ObjectIdentity(request.oid))
            )
        )

        # SNMPの結果に応じて、レスポンスを作成する
        if errorIndication:
            print(f"エラー: {errorIndication}")
            return pgw_pb2.SNMPResponse(value="", status=str(errorIndication))
        elif errorStatus:
            print(f"エラー: {errorStatus.prettyPrint()}")
            return pgw_pb2.SNMPResponse(value="", status=errorStatus.prettyPrint())
        else:
            # 成功した場合、取得した値をレスポンスに詰める
            result_value = varBinds[0][1].prettyPrint()
            print(f"成功: value={result_value}")
            return pgw_pb2.SNMPResponse(value=result_value, status="OK")

def serve():
    # gRPCサーバーを起動
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pgw_pb2_grpc.add_SNMPServicer_to_server(SNMPServicer(), server)
    server.add_insecure_port('[::]:50051') # 50051番ポートで待ち受ける
    server.start()
    print("gRPCサーバー起動完了。ポート50051で待機中...")
    try:
        while True:
            time.sleep(86400) # 1日待機
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
