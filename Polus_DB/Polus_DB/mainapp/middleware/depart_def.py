from django.utils.deprecation import MiddlewareMixin
from ..models import *

class Depart_def(MiddlewareMixin):

    # Записываем id участка пользователя пользователя
    def process_request(self, request):
        if request.user.is_authenticated:
            request.department = Employess.objects.select_related('rang_id__department_id').\
                get(user_id=request.user.id).rang_id.department_id