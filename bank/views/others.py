import csv
import json

from django.db import connection
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import pymysql

from bank.models import Account, Loan, Bank


def account_transfer(request):
    if request.method == 'GET':
        return render(request, 'bank/others/account_transfer.html')
    else:
        from_account_number = request.POST.get('from_account', '')
        to_account_number = request.POST.get('to_account', '')
        amount = request.POST.get('amount', '')

        if not from_account_number or not to_account_number or not amount:
            return render(request, 'bank/others/account_transfer.html', {'error': '所有字段都是必填的。'})

        try:
            amount = float(amount)
        except ValueError:
            return render(request, 'bank/others/account_transfer.html', {'error': '转账金额必须是数字。'})

        conn = pymysql.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                # 调用存储过程
                cursor.callproc('transfer_funds', (from_account_number, to_account_number, amount))
                conn.commit()
                messages.success(request, '转账成功')

        except Exception as e:
            print(e)
            conn.rollback()
            return render(request, 'bank/others/account_transfer.html', {'error': str(e)})
        finally:
            conn.close()
        return redirect('/bank/account')


def customer_assets(request):
    if request.method == 'GET':
        return render(request, 'bank/others/customer_assets.html')
    else:
        customer_id = request.POST.get('customer_id')

        total_balance = 0
        total_loan = 0
        net_assets = 0

        # 调用函数
        with connection.cursor() as cursor:
            cursor.execute("SELECT customer_assets(%s)", [customer_id])
            result = cursor.fetchone()

            if result:
                result_json = json.loads(result[0])
                total_balance = result_json['total_balance']
                total_loan = result_json['total_loan']
                net_assets = result_json['net_assets']

        return render(request, 'bank/others/customer_assets.html', {
            'total_balance': total_balance,
            'total_loan': total_loan,
            'net_assets': net_assets,
            'customer_id': customer_id,
        })

def loan_repay(request):
    if request.method == 'GET':
        return render(request, 'bank/others/loan_repay.html')
    else:
        repayment_data = {
            'customer_id': request.POST.get('customer_id', ''),  # 还款人ID
            'account_id': request.POST.get('account_id', ''),  # 账户ID
            'loan_id': request.POST.get('loan_id', ''),  # 贷款ID
            'repayment_amount': request.POST.get('repayment_amount', '')  # 还款金额
        }

        if not repayment_data['customer_id'] or not repayment_data['account_id'] or not repayment_data['loan_id']:
            return render(request, 'bank/others/loan_repay.html', {'error': '还款人ID、账户ID和贷款ID不能为空。'})

        conn = pymysql.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                # 检查 account_id 和 loan_id 是否存在
                account_id = repayment_data['account_id']
                loan_id = repayment_data['loan_id']
                customer_id = repayment_data['customer_id']

                cursor.execute("SELECT COUNT(*) AS count FROM bank_account WHERE account_number = %s", (account_id,))
                result = cursor.fetchone()
                if result['count'] == 0:
                    raise ValueError(f'账户ID不存在。')

                cursor.execute("SELECT COUNT(*) AS count FROM bank_loan WHERE loan_id = %s", (loan_id,))
                result = cursor.fetchone()
                if result['count'] == 0:
                    raise ValueError(f'贷款ID不存在。')

                # 检查账户是否属于还款人
                cursor.execute("SELECT customer_id FROM bank_account WHERE account_number = %s", (account_id,))
                account_customer_id = cursor.fetchone()['customer_id']
                if account_customer_id != customer_id:
                    raise ValueError(f'账户ID不属于还款人。')

                # 获取当前余额和剩余还款金额
                cursor.execute("SELECT current_balance FROM bank_account WHERE account_number = %s", (account_id,))
                current_balance = float(cursor.fetchone()['current_balance'])

                cursor.execute("SELECT remaining_amount FROM bank_loan WHERE loan_id = %s", (loan_id,))
                remaining_amount = float(cursor.fetchone()['remaining_amount'])

                repayment_amount = float(repayment_data['repayment_amount'])

                if repayment_amount > current_balance:
                    raise ValueError(f'账户余额不足。')

                if repayment_amount > remaining_amount:
                    raise ValueError(f'还款金额超过剩余还款金额。')

                # 更新账户余额和贷款剩余还款金额
                new_balance = current_balance - repayment_amount
                new_remaining_amount = remaining_amount - repayment_amount

                cursor.execute("UPDATE bank_account SET current_balance = %s WHERE account_number = %s", (new_balance, account_id))
                cursor.execute("UPDATE bank_loan SET remaining_amount = %s WHERE loan_id = %s", (new_remaining_amount, loan_id))

                conn.commit()
        except Exception as e:
            conn.rollback()
            # 使用 JavaScript 弹窗显示错误信息
            return render(request, 'bank/others/loan_repay.html', {'error': str(e)})
        finally:
            conn.close()

        return redirect('/bank/loan')

def bank_dump(request):
    # 定义HTTP响应，内容类型为Excel文件
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="banks.csv"'

    # 创建CSV写入器
    writer = csv.writer(response)
    writer.writerow(['银行ID', '名称', '地址', '成立日期', '营业状态', '电话', '邮箱', '服务类型'])

    # 获取所有银行记录并写入CSV
    banks = Bank.objects.all()
    for bank in banks:
        writer.writerow([bank.bank_id, bank.bank_name, bank.bank_address, bank.established_date, bank.operational_status, bank.contact_phone, bank.contact_email, bank.service_type])

    return response