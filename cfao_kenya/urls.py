from django.urls import path, re_path
from . import views
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('No_Active_Pms', NoActivePmsView.as_view(), name='ck_no_active_pms'),

    # Individual Kpi Links
    path('Individual-Kpi/', IndividualKpiView.as_view(), name='Individual_Kpi_Dashboard'),
    path('Individual-Kpi/Submit-Kpi/', SubmitKpiView.as_view(), name='Individual_Kpi_Submit'),
    path('Individual-Kpi/Track-Kpi/', TrackKpiView.as_view(), name='Individual_Kpi_Detail1'),
    path('Individual-Kpi/Track-Kpi/<uuid:pk>', DetailKpiView.as_view(), name='kpi-detail'),
    path('Individual-Kpi/Edit-Kpi/<uuid:pk>', views.EditKpiView.as_view(), name='Individual_Kpi-Edit_One'),
    path('Individual-Kpi/Kpi-Results/', KpiResultView.as_view(), name='Individual_Kpi_Result'),
    path('Individual-Kpi/Kpi-Results/<uuid:pk>', KpiResultUpdateView.as_view(), name='Individual_Kpi_Result_Update'),

    # Staff Kpi Links
    path('Staff-Kpi/', StaffKpiListView.as_view(), name='Staff_Kpi_Dashboard'),
    path('Staff-Kpi/Approve-Kpi', StaffKpiPendingListView.as_view(), name='Staff_Approve_Kpi'),
    path('Staff-Kpi/Approve-Kpi/<int:pk>', StaffKpiApproveView.as_view(), name='Staff_Approve_Kpi_Detail'),
    path('Staff-Kpi/Approve-Kpi/Approve/<int:pk>/<uuid:kpi_id>', views.approve_individual_kpi, name='Staff_Approve_Individual_Kpi'),
    path('Staff-Kpi/Approve-Kpi/Reject/<int:pk>/<uuid:kpi_id>', views.reject_individual_kpi, name='Staff_Reject_Individual_Kpi'),
    path('Staff-Kpi/Track-Kpi', StaffTrackKpiListView.as_view(), name='Staff_Track_Kpi'),
    path('Staff-Kpi/Track-Kpi/<int:pk>', StaffTrackKpiOneListView.as_view(), name='Staff_Track_Kpi_Staff'),
    path('Staff-Kpi/Track-Kpi/<int:pk>/<uuid:kpi_id>', StaffKpiTrackOneView.as_view(), name='Staff_Track_Kpi_Staff_One'),
    path('Staff-Kpi/Approve-Kpi/Approve/<int:pk>/<uuid:kpi_id>/<int:month>', views.approve_individual_kpi, name='Staff_Approve_Kpi_score'),
    path('Staff-Kpi/Kpi-Results', views.staff_kpiresults, name='Staff_Kpi_Results'),
    
    # BU Kpi Links
    # path('BU/', views.bu_dashboard, name='BU_Dashboard'),
    path('BU-Kpi/', views.bu_Kpi, name='BU_Kpi_Dashboard'),
    path('BU-Kpi/Submit-Kpi/', views.bu_Submit_Kpi, name='BU_Kpi_Submit'),
    path('BU-Kpi/Track-Kpi/', views.bu_track_kpi, name='BU_Kpi_Detail1'),
    path('BU-Kpi/Track-Kpi/<uuid:pk>', views.BU_Kpi_Detail_View.as_view(), name='BU_kpi-detail'),
    path('BU-Kpi/Edit-Kpi/', views.bu_edit_kpi, name='BU_Kpi_Edit'),
    path('BU-Kpi/Edit-Kpi/<uuid:pk>', views.BU_Edit_Kpi_View.as_view(), name='BU_Kpi_Edit_One'),
    path('BU-Kpi/Kpi-Results/', views.bu_kpi_result, name='BU_Kpi_Result'),
    path('BU-Kpi/Kpi-Results/<uuid:pk>', views.BU_Kpi_Result_Update.as_view(), name='BU_Kpi_Result_Update'),


    # Company Kpi Links
    # path('Company/', views.company, name='Company_Dashboard'),
    path('Company-Kpi/', views.company_Kpi, name='Company_Kpi_Dashboard'),
    path('Company-Kpi/Submit-Kpi/', views.company_Submit_Kpi, name='Company_Kpi_Submit'),
    path('Company-Kpi/Track-Kpi/', views.company_track_kpi, name='Company_Kpi_Detail1'),
    path('Company-Kpi/Track-Kpi/<uuid:pk>', views.Company_Kpi_Detail_View.as_view(), name='Company_Kpi_Detail'),
    path('Company-Kpi/Edit-Kpi/', views.company_edit_kpi, name='Company_Kpi_Edit'),
    path('Company-Kpi/Edit-Kpi/<uuid:pk>', views.Company_Edit_Kpi_View.as_view(), name='Company_Kpi_Edit_One'),
    path('Company-Kpi/Kpi-Results/', views.company_kpi_result, name='Company_Kpi_Result'),
    path('Company-Kpi/Kpi-Results/<uuid:pk>', views.Company_Kpi_Result_Update.as_view(), name='Company_Kpi_Result_Update'),


    # My Checkin Kpi Links
    path('Check-In/', views.my_check_in, name='Check-In_Kpi_Dashboard'),
    path('Check-In/Submit-CI/', views.checkin_Submit_Kpi, name='Check-In_Submit'),
    path('Check-In/Track-CI/', views.track_check_in, name='Check-In_Detail1'),
    path('Check-In/Track-CI/<uuid:pk>', views.Check_In_Detail_View.as_view(), name='Check-In_Detail'),
    path('Check-In/Edit-CI/', views.check_In_edit, name='Check-In_Edit'),
    path('Check-In/Edit-CI/<uuid:pk>', views.Chech_In_Edit_View.as_view(), name='Check-In_Edit_One'),
    
    
    # Staff Checkin Kpi Links
    path('Check-In/Staff-CI', views.staff_check_in, name='Staff_Check-In_Kpi_Dashboard'),
    path('Check-In/Staff-CI/Approve-CI', views.approve_check_in, name='Staff_Approve_CI'),
    path('Check-In/Staff-CI/Approve-CI/<int:pk>', views.staff_check_in_staff, name='Staff_Approve_CI_list'),
    path('Check-In/Staff-CI/Approve-CI/<int:pk>/<uuid:ci_id>', views.staff_individual_check_in, name='Staff_Approve_CI_Detail1'),
    path('Check-In/Staff-CI/Approve-CI/Approve/<int:pk>/<uuid:ci_id>', views.approve_individual_check_in, name='Staff_Approve_Individual_CI'),
    path('Check-In/Staff-CI/Approve-CI/Reject/<int:pk>/<uuid:ci_id>', views.reject_individual_check_in, name='Staff_Reject_Individual_CI'),
    path('Check-In/Staff-CI/Track-CI/', views.staff_track_check_in, name='Staff_Track_CI'),
    path('Check-In/Staff-CI/Track-CI/<int:pk>', views.staff_track_check_in_staff, name='Staff_Track_CI_Staff'),
    path('Check-In/Staff-CI/Track-CI/<int:pk>/<uuid:ci_id>', views.staff_track_check_in_staff_one, name='Staff_Track_CI_Detail'),

    # My Checkin Kpi Links
    path('Assessment/', views.assessment, name='Assessment_Dashboard'),
    path('Assessment/<uuid:as_id>', views.assessment_view, name='Assessment_View'),
    path('Assessment/<uuid:as_id>/S-TL', views.assessment_s_tl, name='Assessment_TL'),
    path('Assessment/<uuid:as_id>/TL-S', views.assessment_tl_s, name='Assessment_S'),
    path('Assessment/<uuid:as_id>/S-TL/<int:tl_id>', views.assessment_s_tl_one, name='Assessment_TL_One'),
    path('Assessment/<uuid:as_id>/TL-S/<int:s_id>', views.assessment_tl_s_one, name='Assessment_S_One'),
    path('Assessment/<uuid:as_id>/TL-S', views.assessment_s_tl, name='Assessment_S'),

]
