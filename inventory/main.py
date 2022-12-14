from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from decouple import config

REDIS_HOST = config('REDIS_HOST')
REDIS_PORT = config('REDIS_PORT')
REDIS_PASSWORD = config('REDIS_PASSWORD')


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*'],

)

# microservices have unique database
redis = get_redis_connection(
    host=REDIS_HOST,
    port=int(REDIS_PORT),
    password=REDIS_PASSWORD,
    decode_responses=True
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


def format(pk: str):
    product = Product.get(pk)
    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }


@app.get('/products')
def all():
    return [format(pk) for pk in Product.all_pks()]


@app.post("/products")
def create(product: Product):
    return product.save()


@app.get('/products/{pk}')
def get(pk: str):
    return Product.get(pk)


@app.delete('/products/{pk}')
def get(pk: str):
    return Product.delete(pk)
