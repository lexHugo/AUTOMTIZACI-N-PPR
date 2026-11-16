// =============================================================================
// PPR 1001 - Script de la Página de Desglose y Auditoría CIE-10 (cie10.html)
// =============================================================================

// Catálogo de descripciones amigables
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

// Metadatos de Actividades Operativas
const INFO_AO = {
  "3331501": { titulo: "Anemia en < 5 Años", categoriaKey: "nutricion", categoria: "Nutrición & Prevalentes", icon: "fa-droplet", color: "red" },
  "3341401": { titulo: "Parasitosis Intestinal en < 5 Años", categoriaKey: "nutricion", categoria: "Nutrición & Prevalentes", icon: "fa-bacterium", color: "amber" },
  "3331101": { titulo: "IRA No Complicada", categoriaKey: "iras", categoria: "Infecciones Respiratorias (IRAs)", icon: "fa-head-side-cough", color: "sky" },
  "3331102": { titulo: "FAPA (Faringoamigdalitis)", categoriaKey: "iras", categoria: "Infecciones Respiratorias (IRAs)", icon: "fa-lungs", color: "blue" },
  "3331103": { titulo: "OMA (Otitis Media Aguda)", categoriaKey: "iras", categoria: "Infecciones Respiratorias (IRAs)", icon: "fa-ear-listen", color: "indigo" },
  "3331104": { titulo: "Sinusitis Aguda", categoriaKey: "iras", categoria: "Infecciones Respiratorias (IRAs)", icon: "fa-virus", color: "purple" },
  "3331105": { titulo: "Neumonía No Complicada", categoriaKey: "iras", categoria: "Infecciones Respiratorias (IRAs)", icon: "fa-lungs-virus", color: "violet" },
  "neumonia": { titulo: "Neumonía con Complicaciones", categoriaKey: "iras", categoria: "Infecciones Respiratorias (IRAs)", icon: "fa-hospital", color: "fuchsia" },
  "3331301": { titulo: "Neumonía Muy Grave (< 2 Meses)", categoriaKey: "iras", categoria: "Infecciones Respiratorias (IRAs)", icon: "fa-circle-exclamation", color: "rose" },
  "3331305": { titulo: "Neumonía Muy Grave (2m a 4a)", categoriaKey: "iras", categoria: "Infecciones Respiratorias (IRAs)", icon: "fa-triangle-exclamation", color: "pink" },
  "3331502": { titulo: "SOBA / ASMA Pediátrico", categoriaKey: "iras", categoria: "Infecciones Respiratorias (IRAs)", icon: "fa-lungs", color: "orange" },
  "3331201": { titulo: "EDA No Complicada", categoriaKey: "edas", categoria: "Enfermedades Diarreicas (EDAs)", icon: "fa-notes-medical", color: "emerald" },
  "3331203": { titulo: "EDA Disentérica", categoriaKey: "edas", categoria: "Enfermedades Diarreicas (EDAs)", icon: "fa-bacteria", color: "teal" },
  "3331204": { titulo: "EDA Persistente", categoriaKey: "edas", categoria: "Enfermedades Diarreicas (EDAs)", icon: "fa-clock-rotate-left", color: "cyan" },
  "3331401": { titulo: "EDA con Deshidratación", categoriaKey: "edas", categoria: "Enfermedades Diarreicas (EDAs)", icon: "fa-faucet-drip", color: "yellow" },
  "3331305_shock": { titulo: "EDA con Deshidratación y Shock", categoriaKey: "edas", categoria: "Enfermedades Diarreicas (EDAs)", icon: "fa-heart-pulse", color: "red" }
};

let datosGlobales = null;
let categoriaActiva = "all";
let vistaActual = "accordion"; // 'accordion' o 'table'

