deactivatimport os
from PIL import Image
from PIL import ImageFilter
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import ( QFileDialog, QLineEdit, QTextEdit, QListWidget, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QButtonGroup, QRadioButton, QPushButton, QLabel)
from PyQt5.QtGui import QPixmap

app = QApplication([])
papka = QPushButton('Папка')
left = QPushButton('Лево')
right = QPushButton('Право')
mirror = QPushButton('Зеркало')
abrakadabra = QPushButton('Резкость')
black = QPushButton('Ч/Б')
lst =  QListWidget()
picktyre = QLabel('')

layoutv1 = QVBoxLayout()
layoutv2 = QVBoxLayout()

layouth1 = QHBoxLayout()
layouth2 = QHBoxLayout()

layouth1.addLayout(layoutv1, 20)
layouth1.addLayout(layoutv2, 80)

layoutv1.addWidget(papka)
layoutv1.addWidget(lst)

layoutv2.addWidget(picktyre)
layoutv2.addLayout(layouth2)

layouth2.addWidget(left)
layouth2.addWidget(right)
layouth2.addWidget(mirror)
layouth2.addWidget(abrakadabra)
layouth2.addWidget(black)



def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
    print(workdir)

def filter(files, extensions):
    filefilter = []
    for f in files:
        for e in extensions:
            if f.endswith(e):    
                filefilter.append(f)
    return(filefilter)

def showFilenamesList():
    chooseWorkdir()
    if workdir != '':
        fileslist = os.listdir(workdir)
        print(fileslist)
        l = filter(fileslist,['.jpg','.bmp','.png'])
        print('После фильтра')
        print(l)
        lst.clear()
        lst.addItems(l)
    else:
        pass

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.filename = None
    def loadImage(self, filename):
        self.filename = filename
        image_path = os.path.join(workdir, filename)
        self.image = Image.open(image_path)
        self.save_dir='Modifed/'
    def showImage(self,path):
        picktyre.hide()
        pixmapimage = QPixmap(path)
        w, h = picktyre.width(), picktyre.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        picktyre.setPixmap(pixmapimage)
        picktyre.show()
    def do_bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
    def do_blur(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)
workimage = ImageProcessor()
def showChosenImage():
    if lst.currentRow() >= 0:
        filename = lst.currentItem().text()
        workimage.loadImage(filename)
        image_path = os.path.join(workdir, workimage.filename)
        print('путь')
        print(image_path)
        workimage.showImage(image_path)

lst.currentRowChanged.connect(showChosenImage)

papka.clicked.connect(showFilenamesList)
black.clicked.connect(workimage.do_bw)
mirror.clicked.connect(workimage.do_flip)
left.clicked.connect(workimage.do_left)
right.clicked.connect(workimage.do_right)
abrakadabra.clicked.connect(workimage.do_blur)

window = QWidget()
window.resize(640,480)
window.setLayout(layouth1)
window.setWindowTitle('Easy Editor')
window.show()
app.exec_()
