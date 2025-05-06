from app.infraDB.repositories.products_repositorie import ProductsRepository

def create_product(data):
    repo = ProductsRepository()

    if "name" in data:
        data["name"] = data["name"].strip().title()

    if "category" in data:
        data["category"] = data["category"].strip().title()

    existingCode = repo.select_by_code(data["code"])
    if existingCode:
        raise ValueError("A product with this code already exists.")

    existing = repo.select_by_name(data["name"])
    if existing:
        raise ValueError("A product with this name already exists.")

    produto = repo.insert_product(data)
    return produto

def get_all_products(name=None, code=None):
    repo = ProductsRepository()

    if code:
        product = repo.select_by_code(code)
        return [product] if product else []

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
        data["name"] = data["name"].strip().title()
        same_name = repo.select_by_name(data["name"])
        if same_name and same_name.id != id:
            raise ValueError("Another product with this name already exists.")
    
    if "category" in data:
        data["category"] = data["category"].strip().title()

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
