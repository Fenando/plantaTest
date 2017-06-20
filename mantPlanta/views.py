from django.shortcuts import render
from mantPlanta import models
from django.http import HttpResponse,HttpResponseRedirect, Http404
from io import BytesIO
from mantPlanta.forms import FormularioSolicitud
from mantPlanta.forms import FormularioCerrarSolicitud
from mantPlanta.forms import FormularioAprobar
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from django.views.generic import ListView
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table
import datetime
import pdfkit
import json
from django.views.generic.base import View
from django.contrib.auth.decorators import permission_required
from mantPlanta.models import Equipo
from django.core import serializers
from django.core.mail import EmailMessage
from django.core.mail import get_connection

from django.template.loader import get_template
from django.template import Context
from datetime import date
#from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def menu(request):
    return render(request, 'menuPrincipal.html')

def menuGeneral(request):
    return render(request, 'menuGeneral.html')

def menuPlanta(request):
    return render(request, 'menuPlanta.html')

def menuExteriores(request):
    return render(request, 'exteriores/menuExteriores.html')

def buscarSolicitud(request,id):
    aMant = id

    try:
        acc = models.Acciones.objects.get(mantencion=aMant)
        return render(request, 'verSolicitudOt.html', {'mant':aMant,'acc': acc})

    except:
        return render(request, 'verSolicitud.html', {'mant':aMant})




#@permission_required('mantPlanta.Mantencion', login_url="/ultimaSolicitud/")
def solicitud(request, equipo_id, area):

    if request.user.groups.filter(name='bkb').exists():
        try:
            mant = models.Mantencion.objects.filter(equipos__nombre=equipo_id).order_by('-equipos', '-fecha','-id').distinct('equipos')
            return buscarSolicitud(request, mant[0])
        except:
            return HttpResponseRedirect('/informacion/' + equipo_id + '/')

    else:
        ei = equipo_id

        idEq = models.Equipo.objects.get(nombre=ei)

        if request.method == 'POST':
            form = FormularioSolicitud(request.POST, request.FILES)
            if form.is_valid():
                print('caca1')
                cd = form.cleaned_data
                print(cd['nOt'])
                mantencion = models.Mantencion(equipos=idEq,causa=cd['causa'],
                                               fecha= datetime.datetime.now(),
                                               solicitante=cd['solicitante'],
                                               correo=cd['email'],
                                               usuario = request.user,
                                               numero_ot = cd['nOt'],
                                               imagen=cd['imagen'])

                try:
                    mantencion.save()
                    connection = get_connection()
                    # Manually open the connection
                    connection.open()
                    if mantencion.id:
                        mID = mantencion.id
                        c = 'http://' + request.POST['url'] + '/' + idEq.area.nombre + '/' + str(mID)

                        html1 = get_template('correoSolicitud.html')
                        d1 = Context({'eName': idEq.nombre, 'url': c, 'y': True})
                        html_content1 = html1.render(d1)
                        subject1 = 'Solicitud para ' + idEq.nombre
                        msg1 = EmailMessage(subject1, html_content1, 'ff.carreno@gmail.com',
                                            to=['lrubio@sopraval.cl','gudinomarco@gmail.com','ff.carreno@gmail.com'])
                                            #to=['ff.carreno@gmail.com'])
                        msg1.content_subtype = "html"  # Main content is now text/html
                        html2 = get_template('correoSolicitud.html')
                        d2 = Context({'eName': idEq.nombre, 'url': c})
                        html_content2 = html2.render(d2)
                        subject2 = 'Solicitud para ' + idEq.nombre
                        msg2 = EmailMessage(subject2, html_content2, 'ff.carreno@gmail.com', to=[mantencion.correo])
                        msg2.content_subtype = "html"  # Main content is now text/html

                        # msg1.send()
                        # msg2.send()
                        connection.send_messages([msg1, msg2])
                        # The connection was already open so send_messages() doesn't close it.
                        # We need to manually close the connection.
                        connection.close()
                except:
                    print("Error sending email to %s" %','.join("jkdelarge@gmail.com"))
                return HttpResponseRedirect('/' + idEq.area.nombre + '/')
        else:
            form = FormularioSolicitud
        return render(request,'solicitudMantencion.html',{'form':form,'ei':ei,'ar':idEq.area.nombre,'info':idEq.info})


