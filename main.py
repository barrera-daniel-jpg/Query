# 1. IMPORTACIONES
# Importamos la clase FastAPI para crear nuestra aplicación web
from fastapi import FastAPI, HTTPException, Query

# Importamos BaseModel de Pydantic para definir la estructura de validación de datos.
from pydantic import BaseModel

# 2. INICIALIZACIÓN DE LA APLICACIÓN

# Creamos la instancia principal de la aplicación FastAPI.
app = FastAPI(
    title="API de Tienda Deportiva",
    description="CRUD completo de productos con filtros y validación usando Pydantic",
    version="1.0.0",
)


# 3. MODELOS DE DATOS (ESQUEMAS PYDANTIC)


# Definimos la estructura que deben tener los productos que recibimos vía JSON en el cuerpo de las peticiones (Request Body).
# Pydantic validará automáticamente que los tipos de datos sean correctos.
class Product(BaseModel):
    id: int  # El ID debe ser un número entero
    name: str  # El nombre debe ser una cadena de texto
    price: float  # El precio debe ser un número decimal
    quantity: int  # La cantidad en inventario debe ser un entero
    category: str  # La categoría debe ser texto


# 4. BASE DE DATOS SIMULADA (EN MEMORIA)

# Una lista de diccionarios que simula la base de datos de una tienda de deportes.
products = [
    {
        "id": 1,
        "name": "Balón de Fútbol N° 5",
        "price": 29.99,
        "quantity": 15,
        "category": "Fútbol",
    },
    {
        "id": 2,
        "name": "Zapatillas Running Trail",
        "price": 89.50,
        "quantity": 8,
        "category": "Calzado",
    },
    {
        "id": 3,
        "name": "Raqueta de Tenis Pro",
        "price": 120.00,
        "quantity": 5,
        "category": "Tenis",
    },
    {
        "id": 4,
        "name": "Tapete de Yoga Antideslizante",
        "price": 22.00,
        "quantity": 20,
        "category": "Fitness",
    },
    {
        "id": 5,
        "name": "Mancuernas Hexagonales 5kg (Par)",
        "price": 35.00,
        "quantity": 12,
        "category": "Gimnasio",
    },
    {
        "id": 6,
        "name": "Gafas de Natación Anti-empañamiento",
        "price": 15.50,
        "quantity": 25,
        "category": "Natación",
    },
    {
        "id": 7,
        "name": "Bicicleta de Montaña R29",
        "price": 450.00,
        "quantity": 3,
        "category": "Ciclismo",
    },
    {
        "id": 8,
        "name": "Camiseta Térmica Transpirable",
        "price": 24.99,
        "quantity": 18,
        "category": "Ropa Deportiva",
    },
    {
        "id": 9,
        "name": "Cuerda para Saltar de Alta Velocidad",
        "price": 12.00,
        "quantity": 30,
        "category": "Fitness",
    },
    {
        "id": 10,
        "name": "Casco de Ciclismo Ligero",
        "price": 42.00,
        "quantity": 10,
        "category": "Ciclismo",
    },
]


# 5. RUTAS DE LA API (ENDPOINTS DEL CRUD)


# --- ENDPOINT GET (OBTENER PRODUCTOS / FILTRAR) ---
# Permite obtener la lista de productos.
# Acepta los Query Parameters opcionales 'category' (para filtrar) y 'limit' (para acotar el total devuelto).
@app.get("/products", summary="Obtener todos los productos o filtrar")
def get_products(
    category: str | None = Query(
        default=None, description="Filtrar por categoría"
    ), #Query() Es una funcion que nos permite configurar un Query Parameter
    limit: int = Query(
        default=10, ge=1, le=50, description="Límite entre 1 y 50"
    ),
):
    # Asignamos la lista inicial
    result = products

    # Si se pasa el parámetro opcional 'category' en la URL (ej: /products?category=Fitness)
    if category:
        result = [
            prod
            for prod in result
            if prod["category"].lower() == category.lower()
        ]

    # Retornamos la lista filtrada acotada por el parámetro 'limit'
    return result[:limit]


# --- ENDPOINT GET POR ID (OBTENER UN SOLO PRODUCTO) ---
# Busca un producto específico usando su ID recibido en la ruta (Path Parameter).
@app.get("/products/{product_id}", summary="Obtener producto por ID")
def get_product(product_id: int):
    for prod in products:
        if prod["id"] == product_id:
            return prod

    # Si no encuentra el producto, lanza un error HTTP 404
    raise HTTPException(status_code=404, detail="Producto no encontrado")


# --- ENDPOINT POST (CREAR PRODUCTO) ---
# Recibe los datos de un nuevo producto en el cuerpo de la petición (JSON) gracias al modelo Product.
@app.post("/products", summary="Crear un nuevo producto")
def create_product(product: Product):
    # .model_dump() convierte el objeto Pydantic a un diccionario nativo de Python
    new_prod_dict = product.model_dump()

    # Agregamos el diccionario a la lista de productos
    products.append(new_prod_dict)

    return {
        "message": "Producto creado exitosamente",
        "product": new_prod_dict,
    }


# --- ENDPOINT PUT (ACTUALIZAR PRODUCTO COMPLETO) ---
# Recibe el ID del producto a actualizar por la URL y el objeto con los datos nuevos en el cuerpo JSON.
@app.put("/products/{product_id}", summary="Actualizar un producto existente")
def update_product(product_id: int, new_data: Product):
    for i, prod in enumerate(products):
        if prod["id"] == product_id:
            # Reemplazamos el diccionario en la posición 'i' por el nuevo
            products[i] = new_data.model_dump()
            return {
                "message": "Producto actualizado correctamente",
                "product": products[i],
            }

    raise HTTPException(status_code=404, detail="Producto no encontrado")


# --- ENDPOINT DELETE (ELIMINAR PRODUCTO) ---
# Recibe el ID en la ruta y elimina el producto correspondiente de la lista.
@app.delete("/products/{product_id}", summary="Eliminar un producto por ID")
def delete_product(product_id: int):
    for prod in products:
        if prod["id"] == product_id:
            products.remove(prod)
            return {
                "message": "Producto eliminado exitosamente",
                "products": products,
            }

    raise HTTPException(status_code=404, detail="Producto no encontrado")