document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form');
    const loginForm = document.getElementById('login-form');
    const messageElement = document.getElementById('message');

    // Función para mostrar el mensaje de resultado
    function displayMessage(text, isSuccess) {
        messageElement.textContent = text;
        messageElement.className = isSuccess ? 'success' : 'error';
    }

    // Lógica para el formulario de REGISTRO
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            // Datos a enviar en formato JSON
            const data = { username, password };

            try {
                const response = await fetch('/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json' // Indicamos que enviamos JSON
                    },
                    body: JSON.stringify(data) // Convertimos el objeto JS a string JSON
                });

                const result = await response.json(); // Leemos la respuesta como JSON

                if (response.ok) {
                    displayMessage(result.message, true);
                    registerForm.reset();
                    // Opcional: Redirigir al login después de un registro exitoso
                    // setTimeout(() => { window.location.href = '/login'; }, 2000);
                } else {
                    displayMessage(result.message, false);
                }

            } catch (error) {
                console.error('Error:', error);
                displayMessage('Error de conexión con el servidor.', false);
            }
        });
    }

    // Lógica para el formulario de LOGIN
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            const data = { username, password };

            try {
                const response = await fetch('/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (response.ok) {
                    displayMessage(result.message, true);
                    // Redirigir a la página de inicio al loguearse
                    window.location.href = '/'; 
                } else {
                    displayMessage(result.message, false);
                }

            } catch (error) {
                console.error('Error:', error);
                displayMessage('Error de conexión con el servidor.', false);
            }
        });
    }
});