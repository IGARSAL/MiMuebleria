document.addEventListener('DOMContentLoaded', () => {
    fetchData();
});

const fetchData = async () => {
    try {
        loadingData(true);
        const res = await fetch("productos/", {
            headers: {
                'Accept': 'application/json'
            }
        });
        if (!res.ok) {
            throw new Error('La red no respode');
        }
        const data = await res.json();
        const productos = JSON.parse(data); // Parse the JSON string into an object
        mostrarCard(productos);
    } catch (error) {
        console.error('Error en la obtención de datos:', error);
    } finally {
        loadingData(false);
    }
};

const mostrarCard = (productos) => {
    const cards = document.getElementById("card-dinamicas");
    const templateCard = document.getElementById("template-card").content;
    const fragment = document.createDocumentFragment();
    const mediaUrl = document.body.getAttribute('data-media-url');

    productos.forEach((producto) => {
        const clone = templateCard.cloneNode(true);
        const precioOriginal = parseFloat(producto.fields.precio);
        const descuento = parseFloat(producto.fields.descuento);
        const precioDescuento = parseFloat(producto.fields.descuento);
        const imagen1Url = producto.fields.imagen1 ? `${mediaUrl}${producto.fields.imagen1}` : '/path/to/default-image.jpg';
        if (descuento > 0) {
            const precioDescuento = (precioOriginal * (1 - descuento / 100)).toFixed(2);
            clone.querySelector("p").textContent = `Precio: $${precioOriginal} - Precio con descuento: $${precioDescuento}`;
            clone.querySelector("a").textContent = `${descuento}% Descuento`;
        } else {
            clone.querySelector("p").textContent = `Precio: $${precioOriginal}`;
            clone.querySelector("a").textContent = '';

        }
        clone.querySelector("h5").textContent = producto.fields.nomProduct;
        clone.querySelector(".card-img-top").setAttribute("src", imagen1Url);
        fragment.appendChild(clone);
    });
    cards.appendChild(fragment);
};

const loadingData = (estado) => {
    const loading = document.getElementById("loading");
    if (estado) {
        loading.classList.remove("d-none");
    } else {
        loading.classList.add("d-none");
    }
};

document.getElementById('pdfout').onclick = function (event) {
    event.preventDefault(); // Evitar la acción predeterminada del enlace

    try {
        var table = document.querySelector('.mitabla');
        var rows = [];

        // Obtener las filas de datos de la tabla
        for (var i = 0; i < table.rows.length; i++) {
            var row = [];

            for (var j = 1; j < table.rows[i].cells.length; j++) {
                var contenido = table.rows[i].cells[j].textContent;
                row.push(contenido);
            }
            rows.push(row);
        }

        // Obtener el importe total del carrito
        var total = document.querySelector('.total_carro').textContent;

        var docDefinition = {
            content: [
                {text: 'Resumen del pedido', style: 'header', alignment: 'center'}, // Centra el título
                {
                    table: {
                        headerRows: 1, // Solo una fila como encabezado
                        widths: ['*', '*', '*'], // Distribuye uniformemente el ancho de las columnas
                        body: [
                            [{text: 'Producto', style: 'tableHeader', alignment: 'center'}, {text: 'Cantidad', style: 'tableHeader', alignment: 'center'}, {text: 'Sub-Total', style: 'tableHeader', alignment: 'center'}], // Encabezado de las columnas
                            ...rows // Filas de datos
                        ]
                    },
                    alignment: 'center' // Centra la tabla
                },
                {text: total, style: 'total', alignment: 'right'} //Inserta el total
            ],
            styles: {
                header: {fontSize: 18, bold: true, margin: [0, 0, 0, 10]},
                footer: {fontSize: 10, italic: true},
                total: {fontSize: 14, bold: true, margin: [0, 10, 0, 0]},
                tableHeader: { bold: true, fillColor: '#CCCCCC' } // Estilo para los encabezados de la tabla
            }
        };

        // Mostrar docDefinition en la consola
        console.log(docDefinition);

        // Crear el PDF
        pdfMake.createPdf(docDefinition).download('Compra.pdf');
    } catch (error) {
        console.error("Error en la generación del PDF:", error);
        alert("Error en la generación del PDF. Consulta la consola para más detalles.");
    }
};
