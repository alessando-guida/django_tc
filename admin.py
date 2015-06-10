from django.contrib import admin

# Register your models here.
from manuali.models import Clienti, Manuali, Manuali_usciti, Lingua


class ClientiAdmin(admin.ModelAdmin):
    #fields = ('cliente_id','nome_azienda')
    #show fields in the table
    list_display = ('cliente_id','nome_azienda', 'nome_contatto', 'data_inizio')



class ManualiAdmin(admin.ModelAdmin):

    def print_btn(self, obj):
        #return '<form method="get" action="/admin/manuali/manuali_usciti/add/"> <button type="submit" name="codice" value="%s">Stampa</button> </form>' % (obj.codice)
        #html senza usare il tag form che da problemi
        return '<button formmethod="get" formaction="/admin/manuali/manuali_usciti/add/" type="submit" name="codice" value="%s">Stampa</button>' % (obj.codice)

    print_btn.short_description = 'Azione'
    print_btn.allow_tags = True

    #parametri visualizzazione della lista
    list_display = ('codice', 'stato', 'data_rilascio', 'applicazione', 'lingua', 'file_link', 'print_btn',)
    #aggiungiamo un filtro sullo stato del manuale
    list_filter = ('stato', 'applicazione','documento', 'linea', 'tipo','lingua',)
    ordering = ('-data_rilascio',)


    actions = ['download_csv']

    def download_csv(self, request, queryset):
        """
        Function to add the download action to download as CSV the selected fields.
        """
        """
        :param request:
        :param queryset:
        :return:
        """
        import csv
        from django.http import HttpResponse


        #creates file on root
        f = open("some.csv", "w")
        writer = csv.writer(f)
        writer.writerow(['codice', 'stato', 'data_rilascio', 'applicazione', 'lingua', 'file_link', 'note'])
        for s in queryset:
            writer.writerow([s.codice, s.stato, s.data_rilascio, s.applicazione, s.lingua, s.file_link, s.note])
        f.close()

        #download the file
        f = open("some.csv", "r")
        response = HttpResponse(f, content_type="text/csv")
        response['Content-Disposition'] = 'attachment; filename=tabella_manuali_esportati.csv'
        return response

    download_csv.short_description = "Scarica file excell per elementi selezionati."


class Manuali_uscitiAdmin(admin.ModelAdmin):

    #form = Mytest

    list_display = ('matricola', 'codice','data_stampa', 'cliente', 'get_file')
    #fields = ('matricola','codice','get_file')
    #display foregigh key as a read only as it is not part of the table
    readonly_fields = ('get_file',)
    list_display_links = ('matricola',)
    fieldsets = (
        (None, {'fields': ('matricola', ('codice', 'get_file'), 'data_stampa','cliente','note',)}
        ),
    )
    search_fields = ['matricola']
    list_filter = ('cliente',)
    ordering = ('-data_stampa', '-matricola',)




    # def get_inline_instances(self, request, obj):
    #     out = super(Manuali_uscitiAdmin, self).get_inline_instances(request, obj)
    #     print("HELLLOOOO OBJ:", obj)
    #     if request.method == 'GET' and 'codice' in request.GET:
    #             codice = request.GET.get('codice', None)
    #             if codice is not None:
    #                 #set the default foreign key as the indicated instance
    #                 print("ecci il codice: ", codice)
    #
    #                 print("oggetto", Manuali.objects.filter(codice=codice))
    #
    #
    #     return out

    # def get_object(self, request, object_id, from_field=None):
    #    print("REQUEST: --- ", request)
    #    print("OBJECT ID: --- ", object_id)
    #    obj = super(Manuali_uscitiAdmin, self).get_object(request, object_id)
    #    if obj is not None:
    #        print("OBJ:", obj.get_file())
    #        obj.get_file = "test"
    #    return obj

    # def get_readonly_fields(self, request, obj=None):
    #     out = super(Manuali_uscitiAdmin, self).get_readonly_fields(request)
    #     if obj:
    #         print("---OBJ: ", obj.get_file)
    #         obj.get_file = "test"
    #
    #     return out



    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "codice":
            print("----INIZIO----")
            print("kwargs:", **kwargs)
            print("db_field:", db_field)
            print("request:", request)

            if request.method == 'GET' and 'codice' in request.GET:
                codice = request.GET.get('codice', None)
                if codice is not None:
                    #set the default foreign key as the indicated instance
                    print("ecci il codice: ", codice)
                    myobj = Manuali.objects.filter(codice=codice)

                    kwargs['queryset'] = myobj
                    kwargs['initial'] = myobj



            #print("TEST", self.mytest(request))
            #mytest= super(Manuali_uscitiAdmin, self).get_readonly_fields(request)
            #mytest = self.get_readonly_fields(request)
            #print("TEST", mytest)

            print("request.GET", request.GET )
            #print("kwargs:", myobj[0].file_link())
            print("kwargs:", kwargs)
            print("----FINE----")
            #return db_field.formfield(**kwargs)
        return super(Manuali_uscitiAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)








#register all my admin interfaces
admin.site.register(Clienti, ClientiAdmin, verbose_name_plural="Clienti")
admin.site.register(Manuali, ManualiAdmin)
admin.site.register(Manuali_usciti, Manuali_uscitiAdmin)
admin.site.register(Lingua)


