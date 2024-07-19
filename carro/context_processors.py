def importe_total_carro(request):
    total = 0
    if request.user.is_authenticated:
        carro = request.session.get("carro", {})
        for key, value in carro.items():
            total += float(value["precio"]) * value["stock"]

    return {"importe_total_carro": total}