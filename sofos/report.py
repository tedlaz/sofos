import yaml
import PyQt5.QtCore as Qc
import PyQt5.QtGui as Qg
import PyQt5.QtPrintSupport as Qp
# For testing
import PyQt5.QtWidgets as Qw
import sys


def open_yaml(filename):
    data = None
    with open(filename) as ofile:
        data = yaml.load(ofile.read())
    return data


class TableReport():
    def __init__(self, settings, data):
        """
        :param yaml_file: yaml file with report configuration data
        :param data: Actual data to be reported
        """
        self.settings = settings
        self.data = data
        self.init_printer()
        self.create_fonts()
        self.preview()

    def init_printer(self, left=52, top=52, from_right=52, from_bottom=52):
        self.printer = Qp.QPrinter()
        self.printer.setPaperSize(Qp.QPrinter.A4)
        self.printer.setFullPage(True)
        self.printer.setOutputFormat(Qp.QPrinter.PdfFormat)
        orientation = self.settings.get('Orientation', 0)
        if orientation in (0, 'Portrait'):
            self.printer.setOrientation(Qp.QPrinter.Portrait)
        else:
            self.printer.setOrientation(Qp.QPrinter.Landscape)
        self.paper_height = self.printer.paperRect().height()
        self.paper_width = self.printer.paperRect().width()
        print('Paper height:%s Width:%s' % (
            self.paper_height, self.paper_width))
        self.left, self.top = left, top
        self.right = self.paper_width - from_right
        self.bottom = self.paper_height - from_bottom
        self.width = self.paper_width - left - from_right
        self.height = self.paper_height - top - from_bottom
        self.x_middle = self.paper_width / 2
        self.y_middle = self.paper_height / 2
        # print(self.left, self.top, self.right, self.bottom,
        #       self.width, self.height)

    def create_fonts(self):
        self.font_family = self.settings.get('FontFamily', 'Helvetica')
        self.fontSize = self.settings.get('FontSize', 9)
        self.fh1 = self.font(20, 1)
        self.fh2 = self.font(12, 3)
        self.fh3 = self.font(10, 2)
        self.fth = self.font(self.fontSize, 1)  # table header
        self.ftl = self.font(self.fontSize, 0)  # table line
        self.fpf = self.font(self.fontSize, 0)  # page footer
        self.tableMetrics = Qg.QFontMetrics(self.ftl)
        self.tableHeaderHeight = int(self.tableMetrics.height() * 3)
        self.tableColumnHeight = int(self.tableMetrics.height() * 1.7)

    def font(self, size, typ=0):
        """
        typ: 0=normal, 1=bold, 2=italic, 3=bolditalic
        """
        new_font = Qg.QFont(self.font_family, size)
        if typ in (1, 3):
            new_font.setBold(True)
        if typ in (2, 3):
            new_font.setItalic(True)
        return new_font

    def align(self, opt=0):
        if opt == 0:
            option = Qg.QTextOption(Qc.Qt.AlignLeft | Qc.Qt.AlignVCenter)
        elif opt == 1:
            option = Qg.QTextOption(Qc.Qt.AlignCenter | Qc.Qt.AlignVCenter)
        else:
            option = Qg.QTextOption(Qc.Qt.AlignRight | Qc.Qt.AlignVCenter)
        option.setWrapMode(Qg.QTextOption.WordWrap)
        return option

    def txt(self, width, height, val, align, font, offsetx=0, offsety=3):
        """Draw text into box(xvl, yvl, wid, hei)
        :param xvl: absolute x value
        :param yvl: absolute y value
        :param width: the width of the box
        :param height: the height of the box
        """
        self.pnt.save()
        self.pnt.setFont(font)
        self.x, self.y = self.x + offsetx, self.y + offsety  # Add offset
        flags = Qc.Qt.TextDontClip | Qc.Qt.TextWordWrap
        font_height = self.pnt.fontMetrics().height()
        min_height = font_height + offsety
        height = min_height if height < min_height else height
        drec = Qc.QRectF(self.x, self.y, width, height)
        brec = self.pnt.fontMetrics().boundingRect(drec.toRect(), flags, val)
        if brec.height() > height:
            height = brec.height()
        if self.y + height > self.bottom:
            print('You must change page', height, self.y, self.bottom)
            self.new_page()
            self.x, self.y = self.left, self.top
        print('x=%s y=%s height=%s' % (self.x, self.y, self.height))
        val_width = self.pnt.fontMetrics().width(val)
        if val_width > self.width:
            print('width is:', val_width)
        self.pnt.drawText(Qc.QRectF(self.x, self.y, width, height), val, align)
        self.pnt.restore()
        self.x, self.y = self.x + width, self.y + height

    def txt_row(self, yvl, text, font, align=1):
        """
        text that occupies a row of the report usually centered
        """
        self.y = yvl
        self.x = self.left
        self.txt(self.width, 1, text, self.align(align), font, offsety=3)

    def lineh(self, xapo, xeos, yval, width=None, dots=False):
        """Draw horizontal line"""
        assert xapo <= xeos <= self.right
        assert yval <= self.bottom
        self.pnt.save()
        pen = Qg.QPen()
        pen.setColor(Qc.Qt.black)
        if dots:
            pen.setStyle(Qc.Qt.DotLine)
        if width:
            pen.setWidth(width)
        self.pnt.setPen(pen)
        self.pnt.drawLine(xapo, yval, xeos, yval)
        self.pnt.restore()

    def linev(self, xval, yapo, yeos, width=None, dots=False):
        """Draw vertical line"""
        assert yapo <= yeos <= self.bottom
        assert xval <= self.right
        self.pnt.save()
        pen = Qg.QPen()
        pen.setColor(Qc.Qt.black)
        if dots:
            pen.setStyle(Qc.Qt.DotLine)
        if width:
            pen.setWidth(width)
        self.pnt.setPen(pen)
        self.pnt.drawLine(xval, yapo, xval, yeos)
        self.pnt.restore()

    def box(self, left, top, width, height, color='#000000', fill='#ffffff'):
        self.pnt.save()
        if color:
            self.pnt.setBrush(Qg.QColor(fill))
        self.pnt.setPen(Qg.QColor(color))
        self.pnt.drawRect(left, top, width, height)
        self.pnt.restore()

    def new_page(self):
        self.printer.newPage()
        self.page_number += 1
        self.box(self.left, self.top, self.width, self.height)
        # self.x, self.y = self.left, self.top
        # self.page_footer()
        # self.table_header()

    def _report(self):
        """Create the report"""
        with Qg.QPainter(self.printer) as self.pnt:
            self.box(self.left, self.top, self.width, self.height)
            self.x, self.y = self.left, self.top  # Init x, y
            self.page_number = 1  # Init page_number
            self.txt(self.width, 1, 'Tedlaza ' * 290,
                     self.align(1), self.ftl)
            print('x=%s, y=%s' % (self.x, self.y))
            self.txt_row(705, 'This is test', self.fh1)
            self.txt_row(self.y, 'This is test', self.fh1, 0)
            self.txt_row(self.y, 'This is test', self.fh1, 2)
            self.txt_row(self.y, 'This is test', self.fh2)
            self.txt_row(self.y, 'This is test', self.fh3)
            self.lineh(self.left, self.right, self.y)
            self.lineh(self.left, self.right, self.y + 1)
            self.lineh(self.left, self.right, self.y + 2)
            self.lineh(self.left, self.right, self.y + 3)
            self.linev(100, self.y, self.bottom)
            self.linev(self.x_middle, self.y, self.bottom)
            self.lineh(self.x_middle, self.right, (self.y + self.bottom) / 2)
            self.linev((self.x_middle + self.right) / 2,
                       (self.y + self.bottom) / 2, self.bottom)
            gray = '#ebebeb'
            self.box(self.x_middle + 8, self.y + 8, 50, 50, gray, gray)

    def preview(self):
        self.printer.setOutputFileName('/home/ted/tst.pdf')
        ppp = Qp.QPrintPreviewDialog(self.printer)
        ppp.paintRequested.connect(self._report)
        ppp.exec_()


if __name__ == '__main__':
    yfile = '/home/ted/prj/pyted/qtprint3/tst.yml'
    data = ''
    app = Qw.QApplication(sys.argv)
    trp = TableReport(open_yaml(yfile), data)