# def convertir_pdf(request, equipo_id):
#      equipo = Equipo.objects.get(id=equipo_id)
#      try:
#          mantencion = models.Mantencion.objects.filter(equipos = equipo).filter(realizada = False).order_by('fecha')[0]
#      except ValueError:
#          raise Http404()
#      respose = HttpResponse(content_type='application/pdf')
#      pdf_name = "reporte equipo"
#      respose['Content-Disposition'] = 'filename = "archivo.pdf"'
#      buffer = BytesIO()
#      p = canvas.Canvas(buffer)
#      p.roundRect(0, 750, 694, 120, 20, stroke=0, fill=1)
#      p.setFont('Times-Bold', 32)
#      p.setFillColorRGB(1, 1, 1)
#      p.drawString(150, 800, str(mantencion))
#      p.setFont('Times-Bold', 12)
#      p.setFillColorRGB(0, 0, 0)
#      p.drawString(100, 720,
#                   mantencion.causa)
#      if mantencion.imagen:
#          image_file = ImageReader(mantencion.imagen)
#          p.drawImage(image_file, 100, 100, width=200, height=200)
#      p.showPage()
#      p.save()
#      pdf = buffer.getvalue()
#      buffer.close()
#      respose.write(pdf)
#      return respose
#
# def convertir_pdfT(request, equipo_id):
#
#     return HttpResponse('hola mundo '+ equipo_id.nombre)
#
# def generar_pdf(request, equipo_id):
#     equipo = Equipo.objects.get(id=equipo_id)
#     response = HttpResponse(content_type='application/pdf')
#     pdf_name = "clientes.pdf"  # llamado clientes
#     # la linea 26 es por si deseas descargar el pdf a tu computadora
#     # response['Content-Disposition'] = 'attachment; filename=%s' % pdf_name
#     buff = BytesIO()
#     doc = SimpleDocTemplate(buff,
#                             pagesize=letter,
#                             rightMargin=40,
#                             leftMargin=40,
#                             topMargin=60,
#                             bottomMargin=18,
#                             )
#     mantenciones = []
#     styles = getSampleStyleSheet()
#     header = Paragraph("Reporte de mantencion", styles['Heading1'])
#     mantenciones.append(header)
#     headings = ('Equipo', 'Causa', 'Solicitante', 'fecha')
#     p = models.Mantencion.objects.filter(equipos = equipo).filter(realizada = False).order_by('fecha')[0]
#     allmantencion =  [(p, p.causa, p.solicitante, p.fecha)]
#     t = Table([headings] + allmantencion)
#     t.setStyle(TableStyle(
#         [
#             ('GRID', (0, 0), (3, -1), 1, colors.dodgerblue),
#             ('LINEBELOW', (0, 0), (-1, 0), 2, colors.darkblue),
#             ('BACKGROUND', (0, 0), (-1, 0), colors.dodgerblue)
#         ]
#     ))
#     mantenciones.append(t)
#     doc.build(mantenciones)
#     response.write(buff.getvalue())
#     buff.close()
#     return response
# def generar_report(request, equipo_id):
#     respose = HttpResponse(content_type='application/pdf')
#     respose['Content-Disposition'] = 'filename = "testPdf.pdf"'
#     buffer = BytesIO()
#     c = canvas.Canvas(buffer)
#     #Header
#     c.setLineWidth(.3)
#     c.setFont('Helvetica', 22)
#     c.drawString(30,750, 'Reporte')
#
#     c.setFont('Helvetica',12)
#     c.drawString(30, 735, 'repotes')
#
#     c.setFont('Helvetica-Bold', 12)
#     c.drawString(480,750, str(datetime.date.today()))
#     #start x, heigth end y, heigth
#     c.line(460,747,560,747)
#     c.showPage()
#     c.save()
#     pdf = buffer.getvalue()
#     buffer.close()
#     respose.write(pdf)
#     return respose




def reportEquipo(request):

    e= mantencion

    return render(request,'reportEquipo.html',{'e':e})

def create(request,equipo_id):
    try:
        id_e = models.Equipo.objects.get(nombre=equipo_id)
        mantencion = models.Mantencion.objects.filter(equipos= id_e).filter(realizada=False).order_by('fecha')[0]
        global mantencion
        # Create a URL of our project and go to the template route
        projectUrl = 'http://'+request.get_host() + '/reportEquipo'
        pdf = pdfkit.from_url(projectUrl, False)
        # Generate download
        response = HttpResponse(pdf,content_type='application/pdf')
        response['Content-Disposition'] = 'filename="ourcodeworld.pdf"'

        return response
    except:
        return HttpResponseRedirect('/solicitud/'+equipo_id)

def trozado(request):
    return render(request, 'planoTrozado.html')

def generalCecinasUno(request):
    return render(request, 'plantas/planoCecinasUno.html')

def generalCecinasDos(request):
    return render(request, 'plantas/planoCecinasDos.html')

def servPrimer(request):
    return render(request, 'plantas/planoEdificioServicioUno.html')

def servSegundo(request):
    return render(request, 'plantas/planoEdificioServicioDos.html')

def plantaGeneral(request):
    return render(request, 'planoPlantaGeneral.html')

def plantaFaena(request):
    return render(request, 'plantas/planoFaenadora.html')

def generalTrozado(request):
    return render(request, 'plantas/planoTrozado.html')

def generalProcesos(request):
    return render(request, 'plantas/planoProcesosPosteriores.html')

def generalEmpaque(request):
    return render(request, 'plantas/planoEmpaque.html')

def generalDespacho(request):
    return render(request, 'plantas/planoDespacho.html')

def generalSalaMaqCinco(request):
    return render(request, 'plantas/planoMaquinasCinco.html')

def generalSalaMaqUno(request):
    return render(request, 'plantas/planoMaquinasUno.html')

def generalAdmin(request):
    return render(request, 'plantas/planoOficinasAdministracion.html')

def generalCarton(request):
    return render(request, 'plantas/planoCartonFreezer.html')

def generalSub(request):
    return render(request, 'plantas/planoSubproductos.html')

