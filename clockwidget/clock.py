import os
from qtpy import QtCore, QtGui, QtWidgets
from pydm.widgets.byte import PyDMByteIndicator
from pydm.widgets.channel import PyDMChannel

from .dynlabel import DynamicSizeLabel


class Clock(QtWidgets.QWidget):

    def __init__(self, parent):
        QtWidgets.QWidget.__init__(self, parent)
        self._channels = list()
        self._color = None
        self._hours_address = None
        self._minutes_address = None
        self._seconds_address = None
        self._conn_status = [False, False]
        self._value = [0, 0]

        # Configure the Font
        self.hm_font = QtGui.QFont()
        self.setup_font()

        # Configure the widgets
        layout = QtWidgets.QHBoxLayout()
        self.setLayout(layout)
        self.hm_label = DynamicSizeLabel(self)
        self.hm_label.setFont(self.hm_font)
        self.hm_label.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.seconds_indicator = PyDMByteIndicator(self)
        self.seconds_indicator.showLabels = False
        self.seconds_indicator.bigEndian = True
        self.seconds_indicator.circles = False
        self.seconds_indicator.layout().setSpacing(5)
        self.seconds_indicator.numBits = 6

        seconds_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum,
                                               QtWidgets.QSizePolicy.Maximum)

        self.seconds_indicator.setSizePolicy(seconds_policy)

        layout.addWidget(self.hm_label)
        layout.addWidget(self.seconds_indicator)

        self.color = QtGui.QColor("red")
        self.update_clock()

    def setup_font(self):
        fname = os.path.realpath(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "fonts",
                "Square-Dot-Matrix.ttf"
            )
        )
        font_id = QtGui.QFontDatabase.addApplicationFont(fname)
        family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
        self.hm_font = QtGui.QFont(family)

    def minimumSizeHint(self):
        """
        This property holds the recommended minimum size for the widget.
        
        Returns
        -------
        QSize
        """
        # This is totally arbitrary, I just want *some* visible nonzero size
        return QtCore.QSize(217, 91)

    @QtCore.Property(QtGui.QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, c):
        self._color = c
        self.hm_label.setStyleSheet('color: {}'.format(self._color.name()))
        self.seconds_indicator.onColor = self._color

    @QtCore.Property(str)
    def hoursChannel(self):
        return self._hours_address

    @hoursChannel.setter
    def hoursChannel(self, ch):
        self.create_channel(ch, self._hours_address, self.hours_value_changed,
                            self.hours_conn_changed)
        self._hours_address = ch

    @QtCore.Property(str)
    def minutesChannel(self):
        return self._minutes_address

    @minutesChannel.setter
    def minutesChannel(self, ch):
        self.create_channel(ch, self._minutes_address,
                            self.minutes_value_changed,
                            self.minutes_conn_changed)
        self._minutes_address = ch

    @QtCore.Property(str)
    def secondsChannel(self):
        return self._seconds_address

    @secondsChannel.setter
    def secondsChannel(self, ch):
        self.seconds_indicator.channel = ch
        self._seconds_address = ch

    def hours_conn_changed(self, conn):
        self._conn_status[0] = conn
        self.verify_connection()

    def hours_value_changed(self, value):
        self._value[0] = int(value)
        self.update_clock()

    def minutes_conn_changed(self, conn):
        self._conn_status[1] = conn
        self.verify_connection()

    def minutes_value_changed(self, value):
        self._value[1] = int(value)
        self.update_clock()

    def update_clock(self):
        self.hm_label.setText("{:02d}:{:02d}".format(*self._value))

    def verify_connection(self):
        pass

    def create_channel(self, new_address, old_address, value_callback,
                       conn_callback):
        if new_address != old_address:
            # Remove old connections
            for channel in [c for c in self._channels if
                            c.address == old_address]:
                channel.disconnect()
                self._channels.remove(channel)
            # Load new channel
            self._channel = str(new_address)
            channel = PyDMChannel(address=new_address,
                                  connection_slot=conn_callback,
                                  value_slot=value_callback)
            # Connect write channels if we have them
            channel.connect()
            self._channels.append(channel)
