// =============================================================================
// PPR 1001 - Script Principal de la Aplicación (Monitor de Indicadores & Matriz)
// =============================================================================

// Catálogo de las 25 Actividades Operativas para la Matriz Mensual
const ACTIVIDADES_PPR = [
  // 1. INMUNIZACIONES (9 AOs)
  {
    codigo: "3325401",
    titulo: "Vacunación BCG (Dosis Recién Nacido)",
    criterio: "CPT 90708 (Dosis RN < 28 días)",
    tipo: "CPT",
    grupo: "inmunizaciones",
    grupoTitulo: "Inmunizaciones & Vacunas (ppr1001_vacunas.py)",
    icon: "fa-syringe",
    color: "sky"
  },
  {
    codigo: "3325402",
    titulo: "Vacunación Hepatitis B Pediátrica (HVB)",
    criterio: "CPT 90744 (Dosis RN en 12-24 horas)",
    tipo: "CPT",
    grupo: "inmunizaciones",
    grupoTitulo: "Inmunizaciones & Vacunas (ppr1001_vacunas.py)",
    icon: "fa-syringe",
    color: "sky"
  },
  {
    codigo: "3325403",
    titulo: "Vacunación Pentavalente (1ra, 2da, 3ra Dosis)",
    criterio: "CPT 90723, 90720 (Lab 1, 2, 3 a 2m, 4m, 6m)",
    tipo: "CPT",
    grupo: "inmunizaciones",
    grupoTitulo: "Inmunizaciones & Vacunas (ppr1001_vacunas.py)",
    icon: "fa-syringe",
    color: "sky"
  },
  {
    codigo: "3325404",
    titulo: "Vacunación Antipolio (IPV / APO)",
    criterio: "CPT 90713 (IPV) y CPT 90712 (APO)",
    tipo: "CPT",
    grupo: "inmunizaciones",
    grupoTitulo: "Inmunizaciones & Vacunas (ppr1001_vacunas.py)",
    icon: "fa-syringe",
    color: "sky"
  },
  {
    codigo: "3325405",
    titulo: "Vacunación Rotavirus (1ra y 2da Dosis)",
    criterio: "CPT 90681 (2 meses y 4 meses)",
    tipo: "CPT",
    grupo: "inmunizaciones",
    grupoTitulo: "Inmunizaciones & Vacunas (ppr1001_vacunas.py)",
    icon: "fa-syringe",
    color: "sky"
  },
  {
    codigo: "3325406",
    titulo: "Vacunación Antineumocócica (1ra, 2da, 3ra Dosis)",
    criterio: "CPT 90669 (2m, 4m y refuerzo al año)",
    tipo: "CPT",
    grupo: "inmunizaciones",
    grupoTitulo: "Inmunizaciones & Vacunas (ppr1001_vacunas.py)",
    icon: "fa-syringe",
    color: "sky"
  },
  {
    codigo: "3325407",
    titulo: "Vacunación SPR (Sarampión, Paperas, Rubéola)",
    criterio: "CPT 90707 (1ra Dosis 12m, 2da Dosis 18m)",
    tipo: "CPT",
    grupo: "inmunizaciones",
    grupoTitulo: "Inmunizaciones & Vacunas (ppr1001_vacunas.py)",
    icon: "fa-syringe",
    color: "sky"
  },
  {
    codigo: "3325408",
    titulo: "Vacunación DPT Refuerzos (1er y 2do Refuerzo)",
    criterio: "CPT 90701 (18 meses y 4 años)",
    tipo: "CPT",
    grupo: "inmunizaciones",
    grupoTitulo: "Inmunizaciones & Vacunas (ppr1001_vacunas.py)",
    icon: "fa-syringe",
    color: "sky"
  },
  {
    codigo: "3325508",
    titulo: "Vacunación Influenza Pediátrica",
    criterio: "CPT 90657 (Lactantes desde 6 meses)",
    tipo: "CPT",
    grupo: "inmunizaciones",
    grupoTitulo: "Inmunizaciones & Vacunas (ppr1001_vacunas.py)",
    icon: "fa-syringe",
    color: "sky"
  },

  // 2. PEDIATRÍA & MORBILIDAD (16 AOs)
  {
    codigo: "3331501",
    titulo: "Anemia por Deficiencia de Hierro",
    criterio: "CIE: D509, D649 (< 5 Años)",
    tipo: "CIE-10",
    grupo: "pediatria",
    grupoTitulo: "Pediatría & Morbilidad Infantil (ppr1001_pediatria.py)",
    icon: "fa-droplet",
    color: "rose"
  },
  {
    codigo: "3341401",
    titulo: "Parasitosis Intestinal en < 5 Años",
    criterio: "CIE: B680, B681, B80, A071...",
    tipo: "CIE-10",
    grupo: "pediatria",
    grupoTitulo: "Pediatría & Morbilidad Infantil (ppr1001_pediatria.py)",
    icon: "fa-bug",
    color: "amber"
  },
  {
    codigo: "3331101",
    titulo: "IRA No Complicada (Resfrío / Rinofaringitis)",
    criterio: "CIE: J00X, J040, J042, J209...",
    tipo: "CIE-10",
    grupo: "pediatria",
    grupoTitulo: "Pediatría & Morbilidad Infantil (ppr1001_pediatria.py)",
    icon: "fa-head-side-cough",
    color: "teal"
  },
  {
    codigo: "3331102",
    titulo: "FAPA (Faringitis y Amigdalitis Aguda)",
    criterio: "CIE: J020, J029, J030, J038, J039",
    tipo: "CIE-10",
    grupo: "pediatria",
    grupoTitulo: "Pediatría & Morbilidad Infantil (ppr1001_pediatria.py)",
    icon: "fa-lungs",
    color: "teal"
  },
  {
    codigo: "3331103",
    titulo: "Otitis Media Aguda (OMA)",
    criterio: "CIE: H650, H651, H660, H669",
    tipo: "CIE-10",
    grupo: "pediatria",
    grupoTitulo: "Pediatría & Morbilidad Infantil (ppr1001_pediatria.py)",
    icon: "fa-ear-listen",
    color: "teal"
  },
  {
    codigo: "3331104",
    titulo: "Sinusitis Aguda",
    criterio: "CIE: J010, J011, J012, J013, J014, J019",
    tipo: "CIE-10",
    grupo: "pediatria",
    grupoTitulo: "Pediatría & Morbilidad Infantil (ppr1001_pediatria.py)",
    icon: "fa-virus",
    color: "teal"
  },
  {
    codigo: "3331105",
    titulo: "Neumonía No Complicada",
    criterio: "CIE: J129, J159, J181",
    tipo: "CIE-10",
    grupo: "pediatria",
    grupoTitulo: "Pediatría & Morbilidad Infantil (ppr1001_pediatria.py)",
    icon: "fa-lungs-virus",
    color: "indigo"
  },
  {
    codigo: "nuemonia",
    titulo: "Neumonía Complicada",
    criterio: "CIE: A369, J13X, J14X, J150...",
    tipo: "CIE-10",
    grupo: "pediatria",
    grupoTitulo: "Pediatría & Morbilidad Infantil (ppr1001_pediatria.py)",
    icon: "fa-hospital",
    color: "indigo"
  },
  {
    codigo: "3331301",
    titulo: "Neumonía Muy Grave en < 2 meses",
    criterio: "CIE: J050, J180, J156, J851, J90X...",
    tipo: "CIE-10",
    grupo: "pediatria",
    grupoTitulo: "Pediatría & Morbilidad Infantil (ppr1001_pediatria.py)",
    icon: "fa-circle-exclamation",
    color: "red"
  },
  {
    codigo: "3331305",
    titulo: "Neumonía Muy Grave (2m a 4 años)",
    criterio: "CIE: J050, J180, J156, J851, J90X...",
    tipo: "CIE-10",
    grupo: "pediatria",
    grupoTitulo: "Pediatría & Morbilidad Infantil (ppr1001_pediatria.py)",
    icon: "fa-triangle-exclamation",
    color: "red"
  },
  {
    codigo: "3331502",
    titulo: "SOBA / Asma Bronquial",
    criterio: "CIE: J210, J440, J450, J459, J46X...",
    tipo: "CIE-10",
    grupo: "pediatria",
    grupoTitulo: "Pediatría & Morbilidad Infantil (ppr1001_pediatria.py)",
    icon: "fa-lungs",
    color: "blue"
  },
  {
    codigo: "3331201",
    titulo: "EDA No Complicada (Acuosa Simple)",
    criterio: "CIE: A009, A020, A049, A084, A090...",
    tipo: "CIE-10",
    grupo: "pediatria",
    grupoTitulo: "Pediatría & Morbilidad Infantil (ppr1001_pediatria.py)",
    icon: "fa-notes-medical",
    color: "amber"
  },
  {
    codigo: "3331203",
    titulo: "EDA Disentérica",
    criterio: "CIE: A030, A039, A042, A045, A060...",
    tipo: "CIE-10",
    grupo: "pediatria",
    grupoTitulo: "Pediatría & Morbilidad Infantil (ppr1001_pediatria.py)",
    icon: "fa-bacteria",
    color: "amber"
  },
  {
    codigo: "3331204",
    titulo: "EDA Persistente (> 14 días)",
    criterio: "CIE: A09X",
    tipo: "CIE-10",
    grupo: "pediatria",
    grupoTitulo: "Pediatría & Morbilidad Infantil (ppr1001_pediatria.py)",
    icon: "fa-clock-rotate-left",
    color: "amber"
  },
  {
    codigo: "3331401",
    titulo: "EDA con Algún Grado de Deshidratación",
    criterio: "CIE: E86X, A090, A084...",
    tipo: "CIE-10",
    grupo: "pediatria",
    grupoTitulo: "Pediatría & Morbilidad Infantil (ppr1001_pediatria.py)",
    icon: "fa-faucet-drip",
    color: "rose"
  },
  {
    codigo: "3331305_shock",
    titulo: "EDA con Deshidratación Severa y Shock",
    criterio: "CIE: R571, E872, K560...",
    tipo: "CIE-10",
    grupo: "pediatria",
    grupoTitulo: "Pediatría & Morbilidad Infantil (ppr1001_pediatria.py)",
    icon: "fa-heart-pulse",
    color: "red"
  }
];