def generalTratamiento(request):
    return render(request, 'plantas/planoTratamiento.html')

def generalEdGerencia(request):
    return render(request, 'plantas/planoEdificioIngenieria.html')

def generalEntre(request):
    return render(request, 'plantas/planoEntretecho.html')

def cecinasBodegas(request):
    return render(request, 'cecinasUno/planoBodegas.html')

def cecinasDespacho(request):
    return render(request, 'cecinasUno/planoDespachoCecinas.html')

def cecinasPasilloDespacho(request):
    return render(request, 'cecinasUno/planoPasilloDespacho.html')

def cecinasEmpaque(request):
    return render(request, 'cecinasUno/planoEmpaqueCecinas.html')

def cecinasEmbolse(request):
    return render(request, 'cecinasUno/planoEmbolseCecinas.html')

def cecinasMantencion(request):
    return render(request, 'cecinasUno/planoMantencionCecinas.html')

def cecinasProductosTerminados(request):
    return render(request, 'cecinasUno/planoProductosTerminadosCecinas.html')

def cecinasPasilloFiltroSanitario(request):
    return render(request, 'cecinasUno/planoPasilloFiltroSanitarioCecinas.html')

def cecinasFiltroSanitario(request):
    return render(request, 'cecinasUno/planoFiltroSanitarioCecinas.html')

def cecinasSalaSalmuera(request):
    return render(request, 'cecinasUno/planoSalaSalmueraCecinas.html')

def cecinasTallerMantencion(request):
    return render(request, 'cecinasUno/planoTallerMantencionCecinas.html')

def cecinasOficinasInterior(request):
    return render(request, 'cecinasUno/planoOficinasInteriorCecinas.html')

def cecinasOficinasExterior(request):
    return render(request, 'cecinasUno/planoOficinasExteriorCecinas.html')

def cecinasLavadoBandejas(request):
    return render(request, 'cecinasUno/planoLavadoBandejasCecinas.html')

def cecinasCamaraReposo(request):
    return render(request, 'cecinasUno/planoCamaraReposoCecinas.html')

def cecinasCamaraEnfriadoAire(request):
    return render(request, 'cecinasUno/planoCamaraEnfriadoAireCecinas.html')

def cecinasCamaraMateriasPrimas(request):
    return render(request, 'cecinasUno/planoCamaraMateriasPrimasCecinas.html')

def cecinasDuchasEnfriamiento(request):
    return render(request, 'cecinasUno/planoSalaDuchasEnfriamientoCecinas.html')

def cecinasEmbutidoras(request):
    return render(request, 'cecinasUno/planoEmbutidorasCecinas.html')

def cecinasHumidificador(request):
    return render(request, 'cecinasUno/planoHumidificadorCecinas.html')

def cecinasPasilloInteriorDos(request):
    return render(request, 'cecinasUno/planoPasilloInteriorDosCecinas.html')

def cecinasMasajeoInyectado(request):
    return render(request, 'cecinasUno/planoMasajeoInyectadoCecinas.html')

def cecinasPasilloInterior(request):
    return render(request, 'cecinasUno/planoPasilloInteriorCecinas.html')

def cecinasRecepcion(request):
    return render(request, 'cecinasUno/planoRecepcionCecinas.html')

def cecinasHornosAhumadores(request):
    return render(request, 'cecinasUno/planoHornosAhumadoresCecinas.html')

def cecinasPasilloIngreso(request):
    return render(request, 'cecinasUno/planoPasilloIngresoCecinas.html')

def cecinasExteriores(request):
    return render(request, 'cecinasUno/planoExterioresCecinas.html')

def cecinasSalaMaquinas(request):
    return render(request, 'cecinasUno/planoSalaMaquinasCecinas.html')

def cecinasPasilloEmbutidoras(request):
    return render(request, 'cecinasUno/planoPasilloEmbutidoraCecinas.html')

def EdificioServicioUnoCasinoCecinas(request):
    return render(request, 'edificioServicio/planoCasinoCecinasEdificioServicioUno.html')

def EdificioServicioUnoSalaCambioCecinas(request):
    return render(request, 'edificioServicio/planoSalaCambioCecinasEdificioServicioUno.html')

def EdificioServicioUnoBanoVaronesCuatro(request):
    return render(request, 'edificioServicio/planoBanoVaronesCuatro.html')

def EdificioServicioUnoBanoVaronesTres(request):
    return render(request, 'edificioServicio/planoBanoVaronesTres.html')

def EdificioServicioUnoBanoVaronesDos(request):
    return render(request, 'edificioServicio/planoBanoVaronesDos.html')

def EdificioServicioUnoBanoVaronesUno(request):
    return render(request, 'edificioServicio/planoBanoVaronesUno.html')

def EdificioServicioUnoBanoDamasUno(request):
    return render(request, 'edificioServicio/planoBanoDamasUno.html')

def EdificioServicioPasilloCecinas(request):
    return render(request, 'edificioServicio/planoPasilloCecinas.html')

def EdificioServicioPasilloFaena(request):
    return render(request, 'edificioServicio/planoPasilloFaena.html')

def EdificioServicioPasillo(request):
    return render(request, 'edificioServicio/planoPasilloServicio.html')

