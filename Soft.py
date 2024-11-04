import re
import shutil
import subprocess
import sys
import json
import os
import tempfile
import uuid
import hashlib
from PyQt5.QtWidgets import (QDialog, QApplication, QWidget, QTabWidget, QVBoxLayout, QPushButton, QLineEdit,
                             QMessageBox, QHBoxLayout, QLabel, QComboBox, QTextEdit, QGridLayout, QSizePolicy,
                             QSplitter, QCompleter, QMenu)
from PyQt5.QtCore import Qt, QSize, QRegularExpression, QTime, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QTextCursor, QTextCharFormat, QColor, QFont, QPainter, QBrush, QPen, QKeyEvent, \
    QSyntaxHighlighter

from Bai_Toan_Dem_So import ConditionDialog
from Diem_Trong_Tam_Giac import SpecialPointsTab
from Tich_Vo_Huong_Co_Huong import VectorCalculatorDialog
from Tim_Hinh_Chieu import ProjectionCalculatorDialog
from Tinh_Dien_Tich_The_Tich import GeometryCalculatorDialog
from Tinh_Gioi_Ham import LimitCalculatorDialog
from giai_hpt import SystemOfEquationsSolverDialog
from giai_pt import AdvancedEquationSolverDialog
from khoang_cach_diem_to_mp import PlaneDistanceCalculatorDialog
from may_tinh import Calculator
from phan_tich_dathuc import PolynomialOperationsDialog
from sum_huu_han import FiniteSumCalculatorDialog
from tich_phan import *
from nguyenham import *
from dao_ham import *
from khoang_cach_2diem import *
from khoang_cach_diem_to_duong import *
from khoang_cach_dt_to_dt import *
from to_hop_xac_suat import CombinatoricsCalculatorDialog
from may_tinh import *
from giai_toan_thong_ke import *
# ICON_DIR = os.path.join(os.path.dirname(__file__), 'icons')


def resource_path(relative_path):
    """ Lấy đường dẫn tuyệt đối của tài nguyên cho cả chế độ dev và khi chạy từ file .exe."""
    try:
        # Đường dẫn được xác định bởi PyInstaller
        base_path = sys._MEIPASS
    except Exception:
        # Đường dẫn khi chạy script Python thông thường
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
ICON_DIR = resource_path('icons')



# def generate_key(mac_address):
#     # Chuẩn hóa địa chỉ MAC
#     normalized_mac = mac_address.replace(':', '').upper()
#     # Tạo hash từ địa chỉ MAC chuẩn hóa
#     hashed_mac = hashlib.sha256(normalized_mac.encode()).hexdigest()
#     # Lấy 3 ký tự đầu tiên, bỏ qua ký tự thứ 4, và lấy thêm 5 ký tự tiếp theo
#     key = hashed_mac[:3] + hashed_mac[4:9]
#     return key


# def verify_key(input_key, mac_address):
#     # Chuẩn hóa địa chỉ MAC
#     normalized_mac = mac_address.replace(':', '').upper()
#     # Tạo hash từ địa chỉ MAC đã chuẩn hóa
#     hashed_mac = hashlib.sha256(normalized_mac.encode()).hexdigest()
#     # Lấy 3 ký tự đầu tiên, bỏ qua ký tự thứ 4, và lấy thêm 5 ký tự tiếp theo để tạo expected_key
#     expected_key = hashed_mac[:3] + hashed_mac[4:9]
#     # So sánh input_key với expected_key
#     return input_key == expected_key


# def save_activated_key(activated_key):
#     with open("keyMathType.txt", "w",encoding='utf-8') as file:
#         file.write(activated_key)

# def read_activated_key():
#     try:
#         with open("keyMathType.txt", "r",encoding='utf-8') as file:
#             return file.read().strip()
#     except FileNotFoundError:
#         return None



class LatexSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(LatexSyntaxHighlighter, self).__init__(parent)
        self.highlightingRules = []

        drawFormat = QTextCharFormat()
        drawFormat.setForeground(QColor("green"))

        rectangleFormat = QTextCharFormat()
        rectangleFormat.setForeground(QColor("blue"))

        circleFormat = QTextCharFormat()
        circleFormat.setForeground(QColor("red"))

        mathFormat = QTextCharFormat()
        mathFormat.setForeground(QColor("magenta"))

        draw1Format = QTextCharFormat()
        draw1Format.setForeground(QColor("blue"))
        draw2Format = QTextCharFormat()
        draw2Format.setForeground(QColor("purple"))
        draw3Format = QTextCharFormat()
        draw3Format.setForeground(QColor("#FF9900"))
        # Tạo các quy tắc sáng tỏ cho từng từ khóa và màu sắc tương ứng
        drawPattern = QRegularExpression(r'\\draw')
        draw1Pattern = QRegularExpression(r'\\coordinate')
        draw2Pattern = QRegularExpression(r'\\def')
        draw3Pattern = QRegularExpression(r'\\fill')
        rectanglePattern = QRegularExpression(r'\\rectangle')
        circlePattern = QRegularExpression(r'\\circle')
        mathPattern = QRegularExpression(r'\$(.*?)\$')

        self.highlightingRules.append((drawPattern, drawFormat))
        self.highlightingRules.append((draw1Pattern, draw1Format))
        self.highlightingRules.append((draw2Pattern, draw2Format))
        self.highlightingRules.append((draw3Pattern, draw3Format))
        self.highlightingRules.append((rectanglePattern, rectangleFormat))
        self.highlightingRules.append((circlePattern, circleFormat))
        self.highlightingRules.append((mathPattern, mathFormat))

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegularExpression(pattern)
            matchIterator = expression.globalMatch(text)
            while matchIterator.hasNext():
                match = matchIterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)

class CalculationTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QGridLayout(self)  # Sử dụng QGridLayout
        self.initUI()

    def initUI(self):
        functions = [
            ("Đạo Hàm", self.openDerivativeDialog),
            ("Nguyên Hàm", self.openAntiderivativeDialog),
            ("Tích Phân", self.openIntegralDialog),
            ("Độ Dài AB", self.openDistanceCalculatorDialog),
            ("d(A,Delta)", self.openLineDistanceCalculatorDialog),
            ("d(Delta1,Delta2)", self.open3DLineDistanceCalculatorDialog),
            ("d(A,(P))", self.openPlainDistanceCalculatorDialog),
            ("Giải PT-BPT", self.openAdvancedEquationSolverDialog),
            ("Giải HPT", self.openHPTAdvancedEquationSolverDialog),
            ("Đa Thức", self.openPolynomialOperationsDialog),
            ("Tổ Hợp A-P-C", self.openCombinatoricsCalculatorDialog),
            ("Tổng Hữu Hạn-f(x_0)", self.openFiniteSumCalculatorDialog),
            ("Tính Giới Hạn", self.openLimitCalculatorDialog),
            ("Cosin,Vô-Có Hướng", self.openVectorCalculatorDialog),
            ("Tìm Hình Chiếu", self.openProjectionCalculatorDialog),
            ("Diện Tích - Thể Tích", self.openGeometryCalculatorDialog),
            ("Điểm Đặc Biệt ABC", self.openSpecialPointsTab),
            ("Bài Toán Đếm Số", self.openConditionDialog),
            ("Máy Tính Cơ Bản", self.openCalculator),
            ("Giải Toán Thống Kê", self.opengiaitoanthongke),
            # Thêm các chức năng khác tại đây
        ]

        numRows = 4  # Số hàng tối đa cho mỗi cột
        for i, (label, action) in enumerate(functions):
            btn = QPushButton(label)
            btn.clicked.connect(action)
            btn.setFixedSize(260, 60)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: lightblue;
                    border-radius: 15px;
                    border: 1px solid #8f8f91;
                }
                QPushButton:pressed {
                    background-color: #add8e6;
                }
                QPushButton:hover {
                    background-color: #87ceeb;
                }
            """)
            # Thêm nút vào lưới. i % numRows xác định hàng, i // numRows xác định cột
            self.layout.addWidget(btn, i % numRows, i // numRows)
    def opengiaitoanthongke(self):
        dialog = giai_toan_thong_ke(self)
        dialog.exec_()
    def openCalculator(self):
        dialog = Calculator(self)
        dialog.exec_()
    def openConditionDialog(self):
        dialog = ConditionDialog(self)
        dialog.exec_()
    def openSpecialPointsTab(self):
        dialog = SpecialPointsTab(self)
        dialog.exec_()
    def openGeometryCalculatorDialog(self):
        dialog = GeometryCalculatorDialog(self)
        dialog.exec_()
    def openVectorCalculatorDialog(self):
        dialog = VectorCalculatorDialog(self)
        dialog.exec_()
    def openProjectionCalculatorDialog(self):
        dialog = ProjectionCalculatorDialog(self)
        dialog.exec_()
    def openIntegralDialog(self):
        dialog = IntegralCalculatorDialog(self)
        dialog.exec_()
    def openAntiderivativeDialog(self):
        dialog = AntiderivativeCalculatorDialog(self)
        dialog.exec_()
    def openDerivativeDialog(self):
        dialog = DerivativeCalculatorDialog(self)
        dialog.exec_()
    def openDistanceCalculatorDialog(self):
        dialog = DistanceCalculatorDialog(self)
        dialog.exec_()
    def openLineDistanceCalculatorDialog(self):
        dialog = LineDistanceCalculatorDialog(self)
        dialog.exec_()
    def open3DLineDistanceCalculatorDialog(self):
        dialog = Lines3DDistanceCalculatorDialog(self)
        dialog.exec_()
    def openPlainDistanceCalculatorDialog(self):
        dialog = PlaneDistanceCalculatorDialog(self)
        dialog.exec_()
    def openAdvancedEquationSolverDialog(self):
        dialog = AdvancedEquationSolverDialog(self)
        dialog.exec_()
    def openHPTAdvancedEquationSolverDialog(self):
        dialog = SystemOfEquationsSolverDialog(self)
        dialog.exec_()
    def openPolynomialOperationsDialog(self):
        dialog = PolynomialOperationsDialog(self)
        dialog.exec_()
    def openCombinatoricsCalculatorDialog(self):
        dialog = CombinatoricsCalculatorDialog(self)
        dialog.exec_()
    def openFiniteSumCalculatorDialog(self):
        dialog = FiniteSumCalculatorDialog(self)
        dialog.exec_()
    def openLimitCalculatorDialog(self):
        dialog = LimitCalculatorDialog(self)
        dialog.exec_()
class LicenseDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Cài đặt của dialog như bạn đã làm
        self.userClosed = False
        self.setWindowTitle("Bản Quyền")
        self.resize(800, self.height())
        self.layout = QVBoxLayout(self)

        self.macLineEdit = QLineEdit()
        self.macLineEdit.setPlaceholderText("Số Series Máy sẽ được hiển thị ở đây")
        self.macLineEdit.setReadOnly(True)
        self.layout.addWidget(self.macLineEdit)

        self.getMacButton = QPushButton("Lấy Series Máy")
        self.getMacButton.clicked.connect(self.getMachineInfo)
        self.copyMacButton = QPushButton("Copy Mã")
        self.copyMacButton.clicked.connect(self.copyMachineInfo)
        macButtonLayout = QHBoxLayout()
        macButtonLayout.addWidget(self.getMacButton)
        macButtonLayout.addWidget(self.copyMacButton)
        self.layout.addLayout(macButtonLayout)

        self.keyEdit = QLineEdit()
        self.keyEdit.setPlaceholderText("Nhập Key Ứng Dụng")
        self.layout.addWidget(self.keyEdit)

        self.activateButton = QPushButton("Kích Hoạt")
        self.activateButton.clicked.connect(self.activateApp)
        self.layout.addWidget(self.activateButton)
        # Thêm QLabel cho thông tin tác giả với nhiều dòng và hyperlink
        authorInfo = """
                <p>Tác Giả: Nguyễn Văn Sang</p>
                <p>GV THPT Nguyễn Hữu Cảnh - TP HCM</p>
                <p>Liên hệ: nguyensangnhc@gmail.com - Facebook: <a href='https://www.facebook.com/nguyenvan.sang.92798072/'>Facebook Nguyễn Văn Sang</a></p>
                <p>Phần mềm có phí 100K - Vĩnh viễn theo máy</p>
                <p>Momo: 0389.821.115 hoặc số tài khoản VPB như ảnh</p>
                """
        self.authorLabel = QLabel(authorInfo)
        self.authorLabel.setAlignment(Qt.AlignCenter)  # Canh giữa văn bản
        self.authorLabel.setOpenExternalLinks(True)  # Kích hoạt việc mở liên kết bên ngoài
        self.layout.addWidget(self.authorLabel)

        # Thêm QLabel cho logo và điều chỉnh tỷ lệ
        self.logoLabel = QLabel(self)
        # self.logoPixmap = QPixmap('vpb.png')  # Đường dẫn đến file ảnh
        # Điều chỉnh tỷ lệ pixmap để phù hợp nhưng vẫn giữ nguyên tỷ lệ
        # Tạo một QPixmap từ tệp ảnh trong thư mục 'icons'
        # self.logoPixmap = QPixmap(os.path.join(ICON_DIR, 'vpb.png'))
        self.logoPixmap = QPixmap(resource_path(os.path.join(ICON_DIR, 'vpb.png')))
        scaledPixmap = self.logoPixmap.scaled(459, 520, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.logoLabel.setPixmap(scaledPixmap)
        self.logoLabel.setAlignment(Qt.AlignCenter)  # Canh giữa ảnh
        self.layout.addWidget(self.logoLabel)

        self.setLayout(self.layout)

    def closeEvent(self, event):
        # Ghi đè sự kiện đóng để cập nhật trạng thái khi người dùng đóng cửa sổ
        self.userClosed = True
        super().closeEvent(event)
    def copyMachineInfo(self):
        QApplication.clipboard().setText(self.macLineEdit.text())
        QMessageBox.information(self, "Copy Mã", "Mã máy đã được copy vào clipboard.")


    # def getMachineInfo(self):
    #     # Lấy địa chỉ MAC mà không thêm bất kỳ chuỗi nào
    #     mac_address = ':'.join(('%012X' % uuid.getnode())[i:i + 2] for i in range(0, 12, 2))
    #     self.macLineEdit.setText(mac_address)

    # def activateApp(self):
    #     input_key = self.keyEdit.text()
    #     mac_address = self.macLineEdit.text().replace(':', '').upper()
    #     if verify_key(input_key, mac_address):
    #         QMessageBox.information(self, "Kích Hoạt", "Ứng dụng đã được kích hoạt thành công!")
    #         save_activated_key(input_key)
    #         self.userClosed = False  # Cập nhật lại thuộc tính này
    #         self.accept()
    #     else:
    #         QMessageBox.warning(self, "Kích Hoạt", "Key không hợp lệ!")
    #         # self.userClosed = False

class MathSymbolTab(QWidget):
    def __init__(self, symbols, addLatexCallback, parent=None):
        super().__init__(parent)
        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setHorizontalSpacing(5)
        self.layout.setVerticalSpacing(5)
        self.symbols = symbols
        self.addLatexCallback = addLatexCallback
        self.setMaximumHeight(250)
        self.initUI()

    def initUI(self):
        numRows = 4
        i=-1
        for i, (label, item) in enumerate(self.symbols.items()):
            latex = item['latex']
            icon_path = item.get('icon')
            btn = QPushButton()
            if icon_path:
                full_icon_path = os.path.join(ICON_DIR, icon_path)
                originalPixmap = QPixmap(full_icon_path)
                roundedPixmap = createRoundedPixmap(originalPixmap, 15)
                scaledPixmap = roundedPixmap.scaled(100, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                btn.setIcon(QIcon(scaledPixmap))
                btn.setIconSize(scaledPixmap.size())
            else:
                btn.setText(label)
            btn.setFixedSize(100, 60)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: lightblue;
                    border-radius: 15px;
                    border: 1px solid #8f8f91;
                }
                QPushButton:pressed {
                    background-color: #add8e6;
                }
                QPushButton:hover {
                    background-color: #87ceeb;
                }
            """)

            btn.clicked.connect(lambda checked, latex=latex: self.addLatexCallback(latex))
            btn.setEnabled(False)
            self.layout.addWidget(btn, i % numRows, i // numRows)

        dummyWidget = QWidget()
        dummyWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout.addWidget(dummyWidget, 0, (i // numRows) + 1, numRows, 1)

    def addSymbol(self, symbol, latex):
        btn = QPushButton(symbol)
        btn.clicked.connect(lambda checked, latex=latex: self.addLatexCallback(latex))
        btn.setEnabled(False)
        position = len(self.symbols)
        self.layout.addWidget(btn, position // 6, position % 6)
        self.symbols[symbol] = latex

    def enableButtons(self):
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if isinstance(widget, QPushButton):
                widget.setEnabled(True)

def createRoundedPixmap(originalPixmap, radius):
    roundedPixmap = QPixmap(originalPixmap.size())
    roundedPixmap.fill(Qt.transparent)
    painter = QPainter(roundedPixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(QBrush(originalPixmap))
    painter.setPen(QPen(Qt.transparent))
    painter.drawRoundedRect(roundedPixmap.rect(), radius, radius)
    painter.end()
    return roundedPixmap

def load_symbols(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    symbols = {key: value for key, value in data.items() if key != "formattingRules" and key != "autocomplete"}
    autocomplete = data.get("autocomplete", [])
    formattingRules = data.get("formattingRules", [])
    return symbols,autocomplete, formattingRules

def add_symbol_to_json(group, symbol, latex, symbols, filename='symbolmathAuto.json'):
    if group not in symbols:
        symbols[group] = {}
    symbols[group][symbol] = {"latex": latex, "icon": None}
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(symbols, file,ensure_ascii=False, indent=4)

class LoadingDialog(QDialog):
    def __init__(self, start_time):
        super().__init__()
        self.setWindowTitle('Đang Khởi Động')
        self.setGeometry(800, 700, 400, 100)  # Thiết lập kích thước của cửa sổ
        self.start_time = start_time  # Thời điểm bắt đầu khi khởi động
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Label để hiển thị thời gian đếm ngược
        self.timer_label = QLabel('00:00:000')  # Thời gian đếm ngược ban đầu là 0
        self.timer_label.setAlignment(Qt.AlignCenter)  # Căn giữa văn bản trong label
        self.timer_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Tự động mở rộng kích thước
        font = self.timer_label.font()  # Lấy font hiện tại
        font.setPointSize(36)  # Thiết lập kích thước font
        self.timer_label.setFont(font)  # Áp dụng font đã thiết lập
        layout.addWidget(self.timer_label)

        self.setLayout(layout)

        # Thiết lập đồng hồ bấm giờ để tự động cập nhật thời gian đếm ngược
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1)  # Đồng hồ bấm giờ được gọi mỗi miligiây

    def update_timer(self):
        # Lấy thời gian hiện tại
        current_time = QTime.currentTime()

        # Tính thời gian chênh lệch giữa thời gian hiện tại và thời gian bắt đầu
        elapsed_time = self.start_time.msecsTo(current_time)

        # Hiển thị thời gian đếm ngược dạng giờ:phút:giây:miligiây
        self.timer_label.setText(current_time.toString("hh:mm:ss:zzz"))

        # Nếu đã chạy đủ thời gian (ví dụ: 5 giây), đóng cửa sổ
        if elapsed_time >= 5000:
            self.close()
class MathSymbolWidget(QWidget):
    def __init__(self, filename='symbolmathAuto.json'):
        super().__init__()
        # Lấy thời điểm bắt đầu khi khởi động
        start_time = QTime.currentTime()
        self.loading_dialog = LoadingDialog(start_time)
        self.loading_dialog.exec_()
        self.filename = filename
        self.symbols, self.autocomplete, self.formattingRules = load_symbols(self.filename)
        # self.setWindowIcon(QIcon(os.path.join(ICON_DIR, 'logo.ico')))
        self.setWindowIcon(QIcon(resource_path(os.path.join(ICON_DIR, 'logo.ico'))))
        self.isActivated = True  #False
        self.initUI()

    def showLicenseDialog(self):
        dialog = LicenseDialog(self)
        if dialog.exec_():
            self.isActivated = True
            for i in range(self.tabs.count()):
                tab = self.tabs.widget(i)
                if isinstance(tab, MathSymbolTab):
                    tab.enableButtons()
    def initUI(self):
        # Tạo tab "Tính Toán"
        self.tabs = QTabWidget()
        calculationTab = CalculationTab()
        self.tabs.addTab(calculationTab, "Các Nhóm Chức Năng")

        # Không tạo các nút và chức năng khác, chỉ giữ lại tab "Tính Toán"
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(self.tabs)

        mainLayout = QVBoxLayout(self)
        mainLayout.addWidget(splitter)

        # Đặt layout chính là mainLayout, chỉ chứa tab "Tính Toán"
        self.setLayout(mainLayout)

    # def initUI(self):
    #     # self.latexEdit = QTextEdit()
    #     self.latexEdit = CompletableTextEdit(self.autocomplete, self)
    #     self.latexEdit.setPlaceholderText("Enter LaTeX code here...")
    #     self.latexEdit.setMinimumHeight(500)
    #     font = QFont()
    #     font.setPointSize(16)
    #     self.latexEdit.setFont(font)
    #     self.highlighter = LatexSyntaxHighlighter(self.latexEdit.document())

    #     self.tabs = QTabWidget()
    #     ##THAY MÀU CÁC TAB
    #     # self.tabs.setStyleSheet("""
    #     #             QTabWidget::tab-bar {
    #     #                 alignment: left;
    #     #             }
    #     #             QTabBar::tab {
    #     #                 background: SandyBrown;
    #     #                 font-weight: bold;
    #     #                 color: navy;
    #     #                 font-size: 18px;
    #     #                 padding: 1px;
    #     #                 border-radius: 10px;
    #     #                 margin-right: 5px;
    #     #             }
    #     #             QTabBar::tab:selected {
    #     #                 background: skyblue;
    #     #                 border-color: #055;
    #     #             }
    #     #             QTabBar::tab:hover {
    #     #                 background: lightskyblue;
    #     #             }
    #     #         """)

    #     for category, symbols in self.symbols.items():
    #         tab = MathSymbolTab(symbols, self.addLatex)
    #         self.tabs.addTab(tab, category)

    #     self.groupComboBox = QComboBox()
    #     self.groupComboBox.addItems(list(self.symbols.keys()) + ["Add New Group..."])
    #     self.newGroupEdit = QLineEdit()
    #     self.newGroupEdit.setPlaceholderText("Enter new group name")
    #     self.newGroupEdit.setDisabled(True)

    #     self.newSymbolEdit = QTextEdit()
    #     self.newSymbolEdit.setMaximumHeight(40)
    #     self.newLatexEdit = QTextEdit()
    #     self.newLatexEdit.setPlaceholderText("Enter new LaTeX code here...")
    #     self.newLatexEdit.setMaximumHeight(40)

    #     self.addButton = QPushButton("Add Symbol")
    #     self.addButton.clicked.connect(self.addNewSymbol)
    #     self.addauto = QPushButton("Add Auto")
    #     self.addauto.clicked.connect(self.addAuto)
    #     ThreeButtonLayout = QHBoxLayout()
    #     self.copyButton = QPushButton("Copy")
    #     self.copyButton.clicked.connect(self.copyLatex)
    #     self.sizeUpButton = QPushButton("Tăng Size")
    #     self.sizeUpButton.clicked.connect(self.sizeUp)
    #     self.sizeDownButton = QPushButton("Giảm Size")
    #     self.sizeDownButton.clicked.connect(self.sizeDown)
    #     self.KeyButton = QPushButton("Bản Quyền")
    #     self.KeyButton.clicked.connect(self.showLicenseDialog)

    #     ThreeButtonLayout.addWidget(self.copyButton)
    #     ThreeButtonLayout.addWidget(self.sizeUpButton)
    #     ThreeButtonLayout.addWidget(self.sizeDownButton)
    #     ThreeButtonLayout.addWidget(self.KeyButton)
    #     self.copyButton.setFixedHeight(60)
    #     self.sizeUpButton.setFixedHeight(60)
    #     self.sizeDownButton.setFixedHeight(60)
    #     self.KeyButton.setFixedHeight(60)
    #     self.copyButton.setStyleSheet("""
    #         QPushButton {
    #             background-color: #87CEFA;
    #             color: white;
    #             border-radius: 5px;
    #         }
    #         QPushButton:hover {
    #             background-color: #B0E0E6;
    #         }
    #         QPushButton:pressed {
    #             background-color: #4682B4;
    #         }
    #     """)
    #     self.sizeUpButton.setStyleSheet("""
    #         QPushButton {
    #             background-color: #98FB98;
    #             color: black;
    #             border-radius: 5px;
    #         }
    #         QPushButton:hover {
    #             background-color: #90EE90;
    #         }
    #         QPushButton:pressed {
    #             background-color: #32CD32;
    #         }
    #     """)
    #     self.sizeDownButton.setStyleSheet("""
    #         QPushButton {
    #             background-color: #FFB6C1;
    #             color: black;
    #             border-radius: 5px;
    #         }
    #         QPushButton:hover {
    #             background-color: #FFC0CB;
    #         }
    #         QPushButton:pressed {
    #             background-color: #FF69B4;
    #         }
    #     """)
    #     self.KeyButton.setStyleSheet("""
    #         QPushButton {
    #             background-color: #F08080; /* Light Coral */
    #             color: white; /* Màu chữ trắng */
    #             border-radius: 5px; /* Bo tròn góc */
    #         }
    #         QPushButton:hover {
    #             background-color: #FFA07A; /* Light Salmon, màu nền khi hover */
    #         }
    #         QPushButton:pressed {
    #             background-color: #CD5C5C; /* Indian Red, màu nền khi nhấn */
    #         }
    #     """)
    #     addSymbolLayout = QHBoxLayout()
    #     addSymbolLayout.addWidget(QLabel("Group:"))
    #     addSymbolLayout.addWidget(self.groupComboBox)
    #     addSymbolLayout.addWidget(self.newGroupEdit)
    #     addSymbolLayout.addWidget(QLabel("Symbol:"))
    #     addSymbolLayout.addWidget(self.newSymbolEdit)
    #     addSymbolLayout.addWidget(QLabel("LaTeX:"))
    #     addSymbolLayout.addWidget(self.newLatexEdit)
    #     addSymbolLayout.addWidget(self.addButton)
    #     addSymbolLayout.addWidget(self.addauto)

    #     self.groupComboBox.currentTextChanged.connect(self.onGroupChanged)

    #     splitter = QSplitter(Qt.Vertical)
    #     splitter.addWidget(self.tabs)
    #     splitter.addWidget(self.latexEdit)

    #     mainLayout = QVBoxLayout(self)
    #     mainLayout.addWidget(splitter)
    #     mainLayout.addLayout(addSymbolLayout)
    #     mainLayout.addLayout(ThreeButtonLayout)
    #     calculationTab = CalculationTab()
    #     self.tabs.addTab(calculationTab, "Tính Toán")
    #     # self.setLayout(mainLayout)
    #     # Thêm một nút để chuyển đổi việc hiển thị các tab
    #     self.toggleTabsButton = QPushButton("Ẩn/Hiện Tabs")
    #     self.toggleTabsButton.clicked.connect(self.toggleTabsVisibility)
    #     # Ban đầu, giả sử các tab đang được hiển thị
    #     self.tabsVisible = True
    #     # Sửa đổi mainLayout để thêm toggleTabsButton
    #     mainLayout.addWidget(self.toggleTabsButton)
    #     mainLayout.addWidget(splitter)
    #     mainLayout.addLayout(addSymbolLayout)
    #     mainLayout.addLayout(ThreeButtonLayout)
    #     self.setLayout(mainLayout)

    def toggleTabsVisibility(self):
        # Chuyển đổi trạng thái hiển thị của các tab
        self.tabsVisible = not self.tabsVisible
        self.tabs.setVisible(self.tabsVisible)
        # Tùy chỉnh lại kích thước của QTextEdit hoặc layout nếu cần
        if self.tabsVisible:
            self.latexEdit.setMinimumHeight(500)
        else:
            self.latexEdit.setMinimumHeight(700)  # Tăng kích thước khi ẩn tabs
    def addAuto(self):
        # Lấy nội dung từ QTextEdit
        new_content = self.newLatexEdit.toPlainText().strip()

        # Chia nội dung thành các dòng và chỉnh sửa dòng đầu tiên nếu cần
        lines = new_content.splitlines()
        if lines and lines[0].startswith('\\'):
            lines[0] = lines[0][1:]  # Xoá ký tự '\' ở đầu dòng đầu tiên

        # Nối lại các dòng sau khi chỉnh sửa
        new_content = '\n'.join(lines)

        # Kiểm tra xem nội dung nhập vào có phải là rỗng hay không
        if new_content:
            # Đọc file JSON hiện tại
            try:
                with open('symbolmathAuto.json', 'r', encoding='utf-8') as file:
                    data = json.load(file)

                # Thêm nội dung mới vào danh sách autocomplete
                if 'autocomplete' in data:
                    data['autocomplete'].append(new_content)
                else:
                    data['autocomplete'] = [new_content]

                # Ghi lại vào file JSON
                with open('symbolmathAuto.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)

                QMessageBox.information(self, "Success", "The new LaTeX code has been added.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error occurred: {e}")
        else:
            QMessageBox.warning(self, "Warning", "The content to add cannot be empty.")

    def add1Auto(self):
        # Lấy nội dung từ QTextEdit
        new_content = self.newLatexEdit.toPlainText().strip()

        # Kiểm tra xem nội dung nhập vào có phải là rỗng hay không
        if new_content:
            # Đọc file JSON hiện tại
            try:
                with open('symbolmathAuto.json', 'r', encoding='utf-8') as file:
                    data = json.load(file)

                # Thêm nội dung mới vào danh sách autocomplete
                if 'autocomplete' in data:
                    data['autocomplete'].append(new_content)
                else:
                    data['autocomplete'] = [new_content]

                # Ghi lại vào file JSON
                with open('symbolmathAuto.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)

                QMessageBox.information(self, "Success", "The new LaTeX code has been added.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"An error occurred: {e}")
        else:
            QMessageBox.warning(self, "Warning", "The content to add cannot be empty.")

    def sizeUp(self):
        self.latexEdit.zoomIn(1)

    def sizeDown(self):
        self.latexEdit.zoomOut(1)

    def addLatex(self, latex):
        if not self.isActivated:
            QMessageBox.warning(self, "Chưa Kích Hoạt", "Vui lòng kích hoạt ứng dụng trước.")
            return
        cursor = self.latexEdit.textCursor()
        if cursor.atEnd():
            cursor.insertText(latex + "")
        else:
            cursor.insertText(latex)
            cursor.insertText("")
        self.latexEdit.setTextCursor(cursor)
        self.applyFormattingRules(latex)

    def applyFormattingRules(self, text):
        cursor = self.latexEdit.textCursor()
        startPos = cursor.position() - len(text)
        for rule in self.formattingRules:
            pattern = rule['pattern']
            color = rule['color']
            index = text.find(pattern)
            while index != -1:
                cursor.setPosition(startPos + index)
                cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, len(pattern))
                charFormat = QTextCharFormat()
                charFormat.setForeground(QColor(color))
                cursor.mergeCharFormat(charFormat)
                index = text.find(pattern, index + 1)
        self.latexEdit.setTextCursor(cursor)

    def onGroupChanged(self, text):
        if text == "Add New Group...":
            self.newGroupEdit.setDisabled(False)
            self.newGroupEdit.setFocus()
        else:
            self.newGroupEdit.setDisabled(True)
            self.newGroupEdit.clear()

    def addNewSymbol(self):
        try:
            # Kiểm tra xem group hiện tại có phải là "Add New Group..." không
            group = self.groupComboBox.currentText() if self.groupComboBox.currentText() != "Add New Group..." else None
            new_group = self.newGroupEdit.text().strip()
            symbol = self.newSymbolEdit.toPlainText().strip()
            latex = self.newLatexEdit.toPlainText().strip()

            # Nếu không có group nào được chọn và không có new_group nào được nhập
            if not group and not new_group:
                raise ValueError("Please select an existing group or enter a new group name.")

            # Nếu có new_group
            if new_group:
                if new_group in self.symbols:
                    raise ValueError("This group name already exists.")
                group = new_group
                self.groupComboBox.addItem(group)
                self.groupComboBox.setCurrentText(group)
                self.symbols[group] = {}  # Tạo một nhóm mới trong dictionary

            # Kiểm tra đảm bảo symbol và latex không rỗng
            if symbol and latex:
                # Thêm symbol mới vào nhóm
                self.symbols[group][symbol] = {"latex": latex, "icon": None}
                # Ghi lại vào file JSON
                with open(self.filename, 'w', encoding='utf-8') as file:
                    json.dump(self.symbols, file, ensure_ascii=False, indent=4)
                self.update_or_add_tab(group, symbol, latex)
                QMessageBox.information(self, "Success", f"Symbol '{symbol}' added to '{group}' successfully!")
            else:
                raise ValueError("Please enter both symbol and LaTeX.")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def ad1dNewSymbol(self):
        group = self.groupComboBox.currentText() if self.groupComboBox.currentText() != "Add New Group..." else None
        new_group = self.newGroupEdit.text().strip()
        symbol = self.newSymbolEdit.toPlainText().strip()
        latex = self.newLatexEdit.toPlainText().strip()
        if not group and not new_group:
            QMessageBox.warning(self, "Warning", "Please select an existing group or enter a new group name.")
            return
        if new_group:
            group = new_group
            if group in self.symbols:
                QMessageBox.warning(self, "Warning", "This group name already exists.")
                return
            self.groupComboBox.addItem(group)
            self.groupComboBox.setCurrentText(group)
            self.symbols[group] = {}
        if symbol and latex:
            add_symbol_to_json(group, symbol, latex, self.symbols, self.filename)
            self.newSymbolEdit.clear()
            self.newLatexEdit.clear()
            self.newGroupEdit.clear()
            QMessageBox.information(self, "Success", f"Symbol '{symbol}' added to '{group}' successfully!")
            self.update_or_add_tab(group, symbol, latex)
        else:
            QMessageBox.warning(self, "Warning", "Please enter both symbol and LaTeX.")

    def update_or_add_tab(self, group, symbol, latex):
        found = False
        for i in range(self.tabs.count()):
            if self.tabs.tabText(i) == group:
                found = True
                tab = self.tabs.widget(i)
                tab.addSymbol(symbol, latex)
                break
        if not found:
            new_tab = MathSymbolTab({symbol: latex}, self.addLatex)
            self.tabs.addTab(new_tab, group)
            self.symbols[group] = {symbol: latex}

    def copyLatex(self):
        latex = self.latexEdit.toPlainText()
        QApplication.clipboard().setText(latex)

class CompletableTextEdit(QTextEdit):
    MINIMUM_CHARS = 2  # Số ký tự tối thiểu để bắt đầu hiển thị gợi ý
    def __init__(self, autocomplete_list, parent=None):
        super().__init__(parent)
        self.completer = QCompleter(autocomplete_list, self)
        self.completer.setWidget(self)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)  # Thêm dòng này
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.activated.connect(self.insertCompletion)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

    def showContextMenu(self, position):
        contextMenu = QMenu(self)
        compileAction = contextMenu.addAction("Biên Dịch LaTeX")
        compileAction.triggered.connect(self.compileLatex)
        contextMenu.exec_(self.mapToGlobal(position))


    def compileLatex(self):
        selected_text = self.textCursor().selectedText()

        # Loại bỏ các ký tự control không mong muốn
        selected_text = re.sub(r'[\x00-\x1F]+', '', selected_text)
        # Loại bỏ ký tự Paragraph Separator (U+2029)
        selected_text = re.sub('\u2029', '', selected_text)
        temp_tex_path = "temp.tex"
        latex_content = ''
        if "\\documentclass" not in selected_text:
            latex_content = r'''
\documentclass{standalone}
\usepackage{tikz}
\usepackage{amssymb} % Để sử dụng các ký hiệu toán học
\usepackage{amsmath}
\usepackage[mathscr]{euscript} % Để sử dụng \mathscr{D}
\usetikzlibrary{shapes}
\usepackage{ex_test}
%Lệnh viết tắt
\newcommand{\hoac}[1]{\left[\begin{aligned}#1\end{aligned}\right.}
\newcommand{\heva}[1]{\left\{\begin{aligned}#1\end{aligned}\right.}
\begin{document}
''' + selected_text + "\\end{document}"
        if "eqnarray" in selected_text:
            latex_content=latex_content.replace('documentclass{standalone}','documentclass[tikz]{standalone}')
        with open(temp_tex_path, 'w', encoding='utf-8') as temp_tex_file:
            temp_tex_file.write(latex_content)

        try:
            subprocess.check_call(["pdflatex", "-interaction=nonstopmode", temp_tex_path])
            pdf_file = temp_tex_path.replace(".tex", ".pdf")
            png_file = temp_tex_path.replace(".tex", ".png")

            # Chuyển đổi PDF sang PNG
            subprocess.check_call(["magick", "convert", "-density", "300", pdf_file, "-quality", "90", png_file])

            # Hiển thị PNG trong QDialog
            self.showImageDialog(png_file)

        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Lỗi biên dịch", f"Biên dịch LaTeX thất bại: {e}")
            return
        finally:
            # Dọn dẹp các file tạm thời
            for file_path in [temp_tex_path, pdf_file, png_file]:
                if os.path.exists(file_path):
                    os.remove(file_path)

    def showImageDialog(self, image_path):
        dialog = QDialog(self)
        layout = QVBoxLayout(dialog)
        label = QLabel()
        pixmap = QPixmap(image_path)
        label.setPixmap(pixmap)
        layout.addWidget(label)
        dialog.setWindowTitle("Kết quả LaTeX")
        dialog.exec_()

    def te1xtUnderCursor(self):
        tc = self.textCursor()
        tc.select(tc.WordUnderCursor)
        return tc.selectedText()

    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        text = tc.selectedText()

        # Bỏ qua ký tự backslash khi xác định từ dưới con trỏ
        if text.startswith('\\'):
            text = text[1:]

        return text

    ###
    def keyPressEvent(self, event):
        super().keyPressEvent(event)

        if self.completer.popup().isVisible():
            if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab):
                event.ignore()
                return

        text_under_cursor = self.textUnderCursor()
        if len(text_under_cursor) < self.MINIMUM_CHARS:
            self.completer.popup().hide()
            return

        if text_under_cursor != self.completer.completionPrefix():
            self.completer.setCompletionPrefix(text_under_cursor)
            self.completer.popup().setCurrentIndex(self.completer.completionModel().index(0, 0))

            cursor_rect = self.cursorRect()
            cursor_rect.setWidth(self.completer.popup().sizeHintForColumn(
                0) + self.completer.popup().verticalScrollBar().sizeHint().width())
            self.completer.complete(cursor_rect)  # Hiển thị gợi ý

    def insertCompletion(self, completion):
        tc = self.textCursor()
        extra = len(completion) - len(self.completer.completionPrefix())
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])  # Chèn phần hoàn thiện còn thiếu
        self.setTextCursor(tc)

    ###

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     # Thiết lập phông chữ mặc định cho ứng dụng
#     defaultFont = QFont("Arial", 10)  # Thay đổi "Arial" và kích cỡ phông chữ theo ý bạn
#     app.setFont(defaultFont)
#     mathSymbolWidget = MathSymbolWidget()
#     mathSymbolWidget.setWindowTitle('Math Symbol STex')
#     mathSymbolWidget.setWindowFlags(Qt.WindowStaysOnTopHint)
#     mathSymbolWidget.resize(800, 800)
#     # Kiểm tra key đã được kích hoạt từ trước
#     saved_key = read_activated_key()
#     if saved_key and verify_key(saved_key, ':'.join(('%012X' % uuid.getnode())[i:i + 2] for i in range(0, 12, 2)).replace(':', '').upper()):
#         mathSymbolWidget.isActivated = True
#         for i in range(mathSymbolWidget.tabs.count()):
#             tab = mathSymbolWidget.tabs.widget(i)
#             if isinstance(tab, MathSymbolTab):
#                 tab.enableButtons()
#     else:
#         mathSymbolWidget.showLicenseDialog()
#     mathSymbolWidget.show()
#     sys.exit(app.exec_())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    defaultFont = QFont("Arial", 10)
    app.setFont(defaultFont)

    # Bỏ qua việc kiểm tra key và kích hoạt ứng dụng
    mathSymbolWidget = MathSymbolWidget()
    mathSymbolWidget.setWindowTitle('Phần Mềm Giải Toán THPT')
    mathSymbolWidget.setWindowFlags(Qt.WindowStaysOnTopHint)
    mathSymbolWidget.resize(800, 800)
    mathSymbolWidget.isActivated = True  # Đảm bảo ứng dụng luôn được kích hoạt

    # Kích hoạt các nút trong các tab (nếu cần)
    for i in range(mathSymbolWidget.tabs.count()):
        tab = mathSymbolWidget.tabs.widget(i)
        if isinstance(tab, MathSymbolTab):
            tab.enableButtons()

    mathSymbolWidget.show()

    sys.exit(app.exec_())


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     defaultFont = QFont("Arial", 10)
#     app.setFont(defaultFont)

#     # Kiểm tra key đã được kích hoạt từ trước
#     saved_key = read_activated_key()
#     mac_address = ':'.join(('%012X' % uuid.getnode())[i:i+2] for i in range(0, 12, 2)).replace(':', '').upper()

#     if saved_key and verify_key(saved_key, mac_address):
#         # Nếu key đã được kích hoạt từ trước, tiếp tục mở ứng dụng
#         mathSymbolWidget = MathSymbolWidget()
#         mathSymbolWidget.setWindowTitle('Math Symbol STex')
#         mathSymbolWidget.setWindowFlags(Qt.WindowStaysOnTopHint)
#         mathSymbolWidget.resize(800, 800)
#         mathSymbolWidget.isActivated = True
#         for i in range(mathSymbolWidget.tabs.count()):
#             tab = mathSymbolWidget.tabs.widget(i)
#             if isinstance(tab, MathSymbolTab):
#                 tab.enableButtons()
#         mathSymbolWidget.show()
#     else:
#         # Hiển thị dialog nhập key
#         # licenseDialog = LicenseDialog()
#         # Hiển thị dialog nhập key
#         licenseDialog = LicenseDialog()
#         # result = licenseDialog.exec_()
#         if licenseDialog.exec_() == QDialog.Accepted:
#             # Khi nhập đúng key và kích hoạt thành công
#             mathSymbolWidget = MathSymbolWidget()
#             mathSymbolWidget.setWindowTitle('Math Symbol STex')
#             mathSymbolWidget.setWindowFlags(Qt.WindowStaysOnTopHint)
#             mathSymbolWidget.resize(800, 800)
#             mathSymbolWidget.isActivated = True
#             for i in range(mathSymbolWidget.tabs.count()):
#                 tab = mathSymbolWidget.tabs.widget(i)
#                 if isinstance(tab, MathSymbolTab):
#                     tab.enableButtons()
#             mathSymbolWidget.show()
#         else:
#             # Đóng ứng dụng nếu dialog được đóng mà không nhập key
#             sys.exit()

#     sys.exit(app.exec_())