function inicializarCie10Page() {
  // 1. Cargar datos desde localStorage (compartido con Monitor Principal) o sessionStorage
  const guardado = localStorage.getItem('ppr1001_resultado') || sessionStorage.getItem('ultimoResultadoPPR');
  const nombreArchivo = localStorage.getItem('ppr1001_nombre_archivo') || sessionStorage.getItem('ultimoNombreArchivo');

  if (guardado) {
    try {
      const data = JSON.parse(guardado);
      if (nombreArchivo) {
        document.getElementById('currentFileTitle').textContent = `Archivo: ${nombreArchivo}`;
        document.getElementById('currentFileSub').textContent = 'Datos en memoria listos para análisis';
        document.getElementById('headerFileBadge').textContent = nombreArchivo;
        document.getElementById('headerFileBadge').classList.remove('hidden');
      }
      renderizarDesglose(data);
    } catch (e) {
      console.error(e);
      mostrarVacio();
    }
  } else {
    mostrarVacio();
  }

  // 2. Eventos de Archivo
  const fileInput = document.getElementById('fileInput');
  const uploadBtn = document.getElementById('uploadBtn');
  if (uploadBtn && fileInput) {
    uploadBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', async (e) => {
      if (e.target.files.length) await procesarArchivo(e.target.files[0]);
    });
  }

  // 3. Toggle de Vista: Acordeón vs Tabla
  const viewAccBtn = document.getElementById('viewAccordionBtn');
  const viewTblBtn = document.getElementById('viewGlobalTableBtn');

  if (viewAccBtn && viewTblBtn) {
    viewAccBtn.addEventListener('click', () => {
      vistaActual = 'accordion';
      viewAccBtn.className = 'px-2.5 py-1 rounded-lg bg-white text-slate-800 shadow-sm transition';
      viewTblBtn.className = 'px-2.5 py-1 rounded-lg text-slate-500 hover:text-slate-800 transition';
      document.getElementById('aoContainer').classList.remove('hidden');
      document.getElementById('globalTableContainer').classList.add('hidden');
    });

    viewTblBtn.addEventListener('click', () => {
      vistaActual = 'table';
      viewTblBtn.className = 'px-2.5 py-1 rounded-lg bg-white text-slate-800 shadow-sm transition';
      viewAccBtn.className = 'px-2.5 py-1 rounded-lg text-slate-500 hover:text-slate-800 transition';
      document.getElementById('aoContainer').classList.add('hidden');
      document.getElementById('globalTableContainer').classList.remove('hidden');
    });
  }

  // 4. Búsqueda en tiempo real
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.addEventListener('input', filtrarTarjetas);
  }

  // 5. Scroll Top Button
  const btnScrollTop = document.getElementById('btnScrollTop');
  if (btnScrollTop) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 300) {
        btnScrollTop.classList.remove('hidden');
      } else {
        btnScrollTop.classList.add('hidden');
      }
    });
    btnScrollTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', inicializarCie10Page);
} else {
  inicializarCie10Page();
}

