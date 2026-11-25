// =============================================================================
// PPR 1001 - Script Principal Unificado (Monitor de Indicadores & Desglose CIE-10)
// =============================================================================

// Catálogo Oficial de Diagnósticos CIE-10 de Pediatría (MINSA)
const CATALOGO_CIE = {
  "D509": "Anemia por deficiencia de hierro sin especificación (Ferropénica)",
  "D649": "Anemia de tipo no especificado",
  "B680": "Teniasis debida a Taenia solium (cerdo)",
  "B681": "Teniasis debida a Taenia saginata (vaca)",
  "B689": "Teniasis no especificada",
  "B779": "Ascariasis no especificada",
  "B780": "Estrongiloidiasis intestinal",
  "B79": "Tricocefalosis (Trichuris trichiura)",
  "B80": "Oxiuriasis / Enterobiasis",
  "A071": "Giardiasis [lambliasis]",
  "A06": "Amebiasis",
  "B829": "Parasitosis intestinal sin especificación",
  "J00X": "Rinofaringitis aguda [resfriado común]",
  "J040": "Laringitis aguda",
  "J041": "Traqueítis aguda",
  "J042": "Laringotraqueítis aguda",
  "J060": "Faringitis aguda",
  "J068": "Otras infecciones respiratorias agudas",
  "J069": "Infección respiratoria aguda de sitios no especificados",
  "J209": "Bronquitis aguda",
  "J020": "Faringitis estreptocócica",
  "J029": "Faringitis aguda no especificada",
  "J030": "Amigdalitis estreptocócica",
  "J038": "Amigdalitis aguda debida a otros microorganismos",
  "J039": "Amigdalitis aguda no especificada",
  "H650": "Otitis media aguda no supurativa",
  "H651": "Otras otitis medias agudas no supurativas",
  "H660": "Otitis media aguda supurativa",
  "H669": "Otitis media supurativa y no especificada",
  "J010": "Sinusitis maxilar aguda",
  "J011": "Sinusitis frontal aguda",
  "J012": "Sinusitis etmoidal aguda",
  "J013": "Sinusitis esfenoidal aguda",
  "J014": "Pansinusitis aguda",
  "J019": "Sinusitis aguda no especificada",
  "J129": "Neumonía viral no especificada",
  "J159": "Neumonía bacteriana no especificada",
  "J181": "Neumonía lobar no especificada",
  "A369": "Difteria no especificada",
  "A370": "Tos ferina debida a Bordetella pertussis",
  "A371": "Tos ferina debida a Bordetella parapertussis",
  "A378": "Tos ferina debida a otras especies de Bordetella",
  "A379": "Tos ferina no especificada",
  "J120": "Neumonía por adenovirus",
  "J121": "Neumonía por VSR",
  "J122": "Neumonía por virus parainfluenza",
  "J123": "Neumonía por metapneumovirus",
  "J128": "Otras neumonías virales",
  "J13X": "Neumonía debida a Streptococcus pneumoniae",
  "J14X": "Neumonía debida a Haemophilus influenzae",
  "J150": "Neumonía debida a Klebsiella pneumoniae",
  "J151": "Neumonía debida a Pseudomonas",
  "J152": "Neumonía debida a Staphylococcus",
  "J153": "Neumonía debida a Streptococcus del grupo B",
  "J154": "Neumonía debida a otros estreptococos",
  "J157": "Neumonía debida a Mycoplasma pneumoniae",
  "J158": "Otras neumonías bacterianas",
  "J160": "Neumonía por Chlamydia",
  "J168": "Neumonía por otros microorganismos especificados",
  "J050": "Laringitis obstructiva aguda [crup]",
  "J051": "Epiglotitis aguda",
  "J851": "Absceso del pulmón con neumonía",
  "J860": "Piotórax con fístula",
  "J869": "Piotórax sin fístula",
  "J90X": "Derrame pleural no clasificado",
  "J939": "Neumotórax no especificado",
  "J100": "Influenza con neumonía",
  "J110": "Influenza con neumonía (virus no identificado)",
  "J155": "Neumonía debida a Escherichia coli",
  "J156": "Neumonía por otras bacterias gramnegativas",
  "J180": "Bronconeumonía no especificada",
  "J182": "Neumonía hipostática no especificada",
  "J188": "Otras neumonías de microorganismo no especificado",
  "J210": "Bronquiolitis aguda por VSR",
  "J211": "Bronquiolitis aguda por metapneumovirus",
  "J218": "Bronquiolitis aguda por otros microorganismos",
  "J219": "Bronquiolitis aguda no especificada",
  "J440": "Enfermedad pulmonar obstructiva con infección aguda",
  "J441": "Enfermedad pulmonar obstructiva con exacerbación aguda",
  "J448": "Otras enfermedades pulmonares obstructivas crónicas",
  "J449": "Enfermedad pulmonar obstructiva crónica no especificada",
  "J450": "Asma predominantemente alérgica",
  "J451": "Asma no alérgica",
  "J459": "Asma no especificada",
  "J46X": "Estado asmático agudo severo",
  "A009": "Cólera no especificado",
  "A010": "Fiebre tifoidea",
  "A011": "Fiebre paratifoidea A",
  "A012": "Fiebre paratifoidea B",
  "A013": "Fiebre paratifoidea C",
  "A014": "Fiebre paratifoidea no especificada",
  "A020": "Enteritis debida a Salmonella",
  "A040": "Infección debida a Escherichia coli enteropatógena",
  "A041": "Infección debida a Escherichia coli enterotoxígena",
  "A049": "Infección bacteriana intestinal no especificada",
  "A059": "Intoxicación alimentaria bacteriana no especificada",
  "A070": "Balantidiasis",
  "A072": "Criptosporidiosis",
  "A08": "Infecciones intestinales víricas y otras",
  "A082": "Enteritis debida a adenovirus",
  "A083": "Otras enteritis virales",
  "A084": "Infección intestinal viral sin especificación",
  "A090": "Otras gastroenteritis y colitis de origen infeccioso",
  "A099": "Gastroenteritis y colitis de origen no especificado",
  "A030": "Shigelosis debida a Shigella dysenteriae",
  "A039": "Shigelosis de tipo no especificado",
  "A042": "Infección debida a Escherichia coli enteroinvasiva",
  "A043": "Infección debida a Escherichia coli enterohemorrágica",
  "A045": "Enteritis debida a Campylobacter",
  "A060": "Disentería amebiana aguda",
  "A09X": "Diarrea y gastroenteritis de presunto origen infeccioso",
  "E86X": "Depleción del volumen [deshidratación]",
  "R571": "Choque hipovolémico",
  "E872": "Acidosis",
  "K560": "Íleo paralítico"
};

