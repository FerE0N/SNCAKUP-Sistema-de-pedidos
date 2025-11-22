# Changelog

## v2.0.1 — 2025-11-11
- Segunda versión funcional del sistema de toma de órdenes.
- Interfaz web tipo Bento Box en HTML/CSS.
- Generación de código QR al confirmar pedido.
- Implementación de principios SOLID y patrón MVC.

# 📦 CHANGELOG - SNACKUP

## v3.1.0 - 2025-11-11
### Added
- Implementación del sistema SNACKUP en una sola vista principal (`screen_main.html`).
- Estructura modular con secciones dinámicas para:
  - Menú principal.
  - Confirmación de pedidos.
  - Historial de pedidos.

### Updated
- Agregado **header global fijo** con el título centralizado “SNACKUP”.
- Ajustado el **nav principal** para colocarse debajo del header fijo, conservando el diseño original.
- Mejorada la jerarquía visual y la usabilidad de la navegación.

### Fixed
- Se solucionó el problema de superposición del header sobre la barra de navegación.
- Ajustado el espaciado superior del contenido principal para evitar solapamientos.

### Notes
- Este commit marca la **versión estable 3.1.0** del sistema SNACKUP lista para entrega.


## v3.2.0 - 2025-11-12
### Added
Implementación del Patrón Repositorio para desacoplar la lógica de persistencia de datos.

Añadida la interfaz de abstracción IOrderRepository (Principio de Inversión de Dependencias - DIP).

Añadida la implementación concreta JsonOrderRepository que maneja la persistencia en archivos JSON.

Añadido el método get_price() a model/product.py para soportar el Principio Abierto/Cerrado (OCP).

### Updated
Refactorizado main.py para usar Inyección de Dependencias; ahora recibe una instancia de IOrderRepository.

main.py ya no depende de módulos de bajo nivel como json u os para la persistencia.

Actualizado model/order.py para usar el método product.get_price(), permitiendo extensiones futuras (ej. descuentos) sin modificar la clase Order (OCP).

### Fixed
Corregida la violación del Principio de Responsabilidad Única (SRP) en main.py, que ya no se encarga de guardar archivos.

Corregida la violación del Principio de Inversión de Dependencias (DIP); los módulos de alto nivel (main.py) ahora dependen de abstracciones (IOrderRepository) y no de detalles concretos.

## v4.5.0 - 2025-11-21
### Added
- **Sistema de Logging (Trazabilidad)**: Implementación de `LoggerService` (Singleton) para registrar eventos del sistema en MongoDB.
  - Logs de inicio/cierre de sesión (`AuthController`).
  - Logs de creación de órdenes y fallos de pago (`ControllerOrder`).
  - Logs de errores críticos del sistema (`main.py`).
- **Mejoras de UI**:
  - Botón de Logout estilizado en el header con animación.
  - Notificaciones "Toast" para feedback de usuario (éxito/error) reemplazando `alert()`.

### Fixed
- **QR Code Overflow**: Solucionado el desbordamiento de códigos QR en las tarjetas de historial mediante CSS (`.order-qr`).
- **History Loading Error**: Corregido error en la carga del historial debido a rutas corruptas en `main.py`.
- **Order Confirmation**: Solucionado error de conexión y lógica duplicada en la confirmación de pedidos.
- **CSS Syntax**: Corregidos selectores anidados mal formados en `styles.css`.

### 🏗️ Architecture & Design (Reinforced)
- **SOLID Principles**:
  - **SRP (Single Responsibility)**: La lógica de logging se movió a `LoggerService`, desacoplándola de los controladores y la lógica de negocio.
  - **DIP (Dependency Inversion)**: `ControllerOrder` depende de abstracciones (`IPaymentService`, `IOrderRepository`) en lugar de implementaciones concretas.
  - **OCP (Open/Closed)**: El sistema de descuentos (`DiscountStrategy`) permite agregar nuevas reglas sin modificar el código existente.
- **Design Patterns**:
  - **Singleton**: Implementado en `LoggerService`, `MongoConnection` y `QRCodeManager` para garantizar una única instancia global.
  - **Observer**: Utilizado para notificar a `KitchenObserver` y `EmailObserver` cuando se crea una nueva orden.
  - **Strategy**: Aplicado en la selección de descuentos (Estudiante, Happy Hour, Ninguno).
  - **Adapter**: Usado en `PayPalAdapter` para estandarizar la interfaz de pagos.
- **OOP Concepts**:
  - **Encapsulación**: Los controladores gestionan su propio estado y lógica interna.
  - **Polimorfismo**: Las estrategias de descuento y los adaptadores de pago comparten interfaces comunes pero comportamientos distintos.