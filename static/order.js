// Client-side logic: manejar items, eliminar, confirmación y petición al servidor
let items = [];

const productListEl = document.getElementById("product-list");
const totalEl = document.getElementById("total");
const qrArea = document.getElementById("qr-area");
const productListServer = document.getElementById("product-list-server");

// Cargar productos desde servidor
async function loadServerProducts() {
    try {
        const res = await fetch("/api/products");
        const prods = await res.json();
        productListServer.innerHTML = "";
        prods.forEach(p => {
            const li = document.createElement("li");
            li.innerHTML = `<span>${p.name} - $${p.price.toFixed(2)}</span>
                      <div>
                        <button class="small" onclick='addItemFromServer("${p.id}", "${p.name}", ${p.price})'>Agregar</button>
                      </div>`;
            productListServer.appendChild(li);
        });
    } catch (e) {
        console.error("No se pudieron cargar productos:", e);
    }
}
loadServerProducts();

// Añadir desde lista server
function addItemFromServer(id, name, price) {
    items.push({ id, name, price });
    renderList();
}

// Añadir manual
document.getElementById("add-manual").addEventListener("click", () => {
    const name = document.getElementById("new-name").value.trim();
    const price = parseFloat(document.getElementById("new-price").value);
    if (!name || isNaN(price)) {
        alert("Nombre y precio válidos");
        return;
    }
    const id = crypto.randomUUID().slice(0, 8);
    items.push({ id, name, price });
    document.getElementById("new-name").value = "";
    document.getElementById("new-price").value = "";
    renderList();
});

// Renderizar lista de la orden
function renderList() {
    productListEl.innerHTML = "";
    items.forEach((p, idx) => {
        const li = document.createElement("li");
        li.innerHTML = `<span>${p.name} - $${p.price.toFixed(2)}</span>
                    <div>
                      <button class="small" onclick="removeItem('${p.id}')">Eliminar</button>
                    </div>`;
        productListEl.appendChild(li);
    });
    updateTotal();
}

window.removeItem = function (id) {
    items = items.filter(i => i.id !== id);
    renderList();
}

function updateTotal() {
    const total = items.reduce((s, p) => s + Number(p.price), 0);
    totalEl.innerText = `Total: $${total.toFixed(2)}`;
}

// Confirmar orden: enviar al servidor para crear orden y QR
document.getElementById("confirm-btn").addEventListener("click", async () => {
    if (items.length === 0) {
        alert("La orden está vacía.");
        return;
    }
    const clientName = document.getElementById("client-name").value || "Invitado";
    const payload = {
        client: { id_client: "c_guest", name: clientName },
        items: items
    };

    try {
        const res = await fetch("/api/confirm", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.error) {
            alert("Error: " + data.error);
            return;
        }

        // Mostrar QR y resumen
        qrArea.innerHTML = `<h3>Orden confirmada (ID: ${data.order_id})</h3>
                        <p>Total: $${Number(data.total).toFixed(2)}</p>
                        <img src="${data.qr_url}" alt="QR de la orden">`;

        // Vaciar items locales
        items = [];
        renderList();

    } catch (e) {
        console.error(e);
        alert("Error al confirmar la orden.");
    }
});
