from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Sleek Product Management API")


products_db = {
    1:{"name": "Suede Jacket","category": "Jackets", "price": 1299, "stock": 25},
    2:{"name": "Leather Boots","category": "Shoes", "price": 899, "stock": 15},
    3:{"name": "Cotton T-Shirt","category": "Tops", "price": 399, "stock": 50},
    4:{"name":"Tank Top","category":"Tops","price":300,"stock":100},
    5:{"name":"Pleated Trousers","category":"Bottoms","price":1199,"stock":35},
    6:{"name":"Jeans","category":"Bottoms","price":1399,"stock":50},
    7:{"name":"sneakers","category":"Shoes","price":1299,"stock":40},
    8:{"name":"Flannel Shirt","category":"Tops","price":999,"stock":45},
    9:{"name":"Baggy Jeans","category":"Bottoms","price":1399,"stock":63}
}


class Product(BaseModel):
    name: str
    category: str
    price: float
    stock: int




@app.get("/products/")
def get_products(category: str = None):
    if category:
        filtered = {
            product_id: product
            for product_id, product in products_db.items()
            if product["category"].lower() == category.lower()
        }
        return filtered

    return products_db

@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id not in products_db:
        return {"error": "Product not found"}
    return products_db[product_id]


# ==========================================
# 2. CREATE (POST) - Add New Product
# ==========================================


@app.post("/products/")
def create_product(product: Product):
    new_id = max(products_db.keys(), default=0) + 1
    products_db[new_id] = product.dict()
    return {
        "message": "Product created successfully",
        "product_id": new_id,
        "data": products_db[new_id],
    }


# ==========================================
# 3. UPDATE (PUT) - Update Existing Product
# ==========================================


@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: Product):
    if product_id not in products_db:
        return {"error": "Product not found"}

    products_db[product_id] = updated_product.dict()
    return {
        "message": "Product updated successfully",
        "data": products_db[product_id],
    }


# ==========================================
# 4. DELETE (DELETE) - Remove Product
# ==========================================


@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    if product_id not in products_db:
        return {"error": "Product not found"}

    deleted = products_db.pop(product_id)
    return {"message": "Product deleted successfully", "deleted_data": deleted}
