from django.urls import path, re_path
from . import views
from .views import *

app_name = 'tydia'

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
    path('BU/<uuid:pk>', BuDashboardKpiDetailView.as_view(), name='BU_dashboard-detail'),
    path('BU-Kpi/', BuKpi.as_view(), name='BU_Kpi_Dashboard'),
    path('BU-Kpi/Submit-Kpi/', SubmitBuKpiView.as_view(), name='BU_Kpi_Submit'),
    path('BU-Kpi/Track-Kpi/', TrackBuKpiView.as_view(), name='BU_Kpi_Detail1'),
    path('BU-Kpi/Track-Kpi/<uuid:pk>', TrackBuKpiDetailView.as_view(), name='BU_kpi-detail'),
    path('BU-Kpi/Edit-Kpi/<uuid:pk>', TrackBuKpiEditlView.as_view(), name='BU_Kpi_Edit_One'),
    path('BU-Kpi/Kpi-Results/', BuKpiResultListView.as_view(), name='BU_Kpi_Result'),
    path('BU-Kpi/Kpi-Results/<uuid:pk>', views.BuKpiResultUpdateView.as_view(), name='BU_Kpi_Result_Update'),


    # Company Kpi Links
    path('Company/', ComapanyKpiDashboard.as_view(), name='Company_Dashboard'),
    path('Company-Kpi/<uuid:pk>', CompanyDashboardKpiDetailView.as_view(), name='Company_Dashboard_Detail'),
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
    path('Check-In/Staff-CI/Track-CI/BU', StaffTrackCheckInBU.as_view(), name='Staff_Track_CI_BU'),
    path('Check-In/Staff-CI/Track-CI/<int:pk>', StaffTrackStaffCheckIn.as_view(), name='Staff_Track_CI_Staff'),
    path('Check-In/Staff-CI/Track-CI/<int:pk>/BU', StaffTrackStaffCheckInBU.as_view(), name='Staff_Track_CI_Staff_BU'),
    path('Check-In/Staff-CI/Track-CI/<int:pk>/<uuid:ci_id>', StaffTrackStaffDetailCheckIn.as_view(), name='Staff_Track_CI_Detail'),

    # My Checkin Kpi Links
    path('Assessment/', Assessment.as_view(), name='Assessment_Dashboard'),
    path('Assessment/<uuid:as_id>', AssessmentView.as_view(), name='Assessment_View'),
    path('Assessment/TL-S/<uuid:as_id>', AssessmentTlS.as_view(), name='Assessment_S'),
    path('Assessment/<uuid:as_id>/S-TL/<int:tl_id>', AssessmentSTlStaff.as_view(), name='Assessment_TL_One'),
    path('Assessment/<uuid:as_id>/TL-S/<int:s_id>', AssessmentTlSStaff.as_view(), name='Assessment_S_One'),



    path('Assessment/Previous', AssessmentPrevious.as_view(), name='Assessment_Previous'),
    path('Assessment/Previous/<uuid:as_id>', AssessmentPreviousView.as_view(), name='Assessment_Previous_One'),
    path('Assessment/<uuid:as_id>/S-TL/<int:tl_id>/Previous', AssessmentSTlStaffPrevious.as_view(),
         name='Assessment_TL_One_Previous'),
    path('Assessment/TL-S/<uuid:as_id>/Previous', AssessmentTlSStaffPrevious.as_view(), name='Assessment_S_Previous'),
    path('Assessment/<uuid:as_id>/TL-S/<int:s_id>/Previous', AssessmentTlSPreviousStaff.as_view(), name='Assessment_S_One_Previous'),


    path('Report/', Report.as_view(), name='Reports'),
    path('Report/KPI', ReportKPI.as_view(), name='Reports_KPI'),
    path('Report/CheckIn', ReportCheckIn.as_view(), name='Reports_CheckIn'),
    path('Report/Assessment', ReportAssessment.as_view(), name='Reports_Assessment'),
    path('Report/Assessment/<uuid:pk>', ReportAssessmentDetail.as_view(), name='Reports_Assessment_Detail'),
    path('Profile/', Profile.as_view(), name='Profile'),


    path('Admin/', AdminDashboard.as_view(), name='Admin_Dashboard'),

    path('Admin/BUs', AdminBU.as_view(), name='Admin_BUs'),
    path('Admin/BUs/<uuid:bu_id>', AdminBUOne.as_view(), name='Admin_BUs_One'),
    path('Admin/BUs/New', AdminBUNew.as_view(), name='Admin_BUs_New'),

    path('Admin/Teams', AdminTeam.as_view(), name='Admin_Teams'),
    path('Admin/Teams/<uuid:t_id>', AdminTeamOne.as_view(), name='Admin_Teams_One'),
    path('Admin/Teams/New', AdminTeamNew.as_view(), name='Admin_Teams_New'),


    path('Admin/Users', AdminUser.as_view(), name='Admin_Users'),
    path('Admin/Users/New', new_user, name='Admin_Users_New'),
    path('Admin/Users/New/Details/<int:pk>', AdminUserNewDetails.as_view(), name='Admin_Users_New_Details'),
    path('Admin/Users/New/Details/<int:pk>/Staff', AdminUserNewDetailsStaff.as_view(), name='Admin_Users_New_Details_Staff'),
    path('Admin/Users/<int:pk>', AdminUserOne.as_view(), name='Admin_Users_One'),
    path('Admin/Users/<int:pk>/Edit/User', AdminUserOneEditUser.as_view(), name='Admin_Users_One_Edit_User'),
    path('Admin/Users/<int:pk>/Edit/Staff', AdminUserOneEditStaff.as_view(), name='Admin_Users_One_Edit_Staff'),
    path('Admin/Users/Deactivate/<int:pk>', deactivate_account_dashboard, name='Admin_Users_deactivate1'),
    path('Admin/Users/Activate/<int:pk>', activate_account_dashboard, name='Admin_Users_activate1'),
    path('Admin/Users/Reset_Password/<int:pk>', change_password, name='Admin_Users_reset_password'),


    path('Admin/PMS/<uuid:pms_id>', AdminPMS.as_view(), name='Admin_PMS'),
    path('Admin/PMS/Edit/<uuid:pms_id>', AdminPMSEdit.as_view(), name='Admin_PMS_Edit'),
    path('Admin/PMS/New/', AdminPMSNew.as_view(), name='Admin_PMS_New'),
    path('Admin/PMS/<uuid:pms_id>/Staff/', AdminPMSStaff.as_view(), name='Admin_PMS_Staff'),
    path('Admin/PMS/<uuid:pms_id>/Staff/<int:s_id>', AdminPMSStaffOne.as_view(), name='Admin_PMS_Staff_One'),
    path('Admin/PMS/<uuid:pms_id>/Staff/<int:s_id>/Edit', AdminPMSStaffOneEdit.as_view(), name='Admin_PMS_Staff_One_Edit'),

    path('Admin/PMS/<uuid:pms_id>/Individual-Kpi/', AdminPMSIndividual.as_view(), name='Admin_PMS_Individual'),
    path('Admin/PMS/<uuid:pms_id>/Individual-Kpi/<int:s_id>', AdminPMSIndividualStaff.as_view(), name='Admin_PMS_Individual_Staff'),
    path('Admin/PMS/<uuid:pms_id>/Individual-Kpi/<int:s_id>/New', AdminPMSIndividualStaffNew.as_view(), name='Admin_PMS_Individual_Staff_New'),
    path('Admin/PMS/<uuid:pms_id>/Individual-Kpi/<int:s_id>/<uuid:kpi_id>', AdminPMSIndividualStaffOne.as_view(), name='Admin_PMS_Individual_Staff_One'),

    path('Admin/PMS/<uuid:pms_id>/BU-Kpi/', AdminPMSBU.as_view(), name='Admin_PMS_BU'),
    path('Admin/PMS/<uuid:pms_id>/BU-Kpi/<int:s_id>', AdminPMSBUStaff.as_view(), name='Admin_PMS_BU_Staff'),
    path('Admin/PMS/<uuid:pms_id>/BU-Kpi/<int:s_id>/New', AdminPMSBUStaffNew.as_view(), name='Admin_PMS_BU_Staff_New'),
    path('Admin/PMS/<uuid:pms_id>/BU-Kpi/<int:s_id>/<uuid:kpi_id>', AdminPMSBUStaffOne.as_view(), name='Admin_PMS_BU_Staff_One'),

    path('Admin/PMS/<uuid:pms_id>/Company-Kpi/', AdminPMSCompany.as_view(), name='Admin_PMS_Company'),
    path('Admin/PMS/<uuid:pms_id>/Company-Kpi/New', AdminPMSCompanyNew.as_view(), name='Admin_PMS_Company_New'),
    path('Admin/PMS/<uuid:pms_id>/Company-Kpi/<uuid:kpi_id>', AdminPMSCompanyOne.as_view(), name='Admin_PMS_Company_One'),

    path('Admin/PMS/<uuid:pms_id>/Check-In/', AdminPMSCheckIn.as_view(), name='Admin_PMS_CheckIn'),
    path('Admin/PMS/<uuid:pms_id>/Check-In/Score/New', AdminPMSCheckInScoreNew.as_view(), name='Admin_PMS_CheckIn_Score_New'),
    path('Admin/PMS/<uuid:pms_id>/Check-In/Score/<uuid:m_id>', AdminPMSCheckInScoreOne.as_view(), name='Admin_PMS_CheckIn_Score_One'),
    path('Admin/PMS/<uuid:pms_id>/Check-In/<int:s_id>', AdminPMSCheckInStaff.as_view(), name='Admin_PMS_CheckIn_Staff'),
    path('Admin/PMS/<uuid:pms_id>/Check-In/<int:s_id>/New', AdminPMSCheckInStaffNew.as_view(), name='Admin_PMS_CheckInStaff_New'),
    path('Admin/PMS/<uuid:pms_id>/Check-In/<int:s_id>/<uuid:kpi_id>', AdminPMSCheckInStaffOne.as_view(), name='Admin_PMS_CheckIn_Staff_One'),

    path('Admin/PMS/<uuid:pms_id>/Assessment/', AdminPMSAssessment.as_view(), name='Admin_PMS_Assessment'),
    path('Admin/PMS/<uuid:pms_id>/Assessment/<uuid:as_id>', AdminPMSAssessmentOne.as_view(), name='Admin_PMS_Assessment_One'),
    path('Admin/PMS/<uuid:pms_id>/Assessment/<uuid:as_id>/Score/New', AdminPMSAssessmentOneResponseNew.as_view(), name='Admin_PMS_Assessment_One_Response_New'),
    path('Admin/PMS/<uuid:pms_id>/Assessment/<uuid:as_id>/Score/<uuid:m_id>', AdminPMSAssessmentOneResponseOne.as_view(), name='Admin_PMS_Assessment_One_Response_One'),
    path('Admin/PMS/<uuid:pms_id>/Assessment/<uuid:as_id>/S_Tl', AdminPMSAssessmentOneResponseSTl.as_view(), name='Admin_PMS_Assessment_One_STl'),
    path('Admin/PMS/<uuid:pms_id>/Assessment/<uuid:as_id>/S_Tl/<uuid:d_id>', AdminPMSAssessmentOneResponseSTlOne.as_view(), name='Admin_PMS_Assessment_One_STl_One'),
    path('Admin/PMS/<uuid:pms_id>/Assessment/<uuid:as_id>/Tl_S', AdminPMSAssessmentOneResponseTlS.as_view(), name='Admin_PMS_Assessment_One_TlS'),
    path('Admin/PMS/<uuid:pms_id>/Assessment/<uuid:as_id>/Tl_S/<uuid:d_id>', AdminPMSAssessmentOneResponseTlSOne.as_view(), name='Admin_PMS_Assessment_One_TlS_One'),
    path('Admin/PMS/<uuid:pms_id>/Assessment/New', AdminPMSAssessmentNew.as_view(), name='Admin_PMS_Assessment_New'),
    path('Admin/PMS/<uuid:pms_id>/Assessment/<uuid:as_id>/Question/<uuid:q_id>/TL_S', AdminPMSAssessmentOneQuestionOneTlS.as_view(), name='Admin_PMS_Assessment_One_Question_One_Tl_S'),
    path('Admin/PMS/<uuid:pms_id>/Assessment/<uuid:as_id>/Question/<uuid:q_id>/S_TL', AdminPMSAssessmentOneQuestionOneSTl.as_view(), name='Admin_PMS_Assessment_One_Question_One_S_Tl'),
    path('Admin/PMS/<uuid:pms_id>/Assessment/<uuid:as_id>/Question/New/TL_S', AdminPMSAssessmentOneQuestionNewTlS.as_view(), name='Admin_PMS_Assessment_New_Question_One_Tl_S'),
    path('Admin/PMS/<uuid:pms_id>/Assessment/<uuid:as_id>/Question/New/S_TL', AdminPMSAssessmentOneQuestionNewSTl.as_view(), name='Admin_PMS_Assessment_New_Question_One_S_Tl'),
    path('Admin/PMS/<uuid:pms_id>/Check-In/<int:s_id>/New', AdminPMSCheckInStaffNew.as_view(),
         name='Admin_PMS_CheckInStaff_New'),
    path('Admin/PMS/<uuid:pms_id>/Check-In/<int:s_id>/<uuid:kpi_id>', AdminPMSCheckInStaffOne.as_view(),
         name='Admin_PMS_CheckIn_Staff_One'),
    path('Admin/PMS/Send_PWD', reset_all_password, name='Admin_Reset_Password'),
    path('Admin/PMS/<uuid:pms_id>/Matrix', Matrix.as_view(), name='Admin_PMS_Matrix'),
    path('Admin/PMS/<uuid:pms_id>/Matrix/New', AdminPMSMatrixScoreNew.as_view(), name='Admin_PMS_Matrix_New'),
    path('Admin/PMS/<uuid:pms_id>/Matrix/<uuid:m_id>', AdminPMSMatrixScore.as_view(), name='Admin_PMS_Matrix_Score'),
    path('Admin/PMS/<uuid:pms_id>/Matrix/KPI', AdminPMSMatrixKPI.as_view(), name='Admin_PMS_Matrix_KPI'),
    path('Admin/PMS/<uuid:pms_id>/Matrix/KPI/New', AdminPMSMatrixKPINew.as_view(), name='Admin_PMS_Matrix_KPI_New'),
    path('Admin/PMS/<uuid:pms_id>/Matrix/KPI/<uuid:m_id>', AdminPMSMatrixKPIOne.as_view(), name='Admin_PMS_Matrix_KPI_One'),

]
