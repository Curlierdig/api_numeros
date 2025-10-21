document.addEventListener("DOMContentLoaded", function () {
  // Mueve el modal al body para evitar que quede oculto por un ancestro con display:none en móvil
  const modalEl = document.getElementById("adminReporteModal");
  if (modalEl && modalEl.parentElement !== document.body) {
    document.body.appendChild(modalEl);
  }

  const step1 = document.getElementById("step1");
  const step2 = document.getElementById("step2");
  const nextBtn = document.getElementById("nextBtn");
  const prevBtn = document.getElementById("prevBtn");
  const saveBtn = document.getElementById("saveBtn");

  if (nextBtn && prevBtn && saveBtn) {
    nextBtn.addEventListener("click", () => {
      step1.style.display = "none";
      step2.style.display = "block";
      nextBtn.style.display = "none";
      prevBtn.style.display = "inline-block";
      saveBtn.style.display = "inline-block";
    });

    prevBtn.addEventListener("click", () => {
      step1.style.display = "block";
      step2.style.display = "none";
      nextBtn.style.display = "inline-block";
      prevBtn.style.display = "none";
      saveBtn.style.display = "none";
    });
  }

  // --- Mostrar/Ocultar campo "Otro Medio" ---
  const medioContactoSelect = document.getElementById("adminMedioContacto");
  const otroMedioContainer = document.getElementById("otroMedioContainer");

  if (medioContactoSelect && otroMedioContainer) {
    medioContactoSelect.addEventListener("change", function () {
      if (this.value === "otro") {
        otroMedioContainer.style.display = "block";
      } else {
        otroMedioContainer.style.display = "none";
      }
    });
  }

  // --- Mostrar/Ocultar campos de destino ---
  const tipoDestinoSelect = document.getElementById("adminTipoDestino");
  const tarjetaContainer = document.getElementById("tarjetaContainer");
  const ubicacionContainer = document.getElementById("ubicacionContainer");

  if (tipoDestinoSelect) {
    tipoDestinoSelect.addEventListener("change", function () {
      const seleccion = this.value;

      if (seleccion === "Tarjeta") {
        tarjetaContainer.style.display = "block";
        ubicacionContainer.style.display = "none";
      } else if (seleccion === "Ubicación") {
        tarjetaContainer.style.display = "none";
        ubicacionContainer.style.display = "block";
      } else {
        tarjetaContainer.style.display = "none";
        ubicacionContainer.style.display = "none";
      }
    });
  }
});
