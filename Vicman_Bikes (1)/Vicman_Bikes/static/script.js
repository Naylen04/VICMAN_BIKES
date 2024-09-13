function inicializarCarrusel(carruselSelector, productoSelector, prevSelector, nextSelector, productosPorSlide) {
    const carrusel = document.querySelector(carruselSelector);
    const productos = document.querySelectorAll(productoSelector);
    const prevButton = document.querySelector(prevSelector);
    const nextButton = document.querySelector(nextSelector);

    let currentIndex = 0;

    function updateCarrusel() {
        const offset = -currentIndex * (100 / productosPorSlide);
        carrusel.style.transform = `translateX(${offset}%)`;
    }

    prevButton.addEventListener('click', function () {
        if (currentIndex > 0) {
            currentIndex -= productosPorSlide;
        } else {
            currentIndex = Math.floor((productos.length - 1) / productosPorSlide) * productosPorSlide;
        }
        updateCarrusel();
    });

    nextButton.addEventListener('click', function () {
        if (currentIndex < productos.length - productosPorSlide) {
            currentIndex += productosPorSlide;
        } else {
            currentIndex = 0;
        }
        updateCarrusel();
    });

    updateCarrusel();
}

// Llamada para inicializar el carrusel de ofertas
inicializarCarrusel('.carruselOfertas', '.producto', '.prev', '.next', 4);

// Llamada para inicializar el carrusel de productos destacados (ejemplo)
inicializarCarrusel('.carruselDestacados', '.productoDestacado', '.prevDestacados', '.nextDestacados', 4);

// Funcion subpestañas
function mostrarInfo(numProducto) {
    document.getElementById("infoProducto" + numProducto).style.display = "block";
}

function cerrarInfo(numProducto) {
    document.getElementById("infoProducto" + numProducto).style.display = "none";
}