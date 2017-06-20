"""plantaTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login
import mantPlanta.views as views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^$',login,{'template_name':'login.html'}),
    url(r'^menu/$', views.menu, name='menu'),
    url(r'^search/$', views.search, name='search'),
    url(r'^menuGeneral/$', views.menuGeneral, name='menug'),
    url(r'^menuPlanta/$', views.menuPlanta, name='menup'),
    url(r'^menuExteriores/$', views.menuExteriores, name='menuExt'),
    url(r'^(?P<area>[^/]+)/solicitud/(?P<equipo_id>\w{1,3}\d{1,3})/$', views.solicitud, name='solicitud'),
    url(r'^reporte/(?P<equipo_id>[^/]+)/$',views.create, name='reporte'),
    url(r'^reportEquipo/$',views.reportEquipo),
    url(r'^plantaGeneral/$', views.plantaGeneral, name='pgeneral'),
    url(r'^iluminariastrozado/$',views.trozado,name='iluminariastrozado'),
    url(r'^cecinasUno/$',views.generalCecinasUno,name='cuno'),
    url(r'^cecinasDos/$',views.generalCecinasDos,name='cdos'),
    url(r'^serviciosUno/$',views.servPrimer,name='sprimer'),
    url(r'^serviciosDos/$',views.servSegundo,name='ssegundo'),
    url(r'^faenadora/$',views.plantaFaena,name='pfaena'),
    url(r'^generalTrozado/$',views.generalTrozado,name='ptrozado'),
    url(r'^generalProcesos/$',views.generalProcesos,name='pprocesos'),
    url(r'^generalEmpaque/$',views.generalEmpaque,name='pempaque'),
    url(r'^generalDespacho/$',views.generalDespacho,name='pdespacho'),
    url(r'^generalSalaMaqCinco/$',views.generalSalaMaqCinco,name='psalamaqcinco'),
    url(r'^generalSalaMaqUno/$',views.generalSalaMaqUno,name='psalamaquno'),
    url(r'^generalAdmin/$',views.generalAdmin,name='padmin'),
    url(r'^generalCarton/$',views.generalCarton,name='pcarton'),
    url(r'^generalSub/$',views.generalSub,name='psub'),
    url(r'^generalTratamiento/$',views.generalTratamiento,name='ptratamiento'),
    url(r'^generalEdGerencia/$',views.generalEdGerencia,name='pedgerencia'),
    url(r'^generalEntretechos/$',views.generalEntre,name='pentretechos'),
    url(r'^bodegas/$',views.cecinasBodegas,name='bodegas'),
    url(r'^pasillo_despacho_cecinas/$',views.cecinasPasilloDespacho,name='pasillo_despacho_cecinas'),
    url(r'^despacho_cecinas/$',views.cecinasDespacho,name='despacho_cecinas'),
    url(r'^empaque_cecinas/$',views.cecinasEmpaque,name='empaque_cecinas'),
    url(r'^embolse_cecinas/$',views.cecinasEmbolse,name='embolse_cecinas'),
    url(r'^mantencion_cecinas/$',views.cecinasMantencion,name='mantencion_cecinas'),
    url(r'^productos_terminados_cecinas/$',views.cecinasProductosTerminados,name='productos_terminados_cecinas'),
    url(r'^pasillo_filtro_cecinas/$',views.cecinasPasilloFiltroSanitario,name='pasillo_filtro_cecinas'),
    url(r'^filtro_sanitario_cecinas/$',views.cecinasFiltroSanitario,name='filtro_sanitario_cecinas'),
    url(r'^sala_salmuera_cecinas/$',views.cecinasSalaSalmuera,name='sala_salmuera_cecinas'),
    url(r'^taller_mantencion_cecinas/$',views.cecinasTallerMantencion,name='taller_mantencion_cecinas'),
    url(r'^oficinas_interior_cecinas/$',views.cecinasOficinasInterior,name='oficinas_interior_cecinas'),
    url(r'^oficinas_exterior_cecinas/$',views.cecinasOficinasExterior,name='oficinas_exterior_cecinas'),
    url(r'^lavado_bandejas_cecinas/$',views.cecinasLavadoBandejas,name='lavado_bandejas_cecinas'),
    url(r'^camara_reposo_cecinas/$',views.cecinasCamaraReposo,name='camara_reposo_cecinas'),
    url(r'^camara_enfriado_aire_cecinas/$',views.cecinasCamaraEnfriadoAire,name='camara_enfriado_aire_cecinas'),
    url(r'^camara_materias_primas_cecinas/$',views.cecinasCamaraMateriasPrimas,name='camara_materias_primas_cecinas'),
    url(r'^duchas_enfriamiento_cecinas/$',views.cecinasDuchasEnfriamiento,name='duchas_enfriamiento_cecinas'),
    url(r'^embutidoras_cecinas/$',views.cecinasEmbutidoras,name='embutidoras_cecinas'),
    url(r'^humidificador_cecinas/$',views.cecinasHumidificador,name='humidificador_cecinas'),
    url(r'^pasillo_interior_dos_cecinas/$',views.cecinasPasilloInteriorDos,name='pasillo_interior_dos_cecinas'),
    url(r'^masajeo_inyectado_cecinas/$',views.cecinasMasajeoInyectado,name='masajeo_inyectado_cecinas'),
    url(r'^pasillo_interior_cecinas/$',views.cecinasPasilloInterior,name='pasillo_interior_cecinas'),
    url(r'^recepcion_cecinas/$',views.cecinasRecepcion,name='recepcion_cecinas'),
    url(r'^hornos_ahumadores_cecinas/$',views.cecinasHornosAhumadores,name='hornos_ahumadores_cecinas'),
    url(r'^pasillo_ingreso_cecinas/$',views.cecinasPasilloIngreso,name='pasillo_ingreso_cecinas'),
    url(r'^exteriores_cecinas/$',views.cecinasExteriores,name='exteriores_cecinas'),
    url(r'^sala_maquinas_cecinas/$',views.cecinasSalaMaquinas,name='sala_maquinas_cecinas'),
    url(r'^pasillo_embutidoras_cecinas/$',views.cecinasPasilloEmbutidoras,name='pasillo_embutidoras_cecinas'),
    url(r'^casino_cecinas/$',views.EdificioServicioUnoCasinoCecinas,name='casino_cecinas'),
    url(r'^sala_cambio_cecinas/$',views.EdificioServicioUnoSalaCambioCecinas,name='sala_cambio_cecinas'),
    url(r'^bano_varones_4/$',views.EdificioServicioUnoBanoVaronesCuatro,name='bano_varones_4'),
    url(r'^bano_varones_3/$',views.EdificioServicioUnoBanoVaronesTres,name='bano_varones_3'),
    url(r'^bano_varones_2/$',views.EdificioServicioUnoBanoVaronesDos,name='bano_varones_2'),
    url(r'^bano_varones_1/$',views.EdificioServicioUnoBanoVaronesUno,name='bano_varones_1'),
    url(r'^bano_damas_1/$',views.EdificioServicioUnoBanoDamasUno,name='bano_damas_1'),
    url(r'^pasillo_servicio_cecinas/$',views.EdificioServicioPasilloCecinas,name='pasillo_servicio_cecinas'),
    url(r'^pasillo_servicio_faena/$',views.EdificioServicioPasilloFaena,name='pasillo_servicio_faena'),
    url(r'^pasillo_servicio/$',views.EdificioServicioPasillo,name='pasillo_servicio'),
    url(r'^casino_faena/$',views.EdificioServicioCasinoFaena,name='casino_faena'),
    url(r'^entrada_casino_faena/$',views.EdificioServicioEntradaCasinoFaena,name='entrada_casino_faena'),
    url(r'^zona_descanso_faena/$',views.EdificioServicioZonaDescansoFaena,name='zona_descanso_faena'),
    url(r'^bano_casino_faena/$',views.EdificioServicioBanoCasinoFaena,name='bano_casino_faena'),
    url(r'^duchas_casino_faena/$',views.EdificioServicioDuchasCasinoFaena,name='duchas_casino_faena'),
    url(r'^oficinas_casino_faena/$',views.EdificioServicioOficinasCasinoFaena,name='oficinas_casino_faena'),
    url(r'^zona_descanso_cecinas/$',views.EdificioServicioZonaDescansoCecinas,name='zona_descanso_cecinas'),
    url(r'^bano_damas_3/$',views.EdificioServicioSpBanoDamasTres,name='bano_damas_3'),
    url(r'^bano_damas_2/$',views.EdificioServicioSpBanoDamasDos,name='bano_damas_2'),
    url(r'^bano_visitas_2/$',views.EdificioServicioSpBanoVisitasDos,name='bano_visitas_2'),
    url(r'^bano_visitas/$',views.EdificioServicioSpBanoVisitas,name='bano_visitas'),
    url(r'^sala_cambio_faena/$',views.EdificioServicioSpSalaCambio,name='sala_cambio_faena'),
    url(r'^pasillo_servicio_nivel2/$',views.EdificioServicioSpPasillo,name='pasillo_servicio_nivel2'),
    url(r'^pasillo2_servicio_nivel2/$',views.EdificioServicioSpPasilloDos,name='pasillo2_servicio_nivel2'),
    url(r'^bano_damas_4/$',views.EdificioServicioSpBanoDamasCuatro,name='bano_damas_4'),
    url(r'^descolgado_faenadora/$',views.FaenadoraDescolgado,name='descolgado_faenadora'),
    url(r'^matanza_faenadora/$',views.FaenadoraMatanza,name='matanza_faenadora'),
    url(r'^eviscerado_faenadora/$',views.FaenadoraEviscerado,name='eviscerado_faenadora'),
    url(r'^oficinas_matanza/$',views.FaenadoraOficinasMantanza,name='oficinas_matanza'),
    url(r'^mantencion_faenadora/$',views.FaenadoraMantencion,name='mantencion_faenadora'),
    url(r'^oficinas_faenadora/$',views.FaenadoraOficinas,name='oficinas_faenadora'),
    url(r'^filtro_sanitario_faenadora/$',views.FaenadoraFiltroSanitario,name='filtro_sanitario_faenadora'),
    url(r'^camara_traspaso_faenadora/$',views.FaenadoraCamaraTraspaso,name='camara_traspaso_faenadora'),
    url(r'^transferencia_faenadora/$',views.FaenadoraSalaTransferencia,name='transferencia_faenadora'),
    url(r'^lavado_ganchos_faenadora/$',views.FaenadoraLavadoGanchos,name='lavado_ganchos_faenadora'),
    url(r'^camara430_faenadora/$',views.FaenadoraCamara430,name='camara430_faenadora'),
    url(r'^camara440_faenadora/$',views.FaenadoraCamara440,name='camara440_faenadora'),
    url(r'^camara420_faenadora/$',views.FaenadoraCamara420,name='camara420_faenadora'),
    url(r'^duchas_enfriado_faenadora/$',views.FaenadoraDuchasEnfriado,name='duchas_enfriado_faenadora'),
    url(r'^pasarela_faenadora/$',views.FaenadoraPasarela,name='pasarela_faenadora'),
    url(r'^pasillo_faenadora/$',views.FaenadoraPasillo,name='pasillo_faenadora'),
    url(r'^banos_trozado/$',views.TrozadoBanos,name='banos_trozado'),
    url(r'^mantencion_trozado/$',views.TrozadoMantencion,name='mantencion_trozado'),
    url(r'^sala_electrica_trozado/$',views.TrozadoSalaElectrica,name='sala_electrica_trozado'),
    url(r'^sala_lavado_trozado/$',views.TrozadoSalaLavado,name='sala_lavado_trozado'),
    url(r'^pasillo_trozado/$',views.TrozadoPasillo,name='pasillo_trozado'),
    url(r'^sala_reuniones_trozado/$',views.TrozadoSalaReuniones,name='sala_reuniones_trozado'),
    url(r'^sala1_procesos/$',views.ProcesosSalaUno,name='sala1_procesos'),
    url(r'^sala2_procesos/$',views.ProcesosSalaDos,name='sala2_procesos'),
    url(r'^sala3_procesos/$',views.ProcesosSalaTres,name='sala3_procesos'),
    url(r'^sala4_procesos/$',views.ProcesosSalaCuatro,name='sala4_procesos'),
    url(r'^sala5_procesos/$',views.ProcesosSalaCinco,name='sala5_procesos'),
    url(r'^sala6_procesos/$',views.ProcesosSalaSeis,name='sala6_procesos'),
    url(r'^sala7_procesos/$',views.ProcesosSalaSiete,name='sala7_procesos'),
    url(r'^sala8_procesos/$',views.ProcesosSalaOcho,name='sala8_procesos'),
    url(r'^sala9_procesos/$',views.ProcesosSalaNueve,name='sala9_procesos'),
    url(r'^mantencion_procesos/$',views.ProcesosMantencion,name='mantencion_procesos'),
    url(r'^fabrica_hielo_procesos/$',views.ProcesosFabricaHielo,name='fabrica_hielo_procesos'),
    url(r'^pallet_RRHH_procesos/$',views.ProcesosPalletRrhh,name='pallet_RRHH_procesos'),
    url(r'^pasillo_procesos/$',views.ProcesosPasillo,name='pasillo_procesos'),
    url(r'^marinado_procesos/$',views.ProcesosMarinado,name='marinado_procesos'),
    url(r'^sala_procesos/$',views.ProcesosSala,name='sala_procesos'),
    url(r'^sala_trozado/$',views.TrozadoSala,name='sala_trozado'),
    url(r'^camara_pulmon_empaque/$',views.EmpaqueCamaraPulmon,name='camara_pulmon_empaque'),
    url(r'^congelado2_calle1_despacho/$',views.DespachoCalleUno,name='congelado2_calle1_despacho'),
    url(r'^congelado2_calle2_despacho/$',views.DespachoCalleDos,name='congelado2_calle2_despacho'),
    url(r'^congelado3_despacho/$',views.DespachoCongeladoTres,name='congelado3_despacho'),
    url(r'^camara_pallet_despacho/$',views.DespachoCamaraPallet,name='camara_pallet_despacho'),
    url(r'^taller_gruas_cargador_despacho/$',views.DespachoTallerGruas,name='taller_gruas_cargador_despacho'),
    url(r'^pasillo_despacho/$',views.DespachoPasillo,name='pasillo_despacho'),
    url(r'^sala_despacho/$',views.DespachoSala,name='sala_despacho'),
    url(r'^informatica/$',views.DespachoInformatica,name='informatica'),
    url(r'^pasillo_cartonFreezer/$',views.CartonFreezerPasillo,name='pasillo_cartonFreezer'),
    url(r'^sala_electrica_cartonFreezer/$',views.CartonFreezerSalaElectrica,name='sala_electrica_cartonFreezer'),
    url(r'^armado_cajas/$',views.CartonFreezerArmadoCaja,name='armado_cajas'),
    url(r'^armado_cajas_segundo_nivel/$',views.CartonFreezerArmadoCajaDos,name='armado_cajas_segundo_nivel'),
    url(r'^sala_empaque/$',views.EmpaqueSala,name='sala_empaque'),
    url(r'^oficinas_empaque/$',views.EmpaqueOficinas,name='oficinas_empaque'),
    url(r'^cartonFreezer/$',views.CartonFreezer,name='cartonFreezer'),
    url(r'^materias_primas_cecinas2/$',views.CecinasDosMateriasPrimas,name='materias_primas_cecinas2'),
    url(r'^pasillo_cecinas2/$',views.CecinasDosPasillo,name='pasillo_cecinas2'),
    url(r'^preparacion_masas_cecinas2/$',views.CecinasDosPreparacionMasas,name='preparacion_masas_cecinas2'),
    url(r'^espera_hornos_cecinas2/$',views.CecinasDosEsperaHornos,name='espera_hornos_cecinas2'),
    url(r'^sala_cocidos_cecinas2/$',views.CecinasDosSalaCocidos,name='sala_cocidos_cecinas2'),
    url(r'^sala_crudos_cecinas2/$',views.CecinasDosSalaCrudos,name='sala_crudos_cecinas2'),
    url(r'^sala_enfriado_cecinas2/$',views.CecinasDosSalaEnfriado,name='sala_enfriado_cecinas2'),
    url(r'^sala_hornos_cecinas2/$',views.CecinasDosSalaHornos,name='sala_hornos_cecinas2'),
    url(r'^sala_empaque_cecinas2/$',views.CecinasDosSalaEmpaque,name='sala_empaque_cecinas2'),
    url(r'^ingenieria_edificioIngenieria/$',views.EdificioIngenieriaIngenieria,name='ingenieria_edificioIngenieria'),
    url(r'^pasillo_edificioIngenieria/$',views.EdificioIngenieriaPasillo,name='pasillo_edificioIngenieria'),
    url(r'^sala_maq_edificioIngenieria/$',views.EdificioIngenieriaSalaMaq,name='sala_maq_edificioIngenieria'),
    url(r'^oficinas_calidad_admin/$',views.EdificioAdministracionOficinasCalidad,name='oficinas_calidad_admin'),
    url(r'^pasillo_admin/$',views.EdificioAdministracionPasillo,name='pasillo_admin'),
    url(r'^enfermeria_admin/$',views.EdificioAdministracionEnfermeria,name='enfermeria_admin'),
    url(r'^edificio_administracion/$',views.EdificioAdministracion,name='edificio_administracion'),
    url(r'^laboratorio_calidad/$',views.EdificioAdministracionLaboratorio,name='laboratorio_calidad'),
    url(r'^oficinas_ingreso/$',views.EdificioAdministracionOficinasIngreso,name='oficinas_ingreso'),
    url(r'^lavado_rectificado/$',views.EdificioAdministracionLavado,name='lavado_rectificado'),
    url(r'^cecinas_entretecho/$',views.EntretechoCecinas,name='cecinas_entretecho'),
    url(r'^oficinas_maquina_uno/$',views.MaquinasUnoOficinas,name='oficinas_maquina_uno'),
    url(r'^sala_maquina_uno/$',views.MaquinasUnoSala,name='sala_maquina_uno'),
    url(r'^sala_electrica_maquina_cinco/$',views.MaquinasCincoSalaElectrica,name='sala_electrica_maquina_cinco'),
    url(r'^compresores_sala_maquina_cinco/$',views.MaquinasCincoCompresores,name='compresores_sala_maquina_cinco'),
    url(r'^faena_dos_entretecho/$',views.EntretechoFaenaDos,name='faena_dos_entretecho'),
    url(r'^faena_uno_entretecho/$',views.EntretechoFaenaUno,name='faena_uno_entretecho'),
    url(r'^faena_entretecho/$',views.EntretechoFaena,name='faena_entretecho'),
    url(r'^oficinas_subproductos/$',views.SubproductosOficinas,name='oficinas_subproductos'),
    url(r'^generador_subproductos/$',views.SubproductosGenerador,name='generador_subproductos'),
    url(r'^visceras_plumas_subproductos/$',views.SubproductosViscerasPlumas,name='visceras_plumas_subproductos'),
    url(r'^ingreso_visceras_plumas/$',views.SubproductosIngresoViscerasPlumas,name='ingreso_visceras_plumas'),
    url(r'^sala_caldera_subproductos/$',views.SubproductosSalaCaldera,name='sala_caldera_subproductos'),
    url(r'^bodega_subproductos/$',views.SubproductosBodega,name='bodega_subproductos'),
    url(r'^bodega_dos_subproductos/$',views.SubproductosBodegaDos,name='bodega_dos_subproductos'),
    url(r'^sala_electrica_1_subproductos/$',views.SubproductosSalaElectrica,name='sala_electrica_1_subproductos'),
    url(r'^sala_electrica_2_subproductos/$',views.SubproductosSalaElectricaDos,name='sala_electrica_2_subproductos'),
    url(r'^biomasa/$',views.TratamientoBiomasa,name='biomasa'),
    url(r'^estanques_riles/$',views.TratamientoEstanquesRiles,name='estanques_riles'),
    url(r'^oficinas_duchas_riles/$',views.TratamientoOficinasRiles,name='oficinas_duchas_riles'),
    url(r'^decanter_primer_nivel/$',views.TratamientoDecanterUnoRiles,name='decanter_primer_nivel'),
    url(r'^decanter_segundo_nivel/$',views.TratamientoDecanterDosRiles,name='decanter_segundo_nivel'),
    url(r'^sala_electrica_biologica/$',views.TratamientoSalaElectricaBiologica,name='sala_electrica_biologica'),
    url(r'^pasarela/$',views.SubproductosPasarela,name='pasarela'),
    url(r'^biologica/$',views.TratamientoExteriorBiologica,name='biologica'),
    url(r'^gerencia_rrhh/$',views.ExterioresGerencia,name='gerencia_rrhh'),
    url(r'^ingreso_peatonal/$',views.ExterioresIngresoPeatonal,name='ingreso_peatonal'),
    url(r'^faena_exteriores/$',views.ExterioresFaena,name='faena_exteriores'),
    url(r'^cecinas_exteriores/$',views.ExterioresCecinas,name='cecinas_exteriores'),
    url(r'^ingreso_vehicular/$',views.ExterioresIngresoVehicular,name='ingreso_vehicular'),
    url(r'^bodega_uno_exteriores/$',views.ExterioresBodegaUno,name='bodega_uno_exteriores'),
    url(r'^bodega_dos_exteriores/$',views.ExterioresBodegaDos,name='bodega_dos_exteriores'),
    url(r'^bodega_tres_exteriores/$',views.ExterioresBodegaTres,name='bodega_tres_exteriores'),
    url(r'^subproductos_exteriores/$',views.ExterioresSubproductos,name='subproductos_exteriores'),
    url(r'^busqueda/(?P<area>[^/]+)/$', views.busqueda, name='busquedaProyecto'),
    url(r'^reportando/(?P<equipo_id>\w{2}\d{1,3})/$', views.reportes, name='reportando'),
    url(r'^informacion/(?P<equipo_id>\w{2}\d{1,3})/$', views.informacion, name='informando'),
    url(r'^$', login),
    url(r'^aprobar/(?P<equipo_id>\w{2}\d{1,3})/(?P<area>[^/]+)/(?P<mant_id>[^/]+)/$', views.aprobar, name='aprobar'),
    url(r'^verSolicitud/(?P<equipo_id>\w{2}\d{1,3})/(?P<area>[^/]+)/$', views.solicitudCreada, name='verSolicitud'),
    url(r'^correoApro/$', views.correoApro, name='correoApro'),
    url(r'^verSolicitudOt/(?P<id>[^/]+)/$', views.buscarSolicitud, name='verSolicitudOt'),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT,
    }),
    ]
