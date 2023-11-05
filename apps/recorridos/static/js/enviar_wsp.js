// Define una función que toma dos parámetros: numero y mensaje
function enviarWhatsApp(numero, mensaje) {
    // Codificar el mensaje para que sea seguro en una URL
    var mensajeCodificado = encodeURIComponent(mensaje);
    
    // Crear el enlace de WhatsApp con el número y mensaje
    var enlaceWhatsApp = 'https://wa.me/540' + numero + '?text=' + mensaje;
    
    // Abrir WhatsApp en una nueva ventana o pestaña
    window.open(enlaceWhatsApp);
}

document.getElementById('enviar-por-whatsapp-chofer-mi').addEventListener('click', function() {
    // Obtener el número de teléfono al que deseas enviar el mensaje
    var numeroTelefono = document.getElementById('celular-input-chofer').value;  // Obtiene el valor del input oculto
    
    // Obtener el contenido del mensaje
    var mensaje = document.getElementById('lista-pasajeros-wsp-chofer-mi').value;
    
    // Llamar a la función con los parámetros
    enviarWhatsApp(numeroTelefono, mensaje);
});
document.getElementById('enviar-por-whatsapp-celador-mi').addEventListener('click', function() {
    // Obtener el número de teléfono al que deseas enviar el mensaje
    var numeroTelefono = document.getElementById('celular-input-celador').value;  // Obtiene el valor del input oculto
    
    // Obtener el contenido del mensaje
    var mensaje = document.getElementById('lista-pasajeros-wsp-celador-mi').value;
    
    // Llamar a la función con los parámetros
    enviarWhatsApp(numeroTelefono, mensaje);
});

document.getElementById('enviar-por-whatsapp-chofer-mds').addEventListener('click', function() {
    // Obtener el número de teléfono al que deseas enviar el mensaje
    var numeroTelefono = document.getElementById('celular-input-chofer').value;  // Obtiene el valor del input oculto
    
    // Obtener el contenido del mensaje
    var mensaje = document.getElementById('lista-pasajeros-wsp-chofer-mds').value;
    
    // Llamar a la función con los parámetros
    enviarWhatsApp(numeroTelefono, mensaje);
});
document.getElementById('enviar-por-whatsapp-celador-mds').addEventListener('click', function() {
    // Obtener el número de teléfono al que deseas enviar el mensaje
    var numeroTelefono = document.getElementById('celular-input-celador').value;  // Obtiene el valor del input oculto
    
    // Obtener el contenido del mensaje
    var mensaje = document.getElementById('lista-pasajeros-wsp-celador-mds').value;
    
    // Llamar a la función con los parámetros
    enviarWhatsApp(numeroTelefono, mensaje);
});

document.getElementById('enviar-por-whatsapp-chofer-mdi').addEventListener('click', function() {
    // Obtener el número de teléfono al que deseas enviar el mensaje
    var numeroTelefono = document.getElementById('celular-input-chofer').value;  // Obtiene el valor del input oculto
    
    // Obtener el contenido del mensaje
    var mensaje = document.getElementById('lista-pasajeros-wsp-chofer-mdi').value;
    
    // Llamar a la función con los parámetros
    enviarWhatsApp(numeroTelefono, mensaje);
});
document.getElementById('enviar-por-whatsapp-celador-mdi').addEventListener('click', function() {
    // Obtener el número de teléfono al que deseas enviar el mensaje
    var numeroTelefono = document.getElementById('celular-input-celador').value;  // Obtiene el valor del input oculto
    
    // Obtener el contenido del mensaje
    var mensaje = document.getElementById('lista-pasajeros-wsp-celador-mdi').value;
    
    // Llamar a la función con los parámetros
    enviarWhatsApp(numeroTelefono, mensaje);
});

document.getElementById('enviar-por-whatsapp-chofer-ts').addEventListener('click', function() {
    // Obtener el número de teléfono al que deseas enviar el mensaje
    var numeroTelefono = document.getElementById('celular-input-chofer').value;  // Obtiene el valor del input oculto
    
    // Obtener el contenido del mensaje
    var mensaje = document.getElementById('lista-pasajeros-wsp-chofer-ts').value;
    
    // Llamar a la función con los parámetros
    enviarWhatsApp(numeroTelefono, mensaje);
});
document.getElementById('enviar-por-whatsapp-celador-ts').addEventListener('click', function() {
    // Obtener el número de teléfono al que deseas enviar el mensaje
    var numeroTelefono = document.getElementById('celular-input-celador').value;  // Obtiene el valor del input oculto
    
    // Obtener el contenido del mensaje
    var mensaje = document.getElementById('lista-pasajeros-wsp-celador-ts').value;
    
    // Llamar a la función con los parámetros
    enviarWhatsApp(numeroTelefono, mensaje);
});