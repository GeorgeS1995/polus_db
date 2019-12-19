from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import *
from django.views import generic
from django.views import View
from .forms import TypeProductAdd, CharAddFormset, OperationProductAddForm, OperationAssembly
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import uuid
import base64
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


# Create your views here.


def index(request):
    operations = Product_2_characteristic.objects.select_related(
        'product_id', 'product_id__type_of_product_id', 'characteristic_of_product_id', 'operation_history_id',
        'operation_history_id__type_of_operation_id', 'operation_history_id__type_of_defect_id') \
        .distinct('product_id', 'operation_history_id').order_by('-operation_history_id')
    return render(request, 'index.html', context={'operations': operations})

@login_required
def search(request):
    return render(request, 'searching_page.html')


class ESearchView(LoginRequiredMixin, View):
    template_name = 'searching_result.html'

    def get(self, request, *args, **kwargs):
        question = request.GET.get('q')
        if question is not None:
            search_model = Product.objects.select_related('type_of_product_id__department_id').\
                filter(serial_number__contains=question, type_of_product_id__department_id_id=request.department.id).order_by('id')
            paginator = Paginator(search_model, 25)  # Show N objects per page

            page = request.GET.get('page')
            try:
                pages = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                pages = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                pages = paginator.page(paginator.num_pages)
            return render(request, self.template_name, {'product_lists': pages})


class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, generic.DetailView):
    model = Product

    def dictfetchall(self, cursor):
        "Returns all rows from a cursor as a dict"
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

    # Проверяем если доступ у пользака к странице
    def has_permission(self, **kwargs):
        return self.model.objects.select_related().get(id=self.kwargs['pk']).type_of_product_id.department_id_id == self.request.department.id

    def handle_no_permission(self):
        product = self.model.objects.get(id=self.kwargs['pk'])
        return render(self.request, 'mainapp/product_detail.html', {'product': product})

    def get_context_data(self, **kwargs):
        cursor = connection.cursor()
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        # Опыт пиви подсказывает что можно подгружать искуственно добавленные таблицы в orm, исправить
        cursor.execute('select mainapp_product.id, mainapp_product.serial_number, mainapp_type_of_product.model from "mainapp_product_Assembly"'
                       ' join mainapp_product on "mainapp_product_Assembly".to_product_id = mainapp_product.id'
                       ' join mainapp_type_of_product on "mainapp_product".type_of_product_id_id = mainapp_type_of_product.id'
                       ' where "mainapp_product_Assembly".from_product_id = {};'.format(context['product'].pk))
        context['consist'] = self.dictfetchall(cursor)
        cursor.execute('select distinct mainapp_product.id, mainapp_product.serial_number, '
                       'mainapp_type_of_product.model, mainapp_type_of_operation."label", '
                       'mainapp_operation_history.start_date from "mainapp_product_Assembly" join mainapp_product on '
                       '"mainapp_product_Assembly".from_product_id = mainapp_product.id join mainapp_type_of_product '
                       'on "mainapp_product".type_of_product_id_id = mainapp_type_of_product.id join '
                       'mainapp_product_2_characteristic on mainapp_product.id = '
                       'mainapp_product_2_characteristic.product_id_id join mainapp_operation_history on '
                       'mainapp_product_2_characteristic.operation_history_id_id = mainapp_operation_history.id join '
                       'mainapp_type_of_operation on mainapp_operation_history.type_of_operation_id_id = '
                       'mainapp_type_of_operation.id join mainapp_type_of_operation_groups on '
                       'mainapp_type_of_operation_groups.id = '
                       'mainapp_type_of_operation.type_of_operation_groups_id_id where '
                       '"mainapp_product_Assembly".to_product_id = {} and (mainapp_type_of_operation_groups."label" = '
                       '\'Операции разборки\' or mainapp_type_of_operation_groups."label" = \'Сборочные '
                       'операции\') order by mainapp_operation_history.start_date;'.format(context['product'].pk))
        temp_context = self.dictfetchall(cursor)
        # Что б изделие не входило в состав самого себя
        for param_dict in temp_context:
            if param_dict["id"] == context['product'].pk:
                temp_context.remove(param_dict)
        context['in_composition'] = temp_context
        context['operations'] = Product_2_characteristic.objects.select_related('characteristic_of_product_id',
                                                                                'operation_history_id',
                                                                                'operation_history_id__type_of_operation_id',
                                                                                'operation_history_id__type_of_defect_id').filter(
            product_id__exact=context['product'].pk) \
            .distinct('operation_history_id').order_by('-operation_history_id')
        return context

