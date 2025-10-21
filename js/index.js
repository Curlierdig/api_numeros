document.addEventListener("DOMContentLoaded", function () {
  const medioContactoSelect = document.getElementById("medioContacto");
  const otroMedioContainer = document.getElementById("otroMedioContainer");
  const otroMedioInput = document.getElementById("otroMedioEspecificar");

  const tipoDestinoSelect = document.getElementById("tipoDestino");
  const tarjetaContainer = document.getElementById("tarjetaContainer");
  const ubicacionContainer = document.getElementById("ubicacionContainer");
  const numeroTarjetaInput = document.getElementById("numeroTarjeta");
  const direccionInput = document.getElementById("direccion");

  const form = document.getElementById("reporteForm");

  // Mostrar/ocultar campo "Otro medio"
  medioContactoSelect.addEventListener("change", function () {
    if (this.value === "otro") {
      otroMedioContainer.style.display = "block";
      otroMedioInput.required = true;
    } else {
      otroMedioContainer.style.display = "none";
      otroMedioInput.required = false;
    }
  });

  // Mostrar/ocultar campos de "Destino"
  tipoDestinoSelect.addEventListener("change", function () {
    const selection = this.value;
    tarjetaContainer.style.display = selection === "Tarjeta" ? "block" : "none";
    numeroTarjetaInput.required = selection === "Tarjeta";

    ubicacionContainer.style.display = selection === "Ubicacion" ? "block" : "none";
    direccionInput.required = selection === "Ubicacion";
  });

  // Validación del formulario al intentar enviar
  form.addEventListener(
    "submit",
    function (event) {
      // Prevenir el envío si la validación falla
      if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
      }

      // Limpiar validaciones personalizadas previas
      const inputs = form.querySelectorAll(".form-control, .form-select");
      inputs.forEach((input) => input.classList.remove("is-invalid"));

      let isValid = true;

      // === VALIDACIONES PERSONALIZADAS ===

      // 1. Validar Edad (número positivo y lógico)
      const edadInput = document.getElementById("edad");
      const edad = parseInt(edadInput.value, 10);
      if (isNaN(edad) || edad <= 0 || edad > 120) {
        edadInput.classList.add("is-invalid");
        isValid = false;
      }

      // 2. Validar Número de Teléfono (formato 10 dígitos)
      const numeroInput = document.getElementById("numero");
      const numeroRegex = /^\d{10}$/;
      if (!numeroRegex.test(numeroInput.value.replace(/\s/g, ""))) {
        numeroInput.classList.add("is-invalid");
        isValid = false;
      }

      // 3. Validar Número de Tarjeta (16 dígitos numéricos) si es visible
      if (tarjetaContainer.style.display === "block") {
        const tarjetaRegex = /^\d{16}$/;
        if (!tarjetaRegex.test(numeroTarjetaInput.value)) {
          numeroTarjetaInput.classList.add("is-invalid");
          isValid = false;
        }
      }

      // Si la validación de Bootstrap o la personalizada falla, detener
      if (!isValid) {
        event.preventDefault();
        event.stopPropagation();
      }

      // Añadir clases de validación de Bootstrap a todos los campos
      form.classList.add("was-validated");

      if (isValid && form.checkValidity()) {
        // Si todo es válido, aquí iría la lógica para enviar los datos (ej. a una API)
        event.preventDefault(); // Prevenir envío real para este ejemplo
        console.log("Formulario válido. Datos listos para enviar.");
        alert("¡Reporte enviado exitosamente! Gracias por tu colaboración.");

        // Opcional: Cerrar el modal y resetear el formulario
        const modal = bootstrap.Modal.getInstance(document.getElementById("reporteModal"));
        modal.hide();
        form.reset();
        form.classList.remove("was-validated");
      }
    },
    false
  );
});
