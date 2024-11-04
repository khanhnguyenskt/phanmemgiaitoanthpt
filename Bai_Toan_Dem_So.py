from itertools import product
from itertools import combinations
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGridLayout,
                             QLabel, QLineEdit, QCheckBox, QPushButton,
                             QTextEdit, QGroupBox, QHBoxLayout, QSpinBox, QDialog)

class ConditionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        self.setWindowTitle("Bài Toán Đếm Số")  # Đặt tiêu đề cho Dialog

    def initUI(self):
        self.layout = QVBoxLayout(self)

        # Tạo QGroupBox cho nhập liệu và các điều kiện
        self.inputConditionsGroupBox = QGroupBox("Bài Toán Đếm Số")
        self.inputConditionsLayout = QGridLayout()
        self.inputConditionsGroupBox.setLayout(self.inputConditionsLayout)

        # Nhập chuỗi chữ số
        self.digitInputLabel = QLabel("Nhập chuỗi chữ số (ví dụ: 0,1,2,3,4,5):")
        self.digitInput = QLineEdit()
        self.inputConditionsLayout.addWidget(self.digitInputLabel, 0, 0, 1, 2)  # Phân bổ vào 2 cột
        self.inputConditionsLayout.addWidget(self.digitInput, 0, 2, 1, 2)  # Phân bổ vào 2 cột tiếp theo

        self.conditions = []
        # Thêm các điều kiện sử dụng phương thức createCondition
        self.createCondition("Có k chữ số", needInput=True, row=1, col=0)
        self.createCondition("Số chẵn", row=1, col=2)
        self.createCondition("Chia hết cho", needInput=True, row=2, col=0)
        self.createCondition("Số lẻ", row=2, col=2)
        self.createCondition("Bắt đầu bằng", needInput=True, hint="Nhập ab", row=3, col=0)
        self.createCondition("Chữ số khác nhau", row=3, col=2)
        self.createCondition("Không bắt đầu bằng", needInput=True, hint="Nhập ab", row=4, col=0)
        self.createCondition("Không có mặt đồng thời 2 chữ số", needInput=True, hint="Nhập a,b", row=4, col=2)
        self.createCondition("Nhỏ hơn", needInput=True, row=5, col=0)
        self.createCondition("Lớn hơn", needInput=True, row=5, col=2)
        self.createCondition("Luôn có mặt các chữ số", needInput=True, row=6, col=0)
        # Thêm các điều kiện khác theo yêu cầu

        self.layout.addWidget(self.inputConditionsGroupBox)  # Thêm QGroupBox vào layout chính
        # Tạo QGroupBox cho bài toán rút thẻ
        self.cardsGroupBox = QGroupBox("Bài Toán Rút Thẻ")
        self.cardsLayout = QGridLayout()
        self.cardsGroupBox.setLayout(self.cardsLayout)

        # Thêm SpinBox cho giá trị bắt đầu và kết thúc
        self.spinBoxStart = QSpinBox()
        self.spinBoxEnd = QSpinBox()
        self.spinBoxStart.setRange(0, 100)  # Giả sử giới hạn thẻ là từ 0 đến 100
        self.spinBoxEnd.setRange(0, 100)
        self.spinBoxStart.setValue(0)  # Giá trị mặc định
        self.spinBoxEnd.setValue(0)
        self.cardsLayout.addWidget(QLabel("Từ thẻ:"), 0, 0)  # Đặt ở hàng đầu tiên
        self.cardsLayout.addWidget(self.spinBoxStart, 0, 1)
        self.cardsLayout.addWidget(QLabel("Đến thẻ:"), 0, 2)
        self.cardsLayout.addWidget(self.spinBoxEnd, 0, 3)

        # Nhập chuỗi chữ số thông qua QLineEdit
        self.digitInputLabel_Two = QLabel("Nhập các thẻ (ví dụ: 1,2,...,17):")
        self.digitInput_Two = QLineEdit()
        self.cardsLayout.addWidget(self.digitInputLabel_Two, 1, 0, 1, 4)  # Đặt ở hàng tiếp theo
        self.cardsLayout.addWidget(self.digitInput_Two, 2, 0, 1, 4)  # Đặt ở hàng tiếp theo, phân bổ vào 4 cột

        # Thêm các điều kiện cho bài toán rút thẻ
        self.conditionsTwo = []
        self.createCondition_Two("Số thẻ được rút", needInput=True, row=3, col=0)  # Điều chỉnh hàng cho các điều kiện
        self.createCondition_Two("Số thẻ chẵn", needInput=True, row=3, col=2)
        self.createCondition_Two("Tổng chia hết cho", needInput=True, row=4, col=0)
        self.createCondition_Two("Tích chia hết cho", needInput=True, row=4, col=2)
        # Tiếp tục thêm các điều kiện khác nếu cần

        self.layout.addWidget(self.cardsGroupBox)  # Thêm QGroupBox vào layout chính

        # Phần tạo nút và kết quả giữ nguyên
        # Kết quả và nút tính toán
        self.resultText = QTextEdit()
        self.resultText.setReadOnly(True)
        self.layout.addWidget(self.resultText)

        # Tạo QHBoxLayout để chứa các nút
        self.buttonsLayout = QHBoxLayout()

        # Tạo và cấu hình nút thứ nhất
        self.calculateButton = QPushButton("Tính toán bài đếm số")
        self.calculateButton.clicked.connect(self.calculate)  # Giả định bạn đã định nghĩa phương thức calculate
        self.buttonsLayout.addWidget(self.calculateButton)

        # Tạo và cấu hình nút thứ hai
        self.calculateButton2 = QPushButton("Tính toán bài rút thẻ")
        self.calculateButton2.clicked.connect(self.calculate2)  # Giả định bạn sẽ định nghĩa phương thức calculate2
        self.buttonsLayout.addWidget(self.calculateButton2)
        self.calculateButton.setStyleSheet("background-color: blue; color: white;")
        self.calculateButton2.setStyleSheet("background-color: green; color: white;")

        # Thêm QHBoxLayout chứa các nút vào layout chính
        self.layout.addLayout(self.buttonsLayout)

    def calculate2(self):
        self.resultText.clear()  # Xóa kết quả cũ
        # Kiểm tra giá trị SpinBox
        if self.spinBoxStart.value() == 0 and self.spinBoxEnd.value() == 0:
            # Sử dụng QLineEdit nếu SpinBox không được thiết lập
            cards = [int(card) for card in self.digitInput_Two.text().split(',') if card.isdigit()]
        else:
            # Sử dụng giá trị từ SpinBox nếu chúng được thiết lập
            cards = list(range(self.spinBoxStart.value(), self.spinBoxEnd.value() + 1))
        # cards = [int(card) for card in self.digitInput_Two.text().split(',') if
        #          card.isdigit()]  # Chuyển chuỗi thành danh sách số nguyên
        valid_combinations = []  # Danh sách để lưu trữ các tổ hợp thẻ hợp lệ

        # Lấy số lượng thẻ cần rút từ điều kiện "Số thẻ được rút"
        for checkBox, conditionInput in self.conditionsTwo:
            if checkBox.isChecked() and checkBox.text() == "Số thẻ được rút":
                k = int(conditionInput.text())  # Số thẻ cần rút
                for combination in combinations(cards, k):
                    # Xác định xem tổ hợp thẻ này có thỏa mãn các điều kiện còn lại hay không
                    if self.checkOtherConditions(combination):
                        valid_combinations.append(combination)

        # Định dạng và hiển thị kết quả
        formatted_combinations = ["(" + ", ".join(map(str, combo)) + ")" for combo in
                                  valid_combinations]  # Định dạng mỗi tổ hợp vào trong cặp ngoặc đơn
        self.resultText.append(f"Các tổ hợp thẻ: {', '.join(formatted_combinations)}")  # Hiển thị các tổ hợp thẻ
        self.resultText.append(
            f"Số lượng tổ hợp thỏa mãn: {len(valid_combinations)}")  # Hiển thị số lượng tổ hợp thỏa mãn

    def checkOtherConditions(self, combination):
        # Ví dụ, kiểm tra "Số thẻ chẵn", "Tổng chia hết cho", "Tích chia hết cho"
        even_cards = [card for card in combination if card % 2 == 0]

        for checkBox, conditionInput in self.conditionsTwo:
            if checkBox.isChecked():
                if checkBox.text() == "Số thẻ chẵn" and len(even_cards) != int(conditionInput.text()):
                    return False
                if checkBox.text() == "Tổng chia hết cho" and sum(combination) % int(conditionInput.text()) != 0:
                    return False
                if checkBox.text() == "Tích chia hết cho":
                    product = 1
                    for card in combination:
                        product *= card
                    if product % int(conditionInput.text()) != 0:
                        return False
                # Thêm các điều kiện khác ở đây nếu cần

        return True  # Trả về True nếu tổ hợp thẻ thoả mãn tất cả các điều kiện

    def createCondition_Two(self, label, needInput=False, hint="", row=0, col=0):
        checkBox = QCheckBox(label)
        conditionInput = QLineEdit()
        conditionInput.setPlaceholderText(hint)
        conditionInput.setEnabled(False)

        if needInput:
            checkBox.stateChanged.connect(lambda checked, input=conditionInput: input.setEnabled(bool(checked)))
        else:
            conditionInput.setVisible(False)

        # Thêm vào cardsLayout với chỉ số hàng và cột cụ thể
        self.cardsLayout.addWidget(checkBox, row, col)
        if needInput:
            self.cardsLayout.addWidget(conditionInput, row, col + 1)
        self.conditionsTwo.append((checkBox, conditionInput))

    def createCondition(self, label, needInput=False, hint="", row=0, col=0):
        checkBox = QCheckBox(label)
        conditionInput = QLineEdit()
        conditionInput.setPlaceholderText(hint)
        conditionInput.setEnabled(False)

        if needInput:
            checkBox.stateChanged.connect(lambda checked, input=conditionInput: input.setEnabled(bool(checked)))
        else:
            conditionInput.setVisible(False)

        # Thêm vào QGridLayout với chỉ số hàng và cột cụ thể
        self.inputConditionsLayout.addWidget(checkBox, row, col)
        if needInput:
            self.inputConditionsLayout.addWidget(conditionInput, row, col + 1)
        self.conditions.append((checkBox, conditionInput))

    def calculate(self):
        self.resultText.clear()
        digits = self.digitInput.text().split(',')
        valid_numbers = set()

        # Tạo tất cả các số có thể từ chuỗi chữ số nhập vào
        for checkBox, conditionInput in self.conditions:
            if checkBox.isChecked() and checkBox.text() == "Có k chữ số":
                k = int(conditionInput.text())
                for num in product(digits, repeat=k):
                    if num[0] != '0':  # Loại trừ các số bắt đầu bằng 0
                        number = ''.join(num)
                        valid_numbers.add(number)

        # Áp dụng các điều kiện khác
        final_numbers = set()
        for number in valid_numbers:
            if self.applyConditions(number):
                final_numbers.add(number)

        self.resultText.append(f"Các số: {', '.join(sorted(final_numbers))}")
        self.resultText.append(f"Số lượng số thỏa mãn: {len(final_numbers)}")

    def applyConditions(self, number):
        for checkBox, conditionInput in self.conditions:
            if checkBox.isChecked():
                if checkBox.text() == "Luôn có mặt các chữ số":
                    for digit in conditionInput.text().split(','):
                        if digit not in number:
                            return False
                if checkBox.text() == "Chia hết cho" and int(number) % int(conditionInput.text()) != 0:
                    return False
                if checkBox.text() == "Nhỏ hơn" and int(number) >= int(conditionInput.text()):
                    return False
                if checkBox.text() == "Lớn hơn" and int(number) <= int(conditionInput.text()):
                    return False
                if checkBox.text() == "Số chẵn" and int(number[-1]) % 2 != 0:
                    return False
                if checkBox.text() == "Số lẻ" and int(number[-1]) % 2 == 0:
                    return False
                if checkBox.text() == "Chữ số khác nhau" and len(set(number)) != len(number):
                    return False
                if checkBox.text() == "Không có mặt đồng thời 2 chữ số":
                    a, b = conditionInput.text().split(',')
                    if a in number and b in number:
                        return False
                if checkBox.text() == "Bắt đầu bằng" and not number.startswith(conditionInput.text()):
                    return False
                if checkBox.text() == "Không bắt đầu bằng" and number.startswith(conditionInput.text()):
                    return False
                # Thêm logic xử lý cho các điều kiện khác
        return True


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    dialog = ConditionDialog()
    dialog.show()
    sys.exit(app.exec_())

