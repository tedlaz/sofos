from sofos import qt


class Form1(qt.AutoForm):

    def _wtitle(self):
        self.setWindowTitle('Custom Form')

    def _create_fields(self):
        lbs = self.model.field_labels()
        self.widgets['id'] = qt.TIntegerKey(parent=self)
        self.widgets['id'].setVisible(False)
        # for i, fld in enumerate(self.model.field_names()):
        for i, fld in enumerate(['epo', 'ono', 'pat']):
            self.widgets[fld] = qt.wselector(self.model.field_object(fld), self)
            self.fld_layout.insertRow(
                i, qt.Qw.QLabel(lbs[fld]), self.widgets[fld])