// Variables de Estado en Memoria
let currentFile = null;
let datosCargados = null;

// Elementos DOM
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');
const fileLabel = document.getElementById('fileLabel');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const processBtn = document.getElementById('processBtn');
const resetBtn = document.getElementById('resetBtn');
const alertBox = document.getElementById('alertBox');

const resultsTopBar = document.getElementById('resultsTopBar');
const resultsSection = document.getElementById('resultsSection');
const persistedBadge = document.getElementById('persistedBadge');
const persistedFileName = document.getElementById('persistedFileName');
const persistedTime = document.getElementById('persistedTime');

// Elementos Vista Barras vs Matriz
const viewBarsBtn = document.getElementById('viewBarsBtn');
const viewMatrixBtn = document.getElementById('viewMatrixBtn');
const barsViewContainer = document.getElementById('barsViewContainer');
const matrixViewContainer = document.getElementById('matrixViewContainer');
const subFilterGroup = document.getElementById('subFilterGroup');

// =========================================================================
// 1. INICIALIZACIÓN Y PERSISTENCIA (LOCALSTORAGE)
// =========================================================================
function iniciarApp() {
  restaurarDesdeLocalStorage();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', iniciarApp);
} else {
  iniciarApp();
}

function guardarEnLocalStorage(data, nombreArchivo) {
  try {
    localStorage.setItem('ppr1001_resultado', JSON.stringify(data));
    localStorage.setItem('ppr1001_nombre_archivo', nombreArchivo);
    localStorage.setItem('ppr1001_fecha_proceso', new Date().toLocaleTimeString());
    // Sincronizar también con sessionStorage por compatibilidad
    sessionStorage.setItem('ultimoResultadoPPR', JSON.stringify(data));
    sessionStorage.setItem('ultimoNombreArchivo', nombreArchivo);
  } catch (e) {
    console.warn("No se pudo guardar en localStorage (cuota excedida o privado):", e);
  }
}

