// =============================================================================
// PPR 1001 - Script Principal de la Aplicación (Monitor de Indicadores)
// =============================================================================

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

      // Poblar indicadores
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

    // Poblar indicadores
    poblarIndicadores(data);

    resultsTopBar.classList.remove('hidden');
    resultsSection.classList.remove('hidden');

    showAlert('¡Archivo procesado con éxito! Todas las fórmulas e indicadores han sido calculados.', 'success');
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
