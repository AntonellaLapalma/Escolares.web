$(document).ready(function() {
    // Funcion para generar las opciones de niveles
    function generarOpcionesNiveles(selectedOption) {
        // Guarda el valor actual del segundo select
        var selectedValue = $('#selectNiveles1').val();

        // Limpia las opciones actuales del segundo select
        $('#selectNiveles1').empty();

        // Agrega la opcion en blanco al segundo select
        $('#selectNiveles1').append($('<option>', {
            value: '',
            text: ''
        }));

        // Genera las nuevas opciones basadas en el rango y nivel seleccionados
        for (var i = selectedOption.data('inicio'); i <= selectedOption.data('fin'); i++) {
            $('#selectNiveles1').append($('<option>', {
                value: i,
                text: i
            }));
        }

        // Restablece el valor seleccionado del segundo select
        $('#selectNiveles1').val(selectedValue);
    }

    // Captura el evento de cambio en el primer select
    $('#selectNivelEducativo1').on('change', function() {
        var selectedOption = $(this).find(':selected');
        generarOpcionesNiveles(selectedOption);
    });

    // Llama a la funcion inicialmente con la opcion seleccionada actualmente
    var selectedOption = $('#selectNivelEducativo1').find(':selected');
    generarOpcionesNiveles(selectedOption);
});
$(document).ready(function() {
    function generarOpcionesNiveles(selectedOption) {
        var selectedValue = $('#selectNiveles2').val();

        $('#selectNiveles2').empty();

        $('#selectNiveles2').append($('<option>', {
            value: '',
            text: ''
        }));

        for (var i = selectedOption.data('inicio'); i <= selectedOption.data('fin'); i++) {
            $('#selectNiveles2').append($('<option>', {
                value: i,
                text: i
            }));
        }

        $('#selectNiveles2').val(selectedValue);
    }

    $('#selectNivelEducativo2').on('change', function() {
        var selectedOption = $(this).find(':selected');
        generarOpcionesNiveles(selectedOption);
    });

    var selectedOption = $('#selectNivelEducativo2').find(':selected');
    generarOpcionesNiveles(selectedOption);
});
$(document).ready(function() {
    function generarOpcionesNiveles(selectedOption) {
        var selectedValue = $('#selectNiveles3').val();

        $('#selectNiveles3').empty();

        $('#selectNiveles3').append($('<option>', {
            value: '',
            text: ''
        }));

        for (var i = selectedOption.data('inicio'); i <= selectedOption.data('fin'); i++) {
            $('#selectNiveles3').append($('<option>', {
                value: i,
                text: i
            }));
        }

        $('#selectNiveles3').val(selectedValue);
    }

    $('#selectNivelEducativo3').on('change', function() {
        var selectedOption = $(this).find(':selected');
        generarOpcionesNiveles(selectedOption);
    });

    var selectedOption = $('#selectNivelEducativo3').find(':selected');
    generarOpcionesNiveles(selectedOption);
});
$(document).ready(function() {
    function generarOpcionesNiveles(selectedOption) {
        var selectedValue = $('#selectNiveles4').val();

        $('#selectNiveles4').empty();

        $('#selectNiveles4').append($('<option>', {
            value: '',
            text: ''
        }));

        for (var i = selectedOption.data('inicio'); i <= selectedOption.data('fin'); i++) {
            $('#selectNiveles4').append($('<option>', {
                value: i,
                text: i
            }));
        }

        $('#selectNiveles4').val(selectedValue);
    }

    $('#selectNivelEducativo4').on('change', function() {
        var selectedOption = $(this).find(':selected');
        generarOpcionesNiveles(selectedOption);
    });

    var selectedOption = $('#selectNivelEducativo4').find(':selected');
    generarOpcionesNiveles(selectedOption);
});
function cargarDivisiones(selectNivelEducativoId, selectDivisionId, divisionRegistrada) {
    const selectNivelEducativo = document.getElementById(selectNivelEducativoId);
    const selectDivision = document.getElementById(selectDivisionId);

    // Funcion para cargar las divisiones
    function cargarDivisionesInternas(nivelId) {
        // Envia una solicitud AJAX a Django para obtener las divisiones del nivel educativo
        fetch('/cargar-divisiones/?nivel_educativo=' + nivelId)
            .then(response => response.json())
            .then(data => {
                // Limpia las opciones actuales del tercer select
                selectDivision.innerHTML = '';

                // Agrega la opcion vacia como la primera opcion
                const optionVacia = document.createElement('option');
                optionVacia.value = ''; // Valor vacio
                optionVacia.textContent = ''; // Texto para la opcion vacia
                selectDivision.appendChild(optionVacia);

                // Agrega las nuevas opciones basadas en la respuesta de Django
                data.divisiones.forEach(division => {
                    const option = document.createElement('option');
                    option.value = division.id;
                    option.textContent = division.division;
                    selectDivision.appendChild(option);
                });

                // Si tiene una division registrada, selecciona esa opcion
                if (divisionRegistrada) {
                    selectDivision.value = divisionRegistrada;
                }

                // Habilita el tercer select
                selectDivision.removeAttribute('disabled');
            })
            .catch(error => {
                console.error('Error al cargar las divisiones:', error);
            });
    }

    // Llamar a la funcion inicialmente con la opcion seleccionada actualmente
    const nivelIdSeleccionado = selectNivelEducativo.value;
    cargarDivisionesInternas(nivelIdSeleccionado);

    // Captura el evento de cambio en el primer select
    selectNivelEducativo.addEventListener('change', function() {
        const nivelId = this.value;
        cargarDivisionesInternas(nivelId);
    });
}

// Llamar a la funcion para cargar divisiones en el momento de la carga de la pagina
document.addEventListener('DOMContentLoaded', function() {
    // Obtener el valor de la división registrada en Django
    const divisionRegistrada = document.getElementById('selectDivision1').value;
    
    // Llamar a la función para cargar divisiones y pasar la división registrada
    cargarDivisiones('selectNivelEducativo1', 'selectDivision1', divisionRegistrada);
});
document.addEventListener('DOMContentLoaded', function() {
    const divisionRegistrada = document.getElementById('selectDivision2').value;
    
    cargarDivisiones('selectNivelEducativo2', 'selectDivision2', divisionRegistrada);
});
document.addEventListener('DOMContentLoaded', function() {
    const divisionRegistrada = document.getElementById('selectDivision3').value;
    
    cargarDivisiones('selectNivelEducativo3', 'selectDivision3', divisionRegistrada);
});
document.addEventListener('DOMContentLoaded', function() {
    const divisionRegistrada = document.getElementById('selectDivision4').value;
    
    cargarDivisiones('selectNivelEducativo4', 'selectDivision4', divisionRegistrada);
});