function restaurarDesdeLocalStorage() {
  try {
    const rawData = localStorage.getItem('ppr1001_resultado') || sessionStorage.getItem('ultimoResultadoPPR');
    const nombreArchivo = localStorage.getItem('ppr1001_nombre_archivo') || sessionStorage.getItem('ultimoNombreArchivo');
    const fechaProceso = localStorage.getItem('ppr1001_fecha_proceso');

    if (rawData && nombreArchivo) {
      const data = JSON.parse(rawData);
      datosCargados = data;

      // Mostrar badge de persistencia
      persistedFileName.textContent = nombreArchivo;
      persistedTime.textContent = `(Guardado: ${fechaProceso || ''})`;
      persistedBadge.classList.remove('hidden');

      // Habilitar botón de limpiar
      resetBtn.classList.remove('hidden');

      // Poblar indicadores y matriz mensual
      poblarIndicadores(data);

      resultsTopBar.classList.remove('hidden');
      resultsSection.classList.remove('hidden');
    }
  } catch (e) {
    console.error("Error al restaurar desde localStorage:", e);
  }
}

function limpiarLocalStorage() {
  localStorage.removeItem('ppr1001_resultado');
  localStorage.removeItem('ppr1001_nombre_archivo');
  localStorage.removeItem('ppr1001_fecha_proceso');
  sessionStorage.removeItem('ultimoResultadoPPR');
  sessionStorage.removeItem('ultimoNombreArchivo');
}

