from qtpy import QtGui, QtWidgets


class DynamicSizeLabel(QtWidgets.QLabel):
    def __init__(self, *args, **kargs):
        super(DynamicSizeLabel, self).__init__(*args, **kargs)

        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored,
                                                 QtWidgets.QSizePolicy.Ignored))
        self.setText("DynLabel")
        self.set_min_size(8)

    def set_min_size(self, minfs):
        f = self.font()
        f.setPixelSize(minfs)
        br = QtGui.QFontMetrics(f).boundingRect(self.text())

        self.setMinimumSize(br.width(), br.height())

    def resizeEvent(self, event):
        super(DynamicSizeLabel, self).resizeEvent(event)

        if not self.text():
            return

        # --- fetch current parameters ----

        f = self.font()
        cr = self.contentsRect()

        # --- iterate to find the font size that fits the contentsRect ---

        dw = event.size().width() - event.oldSize().width()  # width change
        dh = event.size().height() - event.oldSize().height()  # height change

        fs = max(f.pixelSize(), 1)
        while True:

            f.setPixelSize(fs)
            br = QtGui.QFontMetrics(f).boundingRect(self.text())

            if dw >= 0 and dh >= 0:  # label is expanding

                if br.height() <= cr.height() and br.width() <= cr.width():
                    fs += 1
                else:
                    f.setPixelSize(max(fs - 1, 1))  # backtrack
                    break

            else:  # label is shrinking

                if br.height() > cr.height() or br.width() > cr.width():
                    fs -= 1
                else:
                    break

            if fs < 1:
                break

        # --- update font size ---
        self.setFont(f)
