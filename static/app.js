const formulario = document.querySelector("#prediction-form");

const secaoResultado = document.querySelector("#resultado");
const classePrevista = document.querySelector("#classe-prevista");
const probabilidadeZero = document.querySelector(
    "#probabilidade-zero"
);
const probabilidadeUm = document.querySelector(
    "#probabilidade-um"
);
const barraZero = document.querySelector("#barra-zero");
const barraUm = document.querySelector("#barra-um");
const regrasDecisao = document.querySelector(
    "#regras-decisao"
);
const mensagemErro = document.querySelector(
    "#mensagem-erro"
);
const botao = formulario.querySelector(
    'button[type="submit"]'
);


formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();

    const dados = {
        renda: Number(
            document.querySelector("#renda").value
        ),
        divida: Number(
            document.querySelector("#divida").value
        ),
        numero_atrasos: Number(
            document.querySelector("#numero_atrasos").value
        )
    };

    secaoResultado.hidden = true;
    mensagemErro.hidden = true;
    mensagemErro.textContent = "";

    barraZero.style.width = "0%";
    barraUm.style.width = "0%";

    botao.disabled = true;
    botao.textContent = "Analisando...";

    try {
        const resposta = await fetch("/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(dados)
        });

        const resultado = await resposta.json();

        if (!resposta.ok) {
            const detalhe = Array.isArray(resultado.detail)
                ? resultado.detail[0]?.msg
                : "A API rejeitou a solicitação.";

            throw new Error(detalhe);
        }

        const rotuloClasse = resultado.classe === 1
            ? "Maior risco"
            : "Menor risco";

        classePrevista.textContent =
            `Classe prevista: ${resultado.classe}` +
            ` — ${rotuloClasse}`;

        const percentualZero =
            resultado.probabilidade_classe_0 * 100;

        const percentualUm =
            resultado.probabilidade_classe_1 * 100;

        probabilidadeZero.textContent =
            `${percentualZero.toFixed(1)}%`;

        probabilidadeUm.textContent =
            `${percentualUm.toFixed(1)}%`;

        regrasDecisao.replaceChildren();

        for (const regra of resultado.explicacao.regras) {
            const item = document.createElement("li");
            item.textContent = regra;
            regrasDecisao.appendChild(item);
        }

        secaoResultado.dataset.classe = resultado.classe;
        secaoResultado.hidden = false;

        requestAnimationFrame(() => {
            barraZero.style.width = `${percentualZero}%`;
            barraUm.style.width = `${percentualUm}%`;
        });
    } catch (erro) {
        mensagemErro.textContent =
            "Não foi possível realizar a análise: " +
            erro.message;

        mensagemErro.hidden = false;
    } finally {
        botao.disabled = false;
        botao.textContent = "Analisar cenário";
    }
});