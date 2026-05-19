from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTableWidget,
    QTableWidgetItem, QLineEdit, QTextEdit,
    QMessageBox, QComboBox
)

from api_worker import ApiWorker

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_id = None

        self.setWindowTitle("Post Manager")
        self.resize(1100, 600)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        # LEFT
        left_layout = QVBoxLayout()

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Title", "Author", "Status"]
        )

        self.table.cellClicked.connect(self.select_post)

        left_layout.addWidget(self.table)

        btn_layout = QHBoxLayout()

        self.btn_refresh = QPushButton("Refresh")
        self.btn_add = QPushButton("Tambah")
        self.btn_edit = QPushButton("Edit")
        self.btn_delete = QPushButton("Hapus")

        self.btn_edit.setEnabled(False)
        self.btn_delete.setEnabled(False)

        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)

        left_layout.addLayout(btn_layout)

        # RIGHT
        right_layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Title")

        self.body_input = QTextEdit()

        self.author_input = QLineEdit()
        self.author_input.setPlaceholderText("Author")

        self.slug_input = QLineEdit()
        self.slug_input.setPlaceholderText("Slug")

        self.status_input = QComboBox()
        self.status_input.addItems(["published", "draft"])

        self.detail_label = QLabel("Detail Post")

        right_layout.addWidget(QLabel("Title"))
        right_layout.addWidget(self.title_input)

        right_layout.addWidget(QLabel("Body"))
        right_layout.addWidget(self.body_input)

        right_layout.addWidget(QLabel("Author"))
        right_layout.addWidget(self.author_input)

        right_layout.addWidget(QLabel("Slug"))
        right_layout.addWidget(self.slug_input)

        right_layout.addWidget(QLabel("Status"))
        right_layout.addWidget(self.status_input)

        right_layout.addWidget(self.detail_label)

        self.status_label = QLabel("")
        right_layout.addWidget(self.status_label)

        self.layout.addLayout(left_layout, 2)
        self.layout.addLayout(right_layout, 1)

        # BUTTON EVENTS
        self.btn_refresh.clicked.connect(self.load_posts)
        self.btn_add.clicked.connect(self.add_post)
        self.btn_edit.clicked.connect(self.edit_post)
        self.btn_delete.clicked.connect(self.delete_post)

        self.load_posts()

    def set_loading(self, text):
        self.status_label.setText(text)

    def clear_form(self):
        self.title_input.clear()
        self.body_input.clear()
        self.author_input.clear()
        self.slug_input.clear()

    def get_form_data(self):
        return {
            "title": self.title_input.text(),
            "body": self.body_input.toPlainText(),
            "author": self.author_input.text(),
            "slug": self.slug_input.text(),
            "status": self.status_input.currentText()
        }

    def load_posts(self):
        self.set_loading("Loading posts...")

        self.worker = ApiWorker("GET")
        self.worker.success.connect(self.show_posts)
        self.worker.error.connect(self.show_error)
        self.worker.start()

    def show_posts(self, data):
        posts = data["data"]

        self.table.setRowCount(len(posts))

        for row, post in enumerate(posts):
            self.table.setItem(row, 0,
                               QTableWidgetItem(str(post["id"])))
            self.table.setItem(row, 1,
                               QTableWidgetItem(post["title"]))
            self.table.setItem(row, 2,
                               QTableWidgetItem(post["author"]))
            self.table.setItem(row, 3,
                               QTableWidgetItem(post["status"]))

        self.set_loading("Data berhasil dimuat")

    def select_post(self, row):
        self.selected_id = self.table.item(row, 0).text()

        self.btn_edit.setEnabled(True)
        self.btn_delete.setEnabled(True)

        self.load_detail(self.selected_id)

    def load_detail(self, post_id):
        self.set_loading("Loading detail...")

        self.worker = ApiWorker("GET", f"/{post_id}")
        self.worker.success.connect(self.show_detail)
        self.worker.error.connect(self.show_error)
        self.worker.start()

    def show_detail(self, data):
        post = data["data"]

        self.title_input.setText(post["title"])
        self.body_input.setText(post["body"])
        self.author_input.setText(post["author"])
        self.slug_input.setText(post["slug"])

        self.detail_label.setText(
            f"Comments: {len(post['comments'])}"
        )

        self.set_loading("Detail loaded")

    def add_post(self):
        self.set_loading("Menambahkan post...")

        self.worker = ApiWorker(
            "POST",
            data=self.get_form_data()
        )

        self.worker.success.connect(self.add_success)
        self.worker.error.connect(self.show_error)
        self.worker.start()

    def add_success(self, data):
        QMessageBox.information(
            self,
            "Sukses",
            f"Post berhasil ditambahkan\nID: {data['data']['id']}"
        )

        self.clear_form()
        self.load_posts()

    def edit_post(self):
        if not self.selected_id:
            return

        self.set_loading("Mengupdate post...")

        self.worker = ApiWorker(
            "PUT",
            f"/{self.selected_id}",
            self.get_form_data()
        )

        self.worker.success.connect(self.edit_success)
        self.worker.error.connect(self.show_error)
        self.worker.start()

    def edit_success(self, data):
        QMessageBox.information(
            self,
            "Sukses",
            "Post berhasil diupdate"
        )

        self.load_posts()

    def delete_post(self):
        if not self.selected_id:
            return

        confirm = QMessageBox.question(
            self,
            "Konfirmasi",
            "Yakin ingin menghapus post?"
        )

        if confirm == QMessageBox.Yes:

            self.worker = ApiWorker(
                "DELETE",
                f"/{self.selected_id}"
            )

            self.worker.success.connect(self.delete_success)
            self.worker.error.connect(self.show_error)
            self.worker.start()

    def delete_success(self, data):
        QMessageBox.information(
            self,
            "Sukses",
            "Post berhasil dihapus"
        )

        self.load_posts()

    def show_error(self, message):
        QMessageBox.critical(
            self,
            "Error",
            message
        )

        self.set_loading(message)