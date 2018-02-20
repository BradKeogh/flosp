EDcols_essential = [
'dept_patid',
'hosp_patid',
'age',
'gender',
'site',
'arrival_date',
'arrival_time',
'arrival_mode',
'first_triage_time',
'first_dr_time',
'first_adm_request_time',
'adm_referral_loc',
'departure_method',
'leaving_time',
'flag_adm'
]

EDcols_io_pmth = {
'pas_id':'dept_patid',
'nhs_number':'hosp_patid',
'age':'age',
'gender':'gender',
'department':'site',
'date_of_attendance':'arrival_date',
'time_of_attendance':'arrival_time',
'mode_of_arrival':'arrival_mode',
'triage_time':'first_triage_time',
'dr1_seen':'first_dr_time',
'referred_to__first_referral':'first_adm_request_time',
'referred_to_at_point_of_discharge':'adm_referral_loc',
'departure_method':'departure_method',
'left_dept_time':'leaving_time',
'departure_method':'departure_method'
}