def EdificioServicioCasinoFaena(request):
    return render(request, 'edificioServicio/planoCasinoFaenaEdificioServicioUno.html')

def EdificioServicioEntradaCasinoFaena(request):
    return render(request, 'edificioServicio/planoEntradaCasinoFaena.html')

def EdificioServicioZonaDescansoFaena(request):
    return render(request, 'edificioServicio/planoZonaDescansoCasinoFaena.html')

def EdificioServicioZonaDescansoCecinas(request):
    return render(request, 'edificioServicio/planoZonaDescansoCasinoCecinas.html')

def EdificioServicioBanoCasinoFaena(request):
    return render(request, 'edificioServicio/planoBanoCasinoFaena.html')

def EdificioServicioDuchasCasinoFaena(request):
    return render(request, 'edificioServicio/planoDuchasCasinoFaena.html')

def EdificioServicioOficinasCasinoFaena(request):
    return render(request, 'edificioServicio/planoOficinasCasinoFaena.html')

def EdificioServicioSpBanoDamasTres(request):
    return render(request, 'edificioServicioDos/planoBanoDamasTres.html')

def EdificioServicioSpBanoDamasDos(request):
    return render(request, 'edificioServicioDos/planoBanoDamasDos.html')

def EdificioServicioSpBanoDamasCuatro(request):
    return render(request, 'edificioServicioDos/planoBanoDamasCuatro.html')

def EdificioServicioSpBanoVisitasDos(request):
    return render(request, 'edificioServicioDos/planoBanoVisitasDos.html')

def EdificioServicioSpBanoVisitas(request):
    return render(request, 'edificioServicioDos/planoBanoVisitas.html')

def EdificioServicioSpSalaCambio(request):
    return render(request, 'edificioServicioDos/planoSalaCambioFaena.html')

def EdificioServicioSpPasillo(request):
    return render(request, 'edificioServicioDos/planoPasilloEdificioServicioDos.html')

def EdificioServicioSpPasilloDos(request):
    return render(request, 'edificioServicioDos/planoPasilloDosEdificioServicioDos.html')

def FaenadoraDescolgado(request):
    return render(request, 'faenadora/planoDescolgado.html')

def FaenadoraMatanza(request):
    return render(request, 'faenadora/planoMatanza.html')

def FaenadoraEviscerado(request):
    return render(request, 'faenadora/planoEviscerado.html')

def FaenadoraOficinasMantanza(request):
    return render(request, 'faenadora/planoOficinasMatanza.html')

def FaenadoraMantencion(request):
    return render(request, 'faenadora/planoMantencion.html')

def FaenadoraOficinas(request):
    return render(request, 'faenadora/planoOficinas.html')

def FaenadoraFiltroSanitario(request):
    return render(request, 'faenadora/planoFiltroSanitario.html')

def FaenadoraCamaraTraspaso(request):
    return render(request, 'faenadora/planoCamaraTraspaso.html')

def FaenadoraSalaTransferencia(request):
    return render(request, 'faenadora/planoSalaTransferencia.html')

def FaenadoraLavadoGanchos(request):
    return render(request, 'faenadora/planoLavadoGanchos.html')

def FaenadoraCamara430(request):
    return render(request, 'faenadora/planoCamara430.html')

def FaenadoraCamara440(request):
    return render(request, 'faenadora/planoCamara440.html')

def FaenadoraCamara420(request):
    return render(request, 'faenadora/planoCamara420.html')

def FaenadoraDuchasEnfriado(request):
    return render(request, 'faenadora/planoDuchasEnfriado.html')

def FaenadoraPasarela(request):
    return render(request, 'faenadora/planoPasarelaFaenadora.html')

def FaenadoraPasillo(request):
    return render(request, 'faenadora/planoPasilloFaenadora.html')

def TrozadoBanos(request):
    return render(request, 'trozado/planoBanosTrozado.html')

def TrozadoMantencion(request):
    return render(request, 'trozado/planoMantencionTrozado.html')

def TrozadoSalaElectrica(request):
    return render(request, 'trozado/planoSalaElectricaTrozado.html')

def TrozadoSalaLavado(request):
    return render(request, 'trozado/planoSalaLavadoTrozado.html')

def TrozadoPasillo(request):
    return render(request, 'trozado/planoPasilloTrozado.html')

def TrozadoSalaReuniones(request):
    return render(request, 'trozado/planoSalaReunionesTrozado.html')

def TrozadoSala(request):
    return render(request, 'trozado/planoSalaTrozado.html')

def ProcesosSalaUno(request):
    return render(request, 'procesos/planoSalaUnoProcesos.html')

def ProcesosSalaDos(request):
    return render(request, 'procesos/planoSalaDosProcesos.html')

def ProcesosSalaTres(request):
    return render(request, 'procesos/planoSalaTresProcesos.html')

def ProcesosSalaCuatro(request):
    return render(request, 'procesos/planoSalaCuatroProcesos.html')

def ProcesosSalaCinco(request):
    return render(request, 'procesos/planoSalaCincoProcesos.html')

def ProcesosSalaSeis(request):
    return render(request, 'procesos/planoSalaSeisProcesos.html')

def ProcesosSalaSiete(request):
    return render(request, 'procesos/planoSalaSieteProcesos.html')

