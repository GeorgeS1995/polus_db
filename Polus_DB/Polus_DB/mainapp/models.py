from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Employess(models.Model):
    # внешний ключ на весь став который джанго держит с юзером, в теории у меня тут получается связь много-много
    # следовательно можно даже куралесить давая пользователю несколько рангов
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    rang_id = models.ForeignKey('Rang', on_delete=models.DO_NOTHING)


class Rang(models.Model):
    label = models.CharField(max_length=255)
    department_id = models.ForeignKey('Department', on_delete=models.DO_NOTHING)


class Department(models.Model):
    name = models.CharField(max_length=255)


class Characteristic_of_product(models.Model):
    label = models.CharField(max_length=255)
    type_of_product_id = models.ForeignKey('Type_of_product', on_delete=models.DO_NOTHING)
    units = models.CharField(max_length=255)
    description = models.TextField()


class Type_of_product(models.Model):
    model = models.CharField(max_length=255)
    department_id = models.ForeignKey('Department', on_delete=models.DO_NOTHING)


class Product_2_characteristic(models.Model):
    product_id = models.ForeignKey('Product',on_delete=models.DO_NOTHING)
    characteristic_of_product_id = models.ForeignKey('Characteristic_of_product', on_delete=models.DO_NOTHING)
    operation_history_id = models.ForeignKey('Operation_history', on_delete=models.DO_NOTHING)
    value = models.CharField(max_length=255)

    def get_absolute_url(self):
        # Беру по полю оперейшин_хистори для удобства
        return reverse('product_2_characteristic-detail', args=[str(self.operation_history_id_id)])


class Product(models.Model):
    serial_number = models.CharField(max_length=255)
    type_of_product_id = models.ForeignKey('Type_of_product', on_delete=models.DO_NOTHING)
    Assembly = models.ManyToManyField('Product')

    def get_absolute_url(self):
        return reverse('product-detail', args=[str(self.id)])


class Operation_history(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    type_of_operation_id = models.ForeignKey('Type_of_operation', on_delete=models.DO_NOTHING)
    type_of_defect_id = models.ForeignKey('Type_of_defect', on_delete=models.DO_NOTHING)
    employess_id = models.ForeignKey('Employess', on_delete=models.DO_NOTHING)


#class Assembly(models.Model):
 #   product_id = models.ForeignKey('Product', on_delete=models.DO_NOTHING)
  #  in_composition = models.ForeignKey('Product', on_delete=models.DO_NOTHING)

class Type_of_operation(models.Model):
    label = models.CharField(max_length=255)
    type_of_operation_groups_id = models.ForeignKey('Type_of_operation_groups', on_delete=models.DO_NOTHING)
    department_id = models.ForeignKey('Department', on_delete=models.DO_NOTHING)

# Группировка деталей, что б разные участки могли по разному называть операции передачи, входного контроля и тд
class Type_of_operation_groups(models.Model):
    label = models.CharField(max_length=255)

class Type_of_defect(models.Model):
    label = models.CharField(max_length=255)

