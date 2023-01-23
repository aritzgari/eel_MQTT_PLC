// Botón de activar salida.
async function activarjs() {
    await eel.activarpy()();
}

// Botón de desactivar salida.
async function desactivarjs() {
    await eel.desactivarpy()();
}

// Cargar los datos que tenga el PLC.
window.onload = async function datosjs() {
    // Lanzas la función y guardas el valor en value que es una lista
    let value = await eel.datospy()();
    // Coges los elementos que quieras de la lista y los utilizas en el html mediante getElementById.
    document.getElementById('estado').innerHTML = value[0];
    document.getElementById('contador1').innerHTML = value[1];
    document.getElementById('contador2').innerHTML = value[2];
    document.getElementById('output').innerHTML = value[3];
    // https://sarfraznawaz.wordpress.com/2012/01/26/javascript-self-invoking-functions/
    setTimeout(datosjs, 500);
}

// Introduce datos desde el html a python
function input() {
    var a = document.getElementById("input").value;
    // Comprueba que sea un número
    if (isNaN(a)) {
        alert("Introduce un número.");
    } else{
        eel.inputdatos(a);
    }
}