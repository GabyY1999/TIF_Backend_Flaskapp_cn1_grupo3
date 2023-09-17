// Obtener los elementos select por su ID
const selectDia = document.getElementById('dia');
const selectMes = document.getElementById('mes');
const selectAnio = document.getElementById('anio');

// Llenar el menú desplegable de Día con opciones del 1 al 31
for (let dia = 1; dia <= 31; dia++) {
    const option = document.createElement('option');
    option.value = dia;
    option.text = dia;
    selectDia.appendChild(option);
}

// Llenar el menú desplegable de Mes con opciones de los nombres de los meses
const meses = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
];
for (let i = 0; i < meses.length; i++) {
    const option = document.createElement('option');
    option.value = i + 1;
    option.text = meses[i];
    selectMes.appendChild(option);
}

// Llenar el menú desplegable de Año con opciones de 1900 al año actual
const anioActual = new Date().getFullYear();
for (let anio = 1900; anio <= anioActual; anio++) {
    const option = document.createElement('option');
    option.value = anio;
    option.text = anio;
    selectAnio.appendChild(option);
}

