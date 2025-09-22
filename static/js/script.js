document.addEventListener('DOMContentLoaded', () => {
    const businessForm = document.getElementById('business-form');
    const businessInput = document.getElementById('business-input');
    const generateButton = document.getElementById('generate-button');
    const responseContainer = document.getElementById('response-container');

    businessForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Impede o recarregamento da página

        const idea = businessInput.value.trim();
        if (!idea) {
            alert('Por favor, escreva uma ideia de negócio.');
            return;
        }

        // Estado de "carregando"
        generateButton.disabled = true;
        generateButton.textContent = 'Gerando...';
        responseContainer.classList.remove('hidden');
        responseContainer.innerHTML = '<p class="loader">Aguarde, o agente está trabalhando...</p>';

        try {
            // Chama a API do backend
            const response = await fetch('/api/agente', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ business_idea: idea }),
            });

            const result = await response.json();

            if (!response.ok) {
                // Se a API retornar um erro (ex: status 500)
                throw new Error(result.error || 'Ocorreu um erro no servidor.');
            }
            
            // Mostra o resultado formatado
            responseContainer.innerHTML = `<pre>${result.business_plan}</pre>`;

        } catch (error) {
            console.error('Erro:', error);
            responseContainer.innerHTML = `<p style="color: red;">Erro ao gerar o plano: ${error.message}</p>`;
        } finally {
            // Restaura o botão ao estado original
            generateButton.disabled = false;
            generateButton.innerHTML = '💡 Gerar Mini Plano';
        }
    });
});