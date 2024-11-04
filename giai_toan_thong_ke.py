import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, \
    QGroupBox, QGridLayout, QMessageBox,QCheckBox
import numpy as np
from collections import Counter
class giai_toan_thong_ke(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tính Toán Thống Kê Nâng Cao")

        # Tạo checkbox cho kiểu nhập liệu
        self.groupedDataCheckbox = QCheckBox("Nhập dữ liệu dạng khoảng")
        self.groupedDataCheckbox.stateChanged.connect(self.updateGroupedDataLayout)
        # Thiết lập trạng thái mặc định cho checkbox là đã chọn (tích)


        # Cấu hình các widget cho dữ liệu nhóm có tần số
        self.groupedDataGroupBox = QGroupBox("Thống kê nhóm có tần số")
        self.nhomLineEdit = QLineEdit()
        self.tanSoLineEdit = QLineEdit()
        self.tanSoLineEdit.setPlaceholderText("Nhập tần số, phân tách bằng dấu phẩy")  # Thêm placeholder text
        self.resultTextEdit = QTextEdit()
        self.calculateGroupedDataButton = QPushButton("Tính Thống Kê")
        self.calculateGroupedDataButton.clicked.connect(self.calculateGroupedDataStatistics)

        # Cấu hình layout cho dữ liệu nhóm có tần số
        groupedDataLayout = QVBoxLayout()
        groupedDataLayout.addWidget(QLabel("Dữ liệu riêng lẻ:"))
        groupedDataLayout.addWidget(self.nhomLineEdit)
        groupedDataLayout.addWidget(QLabel("Tần số:"))
        groupedDataLayout.addWidget(self.tanSoLineEdit)
        groupedDataLayout.addWidget(self.calculateGroupedDataButton)
        self.groupedDataGroupBox.setLayout(groupedDataLayout)

        # Cấu hình các widget cho dữ liệu nhóm không có tần số
        self.ungroupedDataGroupBox = QGroupBox("Thống kê nhóm không có tần số")
        self.ungroupedNhomLineEdit = QLineEdit()
        self.ungroupedNhomLineEdit.setPlaceholderText("Nhập dãy số, phân tách bằng dấu phẩy")  # Thêm placeholder text
        self.calculateUngroupedDataButton = QPushButton("Tính Thống Kê")
        self.calculateUngroupedDataButton.clicked.connect(self.calculateUngroupedDataStatistics)

        # Cấu hình layout cho dữ liệu nhóm không có tần số
        ungroupedDataLayout = QVBoxLayout()
        ungroupedDataLayout.addWidget(QLabel("Dữ liệu nhóm:"))
        ungroupedDataLayout.addWidget(self.ungroupedNhomLineEdit)
        ungroupedDataLayout.addWidget(self.calculateUngroupedDataButton)
        self.ungroupedDataGroupBox.setLayout(ungroupedDataLayout)
        self.groupedDataCheckbox.setChecked(True)
        # Tạo layout chính và thêm checkbox vào đó
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.groupedDataCheckbox)
        mainLayout.addWidget(self.groupedDataGroupBox)
        mainLayout.addWidget(self.ungroupedDataGroupBox)
        mainLayout.addWidget(self.resultTextEdit)
        self.resize(1000, 900)
        self.setLayout(mainLayout)

    def updateGroupedDataLayout(self, state):
        if state == 2:  # Kiểm tra nếu checkbox được tích
            self.nhomLineEdit.setPlaceholderText("Nhập dữ liệu dạng nữa khoảng [a;b) không có dấu phẩy")
        else:
            self.nhomLineEdit.setPlaceholderText("Nhập dãy giái trị đại diện, phân tách bằng dấu phẩy")

    def findOutliers(self,data):
        quartile_1, quartile_3 = np.percentile(data, [25, 75])
        iqr = quartile_3 - quartile_1
        lower_bound = quartile_1 - 1.5 * iqr
        upper_bound = quartile_3 + 1.5 * iqr
        outliers = [value for value in data if value < lower_bound or value > upper_bound]
        return outliers
    def convertRangeDataToValues(self,range_data):
        values = []
        ranges = range_data.split()
        for r in ranges:
            start, end = map(int, r[1:-1].split(";"))
            values.append((start + end) / 2)  # Lấy giá trị trung bình của mỗi khoảng
        return np.array(values)

    def calculateRange(self,data):
        return np.max(data) - np.min(data)
    def calculateGroupedDataStatistics(self):
        try:
            # Lấy dữ liệu nhóm từ QLineEdit và chuyển đổi thành mảng numpy
            if self.groupedDataCheckbox.isChecked():
                nhom_str = self.nhomLineEdit.text()
                nhom_str = nhom_str.replace(' ','').replace('),[',') [').replace(');[',') [').replace(')[',') [')
                nhom = self.convertRangeDataToValues(nhom_str)
            else:
                nhom_str = self.nhomLineEdit.text()
                # nhom_str = nhom_str.replace(';', ',').replace(' ','')
                nhom = np.array([float(x.strip()) for x in nhom_str.split(",")])
            # nhom = np.array([float(x.strip()) for x in nhom_str.split(",")])
            # Tính khoảng biến thiên
            data_range = self.calculateRange(nhom)
            # Tìm giá trị ngoại lai
            outliers = self.findOutliers(nhom)
            # Lấy dữ liệu tần số từ QLineEdit và chuyển đổi thành mảng numpy
            tan_so_str = self.tanSoLineEdit.text()
            tan_so = np.array([int(x.strip()) for x in tan_so_str.split(",")])

            # Kiểm tra xem số lượng dữ liệu nhóm và tần số có khớp nhau không
            if len(nhom) != len(tan_so):
                raise ValueError("Số lượng dữ liệu nhóm và tần số không khớp nhau.")

            # Tính các giá trị thống kê
            trung_binh = np.average(nhom, weights=tan_so)
            trung_vi = np.median(nhom)
            phuong_sai = np.average((nhom - trung_binh)**2, weights=tan_so)
            do_lech_chuan = np.sqrt(phuong_sai)
            mot = nhom[np.argmax(tan_so)]
            tu_phan_vi = np.percentile(nhom, [25, 50, 75])

            # Hiển thị kết quả
            result_text = f"Tất cả các giá trị thống kê:\n\n"
            result_text += f"Trung bình: {trung_binh}\n"
            result_text += f"Trung vị: {trung_vi}\n"
            result_text += f"Phương sai: {phuong_sai}\n"
            result_text += f"Độ lệch chuẩn: {do_lech_chuan}\n"
            result_text += f"Mốt: {mot}\n"
            result_text += f"Tứ phân vị: {tu_phan_vi}\n"
            result_text += f"Khoảng biến thiên: {data_range}\n"
            result_text += f"Giá trị ngoại lai: {outliers}\n"
            self.resultTextEdit.setText(result_text)

        except Exception as e:
            # Hiển thị cửa sổ thông báo lỗi
            QMessageBox.warning(self, "Lỗi", f"Có lỗi xảy ra: {e}\nVui lòng kiểm tra lại dữ liệu và thử lại.")

    def calculateUngroupedDataStatistics(self):
        try:
            # Lấy dữ liệu nhóm từ QLineEdit và chuyển đổi thành mảng numpy
            nhom_str = self.ungroupedNhomLineEdit.text()
            nhom = np.array([float(x.strip()) for x in nhom_str.split(",")])
            # Tìm giá trị ngoại lai
            outliers = self.findOutliers(nhom)
            # Tính khoảng biến thiên
            data_range = self.calculateRange(nhom)
            # Tính các giá trị thống kê
            trung_binh = np.mean(nhom)
            trung_vi = np.median(nhom)
            phuong_sai = np.var(nhom)
            do_lech_chuan = np.std(nhom)
            mot = Counter(nhom).most_common(1)[0][0]  # Tìm số xuất hiện nhiều nhất (mốt)
            # Xác định nếu có nhiều hơn một số xuất hiện nhiều nhất
            most_common = Counter(nhom).most_common()
            most_common_values = [str(value) for value, count in most_common if count == most_common[0][1]]
            if len(most_common_values) > 1:
                mot = f"Có các mốt: {', '.join(most_common_values)} với số lần xuất hiện là {most_common[0][1]}"

            tu_phan_vi = np.percentile(nhom, [25, 50, 75])

            # Hiển thị kết quả
            result_text = f"Tất cả các giá trị thống kê:\n\n"
            result_text += f"Trung bình: {trung_binh}\n"
            result_text += f"Trung vị: {trung_vi}\n"
            result_text += f"Phương sai: {phuong_sai}\n"
            result_text += f"Độ lệch chuẩn: {do_lech_chuan}\n"
            result_text += f"Mốt: {mot}\n"
            result_text += f"Tứ phân vị: {tu_phan_vi}\n"
            result_text += f"Khoảng biến thiên: {data_range}\n"
            result_text += f"Giá trị ngoại lai: {outliers}\n"
            self.resultTextEdit.setText(result_text)

        except Exception as e:
            # Hiển thị cửa sổ thông báo lỗi
            QMessageBox.warning(self, "Lỗi", f"Có lỗi xảy ra: {e}\nVui lòng kiểm tra lại dữ liệu và thử lại.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = giai_toan_thong_ke()
    dialog.show()
    sys.exit(app.exec_())
