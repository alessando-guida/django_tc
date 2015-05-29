from django.db import models
from django.core.files.storage import FileSystemStorage
import os

# Create your models here.
class Clienti(models.Model):
    cliente_id = models.IntegerField(null=False, blank=True)
    nome_azienda = models.CharField(null=False, blank=False, max_length=100)
    nome_contatto = models.CharField(null=True, blank=True, max_length=100)
    indirizzo = models.CharField(null=True, blank=True, max_length=300)
    email = models.EmailField(null=True, blank=True)
    tel = models.PositiveIntegerField(null=True, blank=True)
    data_inizio = models.DateField(null=True, blank=True)
    note = models.TextField(max_length="500", null=True, blank=True)

    def __str__(self):
        return self.nome_azienda

    class Meta:
        verbose_name_plural = "Clienti"

class Manuali(models.Model):
    #stato
    IN_USO = "In uso"
    OBSOLETO= "Obsoleto"
    IN_USO_DA_CORREGGERE = "In uso ma da correggere"
    STATO = (
        (IN_USO, "In uso"),
        (OBSOLETO, "Obsoleto"),
        (IN_USO_DA_CORREGGERE, "In uso ma da correggere"),
    )
    #applicazione
    ACQUA = "100C"
    GRADI300= "300C"
    GRADI500 = "500C"
    VAPORE1_9 = "generatore vapore, 1-9 bar"
    APP_0_10V = '0-10 V'
    PERSONALIZZATO =  'personalizzato'

    APPLICAZIONE = (
        (ACQUA, "100C"),
        (GRADI300, "300C"),
        (GRADI500, "500C"),
        (VAPORE1_9, "generatore vapore, 1-9 bar"),
        (APP_0_10V, '0-10 V'),
        (PERSONALIZZATO, 'personalizzato'),
    )

    #Linea di produzione
    SPL = "SPL"
    SPLBA = "SPLBA"
    LD = 'LD'
    ACCESSORI = 'accessori'

    LINEA = (
        (SPL, "SPL"),
        (SPLBA, "SPLBA"),
        (LD, 'LD'),
        (ACCESSORI, 'accessori'),
    )

    #tipo
    BR25_100 = "25-100"
    BR25_350 = "25-350"
    BR600 = '600'
    BR1000 = '1000'

    TIPO = (
        (BR25_100, "25-100"),
        (BR25_350,  "25-350"),
        (BR600, '600'),
        (BR1000, '1000'),
        (ACCESSORI, 'accessori'),
    )

    #tipo documento
    MANUALE = "Manuale"
    SCH = "Scheda tecnica"
    LISTA = 'Lista uso interno'

    DOCUMENTO = (
        (MANUALE, "Manuale"),
        (SCH,  "Scheda tecnica"),
        (LISTA,  'Lista uso interno'),
    )

    codice = models.CharField(null=False, blank=False, max_length=100)
    stato = models.CharField(max_length=100, choices=STATO, default="In uso")
    data_rilascio = models.DateField()
    applicazione = models.CharField(max_length=100, choices=APPLICAZIONE)
    note = models.TextField(max_length="500", null=True, blank=True)
    lingua = models.ForeignKey('Lingua')
    documento = models.CharField(choices=DOCUMENTO, max_length=100, null=True)
    linea = models.CharField(choices=LINEA, max_length=100, null=True)
    tipo = models.CharField(choices=TIPO, max_length=50, null=True)

    #generate dynamic file link based on the type of burner
    def generate_dinamic_filepath(self, filename):
        url = "%s/%s/%s/%s/%s" % (self.documento, self.linea, self.tipo, self.applicazione, filename)
        return url

    file = models.FileField(null=True, blank=True, upload_to=generate_dinamic_filepath)

    def __str__(self):
        return self.codice

    #link per prendere il file
    def file_link(self):
        if self.file:
            return "<a href='%s'>%s</a>" % (self.file.url, os.path.basename(self.file.name))

        else:
            return "Nessun allegato"

    file_link.allow_tags = True
    file_link.short_description = 'File allegato'

    class Meta:
        verbose_name_plural = "Manuali"

class Manuali_usciti(models.Model):
    codice = models.ForeignKey('Manuali')
    matricola = models.PositiveIntegerField(null=True, blank=False)
    data_stampa = models.DateField(null=True, blank=True)
    cliente = models.ForeignKey('Clienti')
    note = models.TextField(max_length="500", null=True, blank=True)

    def __str__(self):
        return " %s, %s" % (self.matricola, self.codice)

    def get_file(self):
        #return self.codice.file
        return self.codice.file_link()

    get_file.allow_tags = True

    class Meta:
        verbose_name_plural = "Manuali Usciti"

class Lingua(models.Model):
    lingua = models.CharField(max_length=100, unique=True, null=False, blank=True, default='Italiano')

    def __str__(self):
        return self.lingua

    class Meta:
        verbose_name_plural = "Lingue"

