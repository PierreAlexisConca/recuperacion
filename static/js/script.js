document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registroForm');
    const statusMessage = document.getElementById('statusMessage');


    // Establecer fecha actual por defecto
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('fecha_registro').value = today;


    form.addEventListener('submit', async function(e) {
        e.preventDefault();


        // Obtener datos del formulario
        const formData = {
            codigo: document.getElementById('codigo').value,
            marca: document.getElementById('marca').value,
            modelo: document.getElementById('modelo').value,
            sistema_operativo: document.getElementById('sistema_operativo').value,
            tipo_equipo: document.getElementById('tipo_equipo').value,
            ram: document.getElementById('ram').value,
            almacenamiento: document.getElementById('almacenamiento').value,
            fecha_mantenimiento: document.getElementById('fecha_mantenimiento').value,
            fecha_registro: document.getElementById('fecha_registro').value,
            estado: document.getElementById('estado').value
        };


        console.log("📝 Datos a enviar:", formData);


        try {
            const response = await fetch('/api/registrar', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });


            const data = await response.json();


            console.log("📥 Respuesta del servidor:", data);


            if (response.ok) {
                mostrarMensaje('✓ Equipo registrado exitosamente en la base de datos', 'success');
                form.reset();
                document.getElementById('fecha_registro').value = today;
               
                // Limpiar mensaje después de 3 segundos
                setTimeout(() => {
                    statusMessage.classList.add('hidden');
                }, 3000);
            } else {
                mostrarMensaje('✗ Error: ' + (data.error || 'Error desconocido'), 'error');
            }
        } catch (error) {
            console.error('Error:', error);
            mostrarMensaje('✗ Error de conexión: ' + error.message, 'error');
        }
    });


    function mostrarMensaje(mensaje, tipo) {
        statusMessage.textContent = mensaje;
        statusMessage.className = `mt-4 p-4 rounded-lg text-center font-semibold ${tipo}`;
        statusMessage.classList.remove('hidden');
    }
});

