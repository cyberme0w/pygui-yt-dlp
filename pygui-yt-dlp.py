import sys, time, threading
from yt_dlp import YoutubeDL
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtWidgets import QLabel, QLineEdit, QPushButton, QProgressBar
from PySide6.QtGui import QPixmap


ytdlp_options = {
    'format': 'm4a/bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }]
}

class MySingleWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Labels and Text fields
        self.lbl_url    = QLabel("URL:")
        self.txt_url    = QLineEdit()
        
        # TODO: Remove me!
        self.txt_url.setText("https://youtu.be/yzzkb3YayGo")

        self.lbl_title  = QLabel("Title:")
        self.txt_title  = QLineEdit()
        self.lbl_artist = QLabel("Artist:")
        self.txt_artist = QLineEdit()
        self.lbl_album  = QLabel("Album:")
        self.txt_album  = QLineEdit()

        # Download
        self.btn_dl = QPushButton("Download single track")
        self.btn_dl.clicked.connect(self.run_download_thread)
        self.prg_dl = QProgressBar()
        self.prg_dl.setHidden(True)

        # Form Layout
        self.form = QtWidgets.QFormLayout()
        self.form.addRow(self.lbl_url, self.txt_url)
        self.form.addRow(self.lbl_title, self.txt_title)
        self.form.addRow(self.lbl_artist, self.txt_artist)
        self.form.addRow(self.lbl_album, self.txt_album)
        self.form.addRow(self.btn_dl)
        self.form.addRow(self.prg_dl)

        # Base Widget
        self.base = QtWidgets.QGridLayout()
        self.base.addItem(self.form, 1, 1)
        #self.base.addWidget(self.lbl_cover, 1, 2, QtCore.Qt.AlignTop)
        self.base.addWidget(self.btn_dl, 2, 1)
        self.base.addWidget(self.prg_dl, 2, 1)

        # Render
        self.setLayout(self.form)

    def download_function(self, url):
        with YoutubeDL(ytdlp_options) as ydl:
            error_code = ydl.download(url)
        
    @QtCore.Slot()
    def run_download_thread(self):
        # Change some text
        self.btn_dl.setText("Downloading ... ")

        # Generate and execute thread
        downloadThread = threading.Thread(
            target=self.download_function,
            args=(
                self.txt_url.displayText(),
            )
        )
        downloadThread.start()

        #TODO: display "Processing" pop-up
        #with YoutubeDL(ytdlp_options) as ydl:
        #    error_code = ydl.download(self.txt_url.displayText())
        #TODO: hide "Processing" pop-up

        self.btn_dl.setText("Download single track")

class MyAlbumWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

class MyMainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Base Window Properties
        self.title = "PyGUI Downloader"
        self.setWindowTitle(self.title)
        self.width = 800
        self.height = 600
        self.setGeometry(0, 0, self.width, self.height)

        # Tab Bar
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(MySingleWidget(), "Single")
        self.tabs.addTab(MyAlbumWidget(), "Album")
        self.setCentralWidget(self.tabs)

class MyWidget(QtWidgets.QWidget):
    def updateCover(self, new_path):
        self.pixmap_cover = QPixmap(new_path)
        self.pixmap_cover = self.pixmap_cover.scaled(128, 128, QtCore.Qt.KeepAspectRatio)

    def __init__(self):
        super().__init__()
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
        self.prg_dl = QProgressBar()
        self.prg_dl.setHidden(True)

        # Form Layout
        self.form = QtWidgets.QFormLayout()
        self.form.addRow(self.lbl_url, self.txt_url)
        self.form.addRow(self.lbl_title, self.txt_title)
        self.form.addRow(self.lbl_artist, self.txt_artist)
        self.form.addRow(self.lbl_album, self.txt_album)

        # Single Layout
        self.single = QtWidgets.QWidget()
        self.base_single = QtWidgets.QGridLayout()
        self.base_single.addItem(self.form, 1, 1)
        self.base_single.addWidget(self.lbl_cover, 1, 2, QtCore.Qt.AlignTop)
        self.base_single.addWidget(self.btn_dl, 2, 1)
        self.base_single.addWidget(self.prg_dl, 2, 1)
        
        # Playlist Layout
        self.playlist = QtWidgets.QWidget()
        self.base_playlist = QtWidgets.QGridLayout(self.playlist)
        self.base_playlist.addItem(self.form, 1, 1)
        self.base_playlist.addWidget(self.lbl_cover, 1, 2, QtCore.Qt.AlignTop)
        self.base_playlist.addWidget(self.btn_dl, 2, 1)

        # Tabs
        self.tabs = QtWidgets.QTabWidget()
        self.tabs.addTab(self.base_single, "Single")
        self.tabs.addTab(self.base_playlist, "Playlist")

        # Root
        self.setLayout(self.tabs)

    @QtCore.Slot()
    def download(self):
        self.btn_dl.setHidden(True)
        self.prg_dl.setHidden(False)
        
        #TODO: display "Processing" pop-up
        with YoutubeDL(ytdlp_options) as ydl:
            error_code = ydl.download(self.txt_url.displayText())
        #TODO: hide "Processing" pop-up
        self.btn_dl.setHidden(False)
        self.prg_dl.setHidden(True)

if(__name__ == "__main__"):
    app = QtWidgets.QApplication([])
    window = MyMainWindow()
    window.show()
    #widget.resize(800, 200)
    sys.exit(app.exec())
