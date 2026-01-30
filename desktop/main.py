import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from api_client import ApiClient, ApiError


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Login')
        self.setModal(True)

        self.base_url = QLineEdit('http://127.0.0.1:8000')
        self.username = QLineEdit('demo')
        self.password = QLineEdit('demo12345')
        self.password.setEchoMode(QLineEdit.Password)

        form = QFormLayout()
        form.addRow('Backend URL', self.base_url)
        form.addRow('Username', self.username)
        form.addRow('Password', self.password)

        self.login_btn = QPushButton('Login')
        self.cancel_btn = QPushButton('Cancel')
        self.login_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

        btns = QHBoxLayout()
        btns.addStretch(1)
        btns.addWidget(self.cancel_btn)
        btns.addWidget(self.login_btn)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addLayout(btns)
        self.setLayout(layout)


class ChartsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def render_distribution(self, dist: dict):
        self.figure.clear()
        ax1 = self.figure.add_subplot(1, 2, 1)
        ax2 = self.figure.add_subplot(1, 2, 2)

        labels = list(dist.keys())
        values = list(dist.values())

        if labels and values:
            ax1.pie(values, labels=labels, autopct='%1.0f%%')
            ax1.set_title('Types (Pie)')

            ax2.bar(labels, values)
            ax2.set_title('Types (Bar)')
            ax2.tick_params(axis='x', labelrotation=45)
        else:
            ax1.text(0.5, 0.5, 'No data', ha='center', va='center')
            ax2.text(0.5, 0.5, 'No data', ha='center', va='center')

        self.figure.tight_layout()
        self.canvas.draw()