// Catálogo de las 25 Actividades Operativas para la Matriz Mensual
const ACTIVIDADES_PPR = [
  // 1. INMUNIZACIONES (9 AOs)
  {
    codigo: "3325401",
    titulo: "VACUNACIÓN BCG EN RECIEN NACIDOS",
    criterio: "CPT 90708 (Dosis RN < 28 días)",
    tipo: "CPT",
    grupo: "inmunizaciones",
    grupoTitulo: "Inmunizaciones & Vacunas (ppr1001_vacunas.py)",
    icon: "fa-syringe",
    color: "sky"
  },
  {
    codigo: "3325402",
    titulo: "VACUNACIÓN HEPATITIS B PEDIÁTRICA (HVB)",
    criterio: "CPT 90744 (Dosis RN en 12-24 horas)",
    tipo: "CPT",
    grupo: "inmunizaciones",
    grupoTitulo: "Inmunizaciones & Vacunas (ppr1001_vacunas.py)",
    icon: "fa-syringe",
    color: "sky"
  },
  {
    codigo: "3325403",
    titulo: "VACUNACIÓN PENTAVALENTE (1ra, 2da, 3ra Dosis)",
    criterio: "CPT 90723, 90720 (Lab 1, 2, 3 a 2m, 4m, 6m)",
    tipo: "CPT",
    grupo: "inmunizaciones",
    grupoTitulo: "Inmunizaciones & Vacunas (ppr1001_vacunas.py)",
    icon: "fa-syringe",
    color: "sky"
  },
  {
    codigo: "3325404",
    titulo: "(BCG + HvB)",
    criterio: "90585 (BCG) y CPT 90744 (HvB)",
    tipo: "CPT",
    grupo: "inmunizaciones",
    grupoTitulo: "Inmunizaciones & Vacunas (ppr1001_vacunas.py)",
    icon: "fa-syringe",
    color: "sky"
  },
  {
    codigo: "3325405",
    titulo: "INFLUENZA PEDIATRICA",
    criterio: "CPT 90681 (2 meses y 4 meses)",
    tipo: "CPT",
    grupo: "inmunizaciones",
    grupoTitulo: "Inmunizaciones & Vacunas (ppr1001_vacunas.py)",
    icon: "fa-syringe",
    color: "sky"
  },
  {
    codigo: "3325406",
    titulo: "INFLUENZA",
    criterio: "CPT 90669 (2m, 4m y refuerzo al año)",
    tipo: "CPT",
    grupo: "inmunizaciones",
    grupoTitulo: "Inmunizaciones & Vacunas (ppr1001_vacunas.py)",
    icon: "fa-syringe",
    color: "sky"
  },
  {
    codigo: "3325407",
    titulo: "VACUNACION NINO DE MADRE CON VIH (NEUMOCOCO 3)",
    criterio: "CPT 90707 (1ra Dosis 12m, 2da Dosis 18m)",
    tipo: "CPT",
    grupo: "inmunizaciones",
    grupoTitulo: "Inmunizaciones & Vacunas (ppr1001_vacunas.py)",
    icon: "fa-syringe",
    color: "sky"
  },
  {
    codigo: "3325408",
    titulo: "ATENCION DE EVENTOS ADVERSOS A VACUNAS",
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
    criterio: "SEGUIMIENTO DEL NINO Y NINA DE ALTO RIESGO",
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
// 1. INICIALIZACIÓN (DATA MART DIRECTO - SIN LOCALSTORAGE)
// =========================================================================
async function iniciarApp() {
  // Limpiar cualquier residuo previo de LocalStorage o SessionStorage
  limpiarResiduosStorage();

  // Consultar automáticamente si ya existen datos acumulados en el Data Mart SQLite
  try {
    const response = await fetch('/api/v1/ppr1001/acumulado');
    if (response.ok) {
      const data = await response.json();
      if (data && data.meses && data.meses.length > 0) {
        datosCargados = data;
        if (persistedFileName) persistedFileName.textContent = "Data Mart (SQLite)";
        if (persistedTime) persistedTime.textContent = `(Meses: ${data.meses.length})`;
        if (persistedBadge) persistedBadge.classList.remove('hidden');
        if (resetBtn) resetBtn.classList.remove('hidden');

        poblarIndicadores(data);
        resultsTopBar.classList.remove('hidden');
        resultsSection.classList.remove('hidden');
      }
    }
  } catch (e) {
    console.log("Data Mart sin datos previos o esperando carga inicial:", e);
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', iniciarApp);
} else {
  iniciarApp();
}

function limpiarResiduosStorage() {
  try {
    localStorage.removeItem('ppr1001_resultado');
    localStorage.removeItem('ppr1001_nombre_archivo');
    localStorage.removeItem('ppr1001_fecha_proceso');
    sessionStorage.removeItem('ultimoResultadoPPR');
    sessionStorage.removeItem('ultimoNombreArchivo');
  } catch (e) {
    // Silencioso
  }
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
  const lowerName = file.name.toLowerCase();
  if (!lowerName.endsWith('.xlsx') && !lowerName.endsWith('.xls') && !lowerName.endsWith('.csv')) {
    showAlert('El archivo seleccionado no es un formato válido (.xlsx, .xls o .csv).', 'error');
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
  processBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> <span>Procesando archivo HIS...</span>';
  hideAlert();

  try {
    const response = await fetch('/api/v1/ppr1001/procesar', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'Ocurrió un error al procesar el archivo HIS (Excel o CSV).');
    }

    datosCargados = data;

    // Actualizar badge con nombre de archivo subido
    persistedFileName.textContent = currentFile.name;
    persistedTime.textContent = `(Cargado: ${new Date().toLocaleTimeString()})`;
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

// Botón: Consultar Acumulado directamente desde el Data Mart SQLite
const btnConsultarDatamart = document.getElementById('btnConsultarDatamart');
if (btnConsultarDatamart) {
  btnConsultarDatamart.addEventListener('click', async () => {
    btnConsultarDatamart.disabled = true;
    btnConsultarDatamart.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> <span>Consultando Data Mart...</span>';
    hideAlert();
    try {
      const response = await fetch('/api/v1/ppr1001/acumulado');
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || 'Error al consultar acumulado del Data Mart.');
      }
      datosCargados = data;
      if (persistedFileName) persistedFileName.textContent = "Data Mart SQLite (Acumulado)";
      if (persistedTime) persistedTime.textContent = `(Sincronizado: ${new Date().toLocaleTimeString()})`;
      if (persistedBadge) persistedBadge.classList.remove('hidden');
      poblarIndicadores(data);
      resultsTopBar.classList.remove('hidden');
      resultsSection.classList.remove('hidden');
      showAlert('¡Datos acumulados cargados exitosamente desde la base de datos Data Mart!', 'success');
      resultsTopBar.scrollIntoView({ behavior: 'smooth' });
    } catch (err) {
      showAlert(err.message, 'error');
    } finally {
      btnConsultarDatamart.disabled = false;
      btnConsultarDatamart.innerHTML = '<i class="fa-solid fa-database text-emerald-300"></i> <span>Ver Acumulado en Base de Datos</span>';
    }
  });
}

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
// 4. MATRIZ COMPARATIVA MES A MES UNIFICADA CON DESGLOSE CIE-10
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

function obtenerConteosCieAO(dataPeriodo, codigo) {
  if (!dataPeriodo || !dataPeriodo.pediatria || !dataPeriodo.pediatria.conteos_cie) return {};
  const key = codigo === 'nuemonia' ? 'neumonia' : codigo;
  return dataPeriodo.pediatria.conteos_cie[key] || {};
}

let todosExpandidos = false;

function poblarMatrizMensual(data) {
  const matrixThead = document.getElementById('matrixThead');
  const matrixTbody = document.getElementById('matrixTbody');
  const monthsCountBadge = document.getElementById('matrixMonthsCountBadge');

  if (!matrixThead || !matrixTbody) return;

  const meses = data.meses || [];
  const mensual = data.mensual || {};
  const mesesFaltantes = new Set(data.meses_faltantes || []);

  // Alerta informativa si existen meses faltantes / huecos en la trama
  const matrixGapAlert = document.getElementById('matrixGapAlert');
  const matrixGapMonthsList = document.getElementById('matrixGapMonthsList');
  if (matrixGapAlert && matrixGapMonthsList) {
    if (mesesFaltantes.size > 0) {
      const nombresFaltantes = Array.from(mesesFaltantes).map(formatearNombreMes).join(', ');
      matrixGapMonthsList.textContent = nombresFaltantes;
      matrixGapAlert.classList.remove('hidden');
    } else {
      matrixGapAlert.classList.add('hidden');
    }
  }

  if (monthsCountBadge) {
    if (mesesFaltantes.size > 0) {
      monthsCountBadge.innerHTML = `<span class="text-emerald-700">${meses.length - mesesFaltantes.size} con datos</span> &bull; <span class="text-amber-700 font-bold">${mesesFaltantes.size} ${mesesFaltantes.size === 1 ? 'pendiente' : 'pendientes'}</span>`;
      monthsCountBadge.classList.remove('bg-emerald-50', 'text-emerald-700', 'border-emerald-200');
      monthsCountBadge.classList.add('bg-amber-50', 'text-amber-800', 'border-amber-200');
    } else {
      monthsCountBadge.textContent = `${meses.length} ${meses.length === 1 ? 'Mes detectado' : 'Meses detectados'}`;
      monthsCountBadge.classList.remove('bg-amber-50', 'text-amber-800', 'border-amber-200');
      monthsCountBadge.classList.add('bg-emerald-50', 'text-emerald-700', 'border-emerald-200');
    }
  }

  // Si no hay desglose mensual en la trama, mostrar mensaje
  if (meses.length === 0) {
    matrixThead.innerHTML = `
      <tr>
        <th class="py-3 px-4">Actividad Operativa</th>
        <th class="py-3 px-4 text-center">Tipo</th>
        <th class="py-3 px-4 text-center">Total Acumulado</th>
      </tr>
    `;
    matrixTbody.innerHTML = `
      <tr>
        <td colspan="3" class="p-8 text-center text-slate-400">
          No se detectaron fechas en el archivo para el desglose mensual.
        </td>
      </tr>
    `;
    return;
  }

  // 1. Construir Encabezados de la Tabla
  let theadHtml = `
    <tr>
      <th class="py-3 px-4 w-80 sm:w-96 sticky left-0 bg-slate-100 z-10 border-r border-slate-200">
        Actividad Operativa &amp; Desglose CIE-10
      </th>
      <th class="py-3 px-3 w-20 text-center border-r border-slate-200">
        Tipo
      </th>
  `;

  meses.forEach(m => {
    const esFaltante = mesesFaltantes.has(m);
    if (esFaltante) {
      theadHtml += `
        <th class="py-2.5 px-3 text-center border-r border-amber-200 bg-amber-50/80 min-w-[95px]" title="Período sin datos en la base de datos (Pendiente de carga)">
          <span class="block font-bold text-amber-900">${formatearNombreMes(m)}</span>
          <span class="inline-flex items-center gap-1 mt-0.5 px-1.5 py-0.5 rounded text-[9px] font-bold bg-amber-200/90 text-amber-900 border border-amber-300">
            <i class="fa-solid fa-clock text-[8px]"></i> Sin datos
          </span>
        </th>
      `;
    } else {
      theadHtml += `
        <th class="py-3 px-3 text-center border-r border-slate-200 min-w-[85px]">
          <span class="block font-bold text-slate-800">${formatearNombreMes(m)}</span>
        </th>
      `;
    }
  });

  theadHtml += `
      <th class="py-3 px-4 text-center bg-emerald-100/70 text-emerald-950 font-extrabold min-w-[110px]">
        Total Acumulado
      </th>
    </tr>
  `;
  matrixThead.innerHTML = theadHtml;

  // 2. Construir Filas de las 25 AOs agrupadas y sus CIE-10 hijos
  let tbodyHtml = '';
  let currentGroup = '';

  ACTIVIDADES_PPR.forEach(ao => {
    // Si cambia de grupo, agregar fila separadora de categoría interactiva (colapsable)
    if (ao.grupo !== currentGroup) {
      currentGroup = ao.grupo;
      const isVac = currentGroup === 'inmunizaciones';
      tbodyHtml += `
        <tr class="btn-toggle-group cursor-pointer select-none ${isVac ? 'bg-sky-50 hover:bg-sky-100/80 text-sky-900 border-sky-200' : 'bg-emerald-50 hover:bg-emerald-100/80 text-emerald-900 border-emerald-200'} font-bold uppercase tracking-wider text-[11px] border-y transition" data-group="${currentGroup}" title="Clic para colapsar o expandir ${isVac ? 'Inmunizaciones' : 'Pediatría'}">
          <td colspan="${meses.length + 3}" class="py-2.5 px-4">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2.5">
                <i class="fa-solid fa-chevron-down text-[10px] transition-transform duration-200" id="chevron-group-${currentGroup}"></i>
                <i class="fa-solid ${isVac ? 'fa-syringe text-sky-600' : 'fa-stethoscope text-emerald-600'}"></i>
                <span>${ao.grupoTitulo}</span>
              </div>
              <div class="flex items-center gap-2 font-normal lowercase tracking-normal text-[11px]">
                <span class="px-2 py-0.5 rounded-full ${isVac ? 'bg-sky-200/70 text-sky-800' : 'bg-emerald-200/70 text-emerald-800'} font-bold">
                  ${isVac ? '9 Actividades' : '16 Actividades'}
                </span>
                <span class="text-slate-400 text-[10px] hidden sm:inline">(clic para colapsar / expandir grupo)</span>
              </div>
            </div>
          </td>
        </tr>
      `;
    }

    const totalVal = obtenerValorAO(data, ao.codigo, ao.grupo);
    const conteosTot = ao.grupo === 'pediatria' ? obtenerConteosCieAO(data, ao.codigo) : {};
    const codigosCieKeys = Object.keys(conteosTot);
    const tieneCie = codigosCieKeys.length > 0;

    // Fila Padre (Actividad Operativa)
    tbodyHtml += `
      <tr id="matrix-row-${ao.codigo}" class="hover:bg-slate-50 transition border-b border-slate-200 matrix-row matrix-parent-row" data-ao="${ao.codigo}" data-grupo="${ao.grupo}" data-search="${ao.codigo.toLowerCase()} ${ao.titulo.toLowerCase()} ${ao.criterio.toLowerCase()}">
        <!-- Nombre AO con toggle acordeón -->
        <td class="py-2.5 px-4 sticky left-0 bg-white border-r border-slate-200 shadow-xs z-1">
          <div class="flex items-center gap-2">
            ${tieneCie ? `
              <button type="button" class="btn-toggle-ao w-6 h-6 rounded hover:bg-slate-100 text-slate-500 hover:text-slate-800 flex items-center justify-center shrink-0 transition" data-ao="${ao.codigo}" title="Mostrar/Ocultar códigos CIE-10">
                <i class="fa-solid fa-chevron-right text-[10px] transition-transform duration-200" id="chevron-${ao.codigo}"></i>
              </button>
            ` : `
              <span class="w-6 h-6 flex items-center justify-center text-slate-300 shrink-0">
                <i class="fa-solid ${ao.grupo === 'inmunizaciones' ? 'fa-syringe text-sky-400' : 'fa-circle-dot'} text-[10px]"></i>
              </span>
            `}
            <span class="font-mono font-bold text-[10px] px-1.5 py-0.5 rounded shrink-0 ${ao.grupo === 'inmunizaciones' ? 'bg-sky-100 text-sky-800' : 'bg-emerald-100 text-emerald-800'}">
              AO ${ao.codigo.toUpperCase()}
            </span>
            <div class="min-w-0 flex-1">
              <span class="font-semibold text-slate-800 block truncate text-xs" title="${ao.titulo}">${ao.titulo}</span>
              <span class="text-[10px] text-slate-400 block truncate">${ao.criterio}</span>
            </div>
            ${tieneCie ? `
              <span class="text-[10px] text-slate-500 bg-slate-100 font-medium px-1.5 py-0.5 rounded border border-slate-200 shrink-0">
                ${codigosCieKeys.length} CIE-10
              </span>
            ` : ''}
          </div>
        </td>

        <!-- Tipo / Criterio -->
        <td class="py-2.5 px-3 text-center border-r border-slate-200 font-mono text-[10px] font-semibold text-slate-500">
          ${ao.tipo}
        </td>
    `;

    // Celdas por Mes (AO)
    meses.forEach(m => {
      const esFaltante = mesesFaltantes.has(m);
      if (esFaltante) {
        tbodyHtml += `
          <td class="py-2.5 px-3 text-center border-r border-amber-100 bg-amber-50/25 font-mono text-slate-400 select-none" title="Mes ${formatearNombreMes(m)}: Sin datos registrados">
            <span class="inline-block px-1.5 py-0.5 rounded bg-slate-100 text-slate-400 text-xs font-semibold">-</span>
          </td>
        `;
      } else {
        const dataMes = mensual[m];
        const valMes = obtenerValorAO(dataMes, ao.codigo, ao.grupo);
        tbodyHtml += `
          <td class="py-2.5 px-3 text-center border-r border-slate-200 font-mono ${valMes > 0 ? 'font-bold text-slate-900 bg-emerald-50/40' : 'text-slate-300'}">
            ${valMes > 0 ? `<span class="inline-block px-1.5 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-xs">${valMes}</span>` : '0'}
          </td>
        `;
      }
    });

    // Celda Total Acumulado (AO)
    tbodyHtml += `
        <td class="py-2.5 px-4 text-center font-mono font-extrabold bg-slate-50/80">
          <span class="inline-block px-2.5 py-0.5 rounded-lg ${totalVal > 0 ? 'bg-emerald-600 text-white shadow-xs' : 'bg-slate-200 text-slate-500'}">
            ${totalVal}
          </span>
        </td>
      </tr>
    `;

    // Filas Hijas (Detalle de cada CIE-10 para esta AO)
    if (tieneCie) {
      codigosCieKeys.forEach(cieCode => {
        const descCie = CATALOGO_CIE[cieCode] || 'Diagnóstico pediátrico';
        const valTotCie = conteosTot[cieCode] || 0;

        tbodyHtml += `
          <tr class="matrix-child-row matrix-child-${ao.codigo} hidden bg-slate-50/70 hover:bg-emerald-50/30 transition border-b border-slate-100" data-parent-ao="${ao.codigo}" data-search="${ao.codigo.toLowerCase()} ${cieCode.toLowerCase()} ${descCie.toLowerCase()}">
            <!-- Nombre y código CIE-10 con sangría -->
            <td class="py-1.5 pl-10 pr-4 sticky left-0 bg-slate-50/95 border-r border-slate-200 shadow-xs z-1">
              <div class="flex items-center gap-2">
                <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 shrink-0"></span>
                <span class="font-mono font-bold text-[10px] px-1.5 py-0.5 rounded bg-white text-slate-700 border border-slate-200 shrink-0 shadow-2xs">${cieCode}</span>
                <span class="text-[11px] text-slate-600 truncate flex-1" title="${descCie}">${descCie}</span>
              </div>
            </td>

            <!-- Tipo -->
            <td class="py-1.5 px-3 text-center border-r border-slate-200 font-mono text-[9px] text-slate-400">
              CIE-10
            </td>
        `;

        // Conteos mensuales del CIE-10
        meses.forEach(m => {
          const esFaltante = mesesFaltantes.has(m);
          if (esFaltante) {
            tbodyHtml += `
              <td class="py-1.5 px-3 text-center border-r border-amber-100 bg-amber-50/20 font-mono text-xs text-slate-400 select-none" title="Mes ${formatearNombreMes(m)}: Sin datos registrados">
                <span class="inline-block px-1.5 py-0.5 rounded bg-slate-100 text-slate-400 text-[11px] font-semibold">-</span>
              </td>
            `;
          } else {
            const conteoMesCie = obtenerConteosCieAO(mensual[m], ao.codigo);
            const valMesCie = conteoMesCie[cieCode] || 0;
            tbodyHtml += `
              <td class="py-1.5 px-3 text-center border-r border-slate-200 font-mono text-xs ${valMesCie > 0 ? 'font-bold text-slate-800 bg-emerald-50/20' : 'text-slate-300'}">
                ${valMesCie > 0 ? `<span class="inline-block px-1.5 py-0.5 rounded bg-slate-200/80 text-slate-800 font-bold text-[11px]">${valMesCie}</span>` : '0'}
              </td>
            `;
          }
        });

        // Total acumulado del CIE-10
        tbodyHtml += `
            <td class="py-1.5 px-4 text-center font-mono font-bold text-xs bg-slate-50/90">
              <span class="inline-block px-2 py-0.5 rounded-full ${valTotCie > 0 ? 'bg-slate-200 text-slate-800 font-bold' : 'text-slate-300'} text-[11px]">
                ${valTotCie}
              </span>
            </td>
          </tr>
        `;
      });
    }
  });

  matrixTbody.innerHTML = tbodyHtml;

  // Registrar listeners para colapsar/expandir Grupos Principales (Inmunizaciones / Pediatría)
  document.querySelectorAll('.btn-toggle-group').forEach(btn => {
    btn.addEventListener('click', () => {
      const group = btn.getAttribute('data-group');
      toggleGroup(group);
    });
  });

  // Registrar listeners de expandir/colapsar para cada botón chevron de AO
  document.querySelectorAll('.btn-toggle-ao').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const aoCode = btn.getAttribute('data-ao');
      toggleAoCie10(aoCode);
    });
  });

  // Si había estado expandido previo, sincronizar
  if (todosExpandidos) {
    expandirTodosCie10(true);
  }
}