// =========================================================================
// 2. DRAG AND DROP & SELECCIÓN DE ARCHIVO EXCEL
// =========================================================================
if (dropzone && fileInput) {
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, preventDefaults, false);
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  ['dragenter', 'dragover'].forEach(eventName => {
    dropzone.addEventListener(eventName, () => {
      dropzone.classList.add('border-sky-500', 'bg-sky-50/50');
    }, false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropzone.addEventListener(eventName, () => {
      dropzone.classList.remove('border-sky-500', 'bg-sky-50/50');
    }, false);
  });

  dropzone.addEventListener('drop', (e) => {
    const dt = e.dataTransfer;
    const files = dt.files;
    if (files.length > 0) handleFile(files[0]);
  });

  fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) handleFile(e.target.files[0]);
  });
}

function handleFile(file) {
  if (!file.name.endsWith('.xlsx') && !file.name.endsWith('.xls')) {
    showAlert('El archivo seleccionado no es un Excel válido (.xlsx o .xls).', 'error');
    return;
  }
  currentFile = file;
  fileName.textContent = `${file.name} (${(file.size / (1024 * 1024)).toFixed(2)} MB)`;
  fileLabel.classList.add('hidden');
  fileInfo.classList.remove('hidden');
  fileInfo.classList.add('inline-flex');
  processBtn.disabled = false;
  resetBtn.classList.remove('hidden');
  hideAlert();
}

resetBtn.addEventListener('click', () => {
  currentFile = null;
  datosCargados = null;
  limpiarLocalStorage();

  fileInput.value = '';
  fileLabel.classList.remove('hidden');
  fileInfo.classList.add('hidden');
  fileInfo.classList.remove('inline-flex');
  processBtn.disabled = true;
  resetBtn.classList.add('hidden');
  persistedBadge.classList.add('hidden');

  resultsTopBar.classList.add('hidden');
  resultsSection.classList.add('hidden');

  const thead = document.getElementById('matrixThead');
  const tbody = document.getElementById('matrixTbody');
  const badge = document.getElementById('matrixMonthsCountBadge');
  if (thead) thead.innerHTML = '';
  if (tbody) tbody.innerHTML = '';
  if (badge) badge.textContent = '0 Meses';

  hideAlert();
});

