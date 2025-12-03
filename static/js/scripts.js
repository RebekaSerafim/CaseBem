// Funções de máscara para formulários

// Validação de formato de CPF (apenas quantidade de dígitos e sequências repetidas)
function validarCPF(cpf) {
    cpf = cpf.replace(/[^\d]+/g, '');

    // Verifica se tem 11 dígitos e não é uma sequência repetida
    return cpf.length === 11 && !/^(\d)\1{10}$/.test(cpf);
}

// Validação de formato de CNPJ (apenas quantidade de dígitos e sequências repetidas)
function validarCNPJ(cnpj) {
    cnpj = cnpj.replace(/[^\d]+/g, '');

    // Verifica se tem 14 dígitos e não é uma sequência repetida
    return cnpj.length === 14 && !/^(\d)\1{13}$/.test(cnpj);
}

// Máscara para CPF: 000.000.000-00 (limita a 11 dígitos)
function mascaraCPF(input) {
    let valor = input.value.replace(/\D/g, ''); // Remove tudo que não é dígito

    // Limita a 11 dígitos
    valor = valor.substring(0, 11);

    // Aplica a máscara usando expressões regulares
    valor = valor.replace(/^(\d{3})(\d)/, '$1.$2');
    valor = valor.replace(/^(\d{3})\.(\d{3})(\d)/, '$1.$2.$3');
    valor = valor.replace(/\.(\d{3})(\d)/, '.$1-$2');

    input.value = valor;
}

// Máscara para CNPJ: 00.000.000/0000-00 (limita a 14 dígitos)
function mascaraCNPJ(input) {
    let valor = input.value.replace(/\D/g, ''); // Remove tudo que não é dígito

    // Limita a 14 dígitos
    valor = valor.substring(0, 14);

    // Aplica a máscara usando expressões regulares
    valor = valor.replace(/^(\d{2})(\d)/, '$1.$2');
    valor = valor.replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3');
    valor = valor.replace(/\.(\d{3})(\d)/, '.$1/$2');
    valor = valor.replace(/(\d{4})(\d)/, '$1-$2');

    input.value = valor;
}

// Máscara para telefone: (00) 00000-0000 ou (00) 0000-0000 (limita a 11 dígitos)
function mascaraTelefone(input) {
    let valor = input.value.replace(/\D/g, ''); // Remove tudo que não é dígito

    // Limita a 11 dígitos
    valor = valor.substring(0, 11);

    if (valor.length <= 10) {
        // Telefone fixo: (00) 0000-0000
        valor = valor.replace(/^(\d{2})(\d)/, '($1) $2');
        valor = valor.replace(/(\d{4})(\d)/, '$1-$2');
    } else {
        // Celular: (00) 00000-0000
        valor = valor.replace(/^(\d{2})(\d)/, '($1) $2');
        valor = valor.replace(/(\d{5})(\d)/, '$1-$2');
    }

    input.value = valor;
}

// Aplicar máscaras quando o documento carregar
document.addEventListener('DOMContentLoaded', function() {
    // Máscara para CPF
    const camposCPF = document.querySelectorAll('input[name="cpf"], input[name="cpf1"], input[name="cpf2"]');
    camposCPF.forEach(function(campo) {
        campo.addEventListener('input', function() {
            // Aplicar máscara primeiro
            mascaraCPF(this);

            // Depois validar o valor mascarado
            if (this.value && !validarCPF(this.value)) {
                this.classList.add("is-invalid");
                this.classList.remove("is-valid");
            } else if (this.value) {
                this.classList.remove("is-invalid");
                this.classList.add("is-valid");
            } else {
                this.classList.remove("is-invalid", "is-valid");
            }
        });

        // Aplicar máscara no valor já existente (para preservar dados em caso de erro)
        if (campo.value) {
            mascaraCPF(campo);
        }
    });

    // Máscara para CNPJ
    const camposCNPJ = document.querySelectorAll('input[name="cnpj"]');
    camposCNPJ.forEach(function(campo) {
        campo.addEventListener('input', function() {
            // Aplicar máscara primeiro
            mascaraCNPJ(this);

            // Depois validar o valor mascarado
            if (this.value && !validarCNPJ(this.value)) {
                this.classList.add("is-invalid");
                this.classList.remove("is-valid");
            } else if (this.value) {
                this.classList.remove("is-invalid");
                this.classList.add("is-valid");
            } else {
                this.classList.remove("is-invalid", "is-valid");
            }
        });

        // Aplicar máscara no valor já existente
        if (campo.value) {
            mascaraCNPJ(campo);
        }
    });

    // Máscara para telefone
    const camposTelefone = document.querySelectorAll('input[name="telefone"], input[name="telefone1"], input[name="telefone2"]');
    camposTelefone.forEach(function(campo) {
        campo.addEventListener('input', function() {
            mascaraTelefone(this);
        });

        // Aplicar máscara no valor já existente
        if (campo.value) {
            mascaraTelefone(campo);
        }
    });
});

// Função para remover máscara antes de enviar o formulário
function removerMascaras() {
    // Remove máscaras de CPF
    const camposCPF = document.querySelectorAll('input[name="cpf"], input[name="cpf1"], input[name="cpf2"]');
    camposCPF.forEach(function(campo) {
        if (campo.value) {
            campo.value = campo.value.replace(/\D/g, '');
        }
    });

    // Remove máscaras de CNPJ
    const camposCNPJ = document.querySelectorAll('input[name="cnpj"]');
    camposCNPJ.forEach(function(campo) {
        if (campo.value) {
            campo.value = campo.value.replace(/\D/g, '');
        }
    });

    // Remove máscaras de telefone
    const camposTelefone = document.querySelectorAll('input[name="telefone"], input[name="telefone1"], input[name="telefone2"]');
    camposTelefone.forEach(function(campo) {
        if (campo.value) {
            campo.value = campo.value.replace(/\D/g, '');
        }
    });
}