async function procesarArchivo(file) {
  if (!file.name.endsWith('.xlsx') && !file.name.endsWith('.xls')) {
    alert('Por favor selecciona un archivo Excel (.xlsx o .xls)');
    return;
  }

  const formData = new FormData();
  formData.append('file', file);

  document.getElementById('loadingBox').classList.remove('hidden');
  document.getElementById('emptyBox').classList.add('hidden');
  document.getElementById('aoContainer').innerHTML = '';
  document.getElementById('globalTableBody').innerHTML = '';

  try {
    const response = await fetch('/api/v1/ppr1001/procesar', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Error al procesar archivo');

    localStorage.setItem('ppr1001_resultado', JSON.stringify(data));
    localStorage.setItem('ppr1001_nombre_archivo', file.name);
    localStorage.setItem('ppr1001_fecha_proceso', new Date().toLocaleTimeString());
    sessionStorage.setItem('ultimoResultadoPPR', JSON.stringify(data));
    sessionStorage.setItem('ultimoNombreArchivo', file.name);

    document.getElementById('currentFileTitle').textContent = `Archivo: ${file.name}`;
    document.getElementById('currentFileSub').textContent = `Procesado: ${new Date().toLocaleTimeString()}`;
    document.getElementById('headerFileBadge').textContent = file.name;
    document.getElementById('headerFileBadge').classList.remove('hidden');

    renderizarDesglose(data);
  } catch (err) {
    alert(err.message);
    mostrarVacio();
  } finally {
    document.getElementById('loadingBox').classList.add('hidden');
  }
}

function mostrarVacio() {
  document.getElementById('emptyBox').classList.remove('hidden');
  document.getElementById('aoContainer').innerHTML = '';
  document.getElementById('globalTableBody').innerHTML = '';
  document.getElementById('statTotalCodigos').textContent = '0';
  document.getElementById('statConRegistros').textContent = '0';
  document.getElementById('statEnCero').textContent = '0';
}

function renderizarDesglose(data) {
  datosGlobales = data;
  const ped = data.pediatria || data;
  const conteos = (ped && ped.conteos_cie) ? ped.conteos_cie : {};

  const container = document.getElementById('aoContainer');
  const globalTableBody = document.getElementById('globalTableBody');

  container.innerHTML = '';
  globalTableBody.innerHTML = '';

  let totalCodigos = 0;
  let conRegistros = 0;
  let enCero = 0;

  let indexCard = 0;

  for (const [keyAO, meta] of Object.entries(INFO_AO)) {
    const codigosDict = conteos[keyAO] || {};
    const codigosKeys = Object.keys(codigosDict);
    if (codigosKeys.length === 0) continue;

    indexCard++;
    const valorAO = (ped && ped[`act_operativa_${keyAO}`]) || (ped && ped[`act_operativa_nuemonia`] && keyAO === 'neumonia') || '0';
    
    let sumAOConRegistros = 0;
    let sumAOEnCero = 0;

    for (const [cie, cnt] of Object.entries(codigosDict)) {
      totalCodigos++;
      if (cnt > 0) {
        conRegistros++;
        sumAOConRegistros++;
      } else {
        enCero++;
        sumAOEnCero++;
      }

      // Llenar fila de la Tabla Global Consolidada
      const descCie = CATALOGO_CIE[cie] || 'Diagnóstico MINSA';
      const tieneReg = cnt > 0;
      const trGlobal = document.createElement('tr');
      trGlobal.className = 'hover:bg-slate-50 transition global-tr';
      trGlobal.dataset.cie = cie.toLowerCase();
      trGlobal.dataset.desc = descCie.toLowerCase();
      trGlobal.dataset.cnt = cnt;
      trGlobal.dataset.cat = meta.categoriaKey;
      trGlobal.innerHTML = `
        <td class="py-2.5 px-4 font-mono font-bold">
          <span class="px-2 py-0.5 rounded-md ${tieneReg ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-slate-100 text-slate-500'}">
            ${cie}
          </span>
        </td>
        <td class="py-2.5 px-4 text-slate-700">${descCie}</td>
        <td class="py-2.5 px-4 text-slate-500 text-[11px]">
          <span class="font-bold text-slate-700">AO ${keyAO}</span> &bull; ${meta.titulo}
        </td>
        <td class="py-2.5 px-4 text-center font-mono font-bold ${tieneReg ? 'text-slate-900' : 'text-slate-300'}">
          ${cnt}
        </td>
        <td class="py-2.5 px-4 text-right">
          ${tieneReg 
            ? '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-100 text-emerald-800"><i class="fa-solid fa-check"></i> Activo</span>'
            : '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-medium bg-slate-100 text-slate-400">En cero</span>'
          }
        </td>
      `;
      globalTableBody.appendChild(trGlobal);
    }

    // Crear Tarjeta con Acordeón
    const aoCard = document.createElement('div');
    aoCard.id = `ao-card-${keyAO}`;
    aoCard.className = 'bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden ao-block transition hover:shadow-md';
    aoCard.dataset.aoKey = keyAO;
    aoCard.dataset.cat = meta.categoriaKey;

    // Todas las tarjetas inician desplegadas para mostrar la lista de códigos CIE-10 inmediatamente
    const isCollapsedByDefault = false;

    aoCard.innerHTML = `
      <!-- Cabecera Clickeable para Acordeón -->
      <div class="ao-header p-3.5 cursor-pointer select-none flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2.5 bg-slate-50/60 hover:bg-slate-100/70 transition">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-xl bg-${meta.color}-100 text-${meta.color}-600 flex items-center justify-center text-sm shadow-sm shrink-0">
            <i class="fa-solid ${meta.icon}"></i>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="text-[10px] font-bold uppercase tracking-wider px-1.5 py-0.5 rounded-md bg-slate-200 text-slate-700 font-mono">AO ${keyAO.toUpperCase()}</span>
              <span class="text-xs text-slate-400 font-medium">${meta.categoria}</span>
            </div>
            <h3 class="text-xs sm:text-sm font-bold text-slate-800 mt-0.5">${meta.titulo}</h3>
          </div>
        </div>

        <div class="flex items-center gap-2.5 self-end sm:self-auto shrink-0">
          <div class="text-right">
            <span class="text-[9px] text-slate-400 block font-medium uppercase">Cumplen</span>
            <span class="text-base font-extrabold text-${meta.color}-600 font-mono">${valorAO}</span>
          </div>
          <div class="h-6 w-px bg-slate-200"></div>
          <div class="text-right">
            <span class="text-[9px] text-slate-400 block font-medium uppercase">CIE Activos</span>
            <span class="text-[11px] font-semibold px-2 py-0.5 rounded-full ${sumAOConRegistros === codigosKeys.length ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-100 text-slate-600'}">
              ${sumAOConRegistros}/${codigosKeys.length}
            </span>
          </div>
          <div class="w-7 h-7 rounded-lg bg-white border border-slate-200 flex items-center justify-center text-slate-400 shadow-sm ml-0.5">
            <i class="fa-solid fa-chevron-down text-xs transition-transform duration-200 ao-chevron ${isCollapsedByDefault ? '' : 'rotate-180'}"></i>
          </div>
        </div>
      </div>

      <!-- Tabla Colapsable -->
      <div class="ao-table-wrapper ${isCollapsedByDefault ? 'hidden' : ''} border-t border-slate-100">
        <div class="overflow-x-auto max-h-80">
          <table class="w-full text-left text-xs">
            <thead class="bg-slate-50 text-slate-500 uppercase tracking-wider font-semibold border-b border-slate-100 sticky top-0 bg-slate-50">
              <tr>
                <th class="py-2.5 px-4 w-28">Código CIE-10</th>
                <th class="py-2.5 px-4">Descripción Clínica</th>
                <th class="py-2.5 px-4 w-32 text-center">Frecuencia</th>
                <th class="py-2.5 px-4 w-28 text-right">Estado</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-100">
              ${codigosKeys.map(cie => {
                const cnt = codigosDict[cie] || 0;
                const desc = CATALOGO_CIE[cie] || 'Diagnóstico MINSA';
                const tieneRegistros = cnt > 0;
                
                return `
                  <tr class="cie-row hover:bg-slate-50/80 transition" data-cie="${cie}" data-desc="${desc.toLowerCase()}" data-cnt="${cnt}">
                    <td class="py-2.5 px-4 font-mono font-bold">
                      <span class="px-2 py-0.5 rounded-md ${tieneRegistros ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-slate-100 text-slate-500'}">
                        ${cie}
                      </span>
                    </td>
                    <td class="py-2.5 px-4 text-slate-700 font-medium">${desc}</td>
                    <td class="py-2.5 px-4 text-center font-mono font-bold text-sm ${tieneRegistros ? 'text-slate-900' : 'text-slate-400'}">
                      ${cnt}
                    </td>
                    <td class="py-2.5 px-4 text-right">
                      ${tieneRegistros 
                        ? '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-semibold bg-emerald-100 text-emerald-800"><i class="fa-solid fa-check text-[9px]"></i> &ge; 1</span>'
                        : '<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[11px] font-medium bg-slate-100 text-slate-400">0</span>'
                      }
                    </td>
                  </tr>
                `;
              }).join('')}
            </tbody>
          </table>
        </div>
      </div>
    `;

    // Evento de Acordeón para abrir/cerrar al hacer clic en la cabecera
    const headerEl = aoCard.querySelector('.ao-header');
    const wrapperEl = aoCard.querySelector('.ao-table-wrapper');
    const chevronEl = aoCard.querySelector('.ao-chevron');

    headerEl.addEventListener('click', () => {
      const isHidden = wrapperEl.classList.toggle('hidden');
      if (isHidden) {
        chevronEl.classList.remove('rotate-180');
      } else {
        chevronEl.classList.add('rotate-180');
      }
    });

    container.appendChild(aoCard);
  }

  // Actualizar contadores globales
  document.getElementById('statTotalCodigos').textContent = totalCodigos;
  document.getElementById('statConRegistros').textContent = conRegistros;
  document.getElementById('statEnCero').textContent = enCero;
  document.getElementById('globalTableBadge').textContent = `${conRegistros} con registros / ${totalCodigos} totales`;

  document.getElementById('emptyBox').classList.add('hidden');
  container.classList.remove('hidden');

  // Si la URL viene con hash específico (ej. #ao-card-3331501), desplazarse hacia la tarjeta
  if (window.location.hash) {
    setTimeout(() => {
      const target = document.querySelector(window.location.hash);
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'center' });
        target.classList.add('ring-2', 'ring-emerald-500');
        setTimeout(() => target.classList.remove('ring-2', 'ring-emerald-500'), 2500);
      }
    }, 150);
  }
}

