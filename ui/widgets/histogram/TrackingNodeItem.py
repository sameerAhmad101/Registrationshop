"""
TrackingNodeItem

:Authors:
	Berend Klein Haneveld
"""
from PySide.QtGui import *
from PySide.QtCore import *
from NodeItem import NodeItem
from core.decorators import overrides


class TrackingNodeItem(NodeItem):
	"""
	TrackingNodeItem
	"""
	# updatePosition = Signal(float)

	def __init__(self):
		super(TrackingNodeItem, self).__init__()

		self._histItem = None
		self._lineIndex = 0
		self._lineRatio = 0.0
		self._position = 0.0
		self._delegate = None

	def setHistogramItem(self, histogramItem):
		self._histItem = histogramItem

	@property
	def delegate(self):
		return self._delegate

	@delegate.setter
	def delegate(self, value):
		self._delegate = value

	@Slot()
	def update(self):
		position = QPointF()
		line = self._histItem._lines[self._lineIndex].line()
		x1 = line.x1()
		x2 = line.x2()
		y1 = line.y1()
		y2 = line.y2()
		y = y1 + self._lineRatio * (y2 - y1)
		x = x1 + self._lineRatio * (x2 - x1)
		position.setX(x)
		position.setY(y)
		super(TrackingNodeItem, self).setPos(position)

	@overrides(NodeItem)
	def mouseMoveEvent(self, event):
		self.setPos(event.scenePos())
		margins = self._histItem._margins
		rect = self._histItem.rect()
		pos = self.pos()
		width = rect.width() - (margins.left() + margins.right() + 1)
		partOfLine = (pos.x() - margins.left()) / width
		# print partOfLine
		self._position = partOfLine
		# self.updatePosition.emit(partOfLine)

	@overrides(NodeItem)
	def setPos(self, position):
		actualPos = QPointF()
		actualPos.setX(position.x())
		actualPos.setY(position.y())

		if self._histItem:
			lines = self._histItem._lines
			if len(lines) == 0:
				return
			margins = self._histItem._margins
			rect = self._histItem.rect()
			width = rect.width() - (margins.left() + margins.right() + 1)
			# Clamp the x value between the left and right border of the histogram
			normX = min(max(margins.left(), position.x()), margins.left() + width)
			xWithinMargins = position.x() - margins.left()
			u = xWithinMargins / float(width)
			u = u * len(self._histItem._lines)
			index = min(max(int(u), 0), len(lines)-1)
			line = lines[index].line()
			x1 = line.x1()
			x2 = line.x2()
			y1 = line.y1()
			y2 = line.y2()
			ratio = (normX - x1) / (x2 - x1)
			actualY = y1 + ratio * (y2 - y1)
			assert normX >= x1
			assert normX <= x2
			actualPos.setY(actualY)
			actualPos.setX(normX)
			self._position = (normX - margins.left()) / width
			if self._delegate:
				self._delegate.updatePos(self._position)
			self._lineIndex = index
			self._lineRatio = ratio

		super(TrackingNodeItem, self).setPos(actualPos)