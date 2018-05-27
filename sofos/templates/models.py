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
        repr_fields = ['epo', 'ono']

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
        repr_fields = ['par']


class ApodoxesType(models.Model):
    '''Τύπος αποδοχών (Μισθός/Ημερομίσθιο/Ωρομίσθιο)'''
    apt = models.CharField('Τύπος αποδοχών', max_length=20, unique=True)

    class Meta:
        table_label = "Τύπος αποδοχών"


class SymbasiType(models.Model):
    '''Τύπος Σύμβασης (Αορίστου/Ορισμένου/Έργου)'''
    syt = models.CharField('Τύπος σύμβασης', max_length=30, unique=True)

    class Meta:
        table_label = "Τύπος σύμβασης"


class Eidikotita(models.Model):
    eip = models.CharField('Ειδικότητα', max_length=50, unique=True)
    eid = models.CharField('Κωδικός ειδικότητας ΙΚΑ', max_length=6)

    class Meta:
        table_label = "Ειδικότητα εργασίας"
        repr_fields = ['eip']


class ApasxolisiType(models.Model):
    """Καθεστώς απασχόλησης Πλήρης/μερική/εκ περιτροπής"""
    apa = models.CharField('Καθεστώς απασχόλησης', max_length=50, unique=True)

    class Meta:
        table_label = "Καθεστώς απασχόλησης"


class ApoxorisiType(models.Model):
    apt = models.CharField('Τύπος απόλυσης', max_length=50, unique=True)

    class Meta:
        table_label = 'Τύπος αποχώρησης'


class Proslipsi(models.Model):
    dpr = models.DateField('Ημ/νία πρόσληψης',)
    erg = models.ForeignKey(Erg, 'Εργαζόμενος')
    par = models.ForeignKey(Parartima, 'Παράρτημα',  default=1,
                            qt_widget='combo')
    apa = models.ForeignKey(ApasxolisiType, 'Καθεστώς απασχόλησης',
                            qt_widget='combo', default=1)
    ert = models.ForeignKey(ErgType, 'Τύπος εργαζομένου',  default=1,
                            qt_widget='combo')
    eid = models.ForeignKey(Eidikotita, 'Ειδικότητα')
    syt = models.ForeignKey(SymbasiType, 'Τύπος σύμβασης',  default=1,
                            qt_widget='combo')
    mer = models.WeekdaysField('Ημέρες εργασίας')
    ora = models.TextField('Πρόγραμμα εργασίας')
    apt = models.ForeignKey(ApodoxesType, 'Τύπος αποδοχών',  default=1,
                            qt_widget='combo')
    amb = models.DecimalField('Αποδοχές')
    dap = models.DateEmptyField('Ημ/νία απόλυσης')
    apot = models.ForeignKey(ApoxorisiType, 'Τύπος απόχώρησης',
                             qt_widget='combo', null=True)

    class Meta:
        table_label = 'Προσλήψεις'
        repr_fields = ['erg', 'dpr']


class Xrisi(models.Model):
    """Έτος"""
    xrisi = models.IntegerField('Χρήση', unique=True)

    class Meta:
        table_label = "Χρήση"


class Minas(models.Model):
    """Μήνας"""
    mon = models.CharField('Μήνας', max_length=15, unique=True)

    class Meta:
        table_label = "Μήνας"


class Paroysies(models.Model):
    """Παρουσίες εργαζομένων"""
    xri = models.ForeignKey(Xrisi, 'Χρήση', qt_widget='combo')
    mon = models.ForeignKey(Minas, 'Μήνας', qt_widget='combo')

    class Meta:
        unique_together = ('xri', 'mon')
        table_label = "Παρουσίες"
        table_child_name = "ParousiesDetails"


class ParoysiaType(models.Model):
    """Κανονικές/Ασθένεια/Υπερωρίες"""
    pty = models.CharField('Τύπος παρουσίας', max_length=50, unique=True)
    kika = models.CharField('Κωδικός ΙΚΑ', max_length=2, unique=True)

    class Meta:
        table_label = "Τύπος παρουσίας"


