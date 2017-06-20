import datetime

from django import forms

class FormularioCerrarSolicitud(forms.Form):
    realizador = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Nombre del trabajador",
                                                               "aria-describedby":"sizing-addon1"}),max_length=30,required=True)
    accion = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","rows":"6","placeholder":"Trabajo realizado (mín 4 palabras)"}),required=True)
    fechac = forms.DateField(widget =forms.TextInput(attrs={"class":"form-control","id":"datepicker"}))
    imagenc = forms.ImageField(widget=forms.FileInput(attrs={"class":"btn btn-primary"}),required=True )
    def clean_fechac(self):
          fechac = self.cleaned_data['fechac']
          if fechac > datetime.date.today():
             fechac = forms.DateField(widget=forms.SelectDateWidget(), initial=datetime.date.today())
             raise forms.ValidationError("Porfavor ingresa una fecha correcta")
          return fechac
    def clean_accion(self):
        accion = self.cleaned_data['accion']
        num_palabras = len(accion.split())
        if num_palabras < 4:
            raise forms.ValidationError("Se requieren como minimo 4 palabras!!")
        return accion


class FormularioSolicitud(forms.Form):
    solicitante = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Solicitante",
                                                                "aria-describedby":"sizing-addon1"}),max_length=30,required=True)
    causa = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","rows":"6","placeholder":"Causa (mín 4 palabras)"}),required=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control", "placeholder":"tu_correo@sopraval.cl",
                                                                "aria-describedby":"sizing-addon1"}),max_length=30,required=True)
    nOt = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","aria-describedby":"sizing-addon1"}),initial=0,required=False)
    imagen = forms.ImageField(widget=forms.FileInput(attrs={"class":"btn btn-primary"}),required=False )
    def clean_causa(self):
        causa = self.cleaned_data['causa']
        num_palabras = len(causa.split())
        if num_palabras < 4:
            raise forms.ValidationError("Se requieren como minimo 4 palabras!!")
        return causa
    def clean_nOt(self):
        nOt = self.cleaned_data['nOt']
        if nOt == None:
            nOt = 0
            return nOt
        elif((nOt < 1000) & (nOt > 0)):
            raise forms.ValidationError("Porfavor ingresa una OT correcta")
            return nOt
        return nOt



class FormularioAprobar(forms.Form):
    nada = forms.TypedChoiceField(coerce=lambda x: x == 'True', choices=((True, 'Aprobar'),(False, 'Rechazar')),widget=forms.RadioSelect, required=True)
    Ots= forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","aria-describedby":"sizing-addon1","value":100}) ,required=True)
    comentario = forms.CharField(widget=forms.Textarea(
        attrs={"class": "form-control", "rows": "6", "placeholder": "Comentarios sobre la mantención (mín 2 palabras)"}),
                             required=False)
    def clean_Ots(self):
        Ots = self.cleaned_data['Ots']
        nada = self.cleaned_data['nada']
        if (nada & (Ots < 1000)):
            raise forms.ValidationError("Porfavor ingresa una OT correcta")
        return Ots
    def clean_comentario(self):
        comentario = self.cleaned_data['comentario']
        num_palabras = len(comentario.split())
        print(comentario)
        if comentario == "":
            comentario = 'Sin comentarios'
        else:
            if num_palabras < 2:
                raise forms.ValidationError("Se requieren como minimo 2 palabras!!")
        return comentario
