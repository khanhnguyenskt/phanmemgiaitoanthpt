from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout, QSpinBox
from sympy.utilities.iterables import variations
from sympy.utilities.iterables import combinations_with_replacement
from sympy.utilities.iterables import product
from sympy.utilities.iterables import permutations
from itertools import permutations
from itertools import permutations, combinations, product
from PyQt5.QtWidgets import QMessageBox
# def stn_chu_so_khac_nhau(numbers, num_digits, divisible_by, greater_than):
#     count = 0
#     for perm in permutations(numbers, num_digits):
#         if perm[0] != 0 and sum(perm) % divisible_by == 0 and int(''.join(map(str, perm))) > greater_than:
#             count += 1
#     return count
def stn_chu_so_khac_nhau(numbers, num_digits, divisible_by, greater_than, nho_hon):
    count = 0
    result = []
    for perm in permutations(numbers, num_digits):
        number = int(''.join(map(str, perm)))
        if perm[0] != 0 and number % divisible_by == 0 and number > greater_than and number < nho_hon:
            count += 1
            result.append(number)
    return count, result

def stn_tuy_y(numbers, num_digits, divisible_by, greater_than, nho_hon):
    count = 0
    result = []
    for perm in product(numbers, repeat=num_digits):
        number = int(''.join(map(str, perm)))
        if perm[0] > 0 and number > greater_than and number < nho_hon:  # Chữ số đầu tiên khác 0, lớn hơn giá trị greater_than và nhỏ hơn giá trị nho_hon
            if number % divisible_by == 0:  # Kiểm tra chia hết cho divisible_by
                count += 1
                result.append(number)
    return count, result

# def stn_chu_so_khac_nhau_always(numbers, num_digits, divisible_by, greater_than, fixed_digits):
#     count = 0
#     result = []
#
#     for perm in permutations(numbers, num_digits):
#         if perm[0] != 0 and int(''.join(map(str, perm))) % divisible_by == 0 and int(''.join(map(str, perm))) > greater_than:
#             number = int(''.join(map(str, perm)))
#             fixed_digits_str = str(fixed_digits)
#             if all(digit in str(number) for digit in fixed_digits_str):
#                 count += 1
#                 result.append(number)
#
#     return count, result

def stn_chu_so_khac_nhau_always(numbers, num_digits, divisible_by, greater_than, fixed_digits, nho_hon):
    count = 0
    result = []

    fixed_digits_list = list(map(int, fixed_digits.split(",")))

    for perm in permutations(numbers, num_digits):
        if perm[0] != 0 and int(''.join(map(str, perm))) % divisible_by == 0 and int(''.join(map(str, perm))) > greater_than and int(''.join(map(str, perm))) < nho_hon:
            number = int(''.join(map(str, perm)))
            if set(str(number)) >= set(map(str, fixed_digits_list)):
                count += 1
                result.append(number)

    return count, result


def tich_chia_het(numbers, num_digits, divisible_by, greater_than, nho_hon):
    count = 0
    result = []

    numbers_list = list(numbers)

    for combination in combinations(numbers_list, num_digits):
        product = 1
        for digit in combination:
            product *= digit

        if product % divisible_by == 0 and greater_than < product < nho_hon:
            count += 1
            result.append(combination)

    return count, result


def tong_chia_het(numbers, num_digits, divisible_by, greater_than, nho_hon):
    count = 0
    result = []

    numbers_list = list(numbers)

    for combination in combinations(numbers_list, num_digits):
        total = sum(combination)

        if total % divisible_by == 0 and greater_than < total < nho_hon:
            count += 1
            result.append(combination)

    return count, result