// Alternar expansión/colapso de Grupos Principales (Inmunizaciones / Pediatría)
function toggleGroup(group, forzarEstado = null) {
  const parentRows = document.querySelectorAll(`.matrix-parent-row[data-grupo="${group}"]`);
  const chevron = document.getElementById(`chevron-group-${group}`);
  if (!parentRows.length) return;

  const deberiaMostrar = forzarEstado !== null ? forzarEstado : parentRows[0].classList.contains('hidden');

  parentRows.forEach(row => {
    const aoCode = row.getAttribute('data-ao');
    if (deberiaMostrar) {
      row.classList.remove('hidden');
      // Si el chevron individual de esta AO estaba abierto, re-mostrar sus hijos CIE-10
      const aoChevron = document.getElementById(`chevron-${aoCode}`);
      if (aoChevron && aoChevron.classList.contains('rotate-90')) {
        document.querySelectorAll(`.matrix-child-${aoCode}`).forEach(c => c.classList.remove('hidden'));
      }
    } else {
      row.classList.add('hidden');
      // Ocultar también cualquier hijo abierto de esta AO
      document.querySelectorAll(`.matrix-child-${aoCode}`).forEach(c => c.classList.add('hidden'));
    }
  });

  if (chevron) {
    if (deberiaMostrar) {
      chevron.classList.remove('-rotate-90');
    } else {
      chevron.classList.add('-rotate-90');
    }
  }
}

