from app.infraBD.repositories.products_repositorie import ProductsRepository

def create_product(data):
    repo = ProductsRepository()

    existing = repo.select_by_name(data["name"])
    if existing:
        raise ValueError("A product with this name already exists.")

    produto = repo.insert_product(data)
    return produto

def get_all_products():
    repo = ProductsRepository()
    return repo.select_all_products()

def get_product_by_id(id: int):
    repo = ProductsRepository()
    return repo.select_product_by_id(id)
