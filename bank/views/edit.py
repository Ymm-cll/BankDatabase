# 银行信息修改处理函数
import pymysql
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect


def bank_edit(request):
    if request.method == 'GET':
        bank_id = request.GET.get("bank_id")
        conn = pymysql.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM bank_bank WHERE bank_id = %s", [bank_id])
            bank = cursor.fetchone()
        return render(request, 'bank/edit/bank_edit.html', {'bank': bank})
    else:
        bank_id = request.POST.get("bank_id")
        bank_data = {
            'bank_id': request.POST.get('bank_id', ''),
            'bank_name': request.POST.get('bank_name', '') or None,
            'bank_address': request.POST.get('bank_address', '') or None,
            'established_date': request.POST.get('established_date', '') or None,
            'operational_status': request.POST.get('operational_status', '') or None,
            'contact_phone': request.POST.get('contact_phone', '') or None,
            'contact_email': request.POST.get('contact_email', '') or None,
            'service_type': request.POST.get('service_type', '') or None,
        }

        conn = pymysql.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            set_clause = ', '.join([f"{k} = %s" for k in bank_data.keys()])
            sql = f"UPDATE bank_bank SET {set_clause} WHERE bank_id = %s"
            cursor.execute(sql, list(bank_data.values()) + [bank_id])
            conn.commit()
        return redirect('../')


def customer_edit(request):
    if request.method == 'GET':
        customer_id = request.GET.get("customer_id")
        conn = pymysql.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM bank_customer WHERE customer_id = %s", [customer_id])
            customer = cursor.fetchone()
        return render(request, 'bank/edit/customer_edit.html', {'customer': customer})
    else:
        customer_id = request.POST.get("customer_id")
        customer_data = {
            'customer_id': request.POST.get('customer_id', ''),
            'customer_name': request.POST.get('customer_name', '') or None,
            'photo_filename': request.POST.get('photo_filename', '') or None,
            'customer_gender': request.POST.get('customer_gender', '') or None,
            'birth_date': request.POST.get('birth_date', '') or None,
            'occupation': request.POST.get('occupation', '') or None,
            'contact_address': request.POST.get('contact_address', '') or None,
            'contact_phone': request.POST.get('contact_phone', '') or None,
            'contact_email': request.POST.get('contact_email', '') or None,
            'customer_level': request.POST.get('customer_level', '') or None,
        }

        if request.FILES.get('photo_upload'):
            photo = request.FILES['photo_upload']
            fs = FileSystemStorage()
            filename = fs.save(photo.name, photo)
            customer_data['photo_filename'] = filename

        conn = pymysql.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            set_clause = ', '.join([f"{k} = %s" for k in customer_data.keys()])
            sql = f"UPDATE bank_customer SET {set_clause} WHERE customer_id = %s"
            cursor.execute(sql, list(customer_data.values()) + [customer_id])
            conn.commit()
        return redirect('../')


def account_edit(request):
    if request.method == 'GET':
        account_number = request.GET.get("account_number")
        conn = pymysql.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM bank_account WHERE account_number = %s", [account_number])
            account = cursor.fetchone()
        return render(request, 'bank/edit/account_edit.html', {'account': account})
    else:
        account_number = request.POST.get("account_number")
        account_data = {
            'account_number': request.POST.get('account_number', ''),
            'customer_id': request.POST.get('customer_id', ''),
            'account_type': request.POST.get('account_type', '') or None,
            'opening_date': request.POST.get('opening_date', '') or None,
            'account_status': request.POST.get('account_status', '') or None,
            'current_balance': request.POST.get('current_balance', '') or None,
            'interest_rate': request.POST.get('interest_rate', '') or None,
            'overdraft_limit': request.POST.get('overdraft_limit', '') or None,
        }

        conn = pymysql.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            set_clause = ', '.join([f"{k} = %s" for k in account_data.keys()])
            sql = f"UPDATE bank_account SET {set_clause} WHERE account_number = %s"
            cursor.execute(sql, list(account_data.values()) + [account_number])
            conn.commit()
        return redirect('../')


def loan_edit(request):
    if request.method == 'GET':
        loan_id = request.GET.get("loan_id")
        conn = pymysql.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM bank_loan WHERE loan_id = %s", [loan_id])
            loan = cursor.fetchone()
        return render(request, 'bank/edit/loan_edit.html', {'loan': loan})
    else:
        loan_id = request.POST.get("loan_id")
        loan_data = {
            'loan_id': request.POST.get('loan_id', ''),
            'account_id': request.POST.get('account_id', ''),
            'loan_amount': request.POST.get('loan_amount', '') or None,
            'disbursement_date': request.POST.get('disbursement_date', '') or None,
            'due_date': request.POST.get('due_date', '') or None,
            'loan_rate': request.POST.get('loan_rate', '') or None,
            'loan_status': request.POST.get('loan_status', '') or None,
            'remaining_amount': request.POST.get('remaining_amount', '') or None,
        }

        conn = pymysql.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            set_clause = ', '.join([f"{k} = %s" for k in loan_data.keys()])
            sql = f"UPDATE bank_loan SET {set_clause} WHERE loan_id = %s"
            cursor.execute(sql, list(loan_data.values()) + [loan_id])
            conn.commit()
        return redirect('../')


def department_edit(request):
    if request.method == 'GET':
        department_id = request.GET.get("department_id")
        conn = pymysql.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM bank_department WHERE department_id = %s", [department_id])
            department = cursor.fetchone()
        return render(request, 'bank/edit/department_edit.html', {'department': department})
    else:
        department_id = request.POST.get("department_id")
        department_data = {
            'department_id': request.POST.get('department_id', ''),
            'bank_id': request.POST.get('bank_id', ''),
            'department_name': request.POST.get('department_name', '') or None,
            'responsibilities': request.POST.get('responsibilities', '') or None,
            'location': request.POST.get('location', '') or None,
            'contact_phone': request.POST.get('contact_phone', '') or None,
            'manager_id': request.POST.get('manager_id', '') or None,
        }

        conn = pymysql.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            set_clause = ', '.join([f"{k} = %s" for k in department_data.keys()])
            sql = f"UPDATE bank_department SET {set_clause} WHERE department_id = %s"
            cursor.execute(sql, list(department_data.values()) + [department_id])
            conn.commit()
        return redirect('../')


def employee_edit(request):
    if request.method == 'GET':
        employee_id = request.GET.get("employee_id")
        conn = pymysql.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM bank_employee WHERE employee_id = %s", [employee_id])
            employee = cursor.fetchone()
        return render(request, 'bank/edit/employee_edit.html', {'employee': employee})
    else:
        employee_id = request.POST.get("employee_id")
        employee_data = {
            'employee_id': request.POST.get('employee_id', ''),
            'department_id': request.POST.get('department_id', ''),
            'employee_name': request.POST.get('employee_name', '') or None,
            'position': request.POST.get('position', '') or None,
            'contact_phone': request.POST.get('contact_phone', '') or None,
            'email_address': request.POST.get('email_address', '') or None,
            'hire_date': request.POST.get('hire_date', '') or None,
            'salary': request.POST.get('salary', '') or None,
            'performance_rating': request.POST.get('performance_rating', '') or None,
        }

        conn = pymysql.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            set_clause = ', '.join([f"{k} = %s" for k in employee_data.keys()])
            sql = f"UPDATE bank_employee SET {set_clause} WHERE employee_id = %s"
            cursor.execute(sql, list(employee_data.values()) + [employee_id])
            conn.commit()
        return redirect('../')