processBtn.addEventListener('click', async () => {
  if (!currentFile) return;

  const formData = new FormData();
  formData.append('file', currentFile);

  processBtn.disabled = true;
  processBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> <span>Procesando con Calamine (Rust)...</span>';
  hideAlert();

  try {
    const response = await fetch('/api/v1/ppr1001/procesar', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'Ocurrió un error al procesar el archivo Excel.');
    }

    datosCargados = data;

    // Guardar copia local persistente
    guardarEnLocalStorage(data, currentFile.name);

    // Actualizar badge
    persistedFileName.textContent = currentFile.name;
    persistedTime.textContent = `(Procesado: ${new Date().toLocaleTimeString()})`;
    persistedBadge.classList.remove('hidden');

    // Poblar indicadores y matriz mensual
    poblarIndicadores(data);

    resultsTopBar.classList.remove('hidden');
    resultsSection.classList.remove('hidden');

    showAlert('¡Archivo procesado con éxito! Todas las fórmulas y la matriz mensual han sido calculadas.', 'success');
    resultsTopBar.scrollIntoView({ behavior: 'smooth' });

  } catch (err) {
    showAlert(err.message, 'error');
  } finally {
    processBtn.disabled = false;
    processBtn.innerHTML = '<i class="fa-solid fa-calculator"></i> <span>Procesar Indicadores</span>';
  }
});

// =========================================================================
// 3. POBLAR INDICADORES PPR (25 ACTIVIDADES OPERATIVAS)
// =========================================================================
function poblarIndicadores(data) {
  const inm = data.inmunizaciones || data;
  const ped = data.pediatria || data;

  if (inm) {
    const mapVacunas = {
      'val_3325401': inm.act_operativa_3325401,
      'val_3325402': inm.act_operativa_3325402,
      'val_3325403': inm.act_operativa_3325403,
      'val_3325404': inm.act_operativa_3325404,
      'val_3325405': inm.act_operativa_3325405,
      'val_3325406': inm.act_operativa_3325406,
      'val_3325407': inm.act_operativa_3325407,
      'val_3325408': inm.act_operativa_3325408,
      'val_3325508': inm.act_operativa_3325508,
    };
    for (const [id, val] of Object.entries(mapVacunas)) {
      const el = document.getElementById(id);
      if (el) el.textContent = val !== undefined ? val : '0';
    }
  }

  if (ped) {
    const mapPediatria = {
      'val_3331501': ped.act_operativa_3331501,
      'val_3341401': ped.act_operativa_3341401,
      'val_3331101': ped.act_operativa_3331101,
      'val_3331102': ped.act_operativa_3331102,
      'val_3331103': ped.act_operativa_3331103,
      'val_3331104': ped.act_operativa_3331104,
      'val_3331105': ped.act_operativa_3331105,
      'val_nuemonia': ped.act_operativa_nuemonia,
      'val_3331301': ped.act_operativa_3331301,
      'val_3331305': ped.act_operativa_3331305,
      'val_3331502': ped.act_operativa_3331502,
      'val_3331201': ped.act_operativa_3331201,
      'val_3331203': ped.act_operativa_3331203,
      'val_3331204': ped.act_operativa_3331204,
      'val_3331401': ped.act_operativa_3331401,
      'val_3331305_shock': ped.act_operativa_3331305_shock,
    };
    for (const [id, val] of Object.entries(mapPediatria)) {
      const el = document.getElementById(id);
      if (el) el.textContent = val !== undefined ? val : '0';
    }
  }

  // Poblar también la matriz comparativa mensual
  poblarMatrizMensual(data);
}

// =========================================================================
// 4. MATRIZ COMPARATIVA MES A MES (OPCIÓN 2: REPORTE CONSOLIDADO)
// =========================================================================
function formatearNombreMes(mesKey) {
  const nombres = {
    '01': 'Ene', '02': 'Feb', '03': 'Mar', '04': 'Abr',
    '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Ago',
    '09': 'Set', '10': 'Oct', '11': 'Nov', '12': 'Dic'
  };
  const parts = mesKey.split('-');
  if (parts.length === 2 && nombres[parts[1]]) {
    return `${nombres[parts[1]]} ${parts[0]}`;
  }
  return mesKey;
}

function obtenerValorAO(dataPeriodo, codigo, grupo) {
  if (!dataPeriodo) return 0;
  const sub = dataPeriodo[grupo];
  if (!sub) return 0;
  const prop = `act_operativa_${codigo}`;
  const raw = sub[prop];
  return raw !== undefined ? parseInt(raw, 10) || 0 : 0;
}

