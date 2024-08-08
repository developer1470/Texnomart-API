import os 
import json
from core.settings import BASE_DIR
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from texnomart.models import Category, Product
from django.core.mail import send_mail
from core.settings import DEFAULT_FROM_EMAIL


@receiver(pre_delete, sender=Category)
def pre_delete_category(sender, instance, **kwargs):
    file_path = os.path.join(BASE_DIR, 'texnomart/category', f'category {instance.id}.json')

    category_data = {
        'id': instance.id,
        'category_name': instance.category_name,
        'slug': instance.slug,
    }

    with open(file_path, 'w') as json_file:
        json.dump(category_data, json_file, indent=4)
    print('Category saved json file before deleted .')



@receiver(post_save, sender=Category)
def post_save_category(sender, instance, created, **kwargs):
    if created:
        print('Category cretaed...')
        subject = 'Category create'
        message = 'Sent message data from category'
        from_mail = DEFAULT_FROM_EMAIL
        to = 'jasurmavlonov24@gmail.com'
        send_mail(subject, message, from_mail, [to], fail_silently=False)
    else:
        print('Category updated')



def post_save_product(sender, instance, created, **kwargs):
    if created:
        print(f"Product created: {instance.product_name} ")
    else:
        print(f'Category  updated: {instance.product_name}   ')

post_save.connect(post_save_product, sender=Product)





@receiver(pre_delete, sender=Product)
def pre_delete_product(sender, instance, **kwargs):
    file_path = os.path.join(BASE_DIR, 'texnomart/product', f'product {instance.id}.json')

    product_data = {
        'id': instance.id,
        'product_name': instance.product_name,
        'slug': instance.slug,
    }

    with open(file_path, 'w') as json_file:
        json.dump(product_data, json_file, indent=4)
    print('Product saved json file and deleted .')


@receiver(post_save, sender=Product)
def post_save_product(sender, instance, created, **kwargs):
    if created:
        print('Product cretaed...')
        subject = 'Product create'
        message = 'Sent message data from product'
        from_mail = DEFAULT_FROM_EMAIL
        to = 'jasurmavlonov24@gmail.com'
        send_mail(subject, message, from_mail, [to], fail_silently=False)
    else:
        print('Product created...')