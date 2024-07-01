from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox


class CheckableComboBox(QComboBox):
    """A custom combo box that allows items to be checked and unchecked.

    Inherits from QComboBox.
    """

    def __init__(self):
        super().__init__()
        self._changed = False
        self.view().pressed.connect(self.handleItemPressed)

    def setItemChecked(self, index, checked=False):
        """Sets the check state of an item in the combo box.

        Args:
            index (int): The index of the item to set the check state for.
            checked (bool): The check state to set for the item. Defaults to False.
        """
        item = self.model().item(
            index, self.modelColumn()
        )  # Get the QStandardItem object for the specified index

        if checked:
            item.setCheckState(Qt.Checked)  # Set the check state to Checked
        else:
            item.setCheckState(Qt.Unchecked)  # Set the check state to Unchecked

    def handleItemPressed(self, index):
        """Handles the pressed signal for an item in the combo box.

        Args:
            index (int): The index of the pressed item.
        """
        item = self.model().itemFromIndex(
            index
        )  # Get the QStandardItem object for the pressed item

        if item.checkState() == Qt.Checked:
            item.setCheckState(
                Qt.Unchecked
            )  # If the item is already checked, uncheck it
        else:
            item.setCheckState(Qt.Checked)  # If the item is unchecked, check it
        self._changed = True  # Set the _changed flag to True to indicate that the combo box has been modified

    def hidePopup(self):
        """Hides the combo box popup.

        If the combo box has not been modified (i.e., _changed is False), the popup is hidden. Otherwise, the
        popup remains visible.
        """
        if not self._changed:
            super().hidePopup()  # Hide the popup if the combo box has not been modified
        self._changed = False  # Reset the _changed flag to False

    def itemChecked(self, index):
        """Returns the check state of an item in the combo box.

        Args:
            index (int): The index of the item to check the state for.

        Returns:
            bool: True if the item is checked, False otherwise.
        """
        item = self.model().item(
            index, self.modelColumn()
        )  # Get the QStandardItem object for the specified index
        return (
            item.checkState() == Qt.Checked
        )  # Return True if the item is checked, False otherwise
