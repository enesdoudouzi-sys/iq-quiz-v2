const API = 'http://localhost:8000';
const L   = ['A','B','C','D'];
const COL = {
  'Allgemeinwissen':      '#4a90e2',
  'Logik & Zahlenfolgen': '#7c5fff',
  'Konzentration':        '#06b6d4',
};
const CK = p => p.includes('Allgemein') ? 'aw' : p.includes('Logik') ? 'log' : 'kz';

let qs=[], cur=0, sc=0, done=false, ti=null, tl=0, st=0;
let cs={aw:0,log:0,kz:0}, cm={aw:0,log:0,kz:0}, times=[], errs=[];
let playerName='', finalIQ=0;

function showStart(){
  document.getElementById('sv').style.display='flex';
  document.getElementById('qv').style.display='none';
  document.getElementById('rv').style.display='none';
  document.getElementById('hv').style.display='none';
}
function showQuiz(){
  document.getElementById('sv').style.display='none';
  document.getElementById('qv').style.display='flex';
  document.getElementById('rv').style.display='none';
  document.getElementById('hv').style.display='none';
}
function showResult(){
  document.getElementById('sv').style.display='none';
  document.getElementById('qv').style.display='none';
  document.getElementById('rv').style.display='block';
  document.getElementById('hv').style.display='none';
}

async function showHS(){
  document.getElementById('sv').style.display='none';
  document.getElementById('hv').style.display='block';
  const res    = await fetch(API+'/api/highscores');
  const scores = await res.json();
  const med    = ['🥇','🥈','🥉'];
  const hl     = document.getElementById('hl');
  if(!scores.length){
    hl.innerHTML='<div class="none">Noch keine Einträge.</div>';
  } else {
    hl.innerHTML = scores.map((s,i)=>`
      <div class="hs-item">
        <span class="hs-rang">${med[i]||((i+1)+'.')}</span>
        <span class="hs-name">${s.name}</span>
        <span class="hs-level">Frage ${s.level}</span>
        <span class="hs-iq">IQ ~${s.iq}</span>
      </div>`).join('');
  }
}

async function startGame(){
  playerName = document.getElementById('ni').value.trim() || 'Spieler';
  cur=0; sc=0; done=false;
  cs={aw:0,log:0,kz:0}; cm={aw:0,log:0,kz:0};
  times=[]; errs=[]; qs=[];
  for(let lvl=1; lvl<=15; lvl++){
    const res = await fetch(API+'/api/frage/'+lvl);
    const d   = await res.json();
    qs.push({
      p:     d.kategorie,
      t:     d.frage,
      o:     ['A','B','C','D'].map(k => d.antworten[k]),
      seq:   d.seq || null,
      s:     lvl <= 5 ? 20 : lvl <= 10 ? 25 : 30,
      level: lvl,
    });
  }
  showQuiz();
  showQ();
}

function showQ(){
  if(cur >= qs.length){ calcResult(); return; }
  const q = qs[cur]; done = false;
  document.getElementById('pf').style.width  = (cur/qs.length*100)+'%';
  document.getElementById('qc').textContent  = (cur+1)+' / '+qs.length;
  document.getElementById('pb').textContent  = q.p.toUpperCase();
  const col = COL[q.p]||'#4a90e2';
  document.getElementById('pdot').style.background = col;
  document.getElementById('pb').style.color        = col;
  document.getElementById('ta').style.stroke       = col;
  document.getElementById('qt').textContent   = q.t;
  document.getElementById('fb').textContent   = '';
  document.getElementById('fb').className     = 'fb';
  document.getElementById('nb').style.display = 'none';
  const sb = document.getElementById('sb');
  if(q.seq){ sb.textContent=q.seq; sb.style.display='block'; }
  else sb.style.display='none';
  const op = document.getElementById('op'); op.innerHTML='';
  q.o.forEach((o,i)=>{
    const b = document.createElement('button');
    b.className = 'opt';
    b.innerHTML = '<span class="badge">'+L[i]+'</span><span>'+o+'</span>';
    b.onclick   = ()=>pick(i);
    op.appendChild(b);
  });
  st = Date.now();
  tick(q.s, q.s);
  ti = setInterval(()=>{ tl--; tick(tl,q.s); if(tl<=0){ clearInterval(ti); tout(); }}, 1000);
}

function tick(l,t){
  tl=l;
  document.getElementById('tn').textContent = l;
  document.getElementById('ta').style.strokeDashoffset = 376.99*(1-l/t);
  const urgent=l<=5, warn=l<=10;
  const col = urgent?'#ef4444': warn?'#f59e0b': (COL[qs[cur]?.p]||'#4a90e2');
  document.getElementById('ta').style.stroke = col;
  document.getElementById('tn').style.color  = urgent?'#ef4444': warn?'#f59e0b':'#f1f5f9';
  const w = document.getElementById('trw');
  if(urgent) w.classList.add('urgent-pulse'); else w.classList.remove('urgent-pulse');
}

