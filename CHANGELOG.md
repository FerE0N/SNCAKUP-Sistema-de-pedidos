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