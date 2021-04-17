#создай тут фоторедактор Easy Editor!
import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QListWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter
from PIL.ImageFilter import BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES, SMOOTH, SMOOTH_MORE, SHARPEN, GaussianBlur, UnsharpMask


app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Easy Editor')
main_win.resize(700, 500)
lb_img = QLabel('Картинка')
btn_dir = QPushButton('Папка')
lw_files = QListWidget()

btn_left = QPushButton('Влево')
btn_right = QPushButton('Вправо')
btn_flip = QPushButton('Отзеркалить')
btn_sharp = QPushButton('Резкость')
btn_color = QPushButton('Ч/Б')

row_lay = QHBoxLayout()
col1_lay = QVBoxLayout()
col2_lay = QVBoxLayout()
col1_lay.addWidget(btn_dir)
col1_lay.addWidget(lw_files)
col2_lay.addWidget(lb_img)
row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_flip)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_color)
col2_lay.addLayout(row_tools)

row_lay.addLayout(col1_lay, 20)
row_lay.addLayout(col2_lay, 80)
main_win.setLayout(row_lay)


main_win.show()

workdir = ''

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def chooseWorkDir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions = ['.jpg', '.jpeg', '.bmp', '.png', '.gif']
    chooseWorkDir()
    filenames = filter(os.listdir(workdir), extensions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)



class ImageProcessor:
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = 'Modified/'

    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)

    def showImage(label, path):
        lb_img.hide()
        pixmapimg = QPixmap(path)
        w, h = lb_img.width(), lb_img.height()
        pixmapimg = pixmapimg.scaled(w, h, Qt.KeepAspectRatio)
        lb_img.setPixmap(pixmapimg)
        lb_img.show()

    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        img_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(img_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        img_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(img_path)

    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        img_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(img_path)

    def do_sharpnes(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        img_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(img_path)

workimg = ImageProcessor()

def showChosenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        workimg.loadImage(filename)
        image_path = os.path.join(workdir, workimg.filename)
        workimg.showImage(image_path)

btn_dir.clicked.connect(showFilenamesList)
lw_files.currentRowChanged.connect(showChosenImage)
btn_color.clicked.connect(workimg.do_bw)
btn_left.clicked.connect(workimg.do_left)
btn_right.clicked.connect(workimg.do_right)
btn_flip.clicked.connect(workimg.do_flip)
btn_sharp.clicked.connect(workimg.do_sharpnes)

app.exec_()