// Alternar expansión de una AO individual
function toggleAoCie10(aoCode, forzarEstado = null) {
  const childRows = document.querySelectorAll(`.matrix-child-${aoCode}`);
  const chevron = document.getElementById(`chevron-${aoCode}`);
  if (!childRows.length) return;

  const deberiaMostrar = forzarEstado !== null ? forzarEstado : childRows[0].classList.contains('hidden');

  childRows.forEach(row => {
    if (deberiaMostrar) {
      row.classList.remove('hidden');
    } else {
      row.classList.add('hidden');
    }
  });

  if (chevron) {
    if (deberiaMostrar) {
      chevron.classList.add('rotate-90', 'text-emerald-600');
    } else {
      chevron.classList.remove('rotate-90', 'text-emerald-600');
    }
  }
}

// Expandir o Colapsar Todos los CIE-10 globalmente
function expandirTodosCie10(expandir) {
  todosExpandidos = expandir;
  const allChildRows = document.querySelectorAll('.matrix-child-row');
  const allChevrons = document.querySelectorAll('.btn-toggle-ao i');
  const toggleBtnText = document.getElementById('toggleAllCie10Text');

  allChildRows.forEach(row => {
    if (expandir) row.classList.remove('hidden');
    else row.classList.add('hidden');
  });

  allChevrons.forEach(chev => {
    if (expandir) chev.classList.add('rotate-90', 'text-emerald-600');
    else chev.classList.remove('rotate-90', 'text-emerald-600');
  });

  if (toggleBtnText) {
    toggleBtnText.textContent = expandir ? 'Colapsar CIE-10' : 'Expandir CIE-10';
  }
}

