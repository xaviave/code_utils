from math import log10

from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QSlider


class LogSlider(QSlider):
    """This class is used to override the QSlider paintEvent, since the normal
    QSlider doesn't support for logarithmic scale we made our own. It is very
    specific and not generalised. It works for values from 0.01-100. I don't think
    it is worth explaining how it works. If a change is necessary rewrite it all.
    """

    def __init__(self, *args):
        super().__init__(*args)

        self.setFixedHeight(40)

    def paintEvent(self, event):
        """Overriding QSlider paintEvent."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(QColor("darkgrey"), 2))

        half = self.height() * 0.5
        threeQuarters = self.height() * 0.75
        full = self.height()

        mainTicks = [
            pow(10, i)
            for i in range(int(self.minimum() / 100), int(self.maximum() / 100 + 1))
        ]
        ticks = []

        # creates x position for log scale ticks
        for n in mainTicks[:-1]:
            for i in range(1, 11):
                ticks.append((log10(n * i) + 2) * (self.width() / (len(mainTicks) - 1)))
        # draws log scale ticks
        for tick in ticks:
            painter.drawLine(int(tick), int(half + 2), int(tick), int(threeQuarters))

        # x/yshift are trial and error values for nicer visual positioning of the tick marks
        yShift = -5
        xShift = -5
        for mainTick in mainTicks:
            x = (log10(mainTick) + 2) * (self.width() / (len(mainTicks) - 1))
            painter.drawLine(int(x), int(half + 2), int(x), int(full - 2))
            painter.setPen(QPen(QColor("black"), 2))
            # draws label for 0.01, 0.1 ... 100
            if mainTick == 0.01:
                painter.drawText(int(x), int(half + yShift), str(mainTick))
            elif mainTick == 0.1:
                painter.drawText(int(x + xShift * 2), int(half + yShift), str(mainTick))
            elif mainTick == 1:
                painter.drawText(int(x + xShift), int(half + yShift), str(mainTick))
            elif mainTick == 10:
                painter.drawText(int(x + xShift * 2), int(half + yShift), str(mainTick))
            else:
                painter.drawText(int(x + xShift * 6), int(half + yShift), str(mainTick))
            painter.setPen(QPen(QColor("darkgrey"), 2))

        # fix end ticks
        painter.drawLine(1, int(half + 2), 1, int(full - 2))
        painter.drawLine(
            int(self.width() - 1), int(half + 2), int(self.width() - 1), int(full - 2)
        )

        super().paintEvent(event)
