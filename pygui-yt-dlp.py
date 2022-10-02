import sys
from yt_dlp import YoutubeDL
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton
from PySide6.QtGui import QPixmap

ydl_opts = {
    'format': 'm4a/bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }]
}

# https://youtu.be/-UWuW2npPGc


class MyWidget(QtWidgets.QWidget):
    def updateCover(self, new_path):
        self.pixmap_cover = QPixmap(new_path)
        self.pixmap_cover = self.pixmap_cover.scaled(128, 128, QtCore.Qt.KeepAspectRatio)

    def __init__(self):
        super().__init__()
        self.title = "PyGui Downloader"
        self.setWindowTitle(self.title)

        # URL and tags
        self.lbl_url    = QLabel("URL:")
        self.txt_url    = QLineEdit()
        self.lbl_title  = QLabel("Title:")
        self.txt_title  = QLineEdit()
        self.lbl_artist = QLabel("Artist:")
        self.txt_artist = QLineEdit()
        self.lbl_album  = QLabel("Album:")
        self.txt_album  = QLineEdit()

        # Cover
        self.pixmap_cover = QPixmap("/home/cyberme0w/Pictures/AlbumCovers/rabbit2.jpg")
        self.pixmap_cover = self.pixmap_cover.scaled(128, 128, QtCore.Qt.KeepAspectRatio)
        self.updateCover("/home/cyberme0w/Pictures/AlbumCovers/test.jpg")
        self.lbl_cover  = QLabel()
        self.lbl_cover.setPixmap(self.pixmap_cover)
        
        # Download
        self.btn_dl = QPushButton("Download")
        self.btn_dl.clicked.connect(self.download)

        # Form Layout
        form = QtWidgets.QFormLayout()
        form.addRow(self.lbl_url, self.txt_url)
        form.addRow(self.lbl_title, self.txt_title)
        form.addRow(self.lbl_artist, self.txt_artist)
        form.addRow(self.lbl_album, self.txt_album)

        # Root Layout
        root = QtWidgets.QGridLayout()
        root.addItem(form, 1, 1)
        root.addWidget(self.lbl_cover, 1, 2, QtCore.Qt.AlignTop)
        root.addWidget(self.btn_dl, 2, 1)
        self.setLayout(root)


    @QtCore.Slot()
    def download(self):
        #TODO: display "Processing" pop-up
        with YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(self.txt_url.displayText())
        #TODO: hide "Processing" pop-up

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.resize(800, 200)
    widget.show()
    sys.exit(app.exec())
