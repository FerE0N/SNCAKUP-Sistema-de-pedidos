// static/order.js

let cart = [];

document.addEventListener("DOMContentLoaded", () => {
    // === Filtros ===
    const filterBtns = document.querySelectorAll(".filter-btn");
    const productCards = document.querySelectorAll(".product-card");

    filterBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            // Activar botón
            filterBtns.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            const filter = btn.dataset.filter;

            productCards.forEach(card => {
                if (filter === "all" || card.dataset.type === filter) {
                    card.style.display = "block";
                } else {
                    card.style.display = "none";
                }
            });
        });
    });

    // Asignar eventos a botones "Agregar"
    const addButtons = document.querySelectorAll(".product-card .btn-add");
    addButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            const name = btn.dataset.name;
            const price = parseFloat(btn.dataset.price);
            addToCart(name, price);
            showToast(`Agregado: ${name}`, "success");
        });
    });

    // Botón de confirmar pedido
    const btnConfirm = document.getElementById("btnConfirmOrder");
    if (btnConfirm) {
        btnConfirm.addEventListener("click", confirmOrder);
    }

    // Botón de cargar historial
    const btnLoadOrders = document.getElementById("btnLoadOrders");
    if (btnLoadOrders) {
        btnLoadOrders.addEventListener("click", loadOrders);
    }

    // Botón cerrar QR
    const btnCloseQR = document.getElementById("btnCloseQR");
    if (btnCloseQR) {
        btnCloseQR.addEventListener("click", () => {
            document.getElementById("qrSection").classList.add("hidden");

            // Reset Cart and UI completely
            cart = [];
            renderCart();

            // Optional: Reset QR image to avoid ghosting
            document.getElementById("qrImage").src = "";
        });
    }
});

// 🛒 Agregar al carrito
function addToCart(name, price) {
    const item = { name, price };
    cart.push(item);
    renderCart();
}

// 🧾 Mostrar carrito actual y calcular total
function renderCart() {
    const cartList = document.getElementById("cart-items");
    const cartTotalSpan = document.getElementById("cart-total");
    cartList.innerHTML = "";

    let total = 0;

    if (cart.length === 0) {
        cartList.innerHTML = '<li class="note">Tu carrito está vacío.</li>';
        cartTotalSpan.textContent = "$0.00";
        return;
    }

    cart.forEach((item, index) => {
        total += item.price;

        const li = document.createElement("li");
        li.innerHTML = `
            <span>${item.name}</span>
            <span style="font-weight:600;">$${item.price}</span>
        `;

        const btnRemove = document.createElement("button");
        btnRemove.textContent = "✕";
        btnRemove.classList.add("btn-remove");
        btnRemove.addEventListener("click", () => removeFromCart(index));

        li.appendChild(btnRemove);
        cartList.appendChild(li);
    });

    cartTotalSpan.textContent = `$${total.toFixed(2)}`;
}

// ❌ Eliminar producto del carrito
function removeFromCart(index) {
    cart.splice(index, 1);
    renderCart();
}

// ✅ Confirmar pedido
function confirmOrder() {
    if (cart.length === 0) {
        alert("Tu carrito está vacío.");
        return;
    }

    const clientNameInput = document.getElementById("clientName");
    const clientName = clientNameInput.value.trim();

    if (!clientName) {
        alert("Por favor ingresa tu nombre.");
        return;
    }

    fetch("/confirm_order", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            items: cart,
            client_name: clientName,
            discount_type: document.getElementById("discountType").value,
        }),
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                document.getElementById("qrSection").classList.remove("hidden");
                document.getElementById("qrImage").src = `data:image/png;base64,${data.qr_base64}`;

                // Use Toast instead of Alert
                showToast(`✅ Pedido confirmado. Total: $${data.total.toFixed(2)}`, "success");

                // Limpiar carrito y renderizar
                cart = [];
                renderCart();
            } else {
                showToast("⚠️ " + data.message, "error");
            }
        })
        .catch((err) => {
            console.error("Error al confirmar pedido:", err);
            showToast("Error de conexión.", "error");
        });
}

// 📦 Cargar pedidos guardados
function loadOrders() {
    const container = document.getElementById("ordersContainer");
    container.innerHTML = '<p class="note">Cargando...</p>';

    fetch("/get_orders")
        .then((res) => res.json())
        .then((orders) => {
            container.innerHTML = "";
            showToast("Historial actualizado", "info");

            if (!orders.length) {
                container.innerHTML = "<p class='note'>No hay pedidos registrados aún.</p>";
                return;
            }

            orders.forEach((order) => {
                const div = document.createElement("div");
                div.classList.add("order-card");

                // Calcular total visualmente si no viene en el objeto (aunque debería)
                const totalDisplay = order.total ? `$${order.total.toFixed(2)}` : "N/A";

                div.innerHTML = `
                    <h3>Orden #${order.id}</h3>
                    <p><strong>Cliente:</strong> ${order.client_name}</p>
                    <p><strong>Total:</strong> ${totalDisplay}</p>
                    <ul class="order-items">
                        ${order.items.map(i => `<li>${i.name} - $${i.price}</li>`).join("")}
                    </ul>
                    <div style="text-align:center;">
                        <img src="data:image/png;base64,${order.qr_base64}" class="order-qr" alt="QR">
                    </div>
                `;
                container.appendChild(div);
            });
        })
        .catch((err) => {
            console.error("Error al cargar pedidos:", err);
            container.innerHTML = "<p class='note' style='color:var(--color-error)'>Error al cargar historial.</p>";
        });
}
// 🍞 Toast Notification
function showToast(message, type = "info") {
    let container = document.getElementById("toast-container");
    if (!container) {
        container = document.createElement("div");
        container.id = "toast-container";
        document.body.appendChild(container);
    }

    const toast = document.createElement("div");
    toast.classList.add("toast", type);
    toast.textContent = message;

    container.appendChild(toast);

    // Auto remove after 3 seconds
    setTimeout(() => {
        toast.style.animation = "fadeOut 0.5s forwards";
        toast.addEventListener("animationend", () => {
            toast.remove();
        });
    }, 3000);
}