// Filtrar tarjetas por búsqueda de texto
function filtrarTarjetas() {
  const q = document.getElementById('searchInput') ? document.getElementById('searchInput').value.trim().toLowerCase() : '';

  // Filtrar Vista 1: Acordeones
  const blocks = document.querySelectorAll('.ao-block');
  blocks.forEach(block => {
    const rows = block.querySelectorAll('.cie-row');
    let blockHasMatch = false;

    rows.forEach(row => {
      const cie = row.dataset.cie.toLowerCase();
      const desc = row.dataset.desc;
      const matchText = !q || cie.includes(q) || desc.includes(q);

      if (matchText) {
        row.classList.remove('hidden');
        blockHasMatch = true;
      } else {
        row.classList.add('hidden');
      }
    });

    // Si se está buscando texto específico, expandir automáticamente la tarjeta que tiene coincidencias
    if (q && blockHasMatch) {
      block.querySelector('.ao-table-wrapper').classList.remove('hidden');
      block.querySelector('.ao-chevron').classList.add('rotate-180');
    }

    if (blockHasMatch) {
      block.classList.remove('hidden');
    } else {
      block.classList.add('hidden');
    }
  });

  // Filtrar Vista 2: Tabla Global Consolidada
  const globalRows = document.querySelectorAll('.global-tr');
  globalRows.forEach(row => {
    const cie = row.dataset.cie;
    const desc = row.dataset.desc;
    const matchText = !q || cie.includes(q) || desc.includes(q);

    if (matchText) {
      row.classList.remove('hidden');
    } else {
      row.classList.add('hidden');
    }
  });
}
