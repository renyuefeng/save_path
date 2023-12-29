from django.contrib import admin
from django.urls import path

# from views import testRequest
from home.views_submit import handle_uploaded_file, get_files, show_file_message, show_file, save_change_message
from home.views_make_sure import contractMakeSure, show_contract_message, show_title_message
from home.views_ok import contract_submit, select_contract_submit
from home.views_word_examine import word_examine, show_examine_message

urlpatterns = [
    # path('contract_submit/', contractSubmit),
    path('get_files/', get_files),
    path(r'contract_make_sure/', contractMakeSure),
    path(r'handle_uploaded_file/', handle_uploaded_file),
    path(r'show_file_message/', show_file_message),
    path(r'show_contract_message/', show_contract_message),
    path(r'show_title_message/', show_title_message),
    path(r'show_file/', show_file),
    path(r'save_change_message/', save_change_message),
    path(r'contract_submit/', contract_submit),
    path(r'word_examine/', word_examine),
    path(r'show_examine_message/', show_examine_message),
    path(r'select_contract_submit/', select_contract_submit),
]