def ProcesosSalaOcho(request):
    return render(request, 'procesos/planoSalaOchoProcesos.html')

def ProcesosSalaNueve(request):
    return render(request, 'procesos/planoSalaNueveProcesos.html')

def ProcesosMantencion(request):
    return render(request, 'procesos/planoMantencionProcesos.html')

def ProcesosFabricaHielo(request):
    return render(request, 'procesos/planoFabricaHieloProcesos.html')

def ProcesosPalletRrhh(request):
    return render(request, 'procesos/planoPalletRrhhProcesos.html')

def ProcesosPasillo(request):
    return render(request, 'procesos/planoPasilloProcesos.html')

def ProcesosMarinado(request):
    return render(request, 'procesos/planoMarinadoProcesos.html')

def ProcesosSala(request):
    return render(request, 'procesos/planoSalaProcesos.html')

def EmpaqueCamaraPulmon(request):
    return render(request, 'empaque/planoCamaraPulmonEmpaque.html')

def EmpaqueSala(request):
    return render(request, 'empaque/planoSalaEmpaque.html')

def EmpaqueOficinas(request):
    return render(request, 'empaque/planoOficinasEmpaque.html')

def DespachoCalleUno(request):
    return render(request, 'despacho/planoCalleUnoDespacho.html')

def DespachoCalleDos(request):
    return render(request, 'despacho/planoCalleDosDespacho.html')

def DespachoCongeladoTres(request):
    return render(request, 'despacho/planoCongelado3Despacho.html')

def DespachoCamaraPallet(request):
    return render(request, 'despacho/planoCamaraPalletDespacho.html')

def DespachoTallerGruas(request):
    return render(request, 'despacho/planoTallerGruasDespacho.html')

def DespachoPasillo(request):
    return render(request, 'despacho/planoPasilloDespacho.html')

def DespachoInformatica(request):
    return render(request, 'despacho/planoInformaticaDespacho.html')

def DespachoSala(request):
    return render(request, 'despacho/planoSalaDespacho.html')

def CartonFreezerPasillo(request):
    return render(request, 'cartonFreezer/planoPasilloCarton.html')

def CartonFreezerSalaElectrica(request):
    return render(request, 'cartonFreezer/planoSalaElectricaCarton.html')

def CartonFreezerArmadoCaja(request):
    return render(request, 'cartonFreezer/planoArmadoCajasCarton.html')

def CartonFreezerArmadoCajaDos(request):
    return render(request, 'cartonFreezer/planoArmadoCajasDosCarton.html')

def CartonFreezer(request):
    return render(request, 'cartonFreezer/planoCartonFreezerCarton.html')

def CecinasDosMateriasPrimas(request):
    return render(request, 'cecinasDos/planoMateriasPrimasCecinasDos.html')

def CecinasDosPreparacionMasas(request):
    return render(request, 'cecinasDos/planoPreparacionMasasCecinasDos.html')

def CecinasDosEsperaHornos(request):
    return render(request, 'cecinasDos/planoEsperaHornosCecinasDos.html')

def CecinasDosSalaCocidos(request):
    return render(request, 'cecinasDos/planoSalaCocidosCecinasDos.html')

def CecinasDosSalaCrudos(request):
    return render(request, 'cecinasDos/planoSalaCrudosCecinasDos.html')

def CecinasDosSalaEnfriado(request):
    return render(request, 'cecinasDos/planoSalaEnfriadoCecinasDos.html')

def CecinasDosSalaHornos(request):
    return render(request, 'cecinasDos/planoSalaHornosCecinasDos.html')

def CecinasDosSalaEmpaque(request):
    return render(request, 'cecinasDos/planoSalaEmpaqueCecinasDos.html')

def CecinasDosSalaIngreso(request):
    return render(request, 'cecinasDos/planoSalaIngresoCecinasDos.html')

def CecinasDosPasillo(request):
    return render(request, 'cecinasDos/planoPasilloCecinasDos.html')

def EdificioIngenieriaIngenieria(request):
    return render(request, 'edificioIngenieria/planoEdificioIngenieriaEdificioIngenieria.html')

def EdificioIngenieriaPasillo(request):
    return render(request, 'edificioIngenieria/planoPasilloEdificioIngenieria.html')

def EdificioIngenieriaSalaMaq(request):
    return render(request, 'edificioIngenieria/planoSalaMaquinaEdificioIngenieria.html')

def EdificioIngenieriaSalaMaq(request):
    return render(request, 'edificioIngenieria/planoSalaMaquinaEdificioIngenieria.html')

def EdificioAdministracionOficinasCalidad(request):
    return render(request, 'edificioAdministracion/planoOficinasCalidadAdministracion.html')

def EdificioAdministracionPasillo(request):
    return render(request, 'edificioAdministracion/planoPasilloFiltroAdministracion.html')

def EdificioAdministracionEnfermeria(request):
    return render(request, 'edificioAdministracion/planoSalaEnfermeriaAdministracion.html')

def EdificioAdministracion(request):
    return render(request, 'edificioAdministracion/planoEdificioAdministracion.html')

def EdificioAdministracionLaboratorio(request):
    return render(request, 'edificioAdministracion/planoLaboratorioCalidad.html')

