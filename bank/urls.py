# coding=utf-8
from django.contrib import admin
from django.urls import path
from bank.views import index,add,delete,edit,search,others

urlpatterns = [
    path("bank/", index.bank_index),
    path("customer/", index.customer_index),
    path("account/", index.account_index),
    path("loan/", index.loan_index),
    path("department/", index.department_index),
    path("employee/", index.employee_index),

    path("bank/bank_add/", add.bank_add),
    path("customer/customer_add/", add.customer_add),
    path("account/account_add/", add.account_add),
    path("loan/loan_add/", add.loan_add),
    path("department/department_add/", add.department_add),
    path("employee/employee_add/", add.employee_add),


    path("bank/bank_edit/", edit.bank_edit),
    path("customer/customer_edit/", edit.customer_edit),
    path("account/account_edit/", edit.account_edit),
    path("loan/loan_edit/", edit.loan_edit),
    path("department/department_edit/", edit.department_edit),
    path("employee/employee_edit/", edit.employee_edit),

    path("bank/bank_delete/", delete.bank_delete),
    path("customer/customer_delete/", delete.customer_delete),
    path("account/account_delete/", delete.account_delete),
    path("loan/loan_delete/", delete.loan_delete),
    path("department/department_delete/", delete.department_delete),
    path("employee/employee_delete/", delete.employee_delete),

    path("bank/bank_search/", search.bank_search),
    path("others/account_transfer/", others.account_transfer),
    path("others/customer_assets/", others.customer_assets),
    path("others/loan_repay/", others.loan_repay),
    path("others/bank_dump/", others.bank_dump),
]
