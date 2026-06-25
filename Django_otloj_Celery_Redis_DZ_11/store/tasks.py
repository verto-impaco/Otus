from celery import shared_task


@shared_task
def log_product_created(product_id, product_name):
    message = f"Новый товар добавлен: {product_name} (ID: {product_id})"
    print(message, flush=True)
    return message