def EdificioAdministracionOficinasIngreso(request):
    return render(request, 'edificioAdministracion/planoOficinasIngreso.html')

def EdificioAdministracionLavado(request):
    return render(request, 'edificioAdministracion/planoSalasRectificadoLavado.html')

def EntretechoCecinas(request):
    return render(request, 'entretechos/planoCecinasEntretecho.html')

def EntretechoFaenaDos(request):
    return render(request, 'entretechos/planoFaenaDosEntretecho.html')

def EntretechoFaenaUno(request):
    return render(request, 'entretechos/planoFaenaUnoEntretecho.html')

def EntretechoFaena(request):
    return render(request, 'entretechos/planoFaenaEntretecho.html')

def MaquinasUnoOficinas(request):
    return render(request, 'salaMaquinasUno/planoOficinasMaquinasUno.html')

def MaquinasUnoSala(request):
    return render(request, 'salaMaquinasUno/planoSalaMaquinasUno.html')

def MaquinasCincoSalaElectrica(request):
    return render(request, 'salaMaquinaCinco/planoSalaElectricaMaquinasCinco.html')

def MaquinasCincoCompresores(request):
    return render(request, 'salaMaquinaCinco/planoCompresoresMaquinasCinco.html')

def SubproductosOficinas(request):
    return render(request, 'subproductos/planoOficinasSubproductos.html')

def SubproductosGenerador(request):
    return render(request, 'subproductos/planoGeneradorSubproductos.html')

def SubproductosViscerasPlumas(request):
    return render(request, 'subproductos/planoSalaViscerasPlumasSubproductos.html')

def SubproductosIngresoViscerasPlumas(request):
    return render(request, 'subproductos/planoIngresoViscerasPlumasSubproductos.html')

def SubproductosSalaCaldera(request):
    return render(request, 'subproductos/planoSalaCalderaSubproductos.html')

def SubproductosBodega(request):
    return render(request, 'subproductos/planoBodegaSubproductos.html')

def SubproductosBodegaDos(request):
    return render(request, 'subproductos/planoBodegaDosSubproductos.html')

def SubproductosSalaElectrica(request):
    return render(request, 'subproductos/planoSalaElectricaUnoSubproductos.html')

def SubproductosSalaElectricaDos(request):
    return render(request, 'subproductos/planoSalaElectricaDosSubproductos.html')

def TratamientoBiomasa(request):
    return render(request, 'tratamiento/planoBiomasa.html')

def TratamientoEstanquesRiles(request):
    return render(request, 'tratamiento/planoEstanquesRiles.html')

def TratamientoOficinasRiles(request):
    return render(request, 'tratamiento/planoOficinasRiles.html')

def TratamientoDecanterUnoRiles(request):
    return render(request, 'tratamiento/planoDecanterUnoRiles.html')

def TratamientoDecanterDosRiles(request):
    return render(request, 'tratamiento/planoDecanterDosRiles.html')

def TratamientoSalaElectricaBiologica(request):
    return render(request, 'tratamiento/planoSalaElectricaBiologica.html')

def SubproductosPasarela(request):
    return render(request, 'subproductos/planoPasarelaSubproductos.html')

def TratamientoExteriorBiologica(request):
    return render(request, 'tratamiento/planoExteriorBiologica.html')

def ExterioresGerencia(request):
    return render(request, 'exteriores/planoGerenciaRRHH.html')

def ExterioresIngresoPeatonal(request):
    return render(request, 'exteriores/planoIngresoPeatonal.html')

def ExterioresFaena(request):
    return render(request, 'exteriores/planoFaenaExterior.html')

def ExterioresCecinas(request):
    return render(request, 'exteriores/planoCecinasExterior.html')

def ExterioresIngresoVehicular(request):
    return render(request, 'exteriores/planoIngresoVehicularExterior.html')

def ExterioresBodegaUno(request):
    return render(request, 'exteriores/planoBodegaUnoExterior.html')

def ExterioresBodegaDos(request):
    return render(request, 'exteriores/planoBodegaDosExterior.html')

def ExterioresBodegaTres(request):
    return render(request, 'exteriores/planoBodegaTresExterior.html')

def ExterioresSubproductos(request):
    return render(request, 'exteriores/planoSubproductosExterior.html')

def busqueda(request, area):
    if request.is_ajax():
        #e = models.Equipo.objects.filter(id__in = models.Mantencion.objects.filter(realizada = 0).values('equipos').distinct(), area__nombre = area)
        eq = models.Mantencion.objects.filter(realizada = 0, equipos__area__nombre = area, rechazada = 0).order_by('equipos','-fecha').distinct('equipos').values('equipos__nombre', 'aprobada','rechazada','fecha_aprec')
        le = list(eq)
        #x = [{'aprobada': False, 'equipos__nombre': 'bm7'}, {'aprobada': False, 'equipos__nombre': 'bm10'}]
        data = json.dumps(le, default=date_handler)
        #data = json.dumps(list(eq))
        #data = serializers.serialize('json', list(e))

        return HttpResponse(data, content_type='application/json')
    else:
        return HttpResponse("Solo Ajax")

def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError


