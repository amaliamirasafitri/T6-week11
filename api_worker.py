from PySide6.QtCore import QThread, Signal
import requests

BASE_URL = "https://api.pahrul.my.id/api/posts"

class ApiWorker(QThread):
    success = Signal(object)
    error = Signal(str)

    def __init__(self, method, endpoint="", data=None):
        super().__init__()
        self.method = method
        self.endpoint = endpoint
        self.data = data

    def run(self):
        try:
            url = BASE_URL + self.endpoint

            if self.method == "GET":
                response = requests.get(url, timeout=10)

            elif self.method == "POST":
                response = requests.post(url, json=self.data, timeout=10)

            elif self.method == "PUT":
                response = requests.put(url, json=self.data, timeout=10)

            elif self.method == "DELETE":
                response = requests.delete(url, timeout=10)

            else:
                self.error.emit("Method tidak valid")
                return

            if response.status_code in [200, 201]:
                self.success.emit(response.json())

            elif response.status_code == 422:
                self.error.emit("Slug sudah digunakan / data tidak valid")

            else:
                self.error.emit(
                    f"Error {response.status_code}: {response.text}"
                )

        except requests.exceptions.Timeout:
            self.error.emit("Request timeout")

        except requests.exceptions.ConnectionError:
            self.error.emit("Koneksi gagal")

        except Exception as e:
            self.error.emit(str(e))