from labs.models import Department, Laboratory
from substances.models import SubstanceName

Laboratory.objects.create(name='Lab 1').save()
Laboratory.objects.create(name='Lab 2').save()

Department.objects.create(name='Física').save()
Department.objects.create(name='Biologia').save()
Department.objects.create(name='Química').save()

SubstanceName.objects.create(name='Ácido Sulfúrico').save()
SubstanceName.objects.create(name='Ácido Nítrico').save()
SubstanceName.objects.create(name='Hidróxido de Magnésio').save()
SubstanceName.objects.create(name='Hidróxido de Alumínio').save()
SubstanceName.objects.create(name='Xilol').save()
SubstanceName.objects.create(name='Benzeno').save()