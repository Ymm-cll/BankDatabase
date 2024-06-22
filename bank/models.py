from django.db import models


# 银行信息模型
class Bank(models.Model):
    bank_id = models.CharField(primary_key=True, max_length=32)  # 银行ID（唯一标识）
    bank_name = models.CharField(max_length=255, null=True, blank=True)  # 银行名称
    bank_address = models.CharField(max_length=255, null=True, blank=True)  # 银行地址
    established_date = models.DateField(null=True, blank=True)  # 成立日期
    operational_status = models.CharField(max_length=50, null=True, blank=True)  # 营业状态（如营业中、已关闭等）
    contact_phone = models.CharField(max_length=50, null=True, blank=True)  # 银行联系方式（电话）
    contact_email = models.EmailField(null=True, blank=True)  # 银行联系方式（邮箱）
    service_type = models.CharField(max_length=100, null=True, blank=True)  # 银行服务类型（如商业服务、个人服务等）

    def __str__(self):
        return self.bank_name


# 客户信息模型
class Customer(models.Model):
    customer_id = models.CharField(primary_key=True, max_length=32)  # 客户ID（唯一标识）
    customer_name = models.CharField(max_length=255, null=True, blank=True)  # 客户姓名
    customer_gender = models.CharField(max_length=10, null=True, blank=True)  # 客户性别
    birth_date = models.DateField(null=True, blank=True)  # 客户出生日期
    occupation = models.CharField(max_length=100, null=True, blank=True)  # 客户职业
    contact_address = models.CharField(max_length=255, null=True, blank=True)  # 联系地址
    contact_phone = models.CharField(max_length=50, null=True, blank=True)  # 联系电话
    contact_email = models.EmailField(null=True, blank=True)  # 联系邮箱
    customer_level = models.CharField(max_length=50, null=True, blank=True)  # 客户级别（如普通、VIP等）
    photo_filename = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.customer_name


# 账户信息模型
class Account(models.Model):
    account_number = models.CharField(primary_key=True, max_length=32)  # 账户号码（唯一标识）
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)  # 客户ID（关联客户信息）
    account_type = models.CharField(max_length=50, null=True, blank=True)  # 账户类型（储蓄账户，支票账户等）
    opening_date = models.DateField(null=True, blank=True)  # 开户日期
    account_status = models.CharField(max_length=50, null=True, blank=True)  # 账户状态（激活，冻结，关闭）
    current_balance = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  # 当前余额
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # 存款利率（针对储蓄账户）
    overdraft_limit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  # 透支限额（针对支票账户）

    def __str__(self):
        return self.account_number


# 贷款信息模型
class Loan(models.Model):
    loan_id = models.CharField(primary_key=True, max_length=32)  # 贷款ID（唯一标识）
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)  # 客户ID（关联客户信息）
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  # 贷款金额
    disbursement_date = models.DateField(null=True, blank=True)  # 贷款发放日期
    due_date = models.DateField(null=True, blank=True)  # 到期日期
    loan_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # 贷款利率
    loan_status = models.CharField(max_length=50, null=True, blank=True)  # 贷款状态（发放中，还款中，已结清）
    remaining_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  # 剩余还款金额

    def __str__(self):
        return str(self.loan_id)


# 银行部门信息模型
class Department(models.Model):
    department_id = models.CharField(primary_key=True, max_length=32)  # 部门ID（唯一标识）
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, null=True)  # 所属银行ID（关联银行信息）
    department_name = models.CharField(max_length=100, null=True, blank=True)  # 部门名称
    responsibilities = models.TextField(null=True, blank=True)  # 部门职责描述
    location = models.CharField(max_length=255, null=True, blank=True)  # 部门位置
    contact_phone = models.CharField(max_length=50, null=True, blank=True)  # 部门联系电话
    manager = models.ForeignKey('Employee', null=True, blank=True, on_delete=models.SET_NULL,
                                related_name='manages')  # 部门经理（关联员工信息）

    def __str__(self):
        return self.department_name


# 员工信息模型
class Employee(models.Model):
    employee_id = models.CharField(primary_key=True, max_length=32)  # 员工ID（唯一标识）
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees', null=True)  # 所属部门ID（关联银行部门信息）
    employee_name = models.CharField(max_length=255, null=True, blank=True)  # 员工姓名
    position = models.CharField(max_length=100, null=True, blank=True)  # 职位
    contact_phone = models.CharField(max_length=50, null=True, blank=True)  # 联系电话
    email_address = models.EmailField(null=True, blank=True)  # 邮箱地址
    hire_date = models.DateField(null=True, blank=True)  # 入职日期
    salary = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  # 工资
    performance_rating = models.CharField(max_length=50, null=True, blank=True)  # 绩效评级

    def __str__(self):
        return self.employee_name
