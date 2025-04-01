const API_URL = "https://seu-backend-no-render.com";

function mostrarCadastro() {
    document.getElementById("login-container").style.display = "none";
    document.getElementById("cadastro-container").style.display = "block";
}

function mostrarLogin() {
    document.getElementById("cadastro-container").style.display = "none";
    document.getElementById("login-container").style.display = "block";
}

async function fazerCadastro() {
    let usuario = document.getElementById("cadastro-usuario").value;
    let senha = document.getElementById("cadastro-senha").value;
    
    let resposta = await fetch(`${API_URL}/cadastrar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usuario, senha })
    });
    let dados = await resposta.json();
    alert(dados.mensagem);
}

async function fazerLogin() {
    let usuario = document.getElementById("login-usuario").value;
    let senha = document.getElementById("login-senha").value;
    
    let resposta = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ usuario, senha })
    });
    let dados = await resposta.json();
    
    if (dados.sucesso) {
        sessionStorage.setItem("token", dados.token);
        window.location.href = "calculadora.html";
    } else {
        alert("Login falhou");
    }
}

async function calcular() {
    let principal = parseFloat(document.getElementById("principal").value);
    let taxa = parseFloat(document.getElementById("taxa").value);
    let tempo = parseFloat(document.getElementById("tempo").value);
    
    let resposta = await fetch(`${API_URL}/calcular`, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Authorization": `Bearer ${sessionStorage.getItem("token")}` },
        body: JSON.stringify({ principal, taxa, tempo })
    });
    let dados = await resposta.json();
    
    document.getElementById("resultado").innerHTML = `Montante: R$ ${dados.montante_final.toFixed(2)}`;
    carregarHistorico();
}

async function carregarHistorico() {
    let resposta = await fetch(`${API_URL}/historico`, {
        headers: { "Authorization": `Bearer ${sessionStorage.getItem("token")}` }
    });
    let dados = await resposta.json();
    
    let lista = document.getElementById("historico-lista");
    lista.innerHTML = "";
    dados.forEach((item, index) => {
        let li = document.createElement("li");
        li.innerHTML = `Valor: R$${item.principal}, Tempo: ${item.tempo} meses, Montante: R$${item.montante_final.toFixed(2)} 
        <button onclick="apagarAplicacao(${index})">Apagar</button>`;
        lista.appendChild(li);
    });
}

async function apagarAplicacao(index) {
    await fetch(`${API_URL}/apagar/${index}`, {
        method: "DELETE",
        headers: { "Authorization": `Bearer ${sessionStorage.getItem("token")}` }
    });
    carregarHistorico();
}

function limparCampos() {
    document.getElementById("principal").value = "";
    document.getElementById("taxa").value = "";
    document.getElementById("tempo").value = "";
}
