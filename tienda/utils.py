from decimal import Decimal, ROUND_HALF_UP

def calcular_precio_descuento(producto):
    if producto.descuento > 0:
        descuento_decimal = Decimal(producto.descuento) / Decimal(100)
        precio_descuento = (producto.precio * (Decimal(1) - descuento_decimal)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    else:
        precio_descuento = producto.precio
    return precio_descuento

