from enum import Enum
from functools import partial
from math import log10

from .log_slider import LogSlider
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget


class DoubleSlider(QWidget):
    accelerated = pyqtSignal(str)

    def __init__(
        self,
        initialValue,
        minValue,
        maxValue,
        maxAcceleration,
        upperSliderPosition,
        lowerSliderPosition,
        numberOfDecimals=2,
        infOverflow=False,
    ):
        super().__init__()

        self.value = initialValue
        self.minValue = minValue
        self.maxValue = maxValue
        self.maxAcceleration = maxAcceleration
        self.numberOfDecimals = numberOfDecimals
        self.infOverflow = infOverflow

        # Min and max value of the sliders
        self.upperSliderPosition = log10(upperSliderPosition) * 100
        self.lowerSliderPosition = log10(lowerSliderPosition) * 100

        self.timer = None

        self.initUI()

    def initUI(self):
        self.upperWidget = QWidget()
        self.upperWidget.setLayout(QHBoxLayout())

        self.lowerWidget = QWidget()
        self.lowerWidget.setLayout(QHBoxLayout())

        # The upper slider is associated with large adjustment
        self.upperLabel = QLabel("Large Adjustment")
        self.upperSlider = LogSlider(Qt.Horizontal)
        self.upperSlider.setRange(-200, 200)
        self.upperSlider.setValue(int(self.upperSliderPosition))
        self.upperSlider.valueChanged.connect(self.onUpperSliderChanged)
        self.upperValueLabel = QLabel(
            f"{round(pow(10, self.upperSlider.value()/100.0), 2):.2f}"
        )
        self.upperValueLabel.setFixedWidth(50)
        self.upperValueLabel.setAlignment(Qt.AlignCenter)

        # The upper slider is associated with small adjustment
        self.lowerLabel = QLabel("Small Adjustment")
        self.lowerSlider = LogSlider(Qt.Horizontal)
        self.lowerSlider.setRange(-200, 200)
        self.lowerSlider.setValue(int(self.lowerSliderPosition))
        self.lowerSlider.valueChanged.connect(self.onLowerSliderChanged)
        self.lowerValueLabel = QLabel(
            f"{round(pow(10, self.lowerSlider.value()/100.0), 2):.2f}"
        )
        self.lowerValueLabel.setFixedWidth(50)
        self.lowerValueLabel.setAlignment(Qt.AlignCenter)

        self.buttons = self.createControls()

        # Displays upperSlider and buttons
        self.upperWidget.layout().addWidget(self.upperLabel)
        self.upperWidget.layout().addWidget(self.upperSlider)
        self.upperWidget.layout().addWidget(self.upperValueLabel)
        self.upperWidget.layout().addWidget(self.buttons[Acceleration.FastUp])
        self.upperWidget.layout().addWidget(self.buttons[Acceleration.FastDown])

        # Displays lowerSlider and buttons
        self.lowerWidget.layout().addWidget(self.lowerLabel)
        self.lowerWidget.layout().addWidget(self.lowerSlider)
        self.lowerWidget.layout().addWidget(self.lowerValueLabel)
        self.lowerWidget.layout().addWidget(self.buttons[Acceleration.SlowUp])
        self.lowerWidget.layout().addWidget(self.buttons[Acceleration.SlowDown])

        # Add upperSlider and lowerSlider to main layout
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)
        self.layout().addWidget(self.upperWidget)
        self.layout().addWidget(self.lowerWidget)

    def _getLogValue(self, value):
        """Gets log value depending on our slider range (-200, 200), our
        logSlider is depending on this specific range.
        """
        return pow(10, value / 100.0)

    def onLowerSliderChanged(self, n):
        """Updates lower slider label that displays the recalculated slider
        value. Prevents the lower slider value from going above the upper
        slider value.
        """
        if n > self.upperSlider.value():
            n = self.upperSlider.value()
        self.lowerSlider.setValue(int(n))
        self.lowerValueLabel.setText(f"{round(self._getLogValue(n), 2):.2f}")

    def onUpperSliderChanged(self, n):
        """Updates upper slider label that displays the recalculated slider
        value. Prevents the upper slider value from going below the lower
        slider value.
        """
        if n < self.lowerSlider.value():
            n = self.lowerSlider.value()
        self.upperSlider.setValue(int(n))
        self.upperValueLabel.setText(f"{round(self._getLogValue(n), 2):.2f}")

    def startTimer(self, accelerationEnum):
        """Allows user to hold down the control buttons to continuously
        increment values.
        """
        self.timer = QTimer()
        self.timer.timeout.connect(partial(self.applyAcceleration, accelerationEnum))
        self.timer.start(100)

    def stopTimer(self):
        self.timer.stop()

    def applyAcceleration(self, accelerationEnum):
        """Applies the appropriate acceleration depending on the enum given as
        a parameter.
        """
        if accelerationEnum == Acceleration.FastDown:
            acceleration = -self._getLogValue(self.upperSlider.value())
        elif accelerationEnum == Acceleration.SlowDown:
            acceleration = -self._getLogValue(self.lowerSlider.value())
        elif accelerationEnum == Acceleration.SlowUp:
            acceleration = self._getLogValue(self.lowerSlider.value())
        elif accelerationEnum == Acceleration.FastUp:
            acceleration = self._getLogValue(self.upperSlider.value())

        self.value += self.maxAcceleration * acceleration / 100
        self.value = clamp(self.value, self.minValue, self.maxValue)
        if self.value == self.maxValue and self.infOverflow:
            emitValue = "inf"
        else:
            emitValue = self.getValueString()
        self.accelerated.emit(emitValue)

    def getValueString(self):
        return f"{round(self.value, self.numberOfDecimals):.{self.numberOfDecimals}f}"

    # creates a dict from acceleration enum to corresponding button, with
    # appropriate connections pre-made
    def createControls(self):
        """Generates control buttons with appropriate connections
        :func:`~DoubleSlider.applyAcceleration`. Returns a dict mapping the
        different acceleration enums to their corresponding button.
        """
        slowUpButton = QPushButton()
        slowUpButton.setObjectName("slowUpButton")

        fastUpButton = QPushButton()
        fastUpButton.setObjectName("fastUpButton")

        fastDownButton = QPushButton()
        fastDownButton.setObjectName("fastDownButton")

        slowDownButton = QPushButton()
        slowDownButton.setObjectName("slowDownButton")

        buttonDict = {
            slowUpButton: Acceleration.SlowUp,
            fastUpButton: Acceleration.FastUp,
            slowDownButton: Acceleration.SlowDown,
            fastDownButton: Acceleration.FastDown,
        }

        for button, direction in buttonDict.items():
            button.clicked.connect(partial(self.applyAcceleration, direction))
            button.released.connect(self.stopTimer)
            button.pressed.connect(partial(self.startTimer, direction))

        return {
            Acceleration.SlowUp: slowUpButton,
            Acceleration.FastUp: fastUpButton,
            Acceleration.SlowDown: slowDownButton,
            Acceleration.FastDown: fastDownButton,
        }


def clamp(value, minValue, maxValue):
    return min(max(value, minValue), maxValue)


class Acceleration(Enum):
    """Enums describing the different types of acceleration that can be applied
    to the machine. The enums are used in applyAcceleration in order to
    determine which slider value to fetch.
    """

    FastUp = -2
    SlowUp = -1
    SlowDown = 1
    FastDown = 2
