from .fautoformtable import AutoFormTable
from .ttextline import TIntegerKey
from .widget_selector import wselector


class AutoFormTableWidget(AutoFormTable):

    def _populate(self):
        _, data = self.model.select_all()
        self.tbl.setRowCount(data['rownum'])
        self.tbl.setColumnCount(data['colnum'])
        # self.tbl.setHorizontalHeaderLabels(data['labels'])
        fields = self.model.field_objects()
        for i, row in enumerate(data['rows']):
            item = TIntegerKey(parent=self)
            item.set(row[0])
            self.tbl.setCellWidget(i, 0, item)
            for j, col in enumerate(fields):
                val = row[j+1]
                item = wselector(fields[col], parent=self)
                print(val)
                item.set(val)
                self.tbl.setCellWidget(i, j+1, item)
        self.tbl.resizeColumnsToContents()