function poblarMatrizMensual(data) {
  const matrixThead = document.getElementById('matrixThead');
  const matrixTbody = document.getElementById('matrixTbody');
  const monthsCountBadge = document.getElementById('matrixMonthsCountBadge');

  if (!matrixThead || !matrixTbody) return;

  const meses = data.meses || [];
  const mensual = data.mensual || {};

  if (monthsCountBadge) {
    monthsCountBadge.textContent = `${meses.length} ${meses.length === 1 ? 'Mes detectado' : 'Meses detectados'}`;
  }

  // Si no hay desglose mensual en la trama, mostrar mensaje
  if (meses.length === 0) {
    matrixThead.innerHTML = `
      <tr>
        <th class="py-3 px-4">Actividad Operativa</th>
        <th class="py-3 px-4 text-center">Total Acumulado</th>
      </tr>
    `;
    matrixTbody.innerHTML = `
      <tr>
        <td colspan="2" class="p-8 text-center text-slate-400">
          No se detectaron fechas en el archivo para el desglose mensual.
        </td>
      </tr>
    `;
    return;
  }

  // 1. Construir Encabezados de la Tabla
  let theadHtml = `
    <tr>
      <th class="py-3 px-4 w-72 sm:w-80 sticky left-0 bg-slate-100 z-10 border-r border-slate-200">
        Actividad Operativa
      </th>
      <th class="py-3 px-3 w-24 text-center border-r border-slate-200">
        Tipo
      </th>
  `;

  meses.forEach(m => {
    theadHtml += `
      <th class="py-3 px-3 text-center border-r border-slate-200 min-w-[80px]">
        <span class="block font-bold text-slate-800">${formatearNombreMes(m)}</span>
      </th>
    `;
  });

  theadHtml += `
      <th class="py-3 px-4 text-center bg-emerald-100/70 text-emerald-950 font-extrabold min-w-[100px]">
        Total Acumulado
      </th>
    </tr>
  `;
  matrixThead.innerHTML = theadHtml;

  // 2. Construir Filas de las 25 AOs agrupadas
  let tbodyHtml = '';
  let currentGroup = '';

  ACTIVIDADES_PPR.forEach(ao => {
    // Si cambia de grupo, agregar fila separadora de categoría
    if (ao.grupo !== currentGroup) {
      currentGroup = ao.grupo;
      const isVac = currentGroup === 'inmunizaciones';
      tbodyHtml += `
        <tr class="${isVac ? 'bg-sky-50 text-sky-900 border-sky-200' : 'bg-emerald-50 text-emerald-900 border-emerald-200'} font-bold uppercase tracking-wider text-[11px] border-y">
          <td colspan="${meses.length + 3}" class="py-2.5 px-4">
            <i class="fa-solid ${isVac ? 'fa-syringe text-sky-600' : 'fa-stethoscope text-emerald-600'} mr-2"></i>
            ${ao.grupoTitulo}
          </td>
        </tr>
      `;
    }

    const totalVal = obtenerValorAO(data, ao.codigo, ao.grupo);
    const linkCie = ao.grupo === 'pediatria' ? `/cie10#ao-card-${ao.codigo === 'nuemonia' ? 'neumonia' : ao.codigo}` : null;

    tbodyHtml += `
      <tr class="hover:bg-slate-50 transition border-b border-slate-100 matrix-row" data-search="${ao.codigo.toLowerCase()} ${ao.titulo.toLowerCase()} ${ao.criterio.toLowerCase()}">
        <!-- Nombre AO -->
        <td class="py-2.5 px-4 sticky left-0 bg-white border-r border-slate-200 shadow-xs">
          <div class="flex items-center gap-2">
            <span class="font-mono font-bold text-[10px] px-1.5 py-0.5 rounded ${ao.grupo === 'inmunizaciones' ? 'bg-sky-100 text-sky-800' : 'bg-emerald-100 text-emerald-800'}">
              AO ${ao.codigo.toUpperCase()}
            </span>
            <div class="min-w-0 flex-1">
              <span class="font-semibold text-slate-800 block truncate text-xs" title="${ao.titulo}">${ao.titulo}</span>
              <span class="text-[10px] text-slate-400 block truncate">${ao.criterio}</span>
            </div>
            ${linkCie ? `
              <a href="${linkCie}" class="ml-1 text-emerald-700 hover:text-emerald-900 text-[10px] shrink-0 font-bold px-1.5 py-0.5 rounded bg-emerald-50 border border-emerald-200 hover:bg-emerald-100 transition" title="Ver códigos CIE-10">
                CIE <i class="fa-solid fa-arrow-right text-[8px]"></i>
              </a>
            ` : ''}
          </div>
        </td>

        <!-- Tipo / Criterio -->
        <td class="py-2.5 px-3 text-center border-r border-slate-200 font-mono text-[10px] font-semibold text-slate-500">
          ${ao.tipo}
        </td>
    `;

    // Celdas por Mes
    meses.forEach(m => {
      const dataMes = mensual[m];
      const valMes = obtenerValorAO(dataMes, ao.codigo, ao.grupo);
      tbodyHtml += `
        <td class="py-2.5 px-3 text-center border-r border-slate-200 font-mono ${valMes > 0 ? 'font-bold text-slate-900 bg-emerald-50/40' : 'text-slate-300'}">
          ${valMes > 0 ? `<span class="inline-block px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-xs">${valMes}</span>` : '0'}
        </td>
      `;
    });

    // Celda Total Acumulado
    tbodyHtml += `
        <td class="py-2.5 px-4 text-center font-mono font-extrabold bg-slate-50/80">
          <span class="inline-block px-2.5 py-0.5 rounded-lg ${totalVal > 0 ? 'bg-emerald-600 text-white shadow-xs' : 'bg-slate-200 text-slate-500'}">
            ${totalVal}
          </span>
        </td>
      </tr>
    `;
  });

  matrixTbody.innerHTML = tbodyHtml;
}