// Botón de alternar todo en la cabecera de la matriz
const btnToggleAllCie10 = document.getElementById('btnToggleAllCie10');
if (btnToggleAllCie10) {
  btnToggleAllCie10.addEventListener('click', () => {
    expandirTodosCie10(!todosExpandidos);
  });
}

// Búsqueda en tiempo real en la Matriz con apertura automática de CIE-10
const matrixSearchInput = document.getElementById('matrixSearchInput');
if (matrixSearchInput) {
  matrixSearchInput.addEventListener('input', (e) => {
    const q = e.target.value.toLowerCase().trim();
    const parentRows = document.querySelectorAll('.matrix-parent-row');
    const childRows = document.querySelectorAll('.matrix-child-row');

    if (!q) {
      // Restaurar visibilidad de padres, hijos y grupos
      document.querySelectorAll('.btn-toggle-group').forEach(btn => {
        btn.classList.remove('hidden');
        const grp = btn.getAttribute('data-group');
        toggleGroup(grp, true);
      });
      parentRows.forEach(p => p.classList.remove('hidden'));
      childRows.forEach(c => {
        if (todosExpandidos) c.classList.remove('hidden');
        else c.classList.add('hidden');
      });
      return;
    }

    // Filtrar padres e hijos
    const parentMatches = new Set();
    const groupMatches = new Set();

    // 1. Revisar si el hijo coincide con la búsqueda
    childRows.forEach(c => {
      const search = c.getAttribute('data-search') || '';
      const parentAo = c.getAttribute('data-parent-ao');
      if (search.includes(q)) {
        c.classList.remove('hidden');
        parentMatches.add(parentAo);
      } else {
        c.classList.add('hidden');
      }
    });

    // 2. Revisar padres
    parentRows.forEach(p => {
      const ao = p.getAttribute('data-ao');
      const grp = p.getAttribute('data-grupo');
      const search = p.getAttribute('data-search') || '';
      if (search.includes(q) || parentMatches.has(ao)) {
        p.classList.remove('hidden');
        if (grp) groupMatches.add(grp);
        const chevron = document.getElementById(`chevron-${ao}`);
        if (chevron && parentMatches.has(ao)) {
          chevron.classList.add('rotate-90', 'text-emerald-600');
        }
      } else {
        p.classList.add('hidden');
      }
    });

    // 3. Mostrar/ocultar y expandir encabezados de grupo según coincidencias
    document.querySelectorAll('.btn-toggle-group').forEach(btn => {
      const grp = btn.getAttribute('data-group');
      if (groupMatches.has(grp)) {
        btn.classList.remove('hidden');
        const chev = document.getElementById(`chevron-group-${grp}`);
        if (chev) chev.classList.remove('-rotate-90');
      } else {
        btn.classList.add('hidden');
      }
    });
  });
}

// Salto desde la Vista de Barras directamente a la Matriz y expansión de esa AO
function cambiarAMatrizYExpandir(aoCode) {
  if (viewMatrixBtn) {
    viewMatrixBtn.click();
  }
  setTimeout(() => {
    toggleGroup('pediatria', true);
    toggleAoCie10(aoCode, true);
    const row = document.getElementById(`matrix-row-${aoCode}`);
    if (row) {
      row.scrollIntoView({ behavior: 'smooth', block: 'center' });
      row.classList.add('bg-emerald-100/60');
      setTimeout(() => row.classList.remove('bg-emerald-100/60'), 2000);
    }
  }, 150);
}

// Conectar botones en vista de barras con salto a la matriz
document.addEventListener('click', (e) => {
  const btn = e.target.closest('.btn-jump-matrix');
  if (btn) {
    const ao = btn.getAttribute('data-ao');
    if (ao) cambiarAMatrizYExpandir(ao);
  }
});


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
