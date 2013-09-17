"""
RenderInfoWidget

:Authors:
	Berend Klein Haneveld
"""

import os
from PySide.QtGui import QWidget
from PySide.QtGui import QGridLayout
from PySide.QtGui import QLabel
from PySide.QtCore import Slot
from PySide.QtCore import Qt
from core.data import DataReader


class RenderInfoWidget(QWidget):
	"""
	RenderInfoWidget shows information about the loaded dataset. Things like
	filenames, range of data values, size of data, etc.
	"""
	def __init__(self):
		super(RenderInfoWidget, self).__init__()

	@Slot(basestring)
	def setFile(self, fileName):
		"""
		Slot that reads properties of the dataset and displays them in a few widgets.
		"""
		if fileName is None:
			return

		# Read info from dataset
		# TODO: read out the real world dimensions in inch or cm
		# TODO: scalar type (int, float, short, etc.)
		imageReader = DataReader()
		imageData = imageReader.GetImageData(fileName)

		directory, name = os.path.split(fileName)
		dimensions = imageData.GetDimensions()
		minimum, maximum = imageData.GetScalarRange()

		nameText = name
		dimsText = "(" + str(dimensions[0]) + ", " + str(dimensions[1]) + ", " + str(dimensions[2]) + ")"
		voxsText = str(dimensions[0] * dimensions[1] * dimensions[2])
		rangText = "[" + str(minimum) + " : " + str(maximum) + "]"

		layout = self.layout()
		if not layout:
			# Create a new layout
			layout = QGridLayout()
			layout.setAlignment(Qt.AlignTop)

			# Create string representations
			nameField = QLabel("File name:")
			dimsField = QLabel("Dimensions:")
			voxsField = QLabel("Voxels:")
			rangField = QLabel("Range:")

			nameField.setAlignment(Qt.AlignRight)
			dimsField.setAlignment(Qt.AlignRight)
			voxsField.setAlignment(Qt.AlignRight)
			rangField.setAlignment(Qt.AlignRight)

			# Create 'dynamic' labels
			self.labelTitle = QLabel(nameText)
			self.labelDimensions = QLabel(dimsText)
			self.labelVoxels = QLabel(voxsText)
			self.labelRange = QLabel(rangText)

			layout.addWidget(nameField, 0, 0)
			layout.addWidget(dimsField, 1, 0)
			layout.addWidget(voxsField, 2, 0)
			layout.addWidget(rangField, 3, 0)

			layout.addWidget(self.labelTitle, 0, 1)
			layout.addWidget(self.labelDimensions, 1, 1)
			layout.addWidget(self.labelVoxels, 2, 1)
			layout.addWidget(self.labelRange, 3, 1)
			self.setLayout(layout)
		else:
			# Just update the text for the 'dynamic' labels
			self.labelTitle.setText(nameText)
			self.labelDimensions.setText(dimsText)
			self.labelVoxels.setText(voxsText)
			self.labelRange.setText(rangText)
