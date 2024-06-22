from django.shortcuts import redirect, get_object_or_404
from bank.models import Bank, Customer, Account, Loan, Department, Employee


# 银行信息删除处理函数
def bank_delete(request):
    bank_id = request.GET.get("bank_id")
    bank = get_object_or_404(Bank, bank_id=bank_id)
    bank.delete()  # 使用 Django ORM 的删除方法
    return redirect('../')


# 客户删除处理函数
def customer_delete(request):
    customer_id = request.GET.get("customer_id")
    customer = get_object_or_404(Customer, customer_id=customer_id)
    customer.delete()  # 使用 Django ORM 的删除方法
    return redirect('../')


# 账户删除处理函数
def account_delete(request):
    account_number = request.GET.get("account_number")
    account = get_object_or_404(Account, account_number=account_number)
    account.delete()  # 使用 Django ORM 的删除方法
    return redirect('../')


# 贷款删除处理函数
def loan_delete(request):
    loan_id = request.GET.get("loan_id")
    loan = get_object_or_404(Loan, loan_id=loan_id)
    loan.delete()  # 使用 Django ORM 的删除方法
    return redirect('../')


# 部门删除处理函数
def department_delete(request):
    department_id = request.GET.get("department_id")
    department = get_object_or_404(Department, department_id=department_id)
    department.delete()  # 使用 Django ORM 的删除方法
    return redirect('../')


# 员工删除处理函数
def employee_delete(request):
    employee_id = request.GET.get("employee_id")
    employee = get_object_or_404(Employee, employee_id=employee_id)
    employee.delete()  # 使用 Django ORM 的删除方法
    return redirect('../')
