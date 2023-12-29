import re

from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from .models import PurchaseContract, PurchaseContractTime

# 主页详情信息 + 搜索
@require_http_methods(['GET'])
def show_contract_message(requeset):
    lis = []
    # 加载
    # file_dir = list(PurchaseContract.objects.all().values('id', 'contract_number', 'first_party', 'second_party', 'sole_id'))
    # file_dir = list(PurchaseContractTime.objects.all().values('id', 'upload_time', 'contract_number', 'first_party', 'second_party', 'sole_id'))
    pur_obj = PurchaseContract.objects.all().order_by('-sole_id_id')
    # .values('contract_number', 'first_party', 'second_party', 'sole_id')
    for i in pur_obj:
        file_dir = {}
        file_dir['contract_number'] = i.contract_number
        file_dir['first_party'] = i.first_party
        file_dir['second_party'] = i.second_party
        file_dir['sole_id'] = i.sole_id.id
        file_dir['id'] = i.id
        file_dir['upload_time'] = i.sole_id.upload_time.strftime('%Y-%m-%d')
        lis.append(file_dir)
    file_dir = lis
    # print(lis)
    # 搜索
    data = requeset.GET
    print('data', data)
    if data:
        pattern = re.compile('^ +| +$')
        file_dir = []
        # print(data)
        # print(data.get('first_party', ''))
        # if requeset.body.contract_number:
        contract_number = pattern.sub('', data.get('contract_number', ''))
        first_party = pattern.sub('', data.get('first_party', ''))
        second_party = pattern.sub('', data.get('second_party', ''))
        # first_party = data.get('first_party', '')
        # second_party = data.get('second_party', '')
        starttime = data.get('upload_time[0]', '')
        endtime = data.get('upload_time[1]', '')
        # print(upload_time)
        sql = 'SELECT * from((SELECT id, upload_time from purchase_contract_time) A LEFT JOIN(SELECT contract_number, first_party, second_party, sole_id_id from purchase_contract) B ON A.id=B.sole_id_id)'
        if contract_number or first_party or second_party or starttime or endtime:
            sql = sql + ' where '
            if contract_number:
                sql = sql + 'contract_number like "%%{}%%" and '.format(contract_number)
            if first_party:
                sql = sql + 'first_party like "%%{}%%" and '.format(first_party)
            if second_party:
                sql = sql + 'second_party like "%%{}%%" and '.format(second_party)
            if starttime and endtime:
                sql = sql + 'upload_time between "{a} 00:00:00" and "{b} 23:59:59" and '.format(a=starttime, b=endtime)
        pattern = re.compile(' *and *$')
        sql = pattern.sub('', sql)
        sql = sql + ' ORDER BY A.upload_time desc'
        print(sql)
        # file_dir_all = PurchaseContract.objects.raw('select id, contract_number, first_party, second_party, sole_id_id from purchase_contract where contract_number like "%%{a}%%" and first_party like "%%{b}%%" and second_party like "%%{c}%%";'.format(a=contract_number, b=first_party, c=second_party))
        file_dir_all = PurchaseContract.objects.raw(sql)
        if file_dir_all:
            for i in file_dir_all:
                dic = {}
                dic['id'] = i.id
                dic['sole_id'] = i.id
                dic['contract_number'] = i.contract_number
                dic['first_party'] = i.first_party
                dic['second_party'] = i.second_party
                dic['upload_time'] = i.upload_time.strftime('%Y-%m-%d')
                file_dir.append(dic)
    return JsonResponse(file_dir, safe=False)

@require_http_methods(['GET'])
def show_title_message(requeset):
    dic_output = {}
    # lis_id = []
    lis_first_party = []
    lis_second_party = []
    file_dir = PurchaseContract.objects.all()
    for i in file_dir:
        # lis_id.append(i.id)
        lis_first_party.append(i.first_party)
        lis_second_party.append(i.second_party)
    # dic_output['id'] = lis_id
    dic_output['first_party'] = list(set(lis_first_party))
    dic_output['second_party'] = list(set(lis_second_party))
    return JsonResponse(dic_output, safe=False)

# @require_http_methods(['POST'])
# def search_message(requeset):
#     data = requeset.body
#     # if
#     file_name = PurchaseContract.objects.get(id=data.id).file_path



def contractMakeSure(request):

    # contract_info = PurchaseContract.objects.get()

    if request.method == 'POST':
        contract_number = request.POST.get('contract_number')
        first_party = request.POST.get('first_party')
        second_party = request.POST.get('second_party')
        place_of_signing = request.POST.get('place_of_signing')
        time_of_signing = request.POST.get('time_of_signing')
        delivery_time = request.POST.get('delivery_time')
        delivery_place = request.POST.get('delivery_place')
        deliverer = request.POST.get('deliverer')
        deliverer_phone = request.POST.get('deliverer_phone')
        payment_method = request.POST.get('payment_method')
        dispute_resolution_method = request.POST.get('payment_method')

        # 获取模型的实例
        contract_info = PurchaseContract.objects.get(contract_number=contract_number)

        # 修改属性

        contract_info.first_party = first_party
        contract_info.second_party = second_party
        # contract_info.place_of_signing = place_of_signing
        # contract_info.time_of_signing = time_of_signing
        # contract_info.delivery_time = delivery_time
        # contract_info.delivery_place = delivery_place
        # contract_info.deliverer = deliverer
        # contract_info.deliverer_phone = deliverer_phone
        # contract_info.payment_method = payment_method
        # contract_info.dispute_resolution_method = dispute_resolution_method

        # 保存修改
        contract_info.save()

    return JsonResponse()
