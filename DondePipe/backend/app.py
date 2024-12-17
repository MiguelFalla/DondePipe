from fastapi import FastAPI, HTTPException, Request
from models import Base, User, Product, Order
from config import engine, SessionLocal

app = FastAPI()

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

@app.post('/api/admin/crearUsuario')
def create_user(request: Request):
    data = request.json()
    new_user = User(**data)
    try:
        session = SessionLocal()
        session.add(new_user)
        session.commit()
        session.close()
        return {"message": "Usuario creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/api/admin/gestionarProductos')
def manage_product(request: Request):
    data = request.json()
    new_product = Product(**data)
    try:
        session = SessionLocal()
        session.add(new_product)
        session.commit()
        session.close()
        return {"message": "Producto creado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/api/cliente/realizarPedidos')
def create_order(request: Request):
    data = request.json()
    new_order = Order(**data)
    try:
        session = SessionLocal()
        session.add(new_order)
        session.commit()
        session.close()
        return {"message": "Pedido realizado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post('/api/cajero/aceptarPagos')
def accept_payment(request: Request):
    data = request.json()
    new_payment = Order(**data)
    try:
        session = SessionLocal()
        session.add(new_payment)
        session.commit()
        session.close()
        return {"message": "Pago aceptado y boleta emitida"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.get('/api/cajero/pedidosActivos')
def get_active_orders():
    try:
        session = SessionLocal()
        active_orders = session.query(Order).filter(Order.details.isnot(None)).all()
        session.close()
        return {"orders": active_orders}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post('/api/cliente/gestionarPerfil')
def manage_profile(request: Request):
    data = request.json()
    try:
        session = SessionLocal()
        user = session.query(User).filter(User.id == data.get("id")).first()
        if user:
            user.username = data.get("username")
            user.password = data.get("password")
            session.commit()
            session.close()
            return {"message": "Perfil actualizado exitosamente"}
        else:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

@app.get('/api/cliente/historialPedidos')
def get_order_history(request: Request):
    user_id = request.query_params.get('user_id')
    try:
        session = SessionLocal()
        order_history = session.query(Order).filter(Order.user_id == user_id).all()
        session.close()
        return {"orders": order_history}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Más rutas para otros roles...