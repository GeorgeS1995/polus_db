from django import forms
from .models import *
from django.forms.models import *
from django.db.models import Max
from django.db import connection
from django.forms import formset_factory
from django.utils.timezone import now
import uuid
import base64
import itertools
from django.db.models import Q


class ModelChoiceField_Label(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


# Я не бууд так топорен, переделать
class ModelChoiceField_Label2(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.model


# Ну сделай нормальный класс ну позязя ну или в БД надо все было идентично называть
class ModelChoiceField_Label3(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.label


class SearchingFrom(forms.Form):
    pass


class TypeProductAdd(forms.Form):
    label = forms.CharField(label="Название модели")
    # метод переопределен в Lib\site-packages\django\forms что выдавать и ID и список и поименам записи
    # department = ModelChoiceField_Label(queryset=Department.objects.all(),
    #                                     empty_label=None, label="Производящий участок")


class CharacteristicAdd(forms.Form):
    label = forms.CharField(label="Название характеристики")
    units = forms.CharField(label="Единицы измерения", required=False)
    description = forms.CharField(label="Описание", required=False)


CharAddFormset = formset_factory(CharacteristicAdd, extra=1)


# Хитрая форма с динамическим набором полей
class OperationProductAddForm(forms.Form):
    def __init__(self, *args, **kwargs):
        chosen_type = kwargs.pop('chose_type')
        self.list_of_char = kwargs.pop('list_of_char')
        self.current_user_id = kwargs.pop('current_user_id')
        self.current_department_id = kwargs.pop('current_department_id')
        # fields = ["fields1", "fields2", "fields3"]
        super(OperationProductAddForm, self).__init__(*args, **kwargs)
        self.fields['serial_number'] = forms.CharField(label="Серийный номер")
        self.fields['type_of_product'] = ModelChoiceField_Label2(queryset=Type_of_product.objects.
                                                                 filter(department_id_id=self.current_department_id),
                                                                 empty_label=None, label="Тип изделия",
                                                                 initial=chosen_type)
        self.fields['type_of_operation'] = ModelChoiceField_Label3(queryset=Type_of_operation.objects.
                                                                   filter(department_id_id=self.current_department_id).
                                                                   exclude(type_of_operation_groups_id_id__label="Сборочные операции"),
                                                                   empty_label=None, label="Операция")
        self.fields['type_of_defect'] = forms.CharField(initial="Годная", label='Причина отбраковки', required=False)
        self.fields['start_date'] = forms.DateTimeField(initial=now, label='Дата начала процесса')
        self.fields['end_date'] = forms.DateTimeField(initial=now, label='Дата окончания процесса')
        for field in self.list_of_char:
            self.fields[field.label] = forms.CharField()
        self.fields['type_of_product'].widget.attrs.update({'onchange': 'changeFormAfterSelect()'})

    # Проверяем если деталь в базе и не передана ли она с участка, в таком случае для детали дост
    def clean(self):
        super(OperationProductAddForm, self).clean()
        # Почему-то сам вызывать проверку на пустоту он не захотел пришлось так
        for field in self.fields:
            if self.cleaned_data.get(field) is None:
                return
        current_product = Product.objects.filter(serial_number=self.cleaned_data["serial_number"], type_of_product_id_id=self.cleaned_data['type_of_product'].id).order_by('-id').first()
        # Проверяем если деталь в базе и не передана ли она с участка, в таком случае для детали доступны только операции поступления
        if current_product is None and Type_of_operation_groups.objects.get(type_of_operation__label=self.cleaned_data["type_of_operation"].label).label != "Поступление на участок":
            msg = "Запись о детали {} еще на создана в БД, провидите сначала операцию входного контроля".format(self.cleaned_data['serial_number'])
            return self.add_error('serial_number', msg)
        elif current_product is None:
            return
        else:
            last_operation = Product_2_characteristic.objects.select_related().filter(Q(product_id__serial_number=self.cleaned_data["serial_number"]), Q(operation_history_id__type_of_operation_id__type_of_operation_groups_id__label="Поступление на участок") | Q(operation_history_id__type_of_operation_id__type_of_operation_groups_id__label="Передача на следующий участок") | Q(operation_history_id__type_of_operation_id__type_of_operation_groups_id__label="Сборочные операции") | Q(operation_history_id__type_of_operation_id__type_of_operation_groups_id__label="Операции разборки")).order_by('-operation_history_id').first()
            current_operation = Type_of_operation_groups.objects.get(type_of_operation__label=self.cleaned_data["type_of_operation"].label).label
            # Если деталь уже на участке и ее пытаются внести на участок снова
            if last_operation.operation_history_id.type_of_operation_id.type_of_operation_groups_id.label == "Поступление на участок" and current_operation == "Поступление на участок":
                msg = "Деталь {} уже проходила входной контроль на участке".format(self.cleaned_data['serial_number'])
                return self.add_error('serial_number', msg)
            # Если деталь не на участке и над ней пытаюстя првоести любую операцию кроме поступления
            if last_operation.operation_history_id.type_of_operation_id.type_of_operation_groups_id.label == "Передача на следующий участок" and current_operation != "Поступление на участок":
                msg = "Деталь {} не на участке, провидите сначала операцию входного контроля".format(self.cleaned_data['serial_number'])
                return self.add_error('serial_number', msg)
            if last_operation.operation_history_id.type_of_operation_id.type_of_operation_groups_id.label == "Сборочные операции" and current_operation == "Поступление на участок":
                msg = "Деталь {} собрана и уже находится на участке".format(self.cleaned_data['serial_number'])
                return self.add_error('serial_number', msg)
            if last_operation.operation_history_id.type_of_operation_id.type_of_operation_groups_id.label == "Операции разборки":
                msg = "Деталь {} разобрана, операции недоступны пока деталь не будет собрана".format(self.cleaned_data['serial_number'])
                return self.add_error('serial_number', msg)

    def clean_type_of_defect(self):
        data = self.cleaned_data['type_of_defect']
        if data == '':
            return Type_of_defect.objects.get(label="Годная").id
        else:
            return Type_of_defect.objects.get_or_create(label=data)[0].id

    def add_operation_2_char(self, operation, product):
        add_operation = Operation_history.objects.create(start_date=self.cleaned_data['start_date'],
                                                         end_date=self.cleaned_data['end_date'],
                                                         employess_id_id=self.current_user_id.id,
                                                         type_of_defect_id_id=self.cleaned_data['type_of_defect'],
                                                         type_of_operation_id_id=operation)
        add_operation.save()
        # Вообще наверное надо перенести в отдельную функцию, но пока хотя б пусть работает.
        for char in self.list_of_char:
            add_char = Product_2_characteristic.objects.create(value=self.cleaned_data[char.label],
                                                               characteristic_of_product_id_id=char.id,
                                                               operation_history_id_id=add_operation.id,
                                                               product_id_id=product)
            add_char.save()

    def save(self):
        # global_operation_type определяю по id type_of_operation
        global_operation_type = self.cleaned_data['type_of_operation'].id
        try:
            Type_of_operation.objects.get(type_of_operation_groups_id_id__label="Поступление на участок", id=global_operation_type)
            add_product = Product.objects.create(serial_number=self.cleaned_data['serial_number'],
                                                 type_of_product_id_id=self.cleaned_data['type_of_product'].id)
            add_product.save()
            self.add_operation_2_char(global_operation_type, add_product.id)
        except Type_of_operation.DoesNotExist:
            product = Product.objects.filter(serial_number=self.cleaned_data['serial_number']).order_by('-id').first()
            self.add_operation_2_char(global_operation_type, product.id)


# Форма сборки, элементы сборки не фиксированы и предполагают правильное написание, при несовпадении в БД или
# отсутсвии на участке предполагается вылет валидатора
class OperationAssembly(forms.Form):
    def __init__(self, *args, **kwargs):
        quantity_of_fileds = kwargs.pop('quantity_of_fileds')
        self.current_user_id = kwargs.pop('current_user_id')
        self.current_department_id = kwargs.pop('current_department_id')
        super(OperationAssembly, self).__init__(*args, **kwargs)
        self.fields["start_date"] = forms.DateTimeField(initial=now, label='Дата сборки')
        self.fields['type_of_defect'] = forms.CharField(initial="Годная", label='Причина отбраковки', required=False)
        self.fields['serial_number'] = forms.CharField(label="Серийный номер")
        self.fields['type_of_product'] = ModelChoiceField_Label2(queryset=Type_of_product.objects.
                                                                 filter(department_id_id=self.current_department_id),
                                                                 empty_label=None, label="Тип изделия")
        self.fields['type_of_operation'] = ModelChoiceField_Label3(queryset=Type_of_operation.objects.
                                                                   filter(department_id_id=self.current_department_id,
                                                                   type_of_operation_groups_id_id__label="Сборочные операции"),
                                                                   empty_label=None, label="Операция")
        for i in range(1, quantity_of_fileds + 1):
            self.fields["Component {}".format(i)] = forms.CharField(label="С/Н Компонента №{}".format(i))

    def clean_type_of_defect(self):
        data = self.cleaned_data['type_of_defect']
        if data == '':
            return Type_of_defect.objects.get(label="Годная").id
        else:
            return Type_of_defect.objects.get_or_create(label=data)[0].id

    # Перед операцией сборки всегда нужно провести операцию разборки
    def clean_serial_number(self):
        data = self.cleaned_data['serial_number']
        current_product = Product_2_characteristic.objects.select_related().filter(Q(product_id__serial_number=data), Q(operation_history_id__type_of_operation_id__type_of_operation_groups_id__label="Сборочные операции") | Q(operation_history_id__type_of_operation_id__type_of_operation_groups_id__label="Операции разборки")).order_by('-operation_history_id').first()
        if current_product is None:
            return data
        if current_product.operation_history_id.type_of_operation_id.type_of_operation_groups_id.label == "Сборочные операции":
            msg = "Изделие {} уже собрано, сначала необходимо провести операцию разборки".format(data)
            raise forms.ValidationError(msg)
        return data


    def clean(self):
        super(OperationAssembly, self).clean()
        # Почему-то сам вызывать проверку на пустоту он не захотел пришлось так
        for field in self.fields:
            if self.cleaned_data.get(field) is None:
                return
        # Сравниваю каждое поле с каждым на повторы
        for field1, field2 in itertools.combinations(self.fields, 2):
            if self.cleaned_data[field1] == self.cleaned_data[field2]:
                msg = "Поля формы не должны повторяться"
                self.add_error(field1, msg)

        # Проверяю свободен ли элемент
        for field in self.fields:
            if field.startswith("Component"):
                component = Product.objects.filter(serial_number=self.cleaned_data[field]).order_by('-id').first()
                # проверяем на наличие элемента в БД
                if component is None:
                    msg = "Изделие с серийным номером: {} не найдено в БД".format(self.cleaned_data[field])
                    self.add_error(field, msg)
                    return
                # если деталь не с нашего участка
                if component.type_of_product_id.department_id_id != self.current_department_id:
                    msg = "Изделие с серийным номером {} заведено в БД, но в данный момент числится на участке {}".format(self.cleaned_data[field], component.type_of_product_id.department_id.name)
                    self.add_error(field, msg)
                    return
                cursor = connection.cursor()
                # Если в выдаче этого запроса последняя операция разборка то значит деталь не находится в составе изделия
                cursor.execute('select distinct mainapp_operation_history.id, mainapp_type_of_operation_groups."label" '
                               'from mainapp_product join "mainapp_product_Assembly" on '
                               '"mainapp_product_Assembly".from_product_id = mainapp_product.id join '
                               'mainapp_product_2_characteristic on mainapp_product_2_characteristic.product_id_id = '
                               'mainapp_product.id join mainapp_operation_history on '
                               'mainapp_product_2_characteristic.operation_history_id_id = mainapp_operation_history.id '
                               'join mainapp_type_of_operation on mainapp_operation_history.type_of_operation_id_id = '
                               'mainapp_type_of_operation.id join mainapp_type_of_operation_groups on '
                               'mainapp_type_of_operation_groups.id = '
                               'mainapp_type_of_operation.type_of_operation_groups_id_id where ('
                               'mainapp_type_of_operation_groups."label" = \'Операции разборки\' or '
                               'mainapp_type_of_operation_groups."label" = \'Сборочные операции\') and '
                               '"mainapp_product_Assembly".to_product_id in (select id from mainapp_product where '
                               'serial_number = \'{}\') order by mainapp_operation_history.id desc limit 1;'.format(
                    self.cleaned_data[field]))
                # На случай пустого массива(то есть еще не существующей операции сборки
                try:
                    if cursor.fetchall()[0][1] == "Сборочные операции":
                        cursor.execute('select mainapp_product.serial_number, "mainapp_product_Assembly".id from '
                                       'mainapp_product join "mainapp_product_Assembly" on '
                                       '"mainapp_product_Assembly".from_product_id = mainapp_product.id where '
                                       '"mainapp_product_Assembly".to_product_id in (select id from mainapp_product where '
                                       'serial_number = \'{}\') order by "mainapp_product_Assembly".id desc limit '
                                       '1;'.format(self.cleaned_data[field]))
                        in_compositoin = cursor.fetchall()[0][0]
                        msg = "Изделие в составе {}. Проведите сперва операцию разборки".format(in_compositoin)
                        self.add_error(field, msg)
                except IndexError:
                    pass

    def list_of_assembly(self):
        list_components = []
        for k in self.fields:
            if k.startswith("Component"):
                list_components.append(self.cleaned_data[k])
        # Получаем словарь с списком последних id из внесенных деталей
        temp_query = Product.objects.filter(serial_number__in=list_components).values('serial_number').annotate(max_id=Max('id'))
        return temp_query

    def save(self):
        add_product = Product.objects.create(serial_number=self.cleaned_data['serial_number'],
                                             type_of_product_id_id=self.cleaned_data['type_of_product'].id)
        add_product.save()
        new_product_id = add_product.id
        list_of_assembly = self.list_of_assembly()
        for i in list_of_assembly:
            connection.cursor().execute('insert into "mainapp_product_Assembly" (from_product_id, to_product_id)'
                                        ' values ({},{});'.format(new_product_id, i["max_id"]))
        add_operation = Operation_history.objects.create(start_date=self.cleaned_data['start_date'],
                                                         end_date=self.cleaned_data['start_date'],
                                                         employess_id_id=self.current_user_id.id,
                                                         type_of_defect_id_id=self.cleaned_data['type_of_defect'],
                                                         type_of_operation_id_id=self.cleaned_data['type_of_operation'].id)
        add_operation.save()
        list_of_char = Characteristic_of_product.objects.filter(type_of_product_id_id=self.cleaned_data['type_of_product'].id)
        for char in list_of_char:
            add_char = Product_2_characteristic.objects.create(value="NULL",
                                                               characteristic_of_product_id_id=char.id,
                                                               operation_history_id_id=add_operation.id,
                                                               product_id_id=add_product.id)
            add_char.save()
