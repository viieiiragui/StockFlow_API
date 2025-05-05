from app.infraBD.repositories.products_repositorie import ProductsRepository

def create_product(data):
    repo = ProductsRepository()

    existing = repo.select_by_name(data["name"])
    if existing:
        raise ValueError("A product with this name already exists.")

    produto = repo.insert_product(data)
    return produto

def get_all_products(name=None):
    repo = ProductsRepository()
    if name:
        return repo.select_products_by_name(name)
    return repo.select_all_products()

def get_product_by_id(id: int):
    repo = ProductsRepository()
    return repo.select_product_by_id(id)

def update_product(id: int, data: dict):
    repo = ProductsRepository()

    existing = repo.select_product_by_id(id)
    if not existing:
        raise ValueError("Product not found")

    if "name" in data:
        same_name = repo.select_by_name(data["name"])
        if same_name and same_name.id != id:
            raise ValueError("Another product with this name already exists.")

    if data.get("current_stock") is not None and data.get("add_stock") is not None:
        raise ValueError("Use only current_stock OR add_stock")

    return repo.update_product(
        id=id,
        name=data.get("name"),
        category=data.get("category"),
        current_stock=data.get("current_stock"),
        add_stock=data.get("add_stock")
    )

def delete_product(id: int):
    repo = ProductsRepository()
    deleted = repo.delete_product(id)
    
    if not deleted:
        raise ValueError("Product not found")
