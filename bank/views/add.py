# 银行信息添加处理函数
import pymysql
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect


def bank_add(request):
    if request.method == 'GET':
        return render(request, 'bank/add/bank_add.html')
    else:
        # 获取POST请求中的所有字段
        bank_data = {
            'bank_id': request.POST.get('bank_id', ''),  # 主键
            'bank_name': request.POST.get('bank_name', '') or None,
            'bank_address': request.POST.get('bank_address', '') or None,
            'established_date': request.POST.get('established_date', '') or None,
            'operational_status': request.POST.get('operational_status', '') or None,
            'contact_phone': request.POST.get('contact_phone', '') or None,
            'contact_email': request.POST.get('contact_email', '') or None,
            'service_type': request.POST.get('service_type', '') or None,
        }

        if not bank_data['bank_id']:
            return render(request, 'bank/add/bank_add.html', {'error': '银行ID不能为空。'})

        conn = pymysql.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            placeholders = ', '.join(['%s'] * len(bank_data))
            columns = ', '.join(bank_data.keys())
            sql = f"INSERT INTO bank_bank ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, list(bank_data.values()))
            conn.commit()
        return redirect('../')


def customer_add(request):
    if request.method == 'GET':
        return render(request, 'bank/add/customer_add.html')
    else:
        customer_data = {
            'customer_id': request.POST.get('customer_id', ''),  # 主键
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

        if not customer_data['customer_id']:
            return render(request, 'bank/add/customer_add.html', {'error': '客户ID不能为空。'})

        if request.FILES.get('photo_upload'):
            photo = request.FILES['photo_upload']
            fs = FileSystemStorage()
            filename = fs.save(photo.name, photo)
            customer_data['photo_filename'] = filename

        conn = pymysql.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            placeholders = ', '.join(['%s'] * len(customer_data))
            columns = ', '.join(customer_data.keys())
            sql = f"INSERT INTO bank_customer ({columns}) VALUES ({placeholders})"
            cursor.execute(sql, list(customer_data.values()))
            conn.commit()
        return redirect('../')


def account_add(request):
    if request.method == 'GET':
        return render(request, 'bank/add/account_add.html')
    else:
        account_data = {
            'account_number': request.POST.get('account_number', ''),  # 主键
            'customer_id': request.POST.get('customer_id', ''),  # 外键
            'account_type': request.POST.get('account_type', '') or None,
            'opening_date': request.POST.get('opening_date', '') or None,
            'account_status': request.POST.get('account_status', '') or None,
            'current_balance': request.POST.get('current_balance', '') or None,
            'interest_rate': request.POST.get('interest_rate', '') or None,
            'overdraft_limit': request.POST.get('overdraft_limit', '') or None,
        }

        if not account_data['account_number']:
            return render(request, 'bank/add/account_add.html', {'error': '账户号码不能为空。'})

        conn = pymysql.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                # 检查 customer_id 是否存在
                customer_id = account_data['customer_id']
                cursor.execute("SELECT COUNT(*) AS count FROM bank_customer WHERE customer_id = %s", (customer_id,))
                result = cursor.fetchone()
                if result['count'] == 0:
                    raise ValueError(f'客户ID不存在。')

                placeholders = ', '.join(['%s'] * len(account_data))
                columns = ', '.join(account_data.keys())
                sql = f"INSERT INTO bank_account ({columns}) VALUES ({placeholders})"
                cursor.execute(sql, list(account_data.values()))
                conn.commit()
        except Exception as e:
            conn.rollback()
            # 使用 JavaScript 弹窗显示错误信息
            return render(request, 'bank/add/account_add.html', {'error': str(e)})
        finally:
            conn.close()

        return redirect('../')


def loan_add(request):
    if request.method == 'GET':
        return render(request, 'bank/add/loan_add.html')
    else:
        loan_data = {
            'loan_id': request.POST.get('loan_id', ''),  # 主键
            'account_id': request.POST.get('account_number', ''),  # 外键
            'loan_amount': request.POST.get('loan_amount', '') or None,
            'disbursement_date': request.POST.get('disbursement_date', '') or None,
            'due_date': request.POST.get('due_date', '') or None,
            'loan_rate': request.POST.get('loan_rate', '') or None,
            'loan_status': request.POST.get('loan_status', '') or None,
            'remaining_amount': request.POST.get('remaining_amount', '') or None,
        }

        if not loan_data['loan_id']:
            return render(request, 'bank/add/loan_add.html', {'error': '贷款ID不能为空。'})

        conn = pymysql.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                # 检查 account_number 是否存在
                account_number = loan_data['account_id']
                cursor.execute("SELECT COUNT(*) AS count FROM bank_account WHERE account_number = %s", (account_number,))
                result = cursor.fetchone()
                if result['count'] == 0:
                    raise ValueError(f'账户ID不存在。')

                placeholders = ', '.join(['%s'] * len(loan_data))
                columns = ', '.join(loan_data.keys())
                sql = f"INSERT INTO bank_loan ({columns}) VALUES ({placeholders})"
                cursor.execute(sql, list(loan_data.values()))
                conn.commit()
        except Exception as e:
            conn.rollback()
            # 使用 JavaScript 弹窗显示错误信息
            return render(request, 'bank/add/loan_add.html', {'error': str(e)})
        finally:
            conn.close()

        return redirect('../')


def department_add(request):
    if request.method == 'GET':
        return render(request, 'bank/add/department_add.html')
    else:
        department_data = {
            'department_id': request.POST.get('department_id', ''),  # 主键
            'bank_id': request.POST.get('bank_id', ''),  # 外键
            'department_name': request.POST.get('department_name', '') or None,
            'responsibilities': request.POST.get('responsibilities', '') or None,
            'location': request.POST.get('location', '') or None,
            'contact_phone': request.POST.get('contact_phone', '') or None,
            'manager_id': request.POST.get('manager_id', None) or None,
        }
        if not department_data['manager_id']:
            department_data['manager_id'] = None

        if not department_data['department_id']:
            return render(request, 'bank/add/department_add.html', {'error': '部门ID不能为空。'})

        conn = pymysql.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                # 检查 bank_id 是否存在
                bank_id = department_data['bank_id']
                cursor.execute("SELECT COUNT(*) AS count FROM bank_bank WHERE bank_id = %s", (bank_id,))
                result = cursor.fetchone()
                if result['count'] == 0:
                    raise ValueError(f'银行ID不存在。')

                placeholders = ', '.join(['%s'] * len(department_data))
                columns = ', '.join(department_data.keys())
                sql = f"INSERT INTO bank_department ({columns}) VALUES ({placeholders})"
                cursor.execute(sql, list(department_data.values()))
                conn.commit()
        except Exception as e:
            conn.rollback()
            # 使用 JavaScript 弹窗显示错误信息
            return render(request, 'bank/add/department_add.html', {'error': str(e)})
        finally:
            conn.close()

        return redirect('../')


def employee_add(request):
    if request.method == 'GET':
        return render(request, 'bank/add/employee_add.html')
    else:
        employee_data = {
            'employee_id': request.POST.get('employee_id', ''),  # 主键
            'department_id': request.POST.get('department_id', ''),  # 外键
            'employee_name': request.POST.get('employee_name', '') or None,
            'position': request.POST.get('position', '') or None,
            'contact_phone': request.POST.get('contact_phone', '') or None,
            'email_address': request.POST.get('email_address', '') or None,
            'hire_date': request.POST.get('hire_date', '') or None,
            'salary': request.POST.get('salary', '') or None,
            'performance_rating': request.POST.get('performance_rating', '') or None,
        }

        if not employee_data['employee_id']:
            return render(request, 'bank/add/employee_add.html', {'error': '员工ID不能为空。'})

        conn = pymysql.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                # 检查 department_id 是否存在
                department_id = employee_data['department_id']
                cursor.execute("SELECT COUNT(*) AS count FROM bank_department WHERE department_id = %s", (department_id,))
                result = cursor.fetchone()
                if result['count'] == 0:
                    raise ValueError(f'部门ID不存在。')

                placeholders = ', '.join(['%s'] * len(employee_data))
                columns = ', '.join(employee_data.keys())
                sql = f"INSERT INTO bank_employee ({columns}) VALUES ({placeholders})"
                cursor.execute(sql, list(employee_data.values()))
                conn.commit()
        except Exception as e:
            conn.rollback()
            # 使用 JavaScript 弹窗显示错误信息
            return render(request, 'bank/add/employee_add.html', {'error': str(e)})
        finally:
            conn.close()

        return redirect('../')