def reportes(request, equipo_id):
    ei = equipo_id
    return render(request, 'menuReporte.html',{'ei':ei})

def informacion(request, equipo_id):
    tipo = models.Equipo.objects.get(nombre=equipo_id)
    mant = list(models.Mantencion.objects.filter(equipos__nombre = equipo_id).order_by('-fecha','-id')[:5])

    imagen = tipo.info.imagen
    a = []
    com = []
    for m in mant:
        if m.realizada:
            acc = models.Acciones.objects.get(mantencion__id = m.id)
            a.append(acc)
        com.append(models.Comentario.objects.filter(mantencion__id = m.id))

    return render(request, 'informacionEquipo.html', {'imagen':imagen,'tipo':tipo,'a':a,'mant':mant,'com':com})




def search(request):
    if request.method == 'GET':
        try:
            if request.GET.get('buscare'):
                x =  request.GET.get('buscare')
                z = str(x).lower()
                print(z)
                e = models.Equipo.objects.get(nombre = z)
                return render(request, 'menuPlanta.html', {'area': e.area.nombre, 'planta': e.area.planta.nombre})
            if request.GET.get('buscaro'):
                x = request.GET.get('buscaro')
                m = models.Mantencion.objects.filter(numero_ot = x)

                return render(request, 'menuPlanta.html', {'m':m})
            if request.GET.get('ver'):
                x = request.GET.get('ver')
                print(x)

                m = models.Mantencion.objects.get(id=int(x))
                print(x)
                return buscarSolicitud(request,m)
            if request.GET.get('fechas'):

                print(request.GET.get('desde'))
                print(request.GET.get('hasta'))
                mFecha = models.Mantencion.objects.filter(fecha__range = (request.GET.get('desde'),request.GET.get('hasta')))
                print(request.GET.get('desde'))
                print(request.GET.get('hasta'))
                return render(request, 'menuPlanta.html', {'mFecha': mFecha})
        except:
               return HttpResponseRedirect('/menuPlanta/')

    return HttpResponseRedirect('/menuPlanta/')


    #    if cx2['nada'] == True:
    #        print('juan pico')

    # form = forms.FormularioSolicitud(request.POST)
    # if form.is_valid():
    # cd = form.cleaned_data
    # a = bool(request.POST['aprobar'])
    #
    # print(a)
    # aMant.fecha_aprec = datetime.datetime.now()
    # aMant.aprobada = a
    # aMant.rechazada = not a
    # if int(request.POST['numero_ot']) > 1:
    #     aMant.numero_ot = request.POST['numero_ot']
    # try:
    #     aMant.save()
    # except:
    #     print('pene')
    #     return Http404()
    # if aMant.id:
    #     html = get_template('correoAprobado.html')
    #     d = Context({'eName': aMant.equipos.nombre, 'fecha': aMant.fecha_aprec,
    #                  'acciones': aMant.aprobada, 'nOt': aMant.numero_ot})
    #     html_content = html.render(d)
    #     subject = 'respuesta de solicitud para ' + aMant.equipos.nombre
    #     msg = EmailMessage(subject, html_content, 'ff.carreno@gmail.com', ['ff.carreno@gmail.com'])
    #     msg.content_subtype = "html"  # Main content is now text/html
    #     msg.send()
    #     return HttpResponseRedirect('/menuPlanta/')


def aprobar(request, equipo_id, mant_id, area):
    idMant = models.Mantencion.objects.get(id=mant_id)
    if not (idMant.rechazada | idMant.aprobada):
        if request.method == 'POST':

            form = FormularioAprobar(request.POST)

            if form.is_valid():
                try:
                    cd = form.cleaned_data
                    idMant.aprobada = cd['nada']
                    idMant.rechazada = not cd['nada']
                    idMant.fecha_aprec = datetime.datetime.now()
                    idMant.numero_ot = cd['Ots']
                    com = models.Comentario(mantencion = idMant, comentario = cd['comentario'], fecha = datetime.datetime.now())
                    idMant.save()

                    if idMant.id:
                        com.save()
                        if com.id:
                            print('1')
                            html1 = get_template('correoAprobado.html')
                            link = request.POST['url']
                            d1 = Context({'eName': idMant.equipos.nombre, 'fecha': idMant.fecha_aprec, 'nOt': idMant.numero_ot, 'acciones':idMant.aprobada,'com':com.comentario, 'link':link})
                            html_content1 = html1.render(d1)
                            subject1 = 'Respuesta de Solicitud '+str(idMant.id)+' para ' + idMant.equipos.nombre
                            msg1 = EmailMessage(subject1, html_content1, 'ff.carreno@gmail.com',
                                                to=['lrubio@sopraval.cl','gudinomarco@gmail.com','ff.carreno@gmail.com',idMant.correo])
                                                #to=['ff.carreno@gmail.com',idMant.correo])

                            msg1.content_subtype = "html"  # Main content is now text/html
                            msg1.send()

                    return HttpResponseRedirect('/menuPlanta/')
                except:
                    form = FormularioAprobar
                    return render(request, 'aprobarSolicitud.html', {'form': form, 'mant': idMant})
        else:
            form = FormularioAprobar

        return render(request, 'aprobarSolicitud.html', {'form': form,'mant':idMant})
    else:
        coms = models.Comentario.objects.filter(mantencion__id=idMant.id).order_by('-fecha')
        if idMant.aprobada:
            if request.method == 'POST':

                if revComentario(request.POST['comentario']):
                    try:
                        com = models.Comentario(mantencion=idMant, comentario=request.POST['comentario'],
                                                fecha=datetime.datetime.now())

                        com.save()
                        if com.id:
                            html1 = get_template('correoAprobadoComent.html')
                            link = request.POST['url']
                            d1 = Context({'eName': idMant.equipos.nombre,'nOt': idMant.numero_ot,'com': com,'link':link})
                            html_content1 = html1.render(d1)
                            subject1 = 'Se agrega comentario a solicitud ' + str(idMant.id) + ' para ' + idMant.equipos.nombre
                            msg1 = EmailMessage(subject1, html_content1, 'ff.carreno@gmail.com',
                                                to=['lrubio@sopraval.cl','gudinomarco@gmail.com','ff.carreno@gmail.com', idMant.correo])
                                                #to=['ff.carreno@gmail.com', idMant.correo])
                            msg1.content_subtype = "html"  # Main content is now text/html
                            msg1.send()

                        return HttpResponseRedirect('/menuPlanta/')
                    except:
                        return render(request, 'aprobarEditarSolicitud.html', {'mant': idMant, 'com':coms})
                else:

                    error =[]
                    error.append('por favor ingrese mas de dos palabras')
                    return render(request, 'aprobarEditarSolicitud.html', {'mant': idMant, 'com': coms,'errors':error})
            else:
                return render(request, 'aprobarEditarSolicitud.html', {'mant': idMant, 'com':coms})

        if idMant.rechazada:
            html = "<html><body><h1>Solicitud: %s </h1><h3>Ya fue rechazada en la fecha: %s</h3></body></html>" % (mant_id,str(idMant.fecha_aprec))
        return HttpResponse(html)


