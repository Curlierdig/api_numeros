$(document).ready(function () {
  // --- 1. INICIALIZACIÓN DE DATATABLES ---
  var tabla = $("#tablaReportes").DataTable({
    ajax: {
      url: "mock2.json",
      dataSrc: "data",
      error: function () {
        alert("Error al cargar los datos de la tabla. Por favor, intente de nuevo más tarde.");
      },
    },
    columns: [
      { data: "id" },
      { data: "nombre" },
      { data: "numero_reportado" },
      { data: "categoria" },
      { data: "fecha" },
      {
        data: "estatus",
        render: function (data) {
          let color = "secondary";
          if (data === "Pendiente") color = "warning";
          if (data === "Resuelto") color = "success";
          if (data === "En Proceso") color = "info";
          if (data === "Descartado") color = "dark";
          const textColor = data === "Pendiente" ? "text-dark" : "";
          return `<span class="badge bg-${color} ${textColor}">${data}</span>`;
        },
      },
      {
        data: null,
        orderable: false,
        searchable: false,
        render: function (data, type, row) {
          return `<button class="btn btn-sm btn-primary btn-ver-reporte" data-id="${row.id}"><i class="bi bi-pencil-square"></i> Ver/Editar</button>`;
        },
      },
    ],
    language: { url: "https://cdn.datatables.net/plug-ins/2.0.5/i18n/es-MX.json" },
    responsive: true,
    layout: { topStart: { buttons: ["csv", "excel", "pdf", "print"] }, topEnd: "pageLength" },
    lengthMenu: [50, 75, 100],
    pageLength: 50,
  });

  // --- 2. LÓGICA DE AUTORIZACIÓN (REVISAR ROL) ---
  function checkUserRoleAndPermissions() {
    if (localStorage.getItem("userRole") !== "superadmin") {
      document.querySelectorAll(".super-admin-only").forEach((el) => el.style.setProperty("display", "none", "important"));
    }
  }
  checkUserRoleAndPermissions();

  // --- 3. LÓGICA DEL MODAL ---
  let currentStep = 1;
  const totalSteps = 2;

  function updateWizardView() {
    $(".report-step").hide();
    $(`#editStep${currentStep}`).show();
    $("#prevBtn").toggle(currentStep > 1);
    $("#nextBtn").toggle(currentStep < totalSteps);
    $("#saveBtn").toggle(currentStep === totalSteps);
  }

  $("#nextBtn").on("click", () => {
    if (currentStep < totalSteps) {
      currentStep++;
      updateWizardView();
    }
  });
  $("#prevBtn").on("click", () => {
    if (currentStep > 1) {
      currentStep--;
      updateWizardView();
    }
  });

  async function fetchReporteCompleto(folio) {
    // Simulación de API con todos los campos necesarios
    const mockData = {
      folio: folio,
      usuario: { nombre: "Juan Pérez García", veces_reportado: 3, edad: 34, sexo: "Hombre", numero_contacto: "614-123-4567", correo: "juan.perez@example.com", municipio: "Chihuahua" },
      reporte: {
        numero_reportado: "656-999-8888",
        fecha_reporte: "2025-10-15",
        categoria: "Fraude",
        medio_contacto: "Llamada",
        descripcion: "Llamaron pidiendo datos de una tarjeta de crédito.",
        supuesto_nombre: "Asesor Bancario Falso",
        supuesto_genero: "Hombre",
        supuesto_trabajo: "Banco Nacional",
        estatus: "En Proceso",
        tipo_destino: "Tarjeta",
        numero_tarjeta: "1234567890123456",
        direccion: "",
      },
    };
    return new Promise((resolve) => setTimeout(() => resolve(mockData), 500));
  }

  function populateModal(data) {
    // Rellena todos los campos del formulario, incluyendo los nuevos
    $("#editNombreUsuario").val(data.usuario.nombre);
    $("#editVecesReportado").val(data.usuario.veces_reportado);
    $("#editEdad").val(data.usuario.edad);
    $("#editSexo").val(data.usuario.sexo);
    $("#editNumeroUsuario").val(data.usuario.numero_contacto);
    $("#editCorreo").val(data.usuario.correo);
    $("#editMunicipio").val(data.usuario.municipio);
    $("#folio-display").text(data.folio);
    $("#editNumeroReportado").val(data.reporte.numero_reportado);
    $("#editFechaReporte").val(data.reporte.fecha_reporte);
    $("#editCategoria").val(data.reporte.categoria);
    $("#editMedioContacto").val(data.reporte.medio_contacto);
    $("#editDescripcion").val(data.reporte.descripcion);
    $("#editSupuestoNombre").val(data.reporte.supuesto_nombre);
    $("#editSupuestoGenero").val(data.reporte.supuesto_genero);
    $("#editSupuestoTrabajo").val(data.reporte.supuesto_trabajo);
    $("#editEstatus").val(data.reporte.estatus);
    $("#editTipoDestino").val(data.reporte.tipo_destino).trigger("change");
    $("#editNumeroTarjeta").val(data.reporte.numero_tarjeta);
    $("#editDireccion").val(data.reporte.direccion);
  }

  $("#tablaReportes tbody").on("click", ".btn-ver-reporte", async function () {
    const data = tabla.row($(this).parents("tr")).data();
    const folio = data.id;
    $("#adminModalLabel").text("Cargando datos...");
    $("#adminReporteModal").modal("show");
    const reporteCompleto = await fetchReporteCompleto(folio);
    populateModal(reporteCompleto);
    currentStep = 1;
    updateWizardView();
  });

  $("#editTipoDestino").on("change", function () {
    const selection = $(this).val();
    $("#tarjetaContainer").toggle(selection === "Tarjeta");
    $("#ubicacionContainer").toggle(selection === "Ubicación");
  });

  // --- LÓGICA DE GUARDADO CON CONFIRMACIÓN ---
  $("#editReportForm").on("submit", function (e) {
    e.preventDefault();
    $("#confirmationModal").modal("show");
  });

  $("#confirmSaveBtn").on("click", function () {
    const folio = $("#folio-display").text();
    $("#confirmationModal").modal("hide");
    $("#adminReporteModal").modal("hide");
    // tabla.ajax.reload();
  });
});
