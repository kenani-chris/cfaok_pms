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
    path('Staff-Kpi/Approve-Kpi/Approve/<int:pk>/<uuid:kpi_id>', approve_individual_kpi,
         name='Staff_Approve_Individual_Kpi'),
    path('Staff-Kpi/Approve-Kpi/Reject/<int:pk>/<uuid:kpi_id>', reject_individual_kpi,
         name='Staff_Reject_Individual_Kpi'),
    path('Staff-Kpi/Track-Kpi', StaffTrackKpiListView.as_view(), name='Staff_Track_Kpi'),
    path('Staff-Kpi/Track-Kpi/<int:pk>', StaffTrackKpiOneListView.as_view(), name='Staff_Track_Kpi_Staff'),
    path('Staff-Kpi/Track-Kpi/<int:pk>/<uuid:kpi_id>', StaffKpiTrackOneView.as_view(), name='Staff_Track_Kpi_Staff_One'),
    path('Staff-Kpi/Approve-Kpi/Approve/<int:pk>/<uuid:kpi_id>/<int:month>', approve_individual_kpi_score,
         name='Staff_Approve_Kpi_score'),
    path('Staff-Kpi/Approve-Kpi/Approve/<int:pk>/<uuid:kpi_id>/<int:month>', approve_individual_kpi_score_dashboard,
         name='Staff_Approve_Kpi_score_dashboard'),

    
    # BU Kpi Links
    path('BU/', BuKpiDashboard.as_view(), name='BU_Dashboard'),
    path('BU-Kpi/', BuKpi.as_view(), name='BU_Kpi_Dashboard'),
    path('BU-Kpi/Submit-Kpi/', SubmitBuKpiView.as_view(), name='BU_Kpi_Submit'),
    path('BU-Kpi/Track-Kpi/', TrackBuKpiView.as_view(), name='BU_Kpi_Detail1'),
    path('BU-Kpi/Track-Kpi/<uuid:pk>', TrackBuKpiDetailView.as_view(), name='BU_kpi-detail'),
    path('BU-Kpi/Edit-Kpi/<uuid:pk>', TrackBuKpiEditlView.as_view(), name='BU_Kpi_Edit_One'),
    path('BU-Kpi/Kpi-Results/', BuKpiResultListView.as_view(), name='BU_Kpi_Result'),
    path('BU-Kpi/Kpi-Results/<uuid:pk>', views.BuKpiResultUpdateView.as_view(), name='BU_Kpi_Result_Update'),


    # Company Kpi Links
    # path('Company/', views.company, name='Company_Dashboard'),
    path('Company-Kpi/', CompanyKpi.as_view(), name='Company_Kpi_Dashboard'),
    path('Company-Kpi/Submit-Kpi/', SubmitCompanyKpiView.as_view(), name='Company_Kpi_Submit'),
    path('Company-Kpi/Edit-Kpi/', EditCompanyKpiView.as_view(), name='Company_Kpi_Edit'),
    path('Company-Kpi/Edit-Kpi/<uuid:pk>', EditCompanyKpiUpdateView.as_view(), name='Company_Kpi_Edit_One'),
    path('Company-Kpi/Kpi-Results/', CompanyKpiResultListView.as_view(), name='Company_Kpi_Result'),
    path('Company-Kpi/Kpi-Results/<uuid:pk>', CompanyKpiResultUpdateView.as_view(), name='Company_Kpi_Result_Update'),
    
    
    # Staff BU Kpi Links
    path('BUs-Kpi/', BUsKpiListView.as_view(), name='BUs_Kpi_Dashboard'),
    path('BUs-Kpi/Approve-Kpi', BUsKpiPendingListView.as_view(), name='BUs_Approve_Kpi'),
    path('BUs-Kpi/Approve-Kpi/<uuid:pk>', BUsKpiApproveView.as_view(), name='BUs_Approve_Kpi_Detail'),
    path('BUs-Kpi/Approve-Kpi/Approve/<uuid:pk>/<uuid:kpi_id>', approve_bu_kpi, name='BUs_Approve_Kpi'),
    path('BUs-Kpi/Approve-Kpi/Reject/<uuid:pk>/<uuid:kpi_id>', reject_bu_kpi, name='BUs_Reject_Kpi'),
    path('BUs-Kpi/Track-Kpi', BUsTrackKpiListView.as_view(), name='BUs_Track_Kpi'),
    path('BUs-Kpi/Track-Kpi/<uuid:pk>', BUsTrackKpiOneListView.as_view(), name='BUs_Track_Kpi_BUs'),
    path('BUs-Kpi/Track-Kpi/<uuid:pk>/<uuid:kpi_id>', BUsKpiTrackOneView.as_view(), name='BUs_Track_Kpi_BUs_One'),
    path('BUs-Kpi/Approve-Kpi/Approve/<uuid:pk>/<uuid:kpi_id>/<int:month>', approve_bu_kpi_score,
         name='BUs_Approve_Kpi_score'),
    path('BUs-Kpi/Approve-Kpi/Approve/<int:pk>/<uuid:kpi_id>/<int:month>', approve_bu_kpi_score_dashboard,
         name='BUs_Approve_Kpi_score_dashboard'),


    # My Checkin Kpi Links
    path('Check-In/', MyCheckIn.as_view(), name='Check-In_Kpi_Dashboard'),
    path('Check-In/Submit-CI/', SubmitCheckIn.as_view(), name='Check-In_Submit'),
    path('Check-In/Track-CI/', TrackCheckIn.as_view(), name='Check-In_Detail1'),
    path('Check-In/Track-CI/<uuid:pk>', DetailCheckIn.as_view(), name='Check-In_Detail'),
    path('Check-In/Edit-CI/<uuid:pk>', EditCheckIn.as_view(), name='Check-In_Edit_One'),
    
    
    # Staff Checkin Kpi Links
    path('Check-In/Staff-CI', StaffCheckIn.as_view(), name='Staff_Check-In_Kpi_Dashboard'),
    path('Check-In/Staff-CI/Approve-CI', StaffApproveCheckIn.as_view(), name='Staff_Approve_CI'),
    path('Check-In/Staff-CI/Approve-CI/<int:pk>', StaffApproveStaffCheckIn.as_view(), name='Staff_Approve_CI_list'),
    path('Check-In/Staff-CI/Approve-CI/<int:pk>/<uuid:ci_id>', StaffApproveStaffCheckInOne.as_view(), name='Staff_Approve_CI_Detail1'),
    path('Check-In/Staff-CI/Track-CI/', StaffTrackCheckIn.as_view(), name='Staff_Track_CI'),
    path('Check-In/Staff-CI/Track-CI/<int:pk>', StaffTrackStaffCheckIn.as_view(), name='Staff_Track_CI_Staff'),
    path('Check-In/Staff-CI/Track-CI/<int:pk>/<uuid:ci_id>', StaffTrackStaffDetailCheckIn.as_view(), name='Staff_Track_CI_Detail'),

    # My Checkin Kpi Links
    path('Assessment/', Assessment.as_view(), name='Assessment_Dashboard'),
    path('Assessment/<uuid:as_id>', AssessmentView.as_view(), name='Assessment_View'),
    path('Assessment/TL-S/<uuid:as_id>', AssessmentTlS.as_view(), name='Assessment_S'),
    path('Assessment/<uuid:as_id>/S-TL/<int:tl_id>', views.assessment_s_tl_one, name='Assessment_TL_One'),
    path('Assessment/<uuid:as_id>/TL-S/<int:s_id>', views.assessment_tl_s_one, name='Assessment_S_One'),

]
