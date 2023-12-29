# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from time import strftime

from django.db import models
import uuid
from smart_contract_manager.settings import MEDIA_ROOT

def user_directory_path(a, b):
    print(a, b)
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'{strftime("%Y-%m-%d")}/{uuid.uuid4()}{b}'

class PurchaseContractTime(models.Model):
    # contract_number = models.CharField(max_length=255, blank=True, null=True, db_comment='合同编号')
    # sole_id = models.CharField(max_length=36, default=uuid.uuid4, db_comment='唯一id')
    upload_time = models.DateTimeField(blank=True, null=True, auto_now_add=True, db_comment='入库时间')
    file_path = models.FileField(upload_to=user_directory_path, db_comment='文件')
    file_name = models.CharField(max_length=255, blank=True, null=True, db_comment='文件名称')
    uploader = models.CharField(max_length=255, blank=True, null=True, db_comment='上传人员')
    contract_sort = models.CharField(max_length=255, blank=True, null=True, db_comment='合同分类')
    # remake = models.CharField(max_length=255, blank=True, null=True, db_comment='备注')

    class Meta:
        managed = True
        db_table = 'purchase_contract_time'
        db_table_comment = '采购合同数据表入库时间表'

class PurchaseContract(models.Model):
    sole_id = models.ForeignKey('PurchaseContractTime', on_delete=models.CASCADE, related_name='purchase_contract', db_comment='唯一id')
    contract_number = models.CharField(max_length=255, blank=True, null=True, db_comment='合同编号')
    first_party = models.CharField(max_length=255, blank=True, null=True, db_comment='甲方')
    second_party = models.CharField(max_length=255, blank=True, null=True, db_comment='乙方')
    place_of_signing = models.CharField(max_length=255, blank=True, null=True, db_comment='签订地点')
    time_of_signing = models.DateTimeField(blank=True, null=True, db_comment='签订时间')
    delivery_time = models.CharField(max_length=255, blank=True, null=True, db_comment='交（提）货时间')
    delivery_place = models.CharField(max_length=255, blank=True, null=True, db_comment='交（提）货地点')
    deliverer = models.CharField(max_length=255, blank=True, null=True, db_comment='交货人')
    deliverer_phone = models.CharField(max_length=255, blank=True, null=True, db_comment='交货人联系方式')
    payment_method = models.CharField(max_length=255, blank=True, null=True, db_comment='付款方式')
    dispute_resolution_method = models.CharField(max_length=255, blank=True, null=True, db_comment='争议解决方式')

    class Meta:
        managed = True
        db_table = 'purchase_contract'
        db_table_comment = '采购合同数据表'


class PurchaseContractDetails(models.Model):
    sole_id = models.ForeignKey('PurchaseContractTime', on_delete=models.CASCADE, related_name='purchase_contract_details', db_comment='唯一id')
    # contract_number = models.CharField(max_length=255, blank=True, null=True, db_comment='合同编号')
    product_name = models.CharField(max_length=255, blank=True, null=True, db_comment='产品名称')
    product_specification = models.CharField(max_length=255, blank=True, null=True, db_comment='产品规格')
    unit = models.CharField(max_length=255, blank=True, null=True, db_comment='单位')
    quantity = models.CharField(max_length=255, blank=True, null=True, db_comment='数量')
    unit_price = models.CharField(max_length=255, blank=True, null=True, db_comment='单价')
    gross_amount = models.CharField(max_length=255, blank=True, null=True, db_comment='总额')
    total_amount = models.CharField(max_length=255, blank=True, null=True, db_comment='合计金额')
    tax_rate = models.CharField(max_length=255, blank=True, null=True, db_comment='税率')

    class Meta:
        managed = True
        db_table = 'purchase_contract_details'
        db_table_comment = '采购明细表'


class ContractSortFeature(models.Model):
    sort_name = models.CharField(max_length=255, blank=True, null=True, db_comment='分类名称')
    word_name = models.CharField(max_length=255, blank=True, null=True, db_comment='字段名称')
    feature = models.CharField(max_length=255, blank=True, null=True, db_comment='特征')

    class Meta:
        managed = True
        db_table = 'contract_sort_feature'
        db_table_comment = '分类特征表'


# class PurchaseContractExamine(models.Model):
#     sole_id = models.ForeignKey('PurchaseContractTime', on_delete=models.CASCADE, related_name='purchase_contract_examine', db_comment='唯一id')
#     # contract_number = models.CharField(max_length=255, blank=True, null=True, db_comment='合同编号')
#     upload_time = models.DateTimeField(blank=True, null=True, auto_now_add=True, db_comment='入库时间')
#
#     class Meta:
#         managed = True
#         db_table = 'purchase_contract_examine'
#         db_table_comment = '采购审查表'

