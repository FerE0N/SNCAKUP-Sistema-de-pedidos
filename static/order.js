// static/order.js

let cart = [];

// 🧭 Navegación entre secciones
document.addEventListener("DOMContentLoaded", () => {
    const navButtons = document.querySelectorAll(".nav-btn");
    const sections = document.querySelectorAll(".bento-box");
    const btnLoadOrders = document.getElementById("btnLoadOrders");
    const ordersContainer = document.getElementById("ordersContainer");

    navButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            const targetId = btn.getAttribute("data-target");
            sections.forEach((sec) => sec.classList.add("hidden"));
            document.getElementById(targetId).classList.remove("hidden");

            // Cambiar el botón activo visualmente
            navButtons.forEach(b => b.classList.remove("active"));
            btn.classList.add("active");

            // Si entra a pedidos registrados, carga los pedidos
            if (targetId === "section-history") loadOrders();
        });
    });

    // Asignar eventos a botones "Agregar"
    const addButtons = document.querySelectorAll(".btn-add");
    addButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
            const name = btn.dataset.name;
            const price = parseFloat(btn.dataset.price);
            addToCart(name, price);
        });
    });

    // Botón de confirmar pedido
    document.getElementById("btnConfirmOrder").addEventListener("click", confirmOrder);

    if (btnLoadOrders) {
        btnLoadOrders.addEventListener("click", async () => {
            try {
                const response = await fetch("/get_orders");
                const orders = await response.json();

                if (!orders.length) {
                    ordersContainer.innerHTML = "<p>No hay pedidos registrados.</p>";
                    return;
                }

                ordersContainer.innerHTML = ""; // Limpia contenido anterior

                orders.forEach(order => {
                    const div = document.createElement("div");
                    div.classList.add("order-card");
                    div.innerHTML = `
            <h3>${order.client_name}</h3>
            <p><strong>ID:</strong> ${order.id}</p>
            <ul>${order.items.map(i => `<li>${i.name} - $${i.price}</li>`).join("")}</ul>
            <img src="/static/qrcodes/${order.qr_filename}" alt="QR de ${order.client_name}">
          `;
                    ordersContainer.appendChild(div);
                });
            } catch (error) {
                console.error("Error al cargar pedidos:", error);
                ordersContainer.innerHTML = "<p>Error al cargar pedidos.</p>";
            }
        });
    }
});

// 🛒 Agregar al carrito
function addToCart(name, price) {
    const item = { name, price };
    cart.push(item);
    renderCart();
}

// 🧾 Mostrar carrito actual
function renderCart() {
    const cartList = document.getElementById("cart-items");
    cartList.innerHTML = "";

    if (cart.length === 0) {
        cartList.innerHTML = "<li>Carrito vacío</li>";
        return;
    }

    cart.forEach((item, index) => {
        const li = document.createElement("li");
        li.textContent = `${item.name} - $${item.price}`;

        const btnRemove = document.createElement("button");
        btnRemove.textContent = "❌";
        btnRemove.classList.add("btn-remove");
        btnRemove.addEventListener("click", () => removeFromCart(index));

        li.appendChild(btnRemove);
        cartList.appendChild(li);
    });
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

    const clientName = document.getElementById("clientName").value.trim();
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
        }),
    })
        .then((res) => res.json())
        .then((data) => {
            if (data.success) {
                document.getElementById("qrSection").classList.remove("hidden");
                document.getElementById("qrImage").src = `/static/qrcodes/${data.qr_filename}`;
                alert("✅ Pedido confirmado correctamente.");
                cart = [];
                renderCart();
            } else {
                alert("⚠️ No se pudo confirmar el pedido.");
            }
        })
        .catch((err) => {
            console.error("Error al confirmar pedido:", err);
        });
}

// 📦 Cargar pedidos guardados
function loadOrders() {
    fetch("/orders")
        .then((res) => res.json())
        .then((orders) => {
            const container = document.getElementById("ordersContainer");
            container.innerHTML = "";

            if (orders.length === 0) {
                container.innerHTML = "<p>No hay pedidos registrados aún.</p>";
                return;
            }

            orders.forEach((order) => {
                const div = document.createElement("div");
                div.classList.add("order-card");
                div.innerHTML = `
          <h3>Orden #${order.id}</h3>
          <p><strong>Cliente:</strong> ${order.client_name}</p>
          <ul>${order.items
                        .map((item) => `<li>${item.name} - $${item.price}</li>`)
                        .join("")}</ul>
          <img src="/static/qrcodes/${order.qr_filename}" class="order-qr">
        `;
                container.appendChild(div);
            });
        })
        .catch((err) => console.error("Error al cargar pedidos:", err));
}
