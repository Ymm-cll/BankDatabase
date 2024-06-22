from django.shortcuts import render
from django.db import connection
import MySQLdb

def bank_search(request):
    bank_id = request.GET.get('bank_id', '')
    bank_name = request.GET.get('bank_name', '')
    bank_address = request.GET.get('bank_address', '')
    established_date = request.GET.get('established_date', '')
    operational_status = request.GET.get('operational_status', '')
    contact_phone = request.GET.get('contact_phone', '')
    contact_email = request.GET.get('contact_email', '')
    service_type = request.GET.get('service_type', '')

    query = "SELECT * FROM bank_bank WHERE 1=1"
    params = []

    if bank_id:
        query += " AND bank_id LIKE %s"
        params.append(f"%{bank_id}%")
    if bank_name:
        query += " AND bank_name LIKE %s"
        params.append(f"%{bank_name}%")
    if bank_address:
        query += " AND bank_address LIKE %s"
        params.append(f"%{bank_address}%")
    if established_date:
        query += " AND established_date LIKE %s"
        params.append(f"%{established_date}%")
    if operational_status:
        query += " AND operational_status LIKE %s"
        params.append(f"%{operational_status}%")
    if contact_phone:
        query += " AND contact_phone LIKE %s"
        params.append(f"%{contact_phone}%")
    if contact_email:
        query += " AND contact_email LIKE %s"
        params.append(f"%{contact_email}%")
    if service_type:
        query += " AND service_type LIKE %s"
        params.append(f"%{service_type}%")

    conn = MySQLdb.connect(host="localhost", user="ymm", passwd="ym20030308", db="bank", charset='utf8')
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, params)
    banks = cursor.fetchall()
    cursor.close()
    conn.close()

    return render(request, 'bank/index/bank_index.html', {'banks': banks})