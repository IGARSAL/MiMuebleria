document.addEventListener('DOMContentLoaded', function() {
    const loading = document.getElementById('loading');
    const container = document.getElementById('card-dinamicas');
    const template = document.getElementById('template-card');

    // Verificar si los elementos están disponibles
    if (!loading || !container || !template) {
        console.error('Uno o más elementos del DOM no se encontraron.');
        return;
    }

    // Mostrar el spinner mientras se cargan los datos
    loading.classList.remove('d-none');

    fetch('tienda/productos/')
        .then(response => {
            if (!response.ok) {
                throw new Error('La respuesta de la red no fue correcta');
            }
            return response.json();
        })
        .then(data => {
            // Ocultar el spinner una vez que los datos se han cargado
            loading.classList.add('d-none');
            
            // Limpiar el contenedor antes de agregar productos
            container.innerHTML = '';

            console.log('Data received:', data); // Para verificar la estructura de los datos

            // Iterar sobre cada producto en los datos obtenidos
            data.forEach(producto => {
                console.log('Processing product:', producto); // Para verificar los datos del producto

                // Asegúrate de que los precios sean números
                const precio = parseFloat(producto.precio);
                const precioDescuento = parseFloat(producto.precio_descuento);

                // Clonar el contenido del template
                const clone = document.importNode(template.content, true);

                // Modificar el contenido del clon
                const card = clone.querySelector('.card');
                const img = card.querySelector('.card-img-top');
                const title = card.querySelector('.card-title');
                const price = card.querySelector('.lead.text-secondary');

                // Configurar la imagen
                img.src = producto.imagen1 ? producto.imagen1 : 'path/to/default-image.jpg';
                img.alt = producto.nombre;

                // Configurar el título
                title.textContent = producto.nombre;

                // Configurar el precio
                if (producto.descuento > 0) {
                    const originalPrice = document.createElement('del');
                    originalPrice.textContent = `$ ${precio.toFixed(2)}`;

                    const discountedPrice = document.createElement('span');
                    discountedPrice.textContent = ` $ ${precioDescuento.toFixed(2)}`;
                    discountedPrice.className = 'text-success';  // Añadir clase para destacar el precio con descuento

                    price.innerHTML = ''; // Limpiar el contenido anterior
                    price.appendChild(originalPrice);
                    price.appendChild(document.createElement('br'));
                    price.appendChild(discountedPrice);

                    const discount = document.createElement('span');
                    discount.className = 'lead text-secondary d-block'; // Cambiar a `span` y añadir clase para estilo
                    discount.textContent = `${producto.descuento}% Descuento`;
                    card.querySelector('.card-body').appendChild(discount);
                } else {
                    price.textContent = `$ ${precio.toFixed(2)}`;
                }

                // Añadir el clon al contenedor
                container.appendChild(clone);
            });
        })
        .catch(error => {
            // Manejar cualquier error que ocurra durante la petición fetch
            console.error('Error fetching products:', error);
            // Ocultar el spinner en caso de error también
            loading.classList.add('d-none');
        });
});



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
function deshabilitaRetroceso(){
    window.location.hash="no-back-button";
    window.location.hash="Again-No-back-button" //chrome
    window.onhashchange=function(){window.location.hash="";}
}
window.onpageshow = function(event) {
    if (event.persisted) {
        window.location.reload();  // Recargar la página al regresar
    }
};
window.onload = function() {
    document.forms[0].reset();  // Restablece el primer formulario en la página
};