class MainWindow(QMainWindow):
    def __init__(self, api: ApiClient):
        super().__init__()
        self.api = api
        self.setWindowTitle('Chem Flow Monitor (Desktop)')

        self.file_label = QLabel('No file selected')
        self.pick_btn = QPushButton('Choose CSV')
        self.upload_btn = QPushButton('Upload')
        self.upload_btn.setEnabled(False)

        self.pick_btn.clicked.connect(self.choose_file)
        self.upload_btn.clicked.connect(self.upload_file)

        upload_row = QHBoxLayout()
        upload_row.addWidget(self.pick_btn)
        upload_row.addWidget(self.file_label, 1)
        upload_row.addWidget(self.upload_btn)

        self.total_label = QLabel('—')
        self.avg_flow_label = QLabel('—')
        self.avg_press_label = QLabel('—')
        self.avg_temp_label = QLabel('—')

        stats_form = QFormLayout()
        stats_form.addRow('Total Equipment', self.total_label)
        stats_form.addRow('Avg Flowrate', self.avg_flow_label)
        stats_form.addRow('Avg Pressure', self.avg_press_label)
        stats_form.addRow('Avg Temperature', self.avg_temp_label)

        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_layout.addLayout(upload_row)
        left_layout.addLayout(stats_form)
        left_layout.addStretch(1)
        left_panel.setLayout(left_layout)

        self.charts = ChartsWidget()

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(self.charts)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(['ID', 'Filename', 'Uploaded', 'Total'])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        self.load_btn = QPushButton('Load Selected')
        self.pdf_btn = QPushButton('Download PDF')
        self.refresh_btn = QPushButton('Refresh History')

        self.load_btn.clicked.connect(self.load_selected)
        self.pdf_btn.clicked.connect(self.download_selected_pdf)
        self.refresh_btn.clicked.connect(self.refresh_history)

        hist_btns = QHBoxLayout()
        hist_btns.addWidget(self.refresh_btn)
        hist_btns.addStretch(1)
        hist_btns.addWidget(self.load_btn)
        hist_btns.addWidget(self.pdf_btn)

        history_panel = QWidget()
        history_layout = QVBoxLayout()
        history_layout.addWidget(QLabel('History (last 5)'))
        history_layout.addWidget(self.table)
        history_layout.addLayout(hist_btns)
        history_panel.setLayout(history_layout)

        root = QWidget()
        root_layout = QVBoxLayout()
        root_layout.addWidget(splitter)
        root_layout.addWidget(history_panel)
        root.setLayout(root_layout)

        self.setCentralWidget(root)

        self.selected_file = None
        self.current_dataset_id = None

        self.refresh_history()

    def choose_file(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Select CSV', '', 'CSV Files (*.csv);;All Files (*)')
        if not path:
            return
        self.selected_file = path
        self.file_label.setText(path)
        self.upload_btn.setEnabled(True)

    def _set_stats(self, dataset):
        self.current_dataset_id = dataset.id
        self.total_label.setText(str(dataset.total_count))
        self.avg_flow_label.setText(self._fmt(dataset.avg_flowrate))
        self.avg_press_label.setText(self._fmt(dataset.avg_pressure))
        self.avg_temp_label.setText(self._fmt(dataset.avg_temperature))
        self.charts.render_distribution(dataset.type_distribution)

    def _fmt(self, v):
        if v is None:
            return '—'
        try:
            return f'{float(v):.2f}'
        except Exception:
            return str(v)

    def upload_file(self):
        if not self.selected_file:
            return
        try:
            dataset = self.api.upload_csv(self.selected_file)
            self._set_stats(dataset)
            self.refresh_history()
            QMessageBox.information(self, 'Upload', f'Uploaded dataset {dataset.id}')
        except ApiError as e:
            QMessageBox.critical(self, 'Upload failed', str(e))

    def refresh_history(self):
        try:
            items = self.api.history()
        except ApiError as e:
            QMessageBox.critical(self, 'History failed', str(e))
            return

        self.table.setRowCount(0)
        for d in items:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(d.id)))
            self.table.setItem(row, 1, QTableWidgetItem(d.original_filename))
            self.table.setItem(row, 2, QTableWidgetItem(d.created_at))
            self.table.setItem(row, 3, QTableWidgetItem(str(d.total_count)))

        self.table.resizeColumnsToContents()

        if items and self.current_dataset_id is None:
            self._set_stats(items[0])

    def _selected_dataset_id(self):
        sel = self.table.selectionModel().selectedRows()
        if not sel:
            return None
        row = sel[0].row()
        item = self.table.item(row, 0)
        if not item:
            return None
        try:
            return int(item.text())
        except Exception:
            return None

    def load_selected(self):
        dataset_id = self._selected_dataset_id()
        if dataset_id is None:
            QMessageBox.information(self, 'Load', 'Select a dataset row first')
            return
        try:
            dataset = self.api.dataset_detail(dataset_id)
            self._set_stats(dataset)
        except ApiError as e:
            QMessageBox.critical(self, 'Load failed', str(e))

    def download_selected_pdf(self):
        dataset_id = self._selected_dataset_id() or self.current_dataset_id
        if dataset_id is None:
            QMessageBox.information(self, 'PDF', 'No dataset selected')
            return

        path, _ = QFileDialog.getSaveFileName(self, 'Save PDF', f'dataset_{dataset_id}_report.pdf', 'PDF Files (*.pdf)')
        if not path:
            return

        try:
            pdf_bytes = self.api.download_report_pdf(dataset_id)
            with open(path, 'wb') as f:
                f.write(pdf_bytes)
            QMessageBox.information(self, 'PDF', f'Saved report to {path}')
        except ApiError as e:
            QMessageBox.critical(self, 'PDF failed', str(e))


def main():
    app = QApplication(sys.argv)

    dlg = LoginDialog()
    if dlg.exec_() != QDialog.Accepted:
        return 0

    api = ApiClient(dlg.base_url.text())
    try:
        api.login(dlg.username.text(), dlg.password.text())
    except ApiError as e:
        QMessageBox.critical(None, 'Login failed', str(e))
        return 1

    w = MainWindow(api)
    w.resize(1100, 720)
    w.show()

    return app.exec_()


if __name__ == '__main__':
    raise SystemExit(main())
