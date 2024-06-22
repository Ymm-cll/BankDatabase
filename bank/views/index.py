import pymysql
from django.shortcuts import render

# Create your views here.
import MySQLdb
from django.shortcuts import render, redirect


# Create your views here.
# 银行信息列表处理函数
def bank_index(request):
    conn = MySQLdb.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "SELECT * FROM bank_bank")
    banks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request, 'bank/index/bank_index.html', {'banks': banks})


def customer_index(request):
    conn = MySQLdb.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(
        "SELECT * FROM bank_customer")
    customers = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request, 'bank/index/customer_index.html', {'customers': customers})


def account_index(request):
    conn = MySQLdb.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM bank_account")
    accounts = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request, 'bank/index/account_index.html', {'accounts': accounts})


def loan_index(request):
    conn = MySQLdb.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM bank_loan")
    loans = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request, 'bank/index/loan_index.html', {'loans': loans})


def department_index(request):
    conn = MySQLdb.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM bank_department")
    departments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request, 'bank/index/department_index.html', {'departments': departments})


def employee_index(request):
    conn = MySQLdb.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM bank_employee")
    employees = cursor.fetchall()
    cursor.close()
    conn.close()
    return render(request, 'bank/index/employee_index.html', {'employees': employees})