def revComentario(comentario):
    comentarios = comentario
    num_palabras = len(comentarios.split())
    if num_palabras < 2:
            return False
    return True


def solicitudCreada(request, equipo_id, area):


    user = request.user

    ei = equipo_id
    mant = models.Mantencion.objects.filter(equipos__nombre=ei, equipos__area__nombre=area, realizada=0).order_by(
        '-fecha','-id')
    aMant = mant[0]
    print(aMant.id)
    if aMant.aprobada:
        print('caca')
        if user.groups.filter(name='bkb').exists():
            if request.method == 'POST':
                form = FormularioCerrarSolicitud(request.POST, request.FILES)
                if form.is_valid():
                    cd = form.cleaned_data

                    acc = models.Acciones(mantencion=aMant, accion=cd['accion'], fecha=cd['fechac'],
                                          usuario=request.user,
                                          realizador=cd['realizador'], imagen=cd['imagenc'])
                    aMant.realizada = True
                    acc.save()
                    aMant.save()
                    if acc.id:

                        html1 = get_template('correoCierre.html')
                        d1 = Context(
                            {'eName': aMant.equipos.nombre, 'fecha': acc.fecha, 'nOt': aMant.numero_ot,
                             'acciones': acc.accion, 'ejecutante': acc.realizador})
                        html_content1 = html1.render(d1)
                        subject1 = 'Cierre de Solicitud ' + str(aMant.id) + ' para ' + aMant.equipos.nombre
                        msg1 = EmailMessage(subject1, html_content1, 'ff.carreno@gmail.com',
                                            to=['lrubio@sopraval.cl','gudinomarco@gmail.com','ff.carreno@gmail.com', aMant.correo])
                                            #to=['ff.carreno@gmail.com', aMant.correo])
                        msg1.content_subtype = "html"  # Main content is now text/html
                        msg1.send()
                    return HttpResponseRedirect('/' + aMant.equipos.area.nombre + '/')

            else:
                form = FormularioCerrarSolicitud()
            return render(request, 'cerrarSolicitud.html',
                          {'form': form, 'mant': aMant, 'ar': aMant.equipos.area.nombre})

    return render(request, 'verSolicitud.html', {'mant': aMant})

#@csrf_exempt
def correoApro(request):
    if request.is_ajax():
        #print(request.POST['u'])
        print(request.GET['u'])
        #print(request.POST['mid'])
        print(request.GET['mid'])
        #idm = request.POST['mid']
        idm = request.GET['mid']
        am = models.Mantencion.objects.get(id = idm )
        html1 = get_template('correoCierreApro.html')
        #link = request.POST['u']
        link = request.GET['u']
        d1 = Context({'amant': am,'link':link})
        html_content1 = html1.render(d1)
        subject1 = 'Recordatorio de respuesta solicitud '+ str(am.id)
        msg1 = EmailMessage(subject1, html_content1, 'ff.carreno@gmail.com',
                            to=['lrubio@sopraval.cl','gudinomarco@gmail.com','ff.carreno@gmail.com', 'gudinomarco@gmail.com'])
                             #to=['ff.carreno@gmail.com'])
        msg1.content_subtype = "html"  # Main content is now text/html
        msg1.send()
        return HttpResponse("exito")
    else:
        return HttpResponse("Solo Ajax")