// Búsqueda en tiempo real en la Matriz
const matrixSearchInput = document.getElementById('matrixSearchInput');
if (matrixSearchInput) {
  matrixSearchInput.addEventListener('input', (e) => {
    const q = e.target.value.toLowerCase().trim();
    const rows = document.querySelectorAll('.matrix-row');
    rows.forEach(r => {
      const text = r.getAttribute('data-search') || '';
      if (!q || text.includes(q)) r.classList.remove('hidden');
      else r.classList.add('hidden');
    });
  });
}

// Toggle entre Vista Barras y Vista Matriz Mensual
if (viewBarsBtn && viewMatrixBtn) {
  viewBarsBtn.addEventListener('click', () => {
    viewBarsBtn.className = 'px-3 py-1.5 rounded-lg bg-white text-slate-800 shadow-sm transition flex items-center gap-1.5';
    viewMatrixBtn.className = 'px-3 py-1.5 rounded-lg text-slate-500 hover:text-slate-800 transition flex items-center gap-1.5';
    if (barsViewContainer) barsViewContainer.classList.remove('hidden');
    if (matrixViewContainer) matrixViewContainer.classList.add('hidden');
    if (subFilterGroup) subFilterGroup.classList.remove('hidden');
  });

  viewMatrixBtn.addEventListener('click', () => {
    viewMatrixBtn.className = 'px-3 py-1.5 rounded-lg bg-white text-slate-800 shadow-sm transition flex items-center gap-1.5';
    viewBarsBtn.className = 'px-3 py-1.5 rounded-lg text-slate-500 hover:text-slate-800 transition flex items-center gap-1.5';
    if (barsViewContainer) barsViewContainer.classList.add('hidden');
    if (matrixViewContainer) matrixViewContainer.classList.remove('hidden');
    if (subFilterGroup) subFilterGroup.classList.add('hidden');
  });
}

// Filtros Sub-pestañas Indicadores
const tabAll = document.getElementById('tabAll');
const tabVacunas = document.getElementById('tabVacunas');
const tabPediatria = document.getElementById('tabPediatria');
const bloqueVacunas = document.getElementById('bloqueVacunas');
const bloquePediatria = document.getElementById('bloquePediatria');

