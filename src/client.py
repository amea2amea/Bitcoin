import socket

# ソケットの作成
# AF_INET       : IPv4 ベースのアドレス体系
# SOCK_STREAM   : TCP/IPの設定
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 接続要求
# 接続先のIPアドレスとポートの割り当て
my_socket.connect(("192.168.0.5", 50030))
my_text = "Hello! This is test message from my sample client!"
# 送信
# Pythonのstring型をそのまま送ることはできないため、
# string.encodeによるエンコード変換
my_socket.sendall(my_text.encode("utf-8"))
