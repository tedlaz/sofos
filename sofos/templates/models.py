from sofos import models


# Create your models here !!
# Following models are for test purposes only
# Delete and replace with yours

class Sex(models.Model):
    sex = models.CharField('Φύλο', max_length=10)

    class Meta:
        table_label = 'Φύλο'


class Xora(models.Model):
    xor = models.CharField('Χώρα', max_length=80, unique=True)

    class Meta:
        table_label = 'Χώρες'


class TaftotitaType(models.Model):
    tat = models.CharField('Τύπος ταυτότητας', max_length=60, unique=True)

    class Meta:
        table_label = 'Τύποι ταυτότητας'


class OikogKat(models.Model):
    oik = models.CharField(
        'Οικογενειακή κατάσταση', max_length=60, unique=True)

    class Meta:
        table_label = 'Οικογενειακή κατάσταση'


class Erg(models.Model):
    epo = models.CharField('Επώνυμο', max_length=30)
    ono = models.CharField('Όνομα', max_length=30)
    pat = models.CharField('Όνομα πατέρα', max_length=30)
    mit = models.CharField('Όνομα μητέρας', max_length=30)
    sex = models.ForeignKey(Sex, 'Φύλο', qt_widget='combo')
    gen = models.DateField('Ημ/νία γέννησης')
    pai = models.IntegerField('Παιδιά')
    xor = models.ForeignKey(Xora, 'Χώρα', qt_widget='combo')
    afm = models.CharNumField('ΑΦΜ', max_length=9, min_length=9)
    ika = models.CharNumField('Αρ.Μητρώου ΙΚΑ', max_length=10, min_length=10)
    amka = models.CharNumField('ΑMKA', max_length=11, min_length=11)
    taft = models.ForeignKey(TaftotitaType, 'Τύπος ταυτότητας',
                             qt_widget='combo')
    taf = models.CharField('Αριθμός ταυτότητας', max_length=20, unique=True)
    oik = models.ForeignKey(OikogKat, 'Οικογενειακή κατάσταση',
                            qt_widget='combo')
    addr = models.CharField('Διεύθυνση', max_length=60)
    mobile = models.CharField('Κινητό τηλέφωνο', max_length=10)

    class Meta:
        unique_together = ['epo', 'ono']
        table_label = 'Εργαζόμενοι'

    def __str__(self):
        return '%s %s' % (self.epo, self.ono)


class ErgType(models.Model):
    '''Ιδιότητα εργαζομένου (Υπάλληλος/Εργάτης)'''
    ert = models.CharField('Ιδιότητα εργαζομένου', max_length=12, unique=True)

    class Meta:
        table_label = 'Ιδιότητα εργαζομένου'


class Parartima(models.Model):
    '''Παράρτημα εταιρείας'''
    par = models.CharField('Παράρτημα', max_length=50, unique=True)
    kad = models.CharField('ΚΑΔ(ΙΚΑ)', max_length=4)

    class Meta:
        table_label = "Παράρτημα"


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
    apt = models.ForeignKey(ApolysiType, 'Τύπος απόλυσης',
                            qt_widget='combo', null=True)

    class Meta:
        table_label = 'Προσλήψεις'

    def __str__(self):
        return '%s %s' % (self.erg, self.dpr)


class Hmerologio(models.Model):
    imper = models.CharField('Ημερολόγιο', max_length=50)

    class Meta:
        table_label = 'Ημερολόγιο εγγραφών'


class Account(models.Model):
    code = models.CharField('Κωδικός λογαριασμού', max_length=30, unique=True)
    aper = models.CharField('Περιγραφή λ/μου', max_length=90, unique=True)

    class Meta:
        table_label = 'Λογαριασμοί λογιστικής'


class Trans(models.Model):
    imer = models.ForeignKey(Hmerologio, 'Ημερολόγιο', qt_widget='combo',
                             default=1)
    trdate = models.DateField('Ημ/νία εγγραφής')
    parko = models.CharField('Παραστατικό', max_length=20)
    per = models.CharField('Περιγραφή', max_length=50)

    class Meta:
        table_label = 'Άρθρα'


class TransDetails(models.Model):
    tran = models.ForeignKey(Trans, 'Άρθρο')
    accn = models.ForeignKey(Account, 'Λογαριασμός')
    dper = models.CharField('Περιγραφή', max_length=30)
    xre = models.DecimalField('Χρέωση')
    pis =  models.DecimalField('Πίστωση')

    class Meta:
        table_label = 'Εγγραφή'