@login_required
def product_2_chardetailview(request, pk):
    characteristics = Product_2_characteristic.objects.select_related(
        'characteristic_of_product_id', ).filter(operation_history_id__exact=pk)
    return render(request, 'mainapp/product_2_characteristic_detail.html', {'characteristics': characteristics, 'pk': pk})

@login_required
def type_product_add_form(request):
    if request.method == "GET":
        form = TypeProductAdd()
        formset = CharAddFormset()
    elif request.method == 'POST':
        form = TypeProductAdd(request.POST)
        formset = CharAddFormset(request.POST)
        if form.is_valid() and formset.is_valid():
            add_type = Type_of_product.objects.create(model=form.cleaned_data['label'],
                                                      department_id_id=request.department.id)
                                                      # department_id_id=form.cleaned_data['department'].id)
            add_type.save()
            new_type_id = add_type.id
            for form in formset:
                add_char = Characteristic_of_product.objects.create(label=form.cleaned_data['label'],
                                                                    type_of_product_id_id=new_type_id,
                                                                    units=form.cleaned_data['units'],
                                                                    description=form.cleaned_data['description'])
                add_char.save()
            return redirect(type_product_add_form)
    return render(request, 'type_product_add_from.html', {'form': form, 'formset': formset})

@login_required
def operation_menu(request):
    return render(request, 'operation_menu.html')

@login_required
def operation_assembly_form(request, quantity_of_fields):
    if request.method == "GET":
        form = OperationAssembly(quantity_of_fileds=quantity_of_fields, current_department_id=request.department.id,
                                 current_user_id=Employess.objects.get(user_id=request.user.id))
    elif request.method == "POST":
        form = OperationAssembly(request.POST, quantity_of_fileds=quantity_of_fields, current_department_id=request.department.id,
                                 current_user_id=Employess.objects.get(user_id=request.user.id))
        if form.is_valid():
            form.save()
    return render(request, 'operation_assembly_form.html', {'form': form, 'quantity_of_fields': quantity_of_fields})

@login_required
def operation_assembly_main(request):
    # выбираем тип детали по умолчанию при вызове ажакс кусочка
    default_product = Type_of_product.objects.filter(department_id_id=request.department.id)
    try:
        default_product[0]
        return render(request, 'operation_assembly_main.html', {'default_product': default_product[0].id})
    except IndexError:
        return render(request, 'operation_assembly_main.html', {'default_product': 0})

@login_required
def operation_add_main(request):
    # выбираем тип детали по умолчанию при вызове ажакс кусочка
    default_product = Type_of_product.objects.filter(department_id_id=request.department.id)
    try:
        default_product[0]
        return render(request, 'operation_add_main.html', {'default_product': default_product[0].id})
    except IndexError:
        return render(request, 'operation_add_main.html', {'default_product': 0})

@login_required
def operation_add_form(request, type_of_product):
    # Функция и страница с js работаю, но дико срут в консоль по пока неустанлвенной причине
    char_queryset = Characteristic_of_product.objects.filter(type_of_product_id_id__id=type_of_product)
    current_type = Type_of_product.objects.get(id=type_of_product)
    if request.method == 'GET':
        form = OperationProductAddForm(list_of_char=char_queryset, chose_type=current_type, current_department_id=request.department.id,
                                       current_user_id=Employess.objects.get(user_id=request.user.id))
    elif request.method == 'POST':
        form = OperationProductAddForm(request.POST, list_of_char=char_queryset, chose_type=current_type,
            current_department_id=request.department.id, current_user_id=Employess.objects.get(user_id=request.user.id))
        if form.is_valid():
            form.save()
    return render(request, 'operation_add_form.html', {'form': form, 'current_type': current_type.id})
