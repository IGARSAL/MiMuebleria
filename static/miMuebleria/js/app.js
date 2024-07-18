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


document.addEventListener('DOMContentLoaded', function() {
    const userTypeField = document.getElementById('id_user');  // Reemplaza con el ID de tu campo de tipo de usuario
   
    userTypeField.addEventListener('change', function() {
        if (userTypeField.value === 'premium') {
            additionalField.style.display = 'block';  // Mostrar campo adicional
        } else {
            additionalField.style.display = 'none';   // Ocultar campo adicional
        }
    });
});