# Generated by Django 4.2.10 on 2024-02-28 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(blank=True, default=False)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed')], default='pending', max_length=15)),
                ('payment_method', models.CharField(choices=[('paypal', 'PayPal'), ('credit_card', 'Credit Card'), ('bank_transfer', 'Bank Transfer')], default='paypal', max_length=15)),
                ('transaction_id', models.CharField(blank=True, max_length=63, null=True)),
                ('is_paid', models.BooleanField(blank=True, default=False)),
                ('cart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='payments', to='cart.cart')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
    ]
