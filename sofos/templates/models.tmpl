from sofos import models


# Create your models here !!
# Following models are for test purposes only
# Delete and replace with yours

class Erg(models.Model):
    epo = models.CharField('Επώνυμο', max_length=30)
    ono = models.CharField('Όνομα', max_length=30)
    pat = models.CharField('Όνομα πατέρα', max_length=30)
    mit = models.CharField('Όνομα μητέρας', max_length=30)
    gen = models.DateField('Ημ/νία γέννησης')
    pai = models.IntegerField('Παιδιά')
    afm = models.CharNumField('ΑΦΜ', max_length=9, min_length=9)
    ika = models.CharNumField('Αρ.Μητρώου ΙΚΑ', max_length=10, min_length=10)
    amka = models.CharNumField('ΑMKA', max_length=11, min_length=11)

    class Meta:
        unique_together = ['epo', 'ono']
        table_label = 'Εργαζόμενοι'

    def __str__(self):
        return '%s %s' % (self.epo, self.ono)


class ApolysiType(models.Model):
    apt = models.CharField('Τύπος απόλυσης', max_length=50, unique=True)

    class Meta:
        table_label = 'Τύποι απόλυσης'

    def __str__(self):
        return self.apt


class Proslipsi(models.Model):
    dpr = models.DateField('Ημ/νία πρόσληψης',)
    erg = models.ForeignKey(Erg, 'Εργαζόμενος')
    ora = models.WeekdaysField('Ημέρες εργασίας')
    pos = models.DecimalField('Αποδοχές')
    dap = models.DateEmptyField('Ημ/νία απόλυσης')
    apt = models.ForeignKey(ApolysiType, 'Τύπος απόλυσης', qt_widget='combo')

    class Meta:
        table_label = 'Προσλήψεις'

    def __str__(self):
        return '%s %s' % (self.erg, self.dpr)