# def stn_chu_so_khac_nhau_always(numbers, num_digits, divisible_by, greater_than, fixed_digits):
#     count = 0
#     result = []
#
#     for perm in permutations(numbers, num_digits):
#         if perm[0] != 0 and int(''.join(map(str, perm))) % divisible_by == 0 and int(''.join(map(str, perm))) > greater_than:
#             count += 1
#             result.append(int(''.join(map(str, perm))))
#
#     # Loại bỏ các số không có đủ các chữ số từ fixed_digits
#     fixed_digits_str = str(fixed_digits)
#     result = [x for x in result if all(digit in str(x) for digit in fixed_digits_str)]
#     return count, result


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Đếm Số Tự Nhiên")
        self.layout = QVBoxLayout()
        self.setup_ui()

    def setup_ui(self):
        # Hàng ngang đầu tiên
        numbers_label = QLabel("Chữ Số K.Nhau Từ")
        self.numbers_input = QLineEdit()
        digits_label = QLabel("Số Chữ Số:")
        self.digits_input = QSpinBox()
        divisible_label = QLabel("Chia Hết:")
        self.divisible_input = QLineEdit()
        greater_than_label = QLabel("Lớn Hơn:")
        self.greater_than_input = QSpinBox()
        nho_hon_label = QLabel("Nhỏ Hơn:")
        self.nho_hon_input = QSpinBox()
        self.nho_hon_input.setRange(0,999999999)
        calculate_button = QPushButton("Calculate")
        calculate_button.clicked.connect(self.calculate)

        input_layout_1 = QHBoxLayout()
        input_layout_1.addWidget(numbers_label)
        input_layout_1.addWidget(self.numbers_input)
        input_layout_1.addWidget(digits_label)
        input_layout_1.addWidget(self.digits_input)
        input_layout_1.addWidget(divisible_label)
        input_layout_1.addWidget(self.divisible_input)
        input_layout_1.addWidget(greater_than_label)
        input_layout_1.addWidget(self.greater_than_input)
        input_layout_1.addWidget(nho_hon_label)
        input_layout_1.addWidget(self.nho_hon_input)
        input_layout_1.addWidget(calculate_button)

        # Hàng ngang thứ 2
        numbers_label2 = QLabel("Chữ Số Tuỳ Ý Từ :")
        self.numbers_input2 = QLineEdit()
        digits_label2 = QLabel("Số Chữ Số:")
        self.digits_input2 = QSpinBox()
        divisible_label2 = QLabel("Chia Hết:")
        self.divisible_input2 = QLineEdit()
        greater_than_label2 = QLabel("Lớn Hơn:")
        self.greater_than_input2 = QSpinBox()
        nho_hon_label2 = QLabel("Nhỏ Hơn:")
        self.nho_hon_input2 = QSpinBox()
        self.nho_hon_input2.setRange(0,999999999)  # Ví dụ giới hạn từ 0 đến 9999
        calculate_button2 = QPushButton("Calculate")
        calculate_button2.clicked.connect(self.calculate2)

        input_layout_2 = QHBoxLayout()
        input_layout_2.addWidget(numbers_label2)
        input_layout_2.addWidget(self.numbers_input2)
        input_layout_2.addWidget(digits_label2)
        input_layout_2.addWidget(self.digits_input2)
        input_layout_2.addWidget(divisible_label2)
        input_layout_2.addWidget(self.divisible_input2)
        input_layout_2.addWidget(greater_than_label2)
        input_layout_2.addWidget(self.greater_than_input2)
        input_layout_2.addWidget(nho_hon_label2)
        input_layout_2.addWidget(self.nho_hon_input2)
        input_layout_2.addWidget(calculate_button2)

        # Hàng ngang thứ 3
        numbers_label3 = QLabel("Chữ Số K.Nhau Từ")
        self.numbers_input3 = QLineEdit()
        digits_label3 = QLabel("Số Chữ Số:")
        self.digits_input3 = QSpinBox()
        divisible_label3 = QLabel("Chia Hết:")
        self.divisible_input3 = QLineEdit()
        fixed_digits_label3 = QLabel("Luôn Có Mặt")
        self.fixed_digits_input3 = QLineEdit()
        greater_than_label3 = QLabel("Lớn Hơn:")
        self.greater_than_input3 = QSpinBox()
        nho_hon_label3 = QLabel("Nhỏ Hơn:")
        self.nho_hon_input3 = QSpinBox()
        self.nho_hon_input3.setRange(0,999999999)  # Ví dụ giới hạn từ 0 đến 9999
        calculate_button3 = QPushButton("Calculate")
        calculate_button3.clicked.connect(self.calculate3)

        input_layout_3 = QHBoxLayout()
        input_layout_3.addWidget(numbers_label3)
        input_layout_3.addWidget(self.numbers_input3)
        input_layout_3.addWidget(digits_label3)
        input_layout_3.addWidget(self.digits_input3)
        input_layout_3.addWidget(divisible_label3)
        input_layout_3.addWidget(self.divisible_input3)
        input_layout_3.addWidget(fixed_digits_label3)
        input_layout_3.addWidget(self.fixed_digits_input3)
        input_layout_3.addWidget(greater_than_label3)
        input_layout_3.addWidget(self.greater_than_input3)
        input_layout_3.addWidget(nho_hon_label3)
        input_layout_3.addWidget(self.nho_hon_input3)
        input_layout_3.addWidget(calculate_button3)
        # Hàng ngang thứ 4
        numbers_label4 = QLabel("Các thẻ đánh số từ")
        self.numbers_input4 = QLineEdit()
        digits_label4 = QLabel("Số Thẻ Được Lấy:")
        self.digits_input4 = QSpinBox()
        divisible_label4 = QLabel("Tích Chia Hết:")
        self.divisible_input4 = QLineEdit()
        greater_than_label4 = QLabel("Lớn Hơn:")
        self.greater_than_input4 = QSpinBox()
        nho_hon_label4 = QLabel("Nhỏ Hơn:")
        self.nho_hon_input4 = QSpinBox()
        self.nho_hon_input4.setRange(0, 999999999)  # Ví dụ giới hạn từ 0 đến 9999
        calculate_button4 = QPushButton("Calculate")
        calculate_button4.clicked.connect(self.calculate4)

        input_layout_4 = QHBoxLayout()
        input_layout_4.addWidget(numbers_label4)
        input_layout_4.addWidget(self.numbers_input4)
        input_layout_4.addWidget(digits_label4)
        input_layout_4.addWidget(self.digits_input4)
        input_layout_4.addWidget(divisible_label4)
        input_layout_4.addWidget(self.divisible_input4)
        input_layout_4.addWidget(greater_than_label4)
        input_layout_4.addWidget(self.greater_than_input4)
        input_layout_4.addWidget(nho_hon_label4)
        input_layout_4.addWidget(self.nho_hon_input4)
        input_layout_4.addWidget(calculate_button4)
        # Hàng ngang thứ 5
        numbers_label5 = QLabel("Các thẻ đánh số từ")
        self.numbers_input5 = QLineEdit()
        digits_label5 = QLabel("Số Thẻ Được Lấy:")
        self.digits_input5 = QSpinBox()
        divisible_label5 = QLabel("Tổng Chia Hết")
        self.divisible_input5 = QLineEdit()
        greater_than_label5 = QLabel("Lớn Hơn:")
        self.greater_than_input5 = QSpinBox()
        nho_hon_label5 = QLabel("Nhỏ Hơn:")
        self.nho_hon_input5 = QSpinBox()
        self.nho_hon_input5.setRange(0, 999999999)  # Ví dụ giới hạn từ 0 đến 9999
        calculate_button5 = QPushButton("Calculate")
        calculate_button5.clicked.connect(self.calculate5)

        input_layout_5 = QHBoxLayout()
        input_layout_5.addWidget(numbers_label5)
        input_layout_5.addWidget(self.numbers_input5)
        input_layout_5.addWidget(digits_label5)
        input_layout_5.addWidget(self.digits_input5)
        input_layout_5.addWidget(divisible_label5)
        input_layout_5.addWidget(self.divisible_input5)
        input_layout_5.addWidget(greater_than_label5)
        input_layout_5.addWidget(self.greater_than_input5)
        input_layout_5.addWidget(nho_hon_label5)
        input_layout_5.addWidget(self.nho_hon_input5)
        input_layout_5.addWidget(calculate_button5)
        # Hàng ngang thứ 6
        so_dung_label6 = QLabel("Số Đúng")
        so_dung_label6.setStyleSheet("color: blue;")
        self.so_dung_input6 = QLineEdit()
        gan_dung_label6 = QLabel("Số Gần Đúng")
        gan_dung_label6.setStyleSheet("color: blue;")
        self.gan_dung_input6 = QLineEdit()
        chinhxac_label6 = QLabel("Độ Chính Xác")
        chinhxac_label6.setStyleSheet("color: blue;")
        self.chinhxac_input6 = QLineEdit()
        quytron_label6 = QLabel("Số Quy Tròn")
        quytron_label6.setStyleSheet("color: blue;")
        self.quytron_input6 = QLineEdit()
        sai_so_tuyetdoi_label6 = QLabel("Sai Số Tuyệt Đối")
        sai_so_tuyetdoi_label6.setStyleSheet("color: blue;")
        self.sai_so_tuyetdoi = QLineEdit()
        sai_so_tuongdoi_label6 = QLabel("Sai Số Tương Đối")
        sai_so_tuongdoi_label6.setStyleSheet("color: blue;")
        self.sai_so_tuongdoi_input6 = QLineEdit()
        xoa_button6 = QPushButton("Nhập Lại")
        xoa_button6.setStyleSheet("color: blue;")
        xoa_button6.clicked.connect(self.nhap_lai)
        calculate_button6 = QPushButton("Calculate")
        calculate_button6.setStyleSheet("color: blue;")
        calculate_button6.clicked.connect(self.calculate6)

        input_layout_6 = QHBoxLayout()
        input_layout_6.addWidget(so_dung_label6)
        input_layout_6.addWidget(self.so_dung_input6)
        input_layout_6.addWidget(gan_dung_label6)
        input_layout_6.addWidget(self.gan_dung_input6)
        input_layout_6.addWidget(chinhxac_label6)
        input_layout_6.addWidget(self.chinhxac_input6)
        input_layout_6.addWidget(quytron_label6)
        input_layout_6.addWidget(self.quytron_input6)
        input_layout_6.addWidget(sai_so_tuyetdoi_label6)
        input_layout_6.addWidget(self.sai_so_tuyetdoi)
        input_layout_6.addWidget(sai_so_tuongdoi_label6)
        input_layout_6.addWidget(self.sai_so_tuongdoi_input6)
        input_layout_6.addWidget(xoa_button6)
        input_layout_6.addWidget(calculate_button6)
        result_label = QLabel("Result:")
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)

        self.layout.addLayout(input_layout_1)
        self.layout.addLayout(input_layout_2)
        self.layout.addLayout(input_layout_3)
        self.layout.addLayout(input_layout_4)
        self.layout.addLayout(input_layout_5)
        self.layout.addLayout(input_layout_6)
        self.layout.addWidget(result_label)
        self.layout.addWidget(self.result_output)

        self.setLayout(self.layout)

    # def calculate(self):
    #     numbers = set(map(int, self.numbers_input.text().split(",")))
    #     num_digits = self.digits_input.value()
    #     divisible_by = int(self.divisible_input.text())
    #     greater_than = self.greater_than_input.value()
    #
    #     result = stn_chu_so_khac_nhau(numbers, num_digits, divisible_by, greater_than)
    #     self.result_output.setPlainText(str(result))
    def nhap_lai(self):
        self.so_dung_input6.clear()
        self.gan_dung_input6.clear()
        self.chinhxac_input6.clear()
        self.quytron_input6.clear()
        self.sai_so_tuyetdoi.clear()
        self.sai_so_tuongdoi_input6.clear()
        self.result_output.clear()

    def calculate(self):
        numbers = set(map(int, self.numbers_input.text().split(",")))
        num_digits = self.digits_input.value()
        divisible_by = int(self.divisible_input.text())
        greater_than = self.greater_than_input.value()
        nho_hon = self.nho_hon_input.value()  # Giá trị nhập từ QSpinBox nho_hon_input

        try:
            count, result = stn_chu_so_khac_nhau(numbers, num_digits, divisible_by, greater_than, nho_hon)
            self.result_output.setPlainText(f"Kết quả: {count}\nCác số thỏa mãn là:\n {result}")
        except Exception as e:
            self.result_output.setPlainText(f"Lỗi: {str(e)}")

    # def calculate2(self):
    #     numbers2 = set(map(int, self.numbers_input2.text().split(",")))
    #     num_digits2 = self.digits_input2.value()
    #     divisible_by2 = int(self.divisible_input2.text())
    #     greater_than2 = self.greater_than_input2.value()
    #
    #     result = stn_tuy_y(numbers2, num_digits2, divisible_by2, greater_than2)
    #     self.result_output.setPlainText(str(result))

    def calculate2(self):
        numbers2 = set(map(int, self.numbers_input2.text().split(",")))
        num_digits2 = self.digits_input2.value()
        divisible_by2 = int(self.divisible_input2.text())
        greater_than2 = self.greater_than_input2.value()
        nho_hon2 = self.nho_hon_input2.value()  # Giá trị nhập từ QSpinBox nho_hon_input2

        try:
            count, result = stn_tuy_y(numbers2, num_digits2, divisible_by2, greater_than2, nho_hon2)
            self.result_output.setPlainText(f"Kết quả: {count}\nCác số thỏa mãn là:\n {result}")
        except Exception as e:
            self.result_output.setPlainText(f"Lỗi: {str(e)}")

    # def calculate3(self):
    #     numbers_input = self.numbers_input3.text()
    #     num_digits = self.digits_input3.value()
    #
    #     try:
    #         divisible_by = int(self.divisible_input3.text())
    #     except ValueError:
    #         QMessageBox.warning(self, "Lỗi", "Chia Hết phải là một số nguyên.")
    #         return
    #
    #     greater_than = self.greater_than_input3.value()
    #     fixed_digits_text = self.fixed_digits_input3.text().strip().replace("'", "")
    #
    #     if not fixed_digits_text:
    #         QMessageBox.warning(self, "Lỗi", "Vui lòng nhập giá trị cho Luôn Có Mặt.")
    #         return
    #
    #     if not fixed_digits_text.isdigit():
    #         QMessageBox.warning(self, "Lỗi", "Giá trị Luôn Có Mặt không hợp lệ. Vui lòng chỉ nhập các chữ số.")
    #         return
    #
    #     fixed_digits = int(fixed_digits_text)
    #
    #     numbers = set(map(int, numbers_input.split(",")))
    #
    #     try:
    #         count, result = stn_chu_so_khac_nhau_always(numbers, num_digits, divisible_by, greater_than, fixed_digits)
    #         self.result_output.setPlainText(str(result))
    #         QMessageBox.information(self, "Kết quả", f"Số lượng các số thỏa mãn: {count}")
    #     except Exception as e:
    #         QMessageBox.warning(self, "Lỗi", str(e))
    def calculate3(self):
        numbers_input = self.numbers_input3.text()
        num_digits = self.digits_input3.value()

        try:
            divisible_by = int(self.divisible_input3.text())
        except ValueError:
            self.result_output.setPlainText("Lỗi: Chia Hết phải là một số nguyên.")
            return

        greater_than = self.greater_than_input3.value()
        fixed_digits_text = self.fixed_digits_input3.text().strip().replace("'", "")

        if not fixed_digits_text:
            self.result_output.setPlainText("Lỗi: Vui lòng nhập giá trị cho Luôn Có Mặt.")
            return

        if not all(digit.isdigit() for digit in fixed_digits_text.split(",")):
            self.result_output.setPlainText("Lỗi: Giá trị Luôn Có Mặt không hợp lệ. Vui lòng chỉ nhập các chữ số.")
            return

        fixed_digits = fixed_digits_text

        numbers = set(map(int, numbers_input.split(",")))

        nho_hon = self.nho_hon_input3.value()  # Giá trị nhập từ QSpinBox nho_hon_input3

        try:
            count, result = stn_chu_so_khac_nhau_always(numbers, num_digits, divisible_by, greater_than, fixed_digits,
                                                        nho_hon)
            self.result_output.setPlainText(f"Kết quả: {count}\nCác số thỏa mãn là:\n {result}")
        except Exception as e:
            self.result_output.setPlainText(f"Lỗi: {str(e)}")

    # def calculate4(self):
    #     numbers_input = self.numbers_input4.text()
    #     num_digits = self.digits_input4.value()
    #
    #     divisible_by_text = self.divisible_input4.text().strip()
    #     try:
    #         divisible_by = int(divisible_by_text)
    #     except ValueError:
    #         self.result_output.setPlainText("Lỗi: Chia Hết phải là một số nguyên.")
    #         return
    #
    #     greater_than = self.greater_than_input4.value()
    #
    #     numbers = set(map(int, numbers_input.split(",")))
    #
    #     nho_hon = self.nho_hon_input4.value()
    #
    #     try:
    #         count, result = tich_chia_het(numbers, num_digits, divisible_by, greater_than, nho_hon)
    #         self.result_output.setPlainText(f"Kết quả: {count}\nCác số thỏa mãn là:\n {result}")
    #     except Exception as e:
    #         self.result_output.setPlainText(f"Lỗi: {str(e)}")

    def calculate4(self):
        numbers_input = self.numbers_input4.text()
        num_digits = self.digits_input4.value()

        divisible_by_text = self.divisible_input4.text().strip()
        try:
            divisible_by = int(divisible_by_text)
        except ValueError:
            self.result_output.setPlainText("Lỗi: Chia Hết phải là một số nguyên.")
            return

        greater_than = self.greater_than_input4.value()

        numbers = set(map(int, numbers_input.split(",")))

        nho_hon = self.nho_hon_input4.value()

        try:
            count, combinations = tich_chia_het(numbers, num_digits, divisible_by, greater_than, nho_hon)
            self.result_output.setPlainText(
                f"Số cách chọn {num_digits} thẻ có tích chia hết cho {divisible_by} là: {count}")
            self.result_output.append("Các tổ hợp thẻ:")
            combination_str = str(combinations)
            self.result_output.append(combination_str)
        except Exception as e:
            self.result_output.setPlainText(f"Lỗi: {str(e)}")

    # def calculate4(self):
    #     numbers_input = self.numbers_input4.text()
    #     num_digits = self.digits_input4.value()
    #
    #     divisible_by_text = self.divisible_input4.text().strip()
    #     try:
    #         divisible_by = int(divisible_by_text)
    #     except ValueError:
    #         self.result_output.setPlainText("Lỗi: Chia Hết phải là một số nguyên.")
    #         return
    #
    #     greater_than = self.greater_than_input4.value()
    #
    #     numbers = set(map(int, numbers_input.split(",")))
    #
    #     nho_hon = self.nho_hon_input4.value()
    #
    #     try:
    #         count, combinations = tich_chia_het(numbers, num_digits, divisible_by, greater_than, nho_hon)
    #         self.result_output.setPlainText(
    #             f"Số cách chọn {num_digits} thẻ có tích chia hết cho {divisible_by} là: {count}")
    #         self.result_output.append("Các tổ hợp thẻ:")
    #         for combination in combinations:
    #             if len(combination) == num_digits:
    #                 combination_str = "(" + ", ".join(str(num) for num in combination) + ")"
    #                 self.result_output.append(combination_str)
    #     except Exception as e:
    #         self.result_output.setPlainText(f"Lỗi: {str(e)}")

    def calculate5(self):
        numbers_input = self.numbers_input5.text()
        num_digits = self.digits_input5.value()

        divisible_by_text = self.divisible_input5.text().strip()
        try:
            divisible_by = int(divisible_by_text)
        except ValueError:
            self.result_output.setPlainText("Lỗi: Chia Hết phải là một số nguyên.")
            return

        greater_than = self.greater_than_input5.value()

        numbers = set(map(int, numbers_input.split(",")))

        nho_hon = self.nho_hon_input5.value()

        try:
            count, combinations = tong_chia_het(numbers, num_digits, divisible_by, greater_than, nho_hon)
            self.result_output.setPlainText(
                f"Số cách chọn {num_digits} thẻ có tổng chia hết cho {divisible_by} là: {count}")
            self.result_output.append("Các tổ hợp thẻ:")
            combination_strs = [f"({', '.join(str(num) for num in combination)})" for combination in combinations]
            result_str = "[" + ", ".join(combination_strs) + "]"
            self.result_output.append(result_str)
        except Exception as e:
            self.result_output.setPlainText(f"Lỗi: {str(e)}")

    # def calculate6(self):
    #     so_dung = self.so_dung_input6.text()
    #     gan_dung = self.gan_dung_input6.text()
    #     chinh_xac = self.chinhxac_input6.text()
    #     sai_so_tuyet_doi = self.sai_so_tuyetdoi.text()
    #     sai_so_tuong_doi = self.sai_so_tuongdoi_input6.text()
    #
    #     # Kiểm tra số lượng ô đã nhập
    #     count = 0
    #     if so_dung:
    #         count += 1
    #     if gan_dung:
    #         count += 1
    #     if chinh_xac:
    #         count += 1
    #     if sai_so_tuyet_doi:
    #         count += 1
    #     if sai_so_tuong_doi:
    #         count += 1
    #
    #     # Tính toán giá trị các ô còn lại
    #     if count == 2:
    #         # Tính giá trị cho ô "Số Đúng" và "Số Gần Đúng"
    #         if so_dung and gan_dung:
    #             chinh_xac = abs(float(so_dung) - float(gan_dung))
    #             sai_so_tuyet_doi = abs(float(so_dung) - float(gan_dung))
    #             sai_so_tuong_doi = abs((float(so_dung) - float(gan_dung)) / float(so_dung))
    #         elif so_dung and chinh_xac:
    #             gan_dung = float(so_dung) + float(chinh_xac)
    #             sai_so_tuyet_doi = float(chinh_xac)
    #             sai_so_tuong_doi = float(chinh_xac) / float(so_dung)
    #         elif so_dung and sai_so_tuyet_doi:
    #             gan_dung = float(so_dung) + float(sai_so_tuyet_doi)
    #             chinh_xac = float(sai_so_tuyet_doi)
    #             sai_so_tuong_doi = float(sai_so_tuyet_doi) / float(so_dung)
    #         elif so_dung and sai_so_tuong_doi:
    #             gan_dung = float(so_dung) + float(so_dung) * float(sai_so_tuong_doi)
    #             chinh_xac = float(so_dung) * float(sai_so_tuong_doi)
    #             sai_so_tuyet_doi = float(so_dung) * float(sai_so_tuong_doi)
    #
    #         # Tính giá trị cho ô "Độ Chính Xác"
    #         if chinh_xac and not sai_so_tuyet_doi:
    #             sai_so_tuyet_doi = float(chinh_xac)
    #         elif sai_so_tuyet_doi and not chinh_xac:
    #             chinh_xac = float(sai_so_tuyet_doi)
    #
    #         # Tính giá trị cho ô "Sai Số Tuyệt Đối"
    #         if sai_so_tuyet_doi and not chinh_xac:
    #             chinh_xac = float(sai_so_tuyet_doi)
    #         elif chinh_xac and not sai_so_tuyet_doi:
    #             sai_so_tuyet_doi = float(chinh_xac)
    #
    #         # Tính giá trị cho ô "Sai Số Tương Đối"
    #         if sai_so_tuong_doi and not sai_so_tuyet_doi:
    #             sai_so_tuyet_doi = float(so_dung) * float(sai_so_tuong_doi)
    #         elif sai_so_tuyet_doi and not sai_so_tuong_doi:
    #             sai_so_tuong_doi = float(sai_so_tuyet_doi) / float(so_dung)
    #
    #         # Cập nhật giá trị các ô
    #         self.chinhxac_input6.setText(str(chinh_xac))
    #         self.sai_so_tuyetdoi.setText(str(sai_so_tuyet_doi))
    #         self.sai_so_tuongdoi_input6.setText(str(sai_so_tuong_doi))
    #         self.gan_dung_input6.setText(str(gan_dung))


    def calculate6(self):
        so_dung = self.so_dung_input6.text()
        gan_dung = self.gan_dung_input6.text()
        chinh_xac = self.chinhxac_input6.text()
        quy_tron = self.quytron_input6.text()
        sai_so_tuyet_doi = self.sai_so_tuyetdoi.text()
        sai_so_tuong_doi = self.sai_so_tuongdoi_input6.text()
        # donvi1=''
        # donvi2=''
        # if len(chinh_xac)==1:
        #     donvi1='đơn vị'
        #     donvi2 = 'chục'
        # elif len(chinh_xac)==2:
        #     donvi1='chục'
        #     donvi2 = 'trăm'
        # elif len(chinh_xac)==3:
        #     donvi1='trăm'
        #     donvi2 = 'nghìn'
        # elif len(chinh_xac)==4:
        #     donvi1='nghìn'
        #     donvi2 = 'chục nghìn'
        # elif len(chinh_xac)==5:
        #     donvi1='chục nghìn'
        #     donvi2 = 'trăm nghìn'
        # Kiểm tra số lượng ô đã nhập
        count = 0
        if so_dung:
            count += 1
        if gan_dung:
            count += 1
        if chinh_xac:
            count += 1
        if quy_tron:
            count += 1
        if sai_so_tuyet_doi:
            count += 1
        if sai_so_tuong_doi:
            count += 1
        # Tính toán giá trị các ô còn lại
        if count == 2:
            # Tính giá trị cho ô "Số Đúng" và "Số Gần Đúng"
            if so_dung and gan_dung:
                chinh_xac = abs(float(so_dung) - float(gan_dung))
                sai_so_tuyet_doi = abs(float(so_dung) - float(gan_dung))
                sai_so_tuong_doi_angang = abs((float(so_dung) - float(gan_dung)) / float(so_dung))
                sai_so_tuong_doi_a = abs((float(so_dung) - float(gan_dung)) / float(gan_dung))
                if float(so_dung) != float(gan_dung):
                    result_text = f"Số Đúng: {so_dung}\nSố Gần Đúng: {gan_dung}\nĐộ Chính Xác: {chinh_xac}\nSố Quy Tròn: {quy_tron}\nSai Số Tuyệt Đối \\Delta là: {sai_so_tuyet_doi} và \\Delta \\leq độ chính xác $d={chinh_xac}$  \nSai số tương đối của số đúng : {sai_so_tuong_doi_angang}\nSai số tương đối của số gần đúng : {sai_so_tuong_doi_a}"
                else:
                    result_text = f"Số Đúng: {so_dung}\nSố Gần Đúng: {gan_dung}\nĐộ Chính Xác: {chinh_xac}\nSố Quy Tròn: {quy_tron}\nSai Số Tuyệt Đối \\Delta là: {sai_so_tuyet_doi} và \\Delta \\leq độ chính xác $d={chinh_xac}$ \nSai số tương đối của số đúng : {sai_so_tuong_doi_angang}\nSai số tương đối của số gần đúng : {sai_so_tuong_doi_a}"
                    # Cập nhật giá trị kết quả đến self.result_output
                self.result_output.setPlainText(result_text)
            elif so_dung and chinh_xac:
                gan_dung = float(so_dung) + float(chinh_xac)
                sai_so_tuyet_doi = float(chinh_xac)
                sai_so_tuong_doi = float(chinh_xac) / float(so_dung)
                result_text = f"Số Đúng: {so_dung}\nSố Gần Đúng: {gan_dung}\nĐộ Chính Xác: {chinh_xac}\nSố Quy Tròn: {quy_tron}\nSai Số Tuyệt Đối: {sai_so_tuyet_doi}\nSai Số Tương Đối: {sai_so_tuong_doi}"
                # Cập nhật giá trị kết quả đến self.result_output
                self.result_output.setPlainText(result_text)
            elif gan_dung and chinh_xac:
                so_dung = float(gan_dung) + float(chinh_xac)
                if "." in chinh_xac:
                    # Trường hợp số thập phân - làm tròn theo số thập phân
                    decimal_part = str(chinh_xac).split('.')[1]  # Lấy phần sau dấu thập phân
                    donvi1 = ''
                    donvi2 = ''
                    if len(decimal_part) == 1:
                        donvi2 = 'đơn vị'
                        donvi1 = 'chục'
                    elif len(decimal_part) == 2:
                        donvi2 = 'chục'
                        donvi1 = 'trăm'
                    elif len(decimal_part) == 3:
                        donvi2 = 'trăm'
                        donvi1 = 'nghìn'
                    elif len(decimal_part) == 4:
                        donvi2 = 'nghìn'
                        donvi1 = 'chục nghìn'
                    elif len(decimal_part) == 5:
                        donvi2 = 'chục nghìn'
                        donvi1 = 'trăm nghìn'
                    chinh_xac = float(chinh_xac)
                    quy_tron = round(float(gan_dung), len(decimal_part)-1)
                else:
                    # Trường hợp số nguyên - làm tròn theo số nguyên
                    #chinh_xac = int(chinh_xac)
                    donvi1 = ''
                    donvi2 = ''
                    if len(chinh_xac) == 1:
                        donvi1 = 'đơn vị'
                        donvi2 = 'chục'
                    elif len(chinh_xac) == 2:
                        donvi1 = 'chục'
                        donvi2 = 'trăm'
                    elif len(chinh_xac) == 3:
                        donvi1 = 'trăm'
                        donvi2 = 'nghìn'
                    elif len(chinh_xac) == 4:
                        donvi1 = 'nghìn'
                        donvi2 = 'chục nghìn'
                    elif len(chinh_xac) == 5:
                        donvi1 = 'chục nghìn'
                        donvi2 = 'trăm nghìn'
                    quy_tron = round(float(gan_dung), -len(chinh_xac))
                #quy_tron = round(float(gan_dung), -len(chinh_xac))
                if abs(float(gan_dung)-float(chinh_xac)-float(quy_tron))>abs(float(gan_dung)+float(chinh_xac)-float(quy_tron)):
                    sai_so_tuyet_doi = abs(float(gan_dung)-float(chinh_xac)-float(quy_tron))
                else:
                    sai_so_tuyet_doi = abs(float(gan_dung)+float(chinh_xac)-float(quy_tron))
                sai_so_tuong_doi = float(sai_so_tuyet_doi) / float(quy_tron)
                gan_dung = float(gan_dung)
                chinh_xac = float(chinh_xac)
                quy_tron=float(quy_tron)
                #result_text = f"Số Đúng: {so_dung}\nSố Gần Đúng: {gan_dung}\nĐộ Chính Xác: {chinh_xac}\nVì Hàng lớn nhất của độ chính xác $d={chinh_xac}$ là hàng {donvi1} nên ta quy tròn $a$ đến hàng {donvi2}. Vậy số quy tròn của $a$ là {quy_tron}\nVì {gan_dung}-{chinh_xac} - {quy_tron} < \\overline{{a}}-{quy_tron}< {gan_dung} + {chinh_xac} - {quy_tron} \n Sai Số Tuyệt Đối Của Số Quy Tròn \\Delta là: {sai_so_tuyet_doi}\nSai Số Tương Đối Số Quy Tròn \\delta là: {sai_so_tuong_doi}"
                result_text = f"Số Đúng Trong Khoảng:({gan_dung - chinh_xac}< \\overline{{a}} < {gan_dung + chinh_xac} )\nSố Gần Đúng: {gan_dung}\nĐộ Chính Xác: {chinh_xac}\nVì hàng lớn nhất của độ chính xác $d={chinh_xac}$ là hàng {donvi1} nên ta quy tròn $a$ đến hàng {donvi2}. Vậy số quy tròn của $a$ là {quy_tron}\nVì {gan_dung - chinh_xac} - {quy_tron} < \\overline{{a}} - {quy_tron} < {gan_dung + chinh_xac} - {quy_tron} \nSai Số Tuyệt Đối Của Số Quy Tròn \\Delta là: {sai_so_tuyet_doi}\nSai Số Tương Đối Số Quy Tròn \\delta<\\dfrac{{\\Delta}}{{{quy_tron}}}< {sai_so_tuong_doi}"
                # Cập nhật giá trị kết quả đến self.result_output
                self.result_output.setPlainText(result_text)
            elif so_dung and sai_so_tuyet_doi:
                gan_dung = float(so_dung) + float(sai_so_tuyet_doi)
                chinh_xac = float(sai_so_tuyet_doi)
                sai_so_tuong_doi = float(sai_so_tuyet_doi) / float(so_dung)
            elif so_dung and sai_so_tuong_doi:
                gan_dung = float(so_dung) + float(so_dung) * float(sai_so_tuong_doi)
                chinh_xac = float(so_dung) * float(sai_so_tuong_doi)
                sai_so_tuyet_doi = float(so_dung) * float(sai_so_tuong_doi)

            # Tính giá trị cho ô "Độ Chính Xác"
            if chinh_xac and not sai_so_tuyet_doi:
                sai_so_tuyet_doi = float(chinh_xac)
            elif sai_so_tuyet_doi and not chinh_xac:
                chinh_xac = float(sai_so_tuyet_doi)

            # Tính giá trị cho ô "Sai Số Tuyệt Đối"
            if sai_so_tuyet_doi and not chinh_xac:
                chinh_xac = float(sai_so_tuyet_doi)
            elif chinh_xac and not sai_so_tuyet_doi:
                sai_so_tuyet_doi = float(chinh_xac)

            # Tính giá trị cho ô "Sai Số Tương Đối"
            if sai_so_tuong_doi and not sai_so_tuyet_doi:
                sai_so_tuyet_doi = float(so_dung) * float(sai_so_tuong_doi)
            elif sai_so_tuyet_doi and not sai_so_tuong_doi:
                sai_so_tuong_doi = float(sai_so_tuyet_doi) / float(so_dung)

            # Cập nhật giá trị các ô
            self.chinhxac_input6.setText(str(chinh_xac))
            self.sai_so_tuyetdoi.setText(str(sai_so_tuyet_doi))
            self.sai_so_tuongdoi_input6.setText(str(sai_so_tuong_doi))
            self.gan_dung_input6.setText(str(gan_dung))
            self.so_dung_input6.setText(str(so_dung))
            self.quytron_input6.setText(str(quy_tron))
            # Hiển thị kết quả trong self.result_output
            #result_text = f"Số Đúng: {so_dung}\nSố Gần Đúng: {gan_dung}\nĐộ Chính Xác: {chinh_xac}\nSố Quy Tròn: {quy_tron}\nSai Số Tuyệt Đối: {sai_so_tuyet_doi}\nSai Số Tương Đối: {sai_so_tuong_doi}"
            #self.result_output.setPlainText(result_text)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
