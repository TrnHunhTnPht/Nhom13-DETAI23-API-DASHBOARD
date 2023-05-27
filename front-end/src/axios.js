import axios from 'axios'

axios.defaults.baseURL = 'http://ec2-18-208-115-16.compute-1.amazonaws.com:8000/'
axios.defaults.headers.common = { 'Authorization': `Bearer ${localStorage.getItem("access_token")}` }


export const REGISTER = 'user/register'
export const LOGIN = 'user/login'
export const VERIFY = 'user/verify_account'
export const SENDOTP = 'send_otp'
export const CHART_DATA = "chart-data"
export const TODAY_USERS = "today-users"
export const NEW_CLIENTS = "new-clients"
export const STATE_OK = "status-success"
export const TOTAL_CHECK_TIME = "total-check-times"
export const GET_INSPECTION = "get-inspection"
export const GET_HO_STATISTIC = "id_statistic"
export const GET_PREDICT_STATISTIC = "predict_result_statistic"
export const GET_INSPECTION_DETAIL = "get-inspection-detail"
export const GET_INSPECTION_ALL_DETAILS = "get-inspection-all-details"
export const GET_USER = "users"
export const UPDATE_DELETE_USER = "user"
export const UPDATE_PASSWORD = "change_password"
export const EXPORT_EXCEL_API = "download_api_data"
