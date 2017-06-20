
    function saludo(nombre){
        var equipo = nombre;

        var urlr = '/'+equipo+'/';
        document.location = urlr;
    }

    function chaner(eqr){
        var equipo = eqr;

        var urlr = document.location+'solicitud/'+equipo;
        document.location = urlr;

     }
     function changex(eq){
        var e = eq;

        var url = document.location+'solicitud/'+e;
        document.location = url;

     }
    function changer(ex){
        var e = ex;


        var url = '/reporteando/'+e;
        document.location = url;

    }


