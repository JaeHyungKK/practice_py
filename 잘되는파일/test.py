from PySide6.QtWidgets import *
from qt_material import apply_stylesheet, QtStyleTools, QUiLoader
from PySide6.QtCore import QThread, QObject, Signal
from PySide6.QtCore import QThread
import sys
import socket
#
#
# class NotepadThread(QThread):
#     def run(self):
#         import subprocess
#         subprocess.run("notepad.exe")
#
#
# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.notepad_thread = NotepadThread()
#         self.setup_ui()
#
#     def setup_ui(self):
#         # 메인 레이아웃
#         main_layout = QVBoxLayout(self)
#
#         h_layout = QHBoxLayout()
#
#         # # 위젯 모음
#         self.text_view = QTextEdit()
#         self.text_view.setFixedSize(590, 500)
#         self.text_view.setReadOnly(True)
#
#         self.command_lineEdit = QLineEdit()
#
#         command_spacer = QSpacerItem(15, 15, QSizePolicy.Fixed, QSizePolicy.Expanding)
#
#         command_button = QPushButton("원격 실행")
#         command_button.setFixedSize(120, 25)
#         command_button.clicked.connect(self.notepad_thread.start)
#
#         # 위젯 추가
#         h_layout.addWidget(self.command_lineEdit)
#         h_layout.addItem(command_spacer)
#         h_layout.addWidget(command_button)
#
#         main_layout.addWidget(self.text_view)
#         main_layout.addLayout(h_layout)
#
#
#
# # if __name__ == "__main__":
# #     from PySide6.QtWidgets import QApplication
# #     app = QApplication([])
# #     main_window = MainWindow()
# #     app.exec()
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     win = MainWindow()
#     win.show()
#
#     while True:
#         app.exec()


class RemoteControlWidget(QWidget, QtStyleTools):
    def __init__(self, *args, **kwargs):
        super(RemoteControlWidget, self).__init__(*args, **kwargs)

        self.socket_thread = None

        # extra = {}
        # extra['font_family'] = 'Roboto'
        # extra['density_scale'] = str(0)
        # theme = 'light_blue.xml'
        # invert = False
        # self.apply_stylesheet(self, theme=theme, extra=extra, invert_secondary=invert)
        self.setMinimumSize(600, 600)
        self.setWindowTitle("Infiltrating")

        self.setup_ui()

    def setup_ui(self):

        # 메인 레이아웃
        main_layout = QVBoxLayout(self)

        h_layout = QHBoxLayout()

        # # 위젯 모음
        self.text_view = QTextEdit()
        self.text_view.setFixedSize(590, 500)
        self.text_view.setReadOnly(True)

        self.command_lineEdit = QLineEdit()

        command_spacer = QSpacerItem(15, 15, QSizePolicy.Fixed, QSizePolicy.Expanding)

        command_button = QPushButton("원격 실행")
        command_button.setFixedSize(120, 25)
        command_button.clicked.connect(self.run_command)

        # 위젯 추가
        h_layout.addWidget(self.command_lineEdit)
        h_layout.addItem(command_spacer)
        h_layout.addWidget(command_button)

        main_layout.addWidget(self.text_view)
        main_layout.addLayout(h_layout)

    def run_command(self):

        command = 'notepad.exe'

        if self.socket_thread is None or not self.socket_thread.isRunning():
            self.socket_thread = SocketThread(command)
            self.socket_thread.start()
        else:
            self.text_view.append("메모장이 이미 실행 중입니다.")


class SocketThread(QThread):
    def __init__(self, command):
        super().__init__()
        self.command = command
        self.result = None
        print(self.command)

    def run(self):
        # command = 'notepad.exe'
        # import subprocess
        # return subprocess.run(command)
        # 무조건 통신할 서버의 아이피를 적어준다.
        ip = '192.168.219.104'
        port = 35555
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, port))

        try:
            client_socket.sendall(str.encode(self.command))
        except WindowsError as w:
            print(w)
            pass

        data = client_socket.recv(102400)
        res_str = str()
        result = repr(data.decode())
        result = result.split(r'\n')
        for r in result:
            res_str += r + '\n'
        self.result = re.sub("'", "", res_str)
        client_socket.close()
        return result


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = RemoteControlWidget()
    win.show()
    while True:
        app.exec()