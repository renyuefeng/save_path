# Generated by Django 4.2.1 on 2023-08-22 06:21

from django.db import migrations, models
import django.db.models.deletion
import home.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseContractTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_time', models.DateTimeField(auto_now_add=True, db_comment='入库时间', null=True)),
                ('file_path', models.FileField(db_comment='文件', upload_to=home.models.user_directory_path)),
                ('file_name', models.CharField(blank=True, db_comment='文件名称', max_length=255, null=True)),
                ('uploader', models.CharField(blank=True, db_comment='上传人员', max_length=255, null=True)),
                ('contract_sort', models.CharField(blank=True, db_comment='合同分类', max_length=255, null=True)),
            ],
            options={
                'db_table': 'purchase_contract_time',
                'db_table_comment': '采购合同数据表入库时间表',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PurchaseContractDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(blank=True, db_comment='产品名称', max_length=255, null=True)),
                ('product_specification', models.CharField(blank=True, db_comment='产品规格', max_length=255, null=True)),
                ('unit', models.CharField(blank=True, db_comment='单位', max_length=255, null=True)),
                ('quantity', models.CharField(blank=True, db_comment='数量', max_length=255, null=True)),
                ('unit_price', models.CharField(blank=True, db_comment='单价', max_length=255, null=True)),
                ('gross_amount', models.CharField(blank=True, db_comment='总额', max_length=255, null=True)),
                ('total_amount', models.CharField(blank=True, db_comment='合计金额', max_length=255, null=True)),
                ('tax_rate', models.CharField(blank=True, db_comment='税率', max_length=255, null=True)),
                ('sole_id', models.ForeignKey(db_comment='唯一id', on_delete=django.db.models.deletion.CASCADE, related_name='purchase_contract_details', to='home.purchasecontracttime')),
            ],
            options={
                'db_table': 'purchase_contract_details',
                'db_table_comment': '采购明细表',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='PurchaseContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_number', models.CharField(blank=True, db_comment='合同编号', max_length=255, null=True)),
                ('first_party', models.CharField(blank=True, db_comment='甲方', max_length=255, null=True)),
                ('second_party', models.CharField(blank=True, db_comment='乙方', max_length=255, null=True)),
                ('place_of_signing', models.CharField(blank=True, db_comment='签订地点', max_length=255, null=True)),
                ('time_of_signing', models.DateTimeField(blank=True, db_comment='签订时间', null=True)),
                ('delivery_time', models.CharField(blank=True, db_comment='交（提）货时间', max_length=255, null=True)),
                ('delivery_place', models.CharField(blank=True, db_comment='交（提）货地点', max_length=255, null=True)),
                ('deliverer', models.CharField(blank=True, db_comment='交货人', max_length=255, null=True)),
                ('deliverer_phone', models.CharField(blank=True, db_comment='交货人联系方式', max_length=255, null=True)),
                ('payment_method', models.CharField(blank=True, db_comment='付款方式', max_length=255, null=True)),
                ('dispute_resolution_method', models.CharField(blank=True, db_comment='争议解决方式', max_length=255, null=True)),
                ('sole_id', models.ForeignKey(db_comment='唯一id', on_delete=django.db.models.deletion.CASCADE, related_name='purchase_contract', to='home.purchasecontracttime')),
            ],
            options={
                'db_table': 'purchase_contract',
                'db_table_comment': '采购合同数据表',
                'managed': True,
            },
        ),
    ]