#IMPORT-export application
from import_export import resources
from manuali.models import Manuali

class ManualiResources(resources.ModelResource):

    class Meta:
        model = Manuali
        #specifica i campi da esportare.
        fields = ('id', 'codice', 'stato')
        #specifica i campi da escludere dalla esportazione.
        #excludefields = ('id', 'codice', 'stato')