function tout(){
  if(done) return; done=true;
  const q = qs[cur];
  cm[CK(q.p)]++;
  times.push(q.s);
  fetch(API+'/api/antwort',{
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({level:q.level, antwort:'X'})
  }).then(r=>r.json()).then(d=>{
    const ri=d.richtige_antwort, ri_idx=L.indexOf(ri);
    errs.push({q, ch:null, to:true, ri_idx, ri_txt:q.o[ri_idx]});
    document.querySelectorAll('.opt')[ri_idx].classList.add('ok');
    document.querySelectorAll('.opt').forEach(b=>b.disabled=true);
    const fb=document.getElementById('fb');
    fb.textContent='⏱ Zeit abgelaufen! Richtig wäre: '+ri+' – '+q.o[ri_idx];
    fb.className='fb to';
    document.getElementById('nb').style.display='block';
  });
}

async function pick(i){
  if(done) return; done=true; clearInterval(ti);
  const el=Math.min((Date.now()-st)/1000, qs[cur].s);
  times.push(el);
  const q=qs[cur]; const k=CK(q.p); cm[k]++;
  const res=await fetch(API+'/api/antwort',{
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({level:q.level, antwort:L[i]})
  });
  const d=await res.json();
  const bs=document.querySelectorAll('.opt');
  const fb=document.getElementById('fb');
  const ri_idx=L.indexOf(d.richtige_antwort);
  if(d.richtig){
    sc++; cs[k]++;
    bs[i].classList.add('ok');
    fb.textContent='✓ Richtig!'; fb.className='fb ok';
  } else {
    bs[i].classList.add('no');
    bs[ri_idx].classList.add('ok');
    errs.push({q, ch:i, to:false, ri_idx, ri_txt:q.o[ri_idx]});
    fb.textContent='✗ Falsch. Richtig wäre: '+d.richtige_antwort+' – '+d.richtige_antwort_text;
    fb.className='fb no';
  }
  bs.forEach(b=>b.disabled=true);
  document.getElementById('nb').style.display='block';
}

document.getElementById('nb').onclick = ()=>{ cur++; showQ(); };

function calcResult(){
  showResult();
  document.getElementById('pf').style.width='100%';
  const avg=times.length ? Math.round(times.reduce((a,b)=>a+b,0)/times.length*10)/10 : 0;
  const iq=Math.min(145, Math.round(72+(sc/qs.length)*60));
  finalIQ=iq;
  document.getElementById('rs').textContent=sc+' von '+qs.length+' Punkten';
  document.getElementById('ri').textContent='IQ ~'+iq;
  let d='';
  if(iq>=130)      d='Hervorragend! Du zeigst eine sehr hohe kognitive Leistungsfähigkeit.';
  else if(iq>=115) d='Sehr gut! Dein Denkvermögen liegt deutlich über dem Durchschnitt.';
  else if(iq>=100) d='Gut! Du befindest dich im normalen bis leicht überdurchschnittlichen Bereich.';
  else if(iq>=85)  d='In Ordnung. Regelmäßiges Üben kann dir helfen, dich zu verbessern.';
  else             d='Noch Potenzial vorhanden – mit Training wirst du dich steigern!';
  document.getElementById('rd').textContent=d;
  document.getElementById('baw').textContent =cs.aw+' / '+cm.aw;
  document.getElementById('blog').textContent=cs.log+' / '+cm.log;
  document.getElementById('bkz').textContent =cs.kz+' / '+cm.kz;
  document.getElementById('bt').textContent  =avg+' Sek.';
  document.getElementById('sn').value        =playerName;
  const ml=document.getElementById('ml'); ml.innerHTML='';
  const mt=document.getElementById('mtit');
  if(!errs.length){
    mt.textContent='Fehlerauswertung';
    ml.innerHTML='<div class="none">Perfekt – keine einzige falsche Antwort! 🎉</div>';
  } else {
    mt.textContent='FEHLERAUSWERTUNG · '+errs.length+' Fehler';
    errs.forEach(({q,ch,to,ri_idx,ri_txt})=>{
      const c=document.createElement('div'); c.className='mc';
      let h='<div class="mm">'+q.p+'</div>';
      if(to) h+='<span class="tob">⏱ Zeit abgelaufen</span>';
      h+='<div class="mq">'+q.t+'</div>';
      if(q.seq) h+='<div class="ms">'+q.seq+'</div>';
      h+='<div class="ar">';
      if(!to && ch!=null)
        h+='<div class="ans-col"><span class="ans-lbl">Deine Antwort</span><span class="pill pno">'+L[ch]+' – '+q.o[ch]+'</span></div>';
      h+='<div class="ans-col"><span class="ans-lbl">Richtige Antwort</span><span class="pill pok">'+L[ri_idx]+' – '+ri_txt+'</span></div></div>';
      c.innerHTML=h; ml.appendChild(c);
    });
  }
}

async function saveHS(){
  const name=document.getElementById('sn').value.trim()||playerName;
  await fetch(API+'/api/highscores',{
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({name, iq:finalIQ, level:sc})
  });
  const btn=document.querySelector('.save-btn');
  btn.textContent='✅ Gespeichert!';
  setTimeout(()=>btn.textContent='💾 Speichern', 2000);
}
