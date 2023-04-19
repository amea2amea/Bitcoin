import socket
from concurrent.futures import ThreadPoolExecutor


# メッセージを受け取る(スレッドプールの関数)
def __handle_message(args_tuple):
    conn, addr, data_sum = args_tuple
    while True:
        # データの受信：データを受信する最大バイトを指定
        data = conn.recv(1024)
        data_sum = data_sum + data.decode("utf-8")

        if not data:
            break

    if data_sum != "":
        print(data_sum)


# ポート番号の取得
def __get_myip():
    
    # 環境においては使用不可だが、下記でも可能
    # socket.gethostname : 実行している環境のホスト名を取得
    # socket.gethostbyname : ホスト名から対応するホスト情報を取得
    # socket.gethostbyname(socket.gethostname()): ルータに接続中のローカルIPアドレスを取得

    # ソケットの作成
    # AF_INET       : IPv4 ベースのアドレス体系
    # SOCK_DGRAM    : データグラムソケット(UDPの設定)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Googleが運営するパブリックDNSサービス（Google Public DNS）を利用
    s.connect(("8.8.8.8", 80))
    # ソケット結び付けられている現在のアドレスを取得
    name = s.getsockname()[0]
    return name


# メイン処理
def main():

    # ソケットの作成
    # AF_INET       : IPv4 ベースのアドレス体系
    # SOCK_STREAM   : ストリームソケット(TCP/IPの設定)
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # max_workers 個のスレッドを非同期実行に使う
    # スレッドプールの作成(多重接続可能にするため)
    executor = ThreadPoolExecutor(max_workers=10)

    # ポート番号の取得
    myhost = __get_myip()
    print("my ip address is now  ...", myhost)
    # ソケットに許可するIPアドレス(空の場合は全てのIPアドレス)とポートやの割り当て
    # ポートは動的・プライベートポート番号（49152-65535）を利用する必要がある
    my_socket.bind((myhost, 50030))
    # 接続(要求)受付状態 (引数：同時接続の相手の数)
    my_socket.listen(1)

    while True:

        # 通信接続要求待ち：接続要求があるまで待機(ブロッキング)
        # 通信接続があれば、接続を受け付け、データ読み書き用の新しいソケット(接続ソケット)が生成される
        # 複数から要求があれば、先頭から順番に行う
        print("Waiting for the connection ...")
        conn, addr = my_socket.accept()
        print("Connected by .. ", addr)
        # 非同期呼び出しを実行(呼び出す関数と引数を指定)
        data_sum = ""
        executor.submit(__handle_message, (conn, addr, data_sum))


# 実行
if __name__ == "__main__":
    main()
