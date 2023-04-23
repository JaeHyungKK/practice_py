import socket
import subprocess
import re
# 자기 자신이 서버이기 때문에 자신의 아이피를 적어준다.
# 프로그램이 실행되는 컴퓨터의 아이피와 아래의 아이피가 일치하지 않을 경우 아래와 같은 에러가 뜸
# OSError: [WinError 10049] 요청한 주소는 해당 컨텍스트에서 유효하지 않습니다
ip = '192.168.219.104'
port = 35555


def receive_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((ip, port))
    server_socket.listen(100)
    client_socket, addr = server_socket.accept()
    print('Connected by', addr)
    try:
        data = client_socket.recv(102400)
        if not data:
            return receive_socket()
        else:
            order = data.decode()
            res = subprocess.run(order, text=True, capture_output=True, shell=True).stdout
            # process = subprocess.Popen(order, stdout=subprocess.PIPE, shell=True)
            # res, err = process.communicate()
            print(res)

            # res = subprocess.run(order).stdout

            ###### check output 일 경우 ######
            # res = subprocess.check_output(order).decode('euc-kr')
            # res = re.sub(r"\r", "", res)
            #################################
            if res is None:
                res = 'None'
            client_socket.send(str.encode(res))

    except WindowsError as w:
        print(w, order)
        pass
    server_socket.close()
    client_socket.close()
    return receive_socket()


receive_socket()