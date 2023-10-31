document.getElementById('enviar-por-whatsapp').addEventListener('click', function() {
    // Obtener el contenido de la lista
    var lista = document.getElementById('lista-pasajeros-wsp').textContent;
    
    // Codificar el contenido para que sea seguro en una URL
    var listaCodificada = encodeURIComponent(lista);
    
    // Número de teléfono al que deseas enviar el mensaje
    var numeroTelefono = document.getElementById('celular-input').value;  // Obtiene el valor del input oculto
    
    // Crear el enlace de WhatsApp
    var enlaceWhatsApp = 'https://api.whatsapp.com/send?phone=+540' + numeroTelefono + '&text=' + listaCodificada;
    
    // Abrir WhatsApp en una nueva ventana o pestaña
    window.open(enlaceWhatsApp);
});
