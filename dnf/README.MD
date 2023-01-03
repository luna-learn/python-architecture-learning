参考
https://blog.csdn.net/enteracity/article/details/103674748
https://github.com/Jiahonzheng/JGM-Automator
https://github.com/bbpp222006/Princess-connection
https://www.likecs.com/show-46003.html

serial 操作串口

opencv 
https://blog.csdn.net/qq_45066628/article/details/119342697
Windows下需安装 opencv-contrib-python

PIL Python Image Library Python图像库

scipy

skimage Scikit-Image
https://blog.csdn.net/weixin_53330467/article/details/124259746

pytesseract

easyocr 图像文字识别
https://blog.csdn.net/u010698107/article/details/121736386
Tesseract OCR github地址：https://github.com/tesseract-ocr/tesseract
Windows Tesseract下载地址：https://digi.bib.uni-mannheim.de/tesseract/
Mac和Linux安装方法参考：https://tesseract-ocr.github.io/tessdoc/Installation.html

yolov5 图像识别
https://blog.csdn.net/qq_45945548/article/details/121701492
https://blog.csdn.net/ACL_lihan/article/details/104011405
https://blog.csdn.net/m0_68036862/article/details/124100537
https://github.com/ultralytics/yolov5
git clone https://github.com/ultralytics/yolov5.git
pip install -r requirements.txt -i  https://pypi.tuna.tsinghua.edu.cn/simple
conda install --channel https://conda.anaconda.org/phygbu --file requirements.txt

labelme 标签
pip install labelme 

Anaconda
Anaconda Prompt
https://www.anaconda.com/
conda config --add channels 'https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/'
conda config --remove channels 'https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/'

conda install opencv

pip install pytesseract -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install opencv-python==3.* -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install opencv-contrib-python -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install matplotlib -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install pandas -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install pywin32 -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install pillow -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install serial -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install scipy -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install scikit-image -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install easyocr -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install protobuf  -i https://pypi.tuna.tsinghua.edu.cn/simple
pip install labelme -i https://pypi.tuna.tsinghua.edu.cn/simple


conda update -n base -c defaults conda

conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/

conda config --remove channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --remove channels channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/

anaconda search -t conda pytesseract
anaconda show phygbu/pytesseract
conda install --channel https://conda.anaconda.org/phygbu pytesseract
conda install --channel https://conda.anaconda.org/phygbu pywin32
conda install --channel https://conda.anaconda.org/phygbu scikit-image
conda install --channel https://conda.anaconda.org/phygbu pandas
conda install --channel https://conda.anaconda.org/phygbu scikit-learn
conda install --channel https://conda.anaconda.org/phygbu torch
conda install --channel https://conda.anaconda.org/phygbu PyYAML
conda install --channel https://conda.anaconda.org/phygbu tensorflow
conda install --channel https://conda.anaconda.org/Esri opencv
conda install opencv
conda install pywin32
conda install pytesseract
conda install pandas
conda install scikit-image
conda install scikit-learn
conda install PyYAML