function activarSubTab(btn, showVac, showPed) {
  [tabAll, tabVacunas, tabPediatria].forEach(b => {
    b.classList.remove('sub-tab-active');
    b.classList.add('text-slate-600');
  });
  btn.classList.add('sub-tab-active');
  btn.classList.remove('text-slate-600');

  if (showVac) bloqueVacunas.classList.remove('hidden');
  else bloqueVacunas.classList.add('hidden');

  if (showPed) bloquePediatria.classList.remove('hidden');
  else bloquePediatria.classList.add('hidden');

  // Sincronizar Leyenda lateral según pestaña activa
  const cards = document.querySelectorAll('.legend-ao-card');
  const vacHeader = document.querySelector('.legend-group-header-vacunas');
  const pedHeader = document.querySelector('.legend-group-header-pediatria');
  const filterInput = document.getElementById('legendFilterInput');
  const query = filterInput ? filterInput.value.toLowerCase().trim() : '';

  if (!query) {
    if (vacHeader) vacHeader.classList.toggle('hidden', !showVac);
    if (pedHeader) pedHeader.classList.toggle('hidden', !showPed);
    cards.forEach(card => {
      const sec = card.getAttribute('data-section');
      if (sec === 'vacunas') card.classList.toggle('hidden', !showVac);
      if (sec === 'pediatria') card.classList.toggle('hidden', !showPed);
    });
  }
}

if (tabAll && tabVacunas && tabPediatria) {
  tabAll.addEventListener('click', () => activarSubTab(tabAll, true, true));
  tabVacunas.addEventListener('click', () => activarSubTab(tabVacunas, true, false));
  tabPediatria.addEventListener('click', () => activarSubTab(tabPediatria, false, true));
}

// Filtrado en tiempo real de la Leyenda Técnica Lateral
const legendFilterInput = document.getElementById('legendFilterInput');
if (legendFilterInput) {
  legendFilterInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase().trim();
    const cards = document.querySelectorAll('.legend-ao-card');
    const vacHeader = document.querySelector('.legend-group-header-vacunas');
    const pedHeader = document.querySelector('.legend-group-header-pediatria');
    
    if (!query) {
      // Re-aplicar filtro de la pestaña actual
      const isAll = tabAll.classList.contains('sub-tab-active');
      const isVac = tabVacunas.classList.contains('sub-tab-active');
      const isPed = tabPediatria.classList.contains('sub-tab-active');
      activarSubTab(isAll ? tabAll : (isVac ? tabVacunas : tabPediatria), isAll || isVac, isAll || isPed);
      return;
    }

    if (vacHeader) vacHeader.classList.remove('hidden');
    if (pedHeader) pedHeader.classList.remove('hidden');

    cards.forEach(card => {
      const searchData = (card.getAttribute('data-search') || '') + ' ' + card.innerText.toLowerCase();
      if (searchData.includes(query)) {
        card.classList.remove('hidden');
      } else {
        card.classList.add('hidden');
      }
    });
  });
}

// Botón Scroll to Top
const btnScrollTop = document.getElementById('btnScrollTop');
if (btnScrollTop) {
  window.addEventListener('scroll', () => {
    if (window.scrollY > 300) btnScrollTop.classList.remove('hidden');
    else btnScrollTop.classList.add('hidden');
  });
  btnScrollTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

// Funciones de Alerta
function showAlert(message, type) {
  alertBox.className = 'mt-3 p-3.5 rounded-xl text-xs border flex items-start gap-2.5 ';
  if (type === 'error') {
    alertBox.className += 'bg-rose-50 border-rose-200 text-rose-800';
    alertBox.innerHTML = `<i class="fa-solid fa-circle-exclamation text-rose-600 mt-0.5"></i> <div>${message}</div>`;
  } else {
    alertBox.className += 'bg-emerald-50 border-emerald-200 text-emerald-800';
    alertBox.innerHTML = `<i class="fa-solid fa-circle-check text-emerald-600 mt-0.5"></i> <div>${message}</div>`;
  }
  alertBox.classList.remove('hidden');
}

function hideAlert() {
  alertBox.classList.add('hidden');
}
