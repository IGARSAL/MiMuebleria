from django.shortcuts import redirect
from tienda.models import Producto

class Carro:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carro = self.session.get("carro")
        if not carro:
            self.carro = self.session["carro"] = {}
        else:
            self.carro = carro
    
    def agregar(self, producto):
        producto_id = str(producto.id)
        if producto_id not in self.carro:
            self.carro[producto_id] = {
                "producto_id": producto.id,
                "nombre": producto.nomProduct,
                "precio": str(producto.precio),
                "stock": 1,
                "imagen1": producto.imagen1.url
            }
        else:
            self.carro[producto_id]["stock"] += 1
            self.carro[producto_id]["precio"] = float(producto.precio)  
        self.guardar_carro()
    
    def guardar_carro(self):
        self.session["carro"] = self.carro
        self.session.modified = True
    
    def eliminar(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carro:
            del self.carro[producto_id]
            self.guardar_carro()
    
    def disminuir_producto(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carro:
            self.carro[producto_id]["stock"] -= 1
            if self.carro[producto_id]["stock"] < 1:
                self.eliminar(producto)
            else:
                self.guardar_carro()

    def obtener_cantidad(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.carro:
            return self.carro[producto_id]['stock']
        return 0


    def vaciar_carro(self):
        self.carro = {}
        self.guardar_carro()
