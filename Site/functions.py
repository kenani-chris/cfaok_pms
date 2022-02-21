from .models import *


def get_staff_account(company, user):
    return Staff.objects.filter(
        staff_company=company,
        staff_person=user,
        staff_active=True
    ).first()


def get_company(companyId):
    return Company.objects.filter(
        company_id=companyId,
        company_status=True
    ).first()