class ParoysiesDetails(models.Model):
    """Παρουσίες εργαζομένων αναλυτικά"""
    mpa = models.ForeignKey(Paroysies, 'Χρήση/Περίοδος', qt_widget='combo')
    pro = models.ForeignKey(Proslipsi, 'Εργαζόμενος')
    pty = models.ForeignKey(ParoysiaType, 'Τύπος παρουσίας', qt_widget='combo')
    apo = models.DateEmptyField('Από')
    eos = models.DateEmptyField('Έως')
    # Κανονικές
    mno = models.IntegerField('Ημέρες εργασίας', default=0)
    mad = models.IntegerField('Ημέρες άδειας με αποδοχές', default=0)
    maa = models.IntegerField('Ημέρες άδειας χωρίς αποδοχές', default=0)
    ony = models.IntegerField('Ώρες νυχτ.προσαύξησης', default=0)
    arm = models.IntegerField('Ημέρες αργίας', default=0)
    aor = models.IntegerField('Ώρες αργίας', default=0)
    # Ασθένεια
    ml3 = models.IntegerField('Ημέρες ασθένειας < 3', default=0)
    mm3 = models.IntegerField('Ημέρες ασθένειας > 3', default=0)
    mm0 = models.IntegerField('Ημέρες ασθένειας χωρίς αποδοχές', default=0)
    epi = models.DecimalField('Επίδομα ΙΚΑ')
    # Υπερωρίες
    yp1 = models.IntegerField('Υπερωρίες 1 ώρες', default=0)
    yp2 = models.IntegerField('Υπερωρίες 2 ώρες', default=0)

    class Meta:
        unique_together = ('mpa', 'pro', 'pty', 'apo')
        table_label = "Παρουσία εργαζομένου"


class MisthodosiaType(models.Model):
    """Τύπος μισθοδοσίας"""
    mtp = models.CharField('Τύπος μισθοδοσίας', max_length=30, unique=True)
    kika = models.CharField('Κωδικός ΙΚΑ', max_length=2, unique=True)

    class Meta:
        table_label = "Τύπος μισθοδοσίας"


class Misthodosia(models.Model):
    """Μισθοδοσία"""
    xri = models.ForeignKey(Xrisi, 'Χρήση', qt_widget='combo')
    mon = models.ForeignKey(Minas, 'Μήνας', qt_widget='combo')
    mtp = models.ForeignKey(MisthodosiaType, 'Τύπος μισθοδοσίας', default=1,
                            qt_widget='combo')
    pro = models.ForeignKey(Proslipsi, 'Εργαζόμενος')
    apo = models.DateEmptyField('Από')
    eos = models.DateEmptyField('Έως')
    mika = models.IntegerField('Ημέρες ΙΚΑ', default=0)
    marg = models.IntegerField('Ημέρες Κυριακών/Αργιών', default=0)
    oarg = models.IntegerField('Ώρες αργίας', default=0)
    onyχ = models.IntegerField('Ώρες νυχτ.προσαύξησης', default=0)
    asl3 = models.IntegerField('Ασθένεια < 3', default=0)
    asm3 = models.IntegerField('Ασθένεια > 3', default=0)
    apod = models.DecimalField('Αποδοχές')
    eika = models.DecimalField('Επίδομα ΙΚΑ')
    pike = models.DecimalField('IKA Εργαζόμενος %')
    pikt = models.DecimalField('IKA Εργοδότης %')
    pika = models.DecimalField('IKA %')
    ike = models.DecimalField('IKA Εργαζόμενου')
    ike1 = models.DecimalField('IKA Εργαζόμενου επιδόματος ασθένειας')
    ikt = models.DecimalField('IKA Εργοδότη')
    fmy = models.DecimalField('Φ.Μ.Υ.')
    eea = models.DecimalField('E.E.A')
    pli = models.DecimalField('Πληρωτέο')

    class Meta:
        unique_together = ("xri", "mon", "mtp", "pro", "apo")
        table_label = "Μισθοδοσία"


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
                             default=2)
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
    pis = models.DecimalField('Πίστωση')

    class Meta:
        table_label = 'Εγγραφή'
