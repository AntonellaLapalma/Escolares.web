function cargarDirecciones(selectAlumnoId, selectDireccionId, botonId) {
    const selectAlumno = document.getElementById(selectAlumnoId);
    const selectDireccion = document.getElementById(selectDireccionId);
    const boton = document.getElementById(botonId);

    // Obtén el valor seleccionado en el primer select (ID del alumno)
    const idAlumno = selectAlumno.value;

    // Envía una solicitud AJAX a Django para obtener las direcciones del alumno
    // ...

    // Ejemplo con fetch
    fetch('/cargar-direcciones/?alumno=' + idAlumno)
        .then(response => response.json())
        .then(data => {
            // Limpia las opciones actuales del segundo select
            selectDireccion.innerHTML = '<option value="" selected disabled>Seleccione una dirección</option>';

            // Agrega las nuevas opciones basadas en la respuesta de Django
            data.direcciones.forEach(direccion => {
                const option = document.createElement('option');
                option.value = direccion.id; // Asegúrate de que esto coincida con el valor que necesitas
                option.textContent = `${direccion.calle} ${direccion.altura} ${direccion.piso} ${direccion.dpto}`; // Formatea el texto correctamente
                selectDireccion.appendChild(option);
            });

            // Habilita el segundo select
            selectDireccion.removeAttribute('disabled');

        })
        .catch(error => {
            console.error('Error al cargar las direcciones:', error);
        });
}
document.getElementById('alumno1').addEventListener('change', function() {
    cargarDirecciones('alumno1', 'direccion1','btn1'); // Usar 'direccion-m' en lugar de 'direccion'
});

document.getElementById('alumno2').addEventListener('change', function() {
    cargarDirecciones('alumno2', 'direccion2'); // Usar 'direccion-md' en lugar de 'direccion'
});

document.getElementById('alumno3').addEventListener('change', function() {
    cargarDirecciones('alumno3', 'direccion3'); // Usar 'direccion-md-i' en lugar de 'direccion'
});

document.getElementById('alumno4').addEventListener('change', function() {
    cargarDirecciones('alumno4', 'direccion4'); // Usar 'direccion-t' en lugar de 'direccion'
});