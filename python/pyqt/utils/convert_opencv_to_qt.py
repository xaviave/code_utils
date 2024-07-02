# PyQt imports
import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap


# TODO delete if not used 2023-01-30
def convert_opencv_to_qt(cv_img):
    """Convert from an opencv image to QPixmap
    Parameters:
    ---------------
    cv_img    opencv image.

    Returns:
    ----------
    QPixmap.fromImage(p)       QPixmap image, (300, 300)

    """
    rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    h, w, ch = rgb_image.shape
    bytes_per_line = ch * w
    convert_to_Qt_format = QImage(
        rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888
    )
    p = convert_to_Qt_format.scaled(300, 300, Qt.KeepAspectRatio)

    return QPixmap.fromImage(p)
