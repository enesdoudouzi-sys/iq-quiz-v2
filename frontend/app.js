const API = 'https://iq-quiz-v2.onrender.com';
const L = ['A','B','C','D'];
const COL = {'Allgemeinwissen':'#4a90e2','Logik & Zahlenfolgen':'#7c5fff','Konzentration':'#06b6d4','Geschichte':'#f59e0b','Wissenschaft & Natur':'#22c55e','Wissenschaft':'#22c55e','Sport':'#ef4444','Mathematik':'#a855f7','Musik':'#ec4899','Geographie':'#14b8a6'};
const KAT_ICONS = {'Allgemeinwissen':'🌍','Logik & Zahlenfolgen':'🧩','Konzentration':'🎯','Geschichte':'📜','Wissenschaft & Natur':'🔬','Wissenschaft':'🔬','Sport':'⚽','Mathematik':'🔢','Musik':'🎵','Geographie':'🗺️'};
const MAX_FRAGEN = 15;
const IQ_TBL = {};
for(var i=0;i<=50;i++){
  if(i===0)IQ_TBL[i]=85;
  else if(i<=5)IQ_TBL[i]=85+i*3;
  else if(i<=10)IQ_TBL[i]=100+(i-5)*3;
  else if(i<=15)IQ_TBL[i]=115+(i-10)*3;
  else if(i<=20)IQ_TBL[i]=130+(i-15)*3;
  else IQ_TBL[i]=Math.min(145,145+(i-20));
}
const PREISE_ARR=['100','200','300','500','1.000','2.000','4.000','8.000','16.000','32.000','64.000','125.000','250.000','500.000','1.000.000'];
function getPreis(lvl){return PREISE_ARR[Math.min(lvl-1,PREISE_ARR.length-1)]+' EUR';}
const SICHER=[5,10,15];

var currentLang='de';
const LANG={
  de:{title:'IQ Test',sub:'Teste deinen IQ · 15 Fragen · 3 Joker',placeholder:'Dein Name...',start:'Jetzt starten',highscores:'Highscores',sekunden:'Sekunden',iqLabel:'Aktueller IQ',joker:'Joker',richtig:'Richtig!',falsch:'Falsch! Ausgeschieden!',zeit:'Zeit abgelaufen! Ausgeschieden!',naechste:'Naechste Frage',ergebnis:'Dein Ergebnis',speichern:'Speichern',gespeichert:'Gespeichert!',nochmal:'Nochmal starten',zurueck:'Zurueck',perfekt:'Perfekt - alle Fragen richtig!',fehler:'FEHLERAUSWERTUNG',deine:'Deine Antwort',richtige:'Richtige Antwort',leiter:'IQ Leiter',schliessen:'Schliessen',telefon:'Telefon-Joker',publikum:'Publikums-Joker',iqNach:'Dein IQ nach dieser Frage',teilen:'Ergebnis teilen'},
  en:{title:'IQ Test',sub:'Test Your IQ · 15 Questions · 3 Lifelines',placeholder:'Your Name...',start:'Start Now',highscores:'Highscores',sekunden:'Seconds',iqLabel:'Current IQ',joker:'Lifelines',richtig:'Correct!',falsch:'Wrong! Game Over!',zeit:'Time Up! Game Over!',naechste:'Next Question',ergebnis:'Your Result',speichern:'Save',gespeichert:'Saved!',nochmal:'Play Again',zurueck:'Back',perfekt:'Perfect - all correct!',fehler:'ERROR ANALYSIS',deine:'Your Answer',richtige:'Correct Answer',leiter:'IQ Ladder',schliessen:'Close',telefon:'Phone Lifeline',publikum:'Audience Lifeline',iqNach:'Your IQ after this question',teilen:'Share Result'},
  tr:{title:'IQ Testi',sub:'IQ\'nunu Test Et · 15 Soru · 3 Joker',placeholder:'Adiniz...',start:'Baslat',highscores:'Yuksek Skorlar',sekunden:'Saniye',iqLabel:'Guncel IQ',joker:'Jokerler',richtig:'Dogru!',falsch:'Yanlis! Elendil!',zeit:'Sure Doldu! Elendil!',naechste:'Sonraki Soru',ergebnis:'Sonucunuz',speichern:'Kaydet',gespeichert:'Kaydedildi!',nochmal:'Tekrar Oyna',zurueck:'Geri',perfekt:'Mukemmel!',fehler:'HATA ANALIZI',deine:'Cevabiniz',richtige:'Dogru Cevap',leiter:'IQ Merdiveni',schliessen:'Kapat',telefon:'Telefon Jokeri',publikum:'Seyirci Jokeri',iqNach:'Bu sorudan sonra IQ'},
  fr:{title:'Test QI',sub:'Questions Illimitees - 3 Jokers',placeholder:'Votre Nom...',start:'Commencer',highscores:'Meilleurs Scores',sekunden:'Secondes',iqLabel:'QI Actuel',joker:'Jokers',richtig:'Correct!',falsch:'Faux! Elimine!',zeit:'Temps Ecoule!',naechste:'Question Suivante',ergebnis:'Votre Resultat',speichern:'Sauvegarder',gespeichert:'Sauvegarde!',nochmal:'Rejouer',zurueck:'Retour',perfekt:'Parfait!',fehler:'ANALYSE ERREURS',deine:'Votre Reponse',richtige:'Bonne Reponse',leiter:'Echelle QI',schliessen:'Fermer',telefon:'Joker Telephone',publikum:'Joker Public',iqNach:'Votre QI apres'},
  es:{title:'Test de IQ',sub:'Preguntas Ilimitadas - 3 Comodines',placeholder:'Tu Nombre...',start:'Comenzar',highscores:'Mejores Puntuaciones',sekunden:'Segundos',iqLabel:'IQ Actual',joker:'Comodines',richtig:'Correcto!',falsch:'Incorrecto! Eliminado!',zeit:'Tiempo Agotado!',naechste:'Siguiente Pregunta',ergebnis:'Tu Resultado',speichern:'Guardar',gespeichert:'Guardado!',nochmal:'Jugar de Nuevo',zurueck:'Volver',perfekt:'Perfecto!',fehler:'ANALISIS ERRORES',deine:'Tu Respuesta',richtige:'Respuesta Correcta',leiter:'Escalera IQ',schliessen:'Cerrar',telefon:'Comodin Telefono',publikum:'Comodin Publico',iqNach:'Tu IQ despues'},
  ar:{title:'اختبار الذكاء',sub:'اسئلة غير محدودة - 3 نجدات',placeholder:'اسمك...',start:'ابدأ الآن',highscores:'أعلى النتائج',sekunden:'ثانية',iqLabel:'الذكاء الحالي',joker:'النجدات',richtig:'صحيح!',falsch:'خطأ! خرجت!',zeit:'انتهى الوقت!',naechste:'السؤال التالي',ergebnis:'نتيجتك',speichern:'حفظ',gespeichert:'تم الحفظ!',nochmal:'العب مجددا',zurueck:'رجوع',perfekt:'ممتاز!',fehler:'تحليل الأخطاء',deine:'إجابتك',richtige:'الإجابة الصحيحة',leiter:'سلم الذكاء',schliessen:'إغلاق',telefon:'نجدة الهاتف',publikum:'نجدة الجمهور',iqNach:'ذكاؤك بعد هذا السؤال'},
};

function T(key){return LANG[currentLang][key]||LANG['de'][key]||key;}

function setLang(lang,btn){
  currentLang=lang;
  document.querySelectorAll('.lang-btn').forEach(function(b){b.classList.remove('active');});
  if(btn)btn.classList.add('active');
  document.body.style.direction=lang==='ar'?'rtl':'ltr';
  var t=LANG[lang];
  document.querySelector('.s-title').textContent=t.title;
  document.querySelector('.s-sub').textContent=t.sub;
  document.getElementById('ni').placeholder=t.placeholder;
  document.querySelector('.s-btn').textContent=t.start;
  document.querySelector('.s-hs').textContent=t.highscores;
  document.querySelector('.t-lbl').textContent=t.sekunden;
  document.querySelector('.iq-live-lbl').textContent=t.iqLabel;
  document.querySelector('.joker-title').textContent=t.joker;
  document.querySelector('.leiter-lbl').textContent=t.leiter;
  document.getElementById('nb').textContent=t.naechste;
  document.querySelector('.jo-close').textContent=t.schliessen;
  document.querySelector('.rv-lbl').textContent=t.ergebnis;
  document.querySelector('.save-btn').textContent=t.speichern;
  document.querySelector('.iq-fb-lbl').textContent=t.iqNach;
}

// ── SOUNDS ────────────────────────────────────────────────
var _ac=null;
function _ctx(){
  if(!_ac||_ac.state==='closed')_ac=new(window.AudioContext||window.webkitAudioContext)();
  if(_ac.state==='suspended')_ac.resume();
  return _ac;
}
function playSound(type){
  try{
    var ctx=_ctx();
    var o=ctx.createOscillator(),g=ctx.createGain();
    o.connect(g);g.connect(ctx.destination);
    if(type==='richtig'){
      o.frequency.setValueAtTime(523,ctx.currentTime);
      o.frequency.setValueAtTime(659,ctx.currentTime+0.1);
      o.frequency.setValueAtTime(784,ctx.currentTime+0.2);
      g.gain.setValueAtTime(0.3,ctx.currentTime);
      g.gain.exponentialRampToValueAtTime(0.001,ctx.currentTime+0.5);
      o.start(ctx.currentTime);o.stop(ctx.currentTime+0.5);
    }else if(type==='falsch'){
      o.frequency.setValueAtTime(200,ctx.currentTime);
      o.frequency.setValueAtTime(150,ctx.currentTime+0.2);
      g.gain.setValueAtTime(0.3,ctx.currentTime);
      g.gain.exponentialRampToValueAtTime(0.001,ctx.currentTime+0.4);
      o.start(ctx.currentTime);o.stop(ctx.currentTime+0.4);
    }else if(type==='tick'){
      o.frequency.setValueAtTime(900,ctx.currentTime);
      g.gain.setValueAtTime(0.12,ctx.currentTime);
      g.gain.exponentialRampToValueAtTime(0.001,ctx.currentTime+0.06);
      o.start(ctx.currentTime);o.stop(ctx.currentTime+0.06);
    }else if(type==='gewonnen'){
      [523,659,784,1047].forEach(function(f,i){
        var o2=ctx.createOscillator(),g2=ctx.createGain();
        o2.connect(g2);g2.connect(ctx.destination);
        o2.frequency.setValueAtTime(f,ctx.currentTime+i*0.15);
        g2.gain.setValueAtTime(0.3,ctx.currentTime+i*0.15);
        g2.gain.exponentialRampToValueAtTime(0.001,ctx.currentTime+i*0.15+0.3);
        o2.start(ctx.currentTime+i*0.15);o2.stop(ctx.currentTime+i*0.15+0.3);
      });
    }else if(type==='sicher'){
      [523,784,1047,784,1047].forEach(function(f,i){
        var o2=ctx.createOscillator(),g2=ctx.createGain();
        o2.connect(g2);g2.connect(ctx.destination);
        o2.frequency.setValueAtTime(f,ctx.currentTime+i*0.1);
        g2.gain.setValueAtTime(0.28,ctx.currentTime+i*0.1);
        g2.gain.exponentialRampToValueAtTime(0.001,ctx.currentTime+i*0.1+0.18);
        o2.start(ctx.currentTime+i*0.1);o2.stop(ctx.currentTime+i*0.1+0.18);
      });
    }else if(type==='joker'){
      o.frequency.setValueAtTime(440,ctx.currentTime);
      o.frequency.setValueAtTime(550,ctx.currentTime+0.08);
      g.gain.setValueAtTime(0.18,ctx.currentTime);
      g.gain.exponentialRampToValueAtTime(0.001,ctx.currentTime+0.2);
      o.start(ctx.currentTime);o.stop(ctx.currentTime+0.2);
    }
  }catch(e){}
}

// ── KONFETTI & ANIMATIONEN ─────────────────────────────────
function animateCount(el,from,to,ms){
  var s=Date.now();
  (function step(){
    var p=Math.min((Date.now()-s)/ms,1),e=1-Math.pow(1-p,3);
    el.textContent='IQ '+Math.round(from+(to-from)*e);
    if(p<1)requestAnimationFrame(step);
  })();
}
var _caf=null;
function launchConfetti(intensity){
  var cv=document.getElementById('cc');
  if(!cv)return;
  var ctx2=cv.getContext('2d');
  cv.width=window.innerWidth;cv.height=window.innerHeight;
  cv.style.display='block';
  if(_caf)cancelAnimationFrame(_caf);
  ctx2.clearRect(0,0,cv.width,cv.height);
  var cols=['#4a90e2','#7c5fff','#ffd700','#22c55e','#f59e0b','#ef4444','#06b6d4','#fff'];
  var n=intensity==='big'?220:intensity==='medium'?90:40;
  var ps=[];
  for(var i=0;i<n;i++){
    var big=intensity==='big';
    ps.push({
      x:big?Math.random()*cv.width:cv.width/2+(Math.random()-.5)*400,
      y:big?Math.random()*-cv.height*.7:-60,
      w:Math.random()*10+4,h:Math.random()*6+3,
      c:cols[Math.floor(Math.random()*cols.length)],
      rot:Math.random()*360,
      vx:(Math.random()-.5)*(big?6:9),
      vy:big?Math.random()*4+1:Math.random()*-9-2,
      vr:(Math.random()-.5)*14,
      grav:big?.13:.3
    });
  }
  var dur=intensity==='big'?3500:intensity==='medium'?2200:1200;
  var end=Date.now()+dur;
  function draw(){
    var now=Date.now();
    ctx2.clearRect(0,0,cv.width,cv.height);
    var alive=false;
    ps.forEach(function(p){
      p.vy+=p.grav;p.x+=p.vx;p.y+=p.vy;p.rot+=p.vr;
      var life=Math.max(0,(end-now)/dur);
      if(p.y<cv.height+30)alive=true;
      ctx2.save();ctx2.globalAlpha=Math.min(1,life*1.5);
      ctx2.translate(p.x,p.y);ctx2.rotate(p.rot*Math.PI/180);
      ctx2.fillStyle=p.c;ctx2.fillRect(-p.w/2,-p.h/2,p.w,p.h);
      ctx2.restore();
    });
    if(alive&&now<end+1500){_caf=requestAnimationFrame(draw);}
    else{cv.style.display='none';}
  }
  draw();
}

// ── LOADING ────────────────────────────────────────────────
function showLoader(txt,pct){
  var s=document.getElementById('loading-screen');
  var b=document.getElementById('load-bar');
  var t=document.getElementById('load-txt');
  if(s)s.style.display='flex';
  if(b)b.style.width=pct+'%';
  if(t)t.textContent=txt;
}
function hideLoader(){
  var s=document.getElementById('loading-screen');
  if(s){
    s.style.opacity='0';
    s.style.transition='opacity .5s';
    s.style.pointerEvents='none';
    setTimeout(function(){s.style.display='none';},500);
  }
}
// Render free tier braucht bis zu 30s zum Starten — mehrfach versuchen
showLoader('Verbinde mit Server...',10);
(function pingServer(attempt){
  var msgs=[
    ['Verbinde mit Server...',10],
    ['Server startet auf (kann 30s dauern)...',30],
    ['Server wacht auf...',50],
    ['Fast da...',70],
    ['Noch einen Moment...',85],
    ['Fast fertig...',95]
  ];
  var m=msgs[Math.min(attempt,msgs.length-1)];
  showLoader(m[0],m[1]);
  fetch(API+'/health',{signal:AbortSignal.timeout?AbortSignal.timeout(8000):undefined})
    .then(function(){hideLoader();})
    .catch(function(){
      if(attempt<6){setTimeout(function(){pingServer(attempt+1);},5000);}
      else{hideLoader();}
    });
})(0);

function getBez(iq){
  if(iq>=145)return 'Genie';
  if(iq>=130)return 'Hochbegabt';
  if(iq>=120)return 'Sehr intelligent';
  if(iq>=116)return 'Ueberdurchschnittlich';
  if(iq>=100)return 'Durchschnittlich';
  if(iq>=94)return 'Leicht unterdurchschnittlich';
  return 'Unterdurchschnittlich';
}

var sessionId='',qs=[],cur=0,sc=0,done=false,ti=null,tl=0,st=0;
var cs={},cm={},times=[],errs=[];
var playerName='',finalIQ=85,gesperrte=[];
var jokerStatus={'5050':true,'telefon':true,'publikum':true};
var selectedKat='alle',selectedSchw='alle';
var isDailyMode=false,_dvTimer=null;
var isOfflineMode=false,offlineQs=[];
var extraJokerUsed=false;
var challengeTarget=0;

function toggleKat(btn,kat){
  document.querySelectorAll('.kat-btn').forEach(function(b){b.classList.remove('active');});
  btn.classList.add('active');
  selectedKat=kat;
}
function toggleSchw(btn,level){
  document.querySelectorAll('.schw-btn').forEach(function(b){b.classList.remove('active');});
  btn.classList.add('active');
  selectedSchw=level;
}

function showStart(){
  document.getElementById('sv').style.display='flex';
  document.getElementById('qv').classList.remove('active');
  document.getElementById('rv').style.display='none';
  document.getElementById('hv').style.display='none';
  document.getElementById('dv').style.display='none';
  document.getElementById('stv').style.display='none';
  clearInterval(_dvTimer);
}
function showQuiz(){
  document.getElementById('sv').style.display='none';
  document.getElementById('qv').classList.add('active');
  document.getElementById('rv').style.display='none';
  document.getElementById('hv').style.display='none';
  document.getElementById('dv').style.display='none';
  document.getElementById('stv').style.display='none';
}
function showResult(){
  document.getElementById('sv').style.display='none';
  document.getElementById('qv').classList.remove('active');
  document.getElementById('rv').style.display='block';
  document.getElementById('hv').style.display='none';
  document.getElementById('dv').style.display='none';
  document.getElementById('stv').style.display='none';
}

function buildLeiter(){
  var el=document.getElementById('leiter');el.innerHTML='';
  for(var l=MAX_FRAGEN;l>=1;l--){
    var d=document.createElement('div');
    d.className='li'+(SICHER.indexOf(l)>=0?' sicher':'');
    d.id='li-'+l;
    var s1=document.createElement('span');s1.textContent=l;
    var s2=document.createElement('span');s2.className='li-preis';s2.textContent=getPreis(l);
    var s3=document.createElement('span');s3.className='li-iq';s3.textContent='IQ '+(IQ_TBL[l]||85);
    d.appendChild(s1);d.appendChild(s2);d.appendChild(s3);
    el.appendChild(d);
  }
}
function updLeiter(lvl){
  document.querySelectorAll('.li').forEach(function(el){
    var l=parseInt(el.id.replace('li-',''));
    el.classList.remove('aktiv','done');
    if(l===lvl)el.classList.add('aktiv');
    else if(l<lvl)el.classList.add('done');
  });
}
function updIQ(iq){
  finalIQ=iq;
  var el=document.getElementById('iq-live');
  el.textContent=iq;
  el.style.animation='none';
  requestAnimationFrame(function(){el.style.animation='iqPop .4s ease';});
  document.getElementById('iq-live-txt').textContent=getBez(iq);
}
function updJoker(){
  document.getElementById('j-5050').disabled=!jokerStatus['5050'];
  document.getElementById('j-telefon').disabled=!jokerStatus['telefon'];
  document.getElementById('j-publikum').disabled=!jokerStatus['publikum'];
  var allUsed=!jokerStatus['5050']&&!jokerStatus['telefon']&&!jokerStatus['publikum'];
  var extraBtn=document.getElementById('extra-joker-btn');
  if(extraBtn)extraBtn.style.display=(allUsed&&!extraJokerUsed)?'flex':'none';
}

function showHS(){
  document.getElementById('sv').style.display='none';
  document.getElementById('hv').style.display='block';
  fetch(API+'/api/highscores').then(function(r){return r.json();}).then(function(scores){
    var hl=document.getElementById('hl');hl.innerHTML='';
    if(!scores.length){
      var d=document.createElement('div');d.className='none';d.textContent='Noch keine Eintraege.';hl.appendChild(d);return;
    }
    for(var i=0;i<scores.length;i++){
      var c=document.createElement('div');c.className='hs-card';
      var r=document.createElement('span');r.className='hs-rang';r.textContent=(i+1)+'.';
      var n=document.createElement('span');n.className='hs-name';n.textContent=scores[i].name;
      var lv=document.createElement('span');lv.className='hs-lv';lv.textContent='Frage '+scores[i].level;
      var iq=document.createElement('span');iq.className='hs-iq';iq.textContent='IQ '+scores[i].iq;
      c.appendChild(r);c.appendChild(n);c.appendChild(lv);c.appendChild(iq);
      hl.appendChild(c);
    }
  });
}

function startGame(){
  isDailyMode=false;isOfflineMode=false;extraJokerUsed=false;
  playerName=document.getElementById('ni').value||'Spieler';
  cur=0;sc=0;done=false;finalIQ=85;gesperrte=[];
  cs={};cm={};times=[];errs=[];qs=[];
  jokerStatus={'5050':true,'telefon':true,'publikum':true};
  updJoker();
  var startBtn=document.querySelector('.s-btn');
  if(startBtn){startBtn.disabled=true;startBtn.textContent='Verbinde...';}
  apiStartWithRetry(0);
}
function apiStartWithRetry(attempt){
  var startBtn=document.querySelector('.s-btn');
  var msgs=['Verbinde...','Server startet... (10s)','Noch einen Moment... (20s)','Fast fertig... (30s)'];
  if(startBtn)startBtn.textContent=msgs[Math.min(attempt,msgs.length-1)];
  fetch(API+'/api/start',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({name:playerName,kategorie:selectedKat,schwierigkeit:selectedSchw})
  }).then(function(r){
    if(!r.ok)throw new Error('HTTP '+r.status);
    return r.json();
  }).then(function(d){
    if(startBtn){startBtn.disabled=false;startBtn.textContent='Jetzt starten';}
    sessionId=d.session_id;
    buildLeiter();updIQ(85);showQuiz();
    setOfflineBadge(false);
    loadAndShowQ(1);
  }).catch(function(){
    if(attempt<3){
      setTimeout(function(){apiStartWithRetry(attempt+1);},8000);
    }else{
      if(startBtn){startBtn.disabled=false;startBtn.textContent='Jetzt starten';}
      if(offlineQs.length>=MAX_FRAGEN){startOfflineGame();}
      else{alert('Server nicht erreichbar. Bitte kurz warten und nochmal versuchen.');}
    }
  });
}

function loadAndShowQ(level){
  if(level>MAX_FRAGEN){calcResult();return;}
  cur=level;done=false;gesperrte=[];
  document.getElementById('iq-fb').style.display='none';
  document.getElementById('nb').style.display='none';
  document.getElementById('fb').textContent='';
  document.getElementById('fb').className='fb';
  document.getElementById('joker-overlay').classList.remove('show');
  if(isOfflineMode&&qs[level]){showQuestion(qs[level]);return;}
  fetch(API+'/api/frage/'+sessionId+'/'+level)
  .then(function(r){return r.json();})
  .then(function(q){qs[level]=q;showQuestion(q);})
  .catch(function(e){alert('Fehler: '+e.message);});
}
function showQuestion(q){
  var level=q.level;
  document.getElementById('qc').textContent=level+' / '+MAX_FRAGEN;
  document.getElementById('pb').textContent=q.kategorie.toUpperCase();
  document.getElementById('preis').textContent=q.preis||getPreis(level);
  var col=COL[q.kategorie]||'#4a90e2';
  document.getElementById('pdot').style.background=col;
  document.getElementById('pb').style.color=col;
  document.getElementById('ta').style.stroke=col;
  document.documentElement.style.setProperty('--cat-col',col);
  document.getElementById('qt').textContent=q.frage;
  document.getElementById('pf').style.width=((level-1)/MAX_FRAGEN*100)+'%';
  // Kategorie-Icon
  var iconEl=document.getElementById('kat-icon-q');
  if(iconEl)iconEl.textContent=KAT_ICONS[q.kategorie]||'';
  // Schwierigkeit Sterne
  var stars=document.getElementById('schw-stars');
  if(stars){var sw=q.schwierigkeit||1;stars.textContent=sw===3?'🔴🔴🔴':sw===2?'🟡🟡':'🟢';}
  var sb=document.getElementById('sb');
  if(q.seq){sb.textContent=q.seq;sb.style.display='block';}else sb.style.display='none';
  var fbox=document.querySelector('.fbox');
  fbox.style.animation='none';
  requestAnimationFrame(function(){fbox.style.animation='fadeUp .35s ease';});
  var op=document.getElementById('op');op.innerHTML='';
  var opts=['A','B','C','D'];
  for(var i=0;i<opts.length;i++){
    var b=document.createElement('button');
    b.className='opt appear';
    b.style.animationDelay=(i*.08)+'s';
    var badge=document.createElement('span');badge.className='badge';badge.textContent=opts[i];
    var txt=document.createElement('span');txt.textContent=q.antworten[opts[i]];
    b.appendChild(badge);b.appendChild(txt);
    b.setAttribute('data-key',opts[i]);
    b.onclick=function(){pick(this.getAttribute('data-key'));};
    op.appendChild(b);
  }
  updLeiter(level);
  var sec=level<=5?20:level<=10?25:30;
  st=Date.now();tick(sec,sec);
  ti=setInterval(function(){tl--;tick(tl,sec);if(tl<=0){clearInterval(ti);tout();}},1000);
}

function tick(l,t){
  tl=l;
  document.getElementById('tn').textContent=l;
  document.getElementById('ta').style.strokeDashoffset=289.03*(1-l/t);
  var u=l<=5,w=l<=10;
  var col=u?'#ef4444':w?'#f59e0b':'#4a90e2';
  document.getElementById('ta').style.stroke=col;
  document.getElementById('tn').style.color=u?'#ef4444':w?'#f59e0b':'#f1f5f9';
  var trw=document.getElementById('trw');
  if(u)trw.classList.add('urgent');else trw.classList.remove('urgent');
  if(l<=5&&l>0)playSound('tick');
}

function tout(){
  if(done)return;done=true;
  var q=qs[cur];if(!q)return;
  var k=q.kategorie;cm[k]=(cm[k]||0)+1;times.push(30);
  errs.push({q:q,ch:null,to:true,ri:q.richtig||'A',erklaerung:q.erklaerung||''});
  document.querySelectorAll('.opt').forEach(function(b){
    if(b.getAttribute('data-key')===q.richtig)b.classList.add('ok');
    b.disabled=true;
  });
  document.getElementById('fb').textContent=T('zeit');
  document.getElementById('fb').className='fb to';
  playSound('falsch');
  showIQFb(false,cur);
  setTimeout(function(){calcResult();},2500);
}

function pick(key){
  if(done)return;done=true;clearInterval(ti);
  var elapsed=Math.min((Date.now()-st)/1000,30);
  times.push(elapsed);
  var q=qs[cur];
  var k=q?q.kategorie:'';cm[k]=(cm[k]||0)+1;
  if(isOfflineMode){
    var richtig=(key===q.richtig);
    var iq=IQ_TBL[richtig?cur:Math.max(0,cur-1)]||85;
    handleAnswer(key,{richtig:richtig,richtige_antwort:q.richtig,richtige_antwort_text:q.antworten[q.richtig],erklaerung:q.erklaerung||'',iq:iq,sicher_level:0},k);
    return;
  }
  fetch(API+'/api/antwort',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({session_id:sessionId,level:cur,antwort:key})
  }).then(function(r){return r.json();}).then(function(d){handleAnswer(key,d,k);});
}
function handleAnswer(key,d,k){
  var q=qs[cur];
  var bs=document.querySelectorAll('.opt');
  var fb=document.getElementById('fb');
  bs.forEach(function(b){
    if(b.getAttribute('data-key')===key)b.classList.add(d.richtig?'ok':'no');
    if(!d.richtig&&b.getAttribute('data-key')===d.richtige_antwort)b.classList.add('ok');
    b.disabled=true;
  });
  if(d.richtig){
    sc++;cs[k]=(cs[k]||0)+1;
    fb.textContent=T('richtig');fb.className='fb ok';
    var isSich=SICHER.indexOf(cur)>=0;
    playSound(isSich?'sicher':'richtig');
    launchConfetti(isSich?'medium':'small');
    showIQFb(true,cur);
    if(cur>=MAX_FRAGEN){setTimeout(function(){calcResult();},2000);}
    else{document.getElementById('nb').style.display='block';}
  }else{
    errs.push({q:q,ch:key,to:false,ri:d.richtige_antwort,erklaerung:d.erklaerung||''});
    fb.textContent=T('falsch')+' '+d.richtige_antwort+' - '+d.richtige_antwort_text;
    fb.className='fb no';
    playSound('falsch');
    showIQFb(false,cur);
    setTimeout(function(){calcResult();},2500);
  }
  updIQ(d.iq||finalIQ);
}

function showIQFb(richtig,level){
  var iq=richtig?IQ_TBL[level]||85:IQ_TBL[Math.max(0,level-1)]||85;
  updIQ(iq);
  document.getElementById('iq-fb-num').textContent='IQ '+iq;
  document.getElementById('iq-fb-bez').textContent=getBez(iq);
  document.getElementById('iq-fb').style.display='block';
}

document.getElementById('nb').onclick=function(){loadAndShowQ(cur+1);};

function useJoker(typ){
  if(!jokerStatus[typ])return;
  fetch(API+'/api/joker',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({session_id:sessionId,level:cur,typ:typ,gesperrte:gesperrte})
  }).then(function(r){return r.json();}).then(function(d){
    jokerStatus[typ]=false;updJoker();playSound('joker');
    if(d.typ==='5050'){
      d.entfernte.forEach(function(key){
        gesperrte.push(key);
        document.querySelectorAll('.opt').forEach(function(b){
          if(b.getAttribute('data-key')===key)b.classList.add('gesperrt');
        });
      });
    }else if(d.typ==='telefon'){
      document.getElementById('jo-title').textContent=T('telefon');
      var content=document.getElementById('jo-content');content.innerHTML='';
      var p1=document.createElement('div');p1.className='jo-text';p1.textContent='"'+d.text+'"';
      var p2=document.createElement('div');p2.className='jo-tipp';p2.textContent='Antwort: '+d.tipp;
      content.appendChild(p1);content.appendChild(p2);
      document.getElementById('joker-overlay').classList.add('show');
    }else if(d.typ==='publikum'){
      document.getElementById('jo-title').textContent=T('publikum');
      var content=document.getElementById('jo-content');content.innerHTML='';
      ['A','B','C','D'].forEach(function(key){
        if(gesperrte.indexOf(key)>=0)return;
        var pct=d.stimmen[key]||0;
        var row=document.createElement('div');row.className='pub-bar-row';
        var lbl=document.createElement('span');lbl.className='pub-bar-lbl';lbl.textContent=key;
        var outer=document.createElement('div');outer.className='pub-bar-outer';
        var inner=document.createElement('div');inner.className='pub-bar-inner';inner.style.width='0%';inner.id='pbar-'+key;
        var pctEl=document.createElement('span');pctEl.className='pub-bar-pct';pctEl.textContent=pct+'%';
        outer.appendChild(inner);
        row.appendChild(lbl);row.appendChild(outer);row.appendChild(pctEl);
        content.appendChild(row);
        setTimeout(function(){var el=document.getElementById('pbar-'+key);if(el)el.style.width=pct+'%';},100);
      });
      document.getElementById('joker-overlay').classList.add('show');
    }
  });
}

function closeJoker(){document.getElementById('joker-overlay').classList.remove('show');}

function calcResult(){
  saveStats();
  showResult();
  document.getElementById('pf').style.width='100%';
  var sum=0;for(var i=0;i<times.length;i++)sum+=times[i];
  var avg=times.length?Math.round(sum/times.length*10)/10:0;
  var iq=finalIQ;
  playSound('gewonnen');
  launchConfetti(iq>=130?'big':iq>=115?'medium':'small');
  var emoji=iq>=145?'🧠':iq>=130?'✨':iq>=115?'⭐':iq>=100?'👍':'💪';
  document.getElementById('rv-emoji').textContent=emoji;
  animateCount(document.getElementById('rv-iq'),85,iq,1500);
  document.getElementById('rv-sub').textContent=iq>=130?'Hervorragend!':iq>=115?'Sehr gut!':iq>=100?'Gut!':'Weiter ueben!';
  var rb=document.getElementById('rank-badge');
  if(rb){var rank=getRankBadge(iq);rb.textContent=rank.text;rb.style.background=rank.bg;rb.style.color=rank.col;rb.style.borderColor=rank.border;rb.style.boxShadow='0 0 16px '+rank.border+'44';}
  var totalCm=0;Object.keys(cm).forEach(function(k){totalCm+=cm[k];});
  var totalCs=0;Object.keys(cs).forEach(function(k){totalCs+=cs[k];});
  document.getElementById('baw').textContent=totalCs+' / '+totalCm;
  document.getElementById('blog').textContent=selectedKat==='alle'?'Alle':selectedKat;
  document.getElementById('bkz').textContent=selectedSchw==='alle'?'Alle':selectedSchw==='1'?'Leicht':selectedSchw==='2'?'Mittel':'Schwer';
  document.getElementById('bt').textContent=avg+' Sek.';
  document.getElementById('sn').value=playerName;
  if(isDailyMode){
    var _today=new Date().toISOString().split('T')[0];
    localStorage.setItem('daily_'+_today,JSON.stringify({iq:finalIQ,level:sc}));
    fetch(API+'/api/daily/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:playerName,iq:finalIQ,level:sc})});
    document.getElementById('rv-chip').textContent='📅 Challenge · '+sc+' / '+MAX_FRAGEN+' richtig';
    isDailyMode=false;
  } else {
    document.getElementById('rv-chip').textContent=sc+' / '+MAX_FRAGEN;
  }
  // Challenge-Ergebnis anzeigen
  if(challengeTarget>0){
    var banner=document.getElementById('challenge-banner');
    var res=document.getElementById('challenge-result');
    if(banner)banner.style.display='block';
    if(res){
      if(finalIQ>=challengeTarget){
        res.innerHTML='<div class="challenge-won">🏆 Herausforderung geschlagen! (IQ '+finalIQ+' vs. '+challengeTarget+')</div>';
        launchConfetti('big');
      }else{
        res.innerHTML='<div class="challenge-lost">😤 Knapp daneben! IQ '+finalIQ+' vs. Ziel '+challengeTarget+'</div>';
      }
    }
  }
  document.getElementById('ml').innerHTML='';
  document.getElementById('err-lbl').textContent=errs.length?T('fehler')+': '+errs.length:T('fehler');
  if(!errs.length){
    var d=document.createElement('div');d.className='none';d.textContent=T('perfekt');
    document.getElementById('ml').appendChild(d);
  }else{
    for(var i=0;i<errs.length;i++){
      var e=errs[i];
      var card=document.createElement('div');card.className='err-card';
      var cat=document.createElement('div');cat.className='err-cat';cat.textContent=e.q.kategorie;card.appendChild(cat);
      if(e.to){var tob=document.createElement('span');tob.className='tob';tob.textContent=T('zeit');card.appendChild(tob);}
      var qd=document.createElement('div');qd.className='err-q';qd.textContent=e.q.frage;card.appendChild(qd);
      if(e.q.seq){var sd=document.createElement('div');sd.className='err-seq';sd.textContent=e.q.seq;card.appendChild(sd);}
      var row=document.createElement('div');row.className='err-row';
      if(!e.to&&e.ch){
        var col1=document.createElement('div');col1.className='err-col';
        var lbl1=document.createElement('span');lbl1.className='err-clbl';lbl1.textContent=T('deine');
        var p1=document.createElement('span');p1.className='pill pno';p1.textContent=e.ch+' - '+(e.q.antworten?e.q.antworten[e.ch]:'');
        col1.appendChild(lbl1);col1.appendChild(p1);row.appendChild(col1);
      }
      var col2=document.createElement('div');col2.className='err-col';
      var lbl2=document.createElement('span');lbl2.className='err-clbl';lbl2.textContent=T('richtige');
      var p2=document.createElement('span');p2.className='pill pok';p2.textContent=e.ri+' - '+(e.q.antworten?e.q.antworten[e.ri]:'');
      col2.appendChild(lbl2);col2.appendChild(p2);row.appendChild(col2);
      card.appendChild(row);
      if(e.erklaerung){
        var exp=document.createElement('div');exp.className='err-erkl';
        exp.textContent='💡 '+e.erklaerung;card.appendChild(exp);
      }
      document.getElementById('ml').appendChild(card);
    }
  }
  checkRatingPrompt();
}

function saveHS(){
  var name=document.getElementById('sn').value||playerName;
  fetch(API+'/api/highscores',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({name:name,iq:finalIQ,level:sc})
  }).then(function(){
    var btn=document.querySelector('.save-btn');
    btn.textContent=T('gespeichert');
    setTimeout(function(){btn.textContent=T('speichern');},2000);
  });
}

function shareResult(){
  var text=playerName+' hat beim IQ Test IQ '+finalIQ+' erreicht ('+sc+'/'+MAX_FRAGEN+' richtig)! Teste auch du deinen IQ!';
  var url='https://iq-quiz-v2.onrender.com';
  if(navigator.share){
    navigator.share({title:'IQ Test Ergebnis',text:text,url:url}).catch(function(){});
  }else{
    navigator.clipboard&&navigator.clipboard.writeText(text+' '+url).then(function(){
      var btn=document.querySelector('.share-btn');
      if(btn){btn.textContent='✅ Kopiert!';setTimeout(function(){btn.textContent='📤 '+T('teilen');},2000);}
    }).catch(function(){alert(text);});
  }
}

// ── STATISTIKEN ────────────────────────────────────────────
function saveStats(){
  var s=JSON.parse(localStorage.getItem('iq_stats')||'{}');
  s.games=(s.games||0)+1;
  s.bestIQ=Math.max(s.bestIQ||0,finalIQ);
  s.totalIQ=(s.totalIQ||0)+finalIQ;
  s.totalCorrect=(s.totalCorrect||0)+sc;
  s.totalQuestions=(s.totalQuestions||0)+MAX_FRAGEN;
  s.catCorrect=s.catCorrect||{};
  s.catTotal=s.catTotal||{};
  Object.keys(cm).forEach(function(k){
    if(!k)return;
    s.catCorrect[k]=(s.catCorrect[k]||0)+(cs[k]||0);
    s.catTotal[k]=(s.catTotal[k]||0)+(cm[k]||0);
  });
  s.history=s.history||[];
  var today=new Date().toISOString().split('T')[0];
  s.history.unshift({iq:finalIQ,level:sc,date:today,daily:isDailyMode});
  if(s.history.length>10)s.history.pop();
  if(isDailyMode){
    var yest=new Date(Date.now()-86400000).toISOString().split('T')[0];
    if(s.lastDaily===yest)s.dailyStreak=(s.dailyStreak||0)+1;
    else if(s.lastDaily!==today)s.dailyStreak=1;
    s.lastDaily=today;
  }
  localStorage.setItem('iq_stats',JSON.stringify(s));
}

function showStats(){
  document.getElementById('sv').style.display='none';
  document.getElementById('stv').style.display='block';
  document.getElementById('qv').classList.remove('active');
  document.getElementById('rv').style.display='none';
  document.getElementById('hv').style.display='none';
  document.getElementById('dv').style.display='none';
  var s=JSON.parse(localStorage.getItem('iq_stats')||'{}');
  var g=s.games||0;
  document.getElementById('st-games').textContent=g||'–';
  document.getElementById('st-best').textContent=s.bestIQ?'IQ '+s.bestIQ:'–';
  document.getElementById('st-avg').textContent=g?'IQ '+Math.round(s.totalIQ/g):'–';
  var acc=s.totalQuestions?Math.round(s.totalCorrect/s.totalQuestions*100):0;
  document.getElementById('st-acc').textContent=g?acc+'%':'–';
  document.getElementById('st-streak').textContent=(s.dailyStreak||0)+' 🔥';
  var chart=document.getElementById('st-chart');chart.innerHTML='';
  var hist=s.history||[];
  if(!hist.length){
    chart.innerHTML='<div style="color:var(--text3);font-size:13px;text-align:center;width:100%;padding-top:40px;">Noch keine Spiele</div>';
  }else{
    hist.slice().reverse().forEach(function(h){
      var pct=Math.max(5,Math.round((h.iq-85)/(145-85)*100));
      var col=h.iq>=130?'var(--gold)':h.iq>=115?'var(--accent)':h.iq>=100?'var(--purple)':'var(--text3)';
      var isDaily=h.daily;
      var wrap=document.createElement('div');
      wrap.style.cssText='flex:1;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;height:100%;cursor:default;';
      wrap.title='IQ '+h.iq+' · '+h.date+(isDaily?' 📅':'');
      var bar=document.createElement('div');
      bar.style.cssText='width:100%;border-radius:4px 4px 0 0;background:'+col+';height:'+pct+'%;min-height:4px;position:relative;'+(isDaily?'border-top:2px solid var(--gold);':'');
      var iqLbl=document.createElement('div');
      iqLbl.style.cssText='font-size:8px;font-weight:700;color:var(--text3);margin-top:2px;text-align:center;';
      iqLbl.textContent=h.iq;
      var dateLbl=document.createElement('div');
      dateLbl.style.cssText='font-size:7px;color:var(--text3);opacity:.7;text-align:center;white-space:nowrap;overflow:hidden;';
      var d=h.date?h.date.slice(5).replace('-','/'):'-';
      dateLbl.textContent=d+(isDaily?' 📅':'');
      wrap.appendChild(bar);wrap.appendChild(iqLbl);wrap.appendChild(dateLbl);chart.appendChild(wrap);
    });
  }
  var cats=document.getElementById('st-cats');cats.innerHTML='';
  var catKeys=Object.keys((s.catTotal)||{}).filter(function(k){return s.catTotal[k]>0;});
  if(!catKeys.length){cats.innerHTML='<div style="color:var(--text3);font-size:13px;text-align:center;padding:1rem;">Noch keine Daten</div>';}
  catKeys.forEach(function(k){
    var pct=s.catTotal[k]?Math.round((s.catCorrect[k]||0)/s.catTotal[k]*100):0;
    var col=COL[k]||'#4a90e2';
    var icon=KAT_ICONS[k]||'';
    var row=document.createElement('div');row.style.cssText='display:flex;align-items:center;gap:10px;margin-bottom:.6rem;';
    var nm=document.createElement('span');nm.style.cssText='font-size:12px;color:var(--text2);width:140px;flex-shrink:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;';nm.textContent=icon+' '+k;
    var out=document.createElement('div');out.style.cssText='flex:1;height:8px;background:var(--border);border-radius:99px;overflow:hidden;';
    var inn=document.createElement('div');inn.style.cssText='height:100%;border-radius:99px;background:'+col+';width:0%;transition:width .8s ease;';
    out.appendChild(inn);
    var pe=document.createElement('span');pe.style.cssText='font-size:12px;font-weight:700;color:var(--text2);width:35px;text-align:right;';
    pe.textContent=pct+'%';
    row.appendChild(nm);row.appendChild(out);row.appendChild(pe);cats.appendChild(row);
    setTimeout(function(){inn.style.width=pct+'%';},100);
  });
}

// ── ZERTIFIKAT ─────────────────────────────────────────────
function downloadCert(){
  document.getElementById('cert-name').textContent=playerName;
  document.getElementById('cert-iq').textContent='IQ '+finalIQ;
  document.getElementById('cert-class').textContent=getBez(finalIQ);
  document.getElementById('cert-detail').textContent=sc+' von 15 Fragen richtig · '+new Date().toLocaleDateString('de-DE',{day:'numeric',month:'long',year:'numeric'});
  document.getElementById('cert-footer').textContent='IQ-Quiz · iq-quiz-v2.onrender.com · '+new Date().toLocaleDateString('de-DE');
  window.print();
}

// ── BILD TEILEN ────────────────────────────────────────────
function shareImage(){
  var cv=document.createElement('canvas');
  cv.width=800;cv.height=450;
  var ctx=cv.getContext('2d');
  // Hintergrund
  var grd=ctx.createLinearGradient(0,0,800,450);
  grd.addColorStop(0,'#060614');grd.addColorStop(1,'#0f1628');
  ctx.fillStyle=grd;ctx.fillRect(0,0,800,450);
  // Dekorationsstreifen
  var acc=ctx.createLinearGradient(0,0,800,0);
  acc.addColorStop(0,'#4a90e2');acc.addColorStop(1,'#7c5fff');
  ctx.fillStyle=acc;ctx.fillRect(0,0,800,5);
  // Brain emoji
  ctx.font='72px Arial';ctx.textAlign='center';
  ctx.fillText('🧠',400,100);
  // IQ Test
  ctx.font='bold 22px Arial';ctx.fillStyle='#94a3b8';ctx.letterSpacing='4px';
  ctx.fillText('IQ TEST',400,140);
  // Name
  ctx.font='bold 28px Arial';ctx.fillStyle='#f1f5f9';
  ctx.fillText(playerName,400,195);
  // IQ Score
  ctx.font='bold 110px Arial';
  var grd2=ctx.createLinearGradient(250,200,550,200);
  grd2.addColorStop(0,'#4a90e2');grd2.addColorStop(1,'#7c5fff');
  ctx.fillStyle=grd2;
  ctx.fillText('IQ '+finalIQ,400,320);
  // Bezeichnung
  ctx.font='bold 20px Arial';ctx.fillStyle='#94a3b8';
  ctx.fillText(getBez(finalIQ),400,360);
  // Score
  ctx.font='16px Arial';ctx.fillStyle='#475569';
  ctx.fillText(sc+'/15 Fragen richtig · '+new Date().toLocaleDateString('de-DE'),400,400);
  // URL
  ctx.font='13px Arial';ctx.fillStyle='#1a2540';
  ctx.fillText('iq-quiz-v2.onrender.com',400,435);
  cv.toBlob(function(blob){
    if(!blob)return;
    var file=new File([blob],'iq-ergebnis.png',{type:'image/png'});
    if(navigator.share&&navigator.canShare&&navigator.canShare({files:[file]})){
      navigator.share({files:[file],title:'Mein IQ Ergebnis'}).catch(function(){downloadBlob(blob);});
    }else{downloadBlob(blob);}
  },'image/png');
}
function downloadBlob(blob){
  var url=URL.createObjectURL(blob);
  var a=document.createElement('a');a.href=url;a.download='iq-ergebnis.png';a.click();
  setTimeout(function(){URL.revokeObjectURL(url);},2000);
}

// ── FREUND HERAUSFORDERN ───────────────────────────────────
function shareChallenge(){
  var url=window.location.origin+window.location.pathname+'?challenge='+finalIQ;
  var text='Kannst du meinen IQ von '+finalIQ+' beim IQ Test schlagen? Probier es!';
  if(navigator.share){
    navigator.share({title:'IQ Challenge',text:text,url:url}).catch(function(){});
  }else{
    navigator.clipboard&&navigator.clipboard.writeText(text+' '+url).then(function(){
      var btn=document.querySelector('.chal-btn');
      if(btn){btn.textContent='✅ Link kopiert!';setTimeout(function(){btn.textContent='🎯 Freund herausfordern';},2500);}
    }).catch(function(){alert(text+'\n\n'+url);});
  }
}
function checkChallenge(){
  try{
    var params=new URLSearchParams(window.location.search);
    var ciq=parseInt(params.get('challenge'));
    if(ciq>0){
      challengeTarget=ciq;
      var banner=document.getElementById('challenge-banner');
      var target=document.getElementById('challenge-target');
      if(banner){banner.style.display='block';}
      if(target){target.textContent='IQ '+ciq;}
    }
  }catch(e){}
}

// ── PUSH-BENACHRICHTIGUNGEN ────────────────────────────────
function toggleNotifications(){
  if(!('Notification' in window)){alert('Benachrichtigungen werden nicht unterstuetzt.');return;}
  var btn=document.getElementById('notif-btn');
  if(localStorage.getItem('notifications_enabled')==='1'){
    localStorage.removeItem('notifications_enabled');
    if(btn){btn.textContent='🔔 Taegl. Erinnerung';btn.classList.remove('active');}
    return;
  }
  Notification.requestPermission().then(function(perm){
    if(perm==='granted'){
      localStorage.setItem('notifications_enabled','1');
      if(btn){btn.textContent='✅ Erinnerung aktiv';btn.classList.add('active');}
      new Notification('IQ Test',{body:'Du bekommst jetzt taeglich eine Erinnerung fuer die Challenge!',icon:'favicon.ico'});
    }else{
      if(btn){btn.textContent='❌ Nicht erlaubt';setTimeout(function(){btn.textContent='🔔 Taegl. Erinnerung';},2000);}
    }
  });
}
function initNotifBtn(){
  var btn=document.getElementById('notif-btn');
  if(!btn)return;
  if(localStorage.getItem('notifications_enabled')==='1'){
    btn.textContent='✅ Erinnerung aktiv';btn.classList.add('active');
  }
}
function checkDailyNotification(){
  if(localStorage.getItem('notifications_enabled')!=='1')return;
  if(Notification.permission!=='granted')return;
  var today=new Date().toISOString().split('T')[0];
  if(!localStorage.getItem('daily_'+today)){
    setTimeout(function(){
      new Notification('🧠 IQ Test',{
        body:'Deine taegl. Challenge wartet! Wie hoch ist dein IQ heute?',
        icon:'favicon.ico'
      });
    },3000);
  }
}

// ── APP BEWERTUNG ──────────────────────────────────────────
function checkRatingPrompt(){
  var s=JSON.parse(localStorage.getItem('iq_stats')||'{}');
  if(s.games===3&&!localStorage.getItem('rating_shown')){
    localStorage.setItem('rating_shown','1');
    setTimeout(function(){
      var m=document.getElementById('rating-modal');
      if(m)m.style.display='flex';
    },1800);
  }
}
function rateApp(){
  document.getElementById('rating-modal').style.display='none';
  window.open('https://play.google.com/store','_blank');
}

// ── EXTRA JOKER ────────────────────────────────────────────
function buyExtraJoker(){
  var btn=document.getElementById('extra-joker-btn');
  if(!btn||extraJokerUsed)return;
  btn.disabled=true;
  var n=3;
  btn.textContent='⏳ '+n+'s Werbung...';
  var iv=setInterval(function(){
    n--;
    btn.textContent='⏳ '+n+'s Werbung...';
    if(n<=0){
      clearInterval(iv);
      grantExtraJoker();
    }
  },1000);
}
function grantExtraJoker(){
  if(!jokerStatus['telefon']){jokerStatus['telefon']=true;}
  else if(!jokerStatus['5050']){jokerStatus['5050']=true;}
  else if(!jokerStatus['publikum']){jokerStatus['publikum']=true;}
  extraJokerUsed=true;
  updJoker();
  playSound('sicher');
  launchConfetti('small');
}

// ── TAEGLICHE CHALLENGE ────────────────────────────────────
function showDailyInfo(){
  document.getElementById('sv').style.display='none';
  document.getElementById('dv').style.display='flex';
  document.getElementById('hv').style.display='none';
  document.getElementById('rv').style.display='none';
  document.getElementById('qv').classList.remove('active');
  var today=new Date();
  var todayStr=today.toISOString().split('T')[0];
  var opts={weekday:'long',day:'numeric',month:'long'};
  document.getElementById('dv-date').textContent=today.toLocaleDateString('de-DE',opts);
  clearInterval(_dvTimer);
  function updCountdown(){
    var now=new Date(),mid=new Date(now);
    mid.setHours(24,0,0,0);
    var d=mid-now;
    var h=Math.floor(d/3600000),m=Math.floor((d%3600000)/60000),s=Math.floor((d%60000)/1000);
    document.getElementById('dv-countdown').textContent='Neue Challenge in '+String(h).padStart(2,'0')+':'+String(m).padStart(2,'0')+':'+String(s).padStart(2,'0');
  }
  updCountdown();
  _dvTimer=setInterval(updCountdown,1000);
  var playedData=localStorage.getItem('daily_'+todayStr);
  if(playedData){
    var pd=JSON.parse(playedData);
    document.getElementById('dv-already').style.display='block';
    document.getElementById('dv-play').style.display='none';
    document.getElementById('dv-score-info').textContent='Dein Ergebnis heute: IQ '+pd.iq+' · '+pd.level+'/15 richtig';
  }else{
    document.getElementById('dv-already').style.display='none';
    document.getElementById('dv-play').style.display='flex';
    var ni=document.getElementById('ni');
    if(ni&&ni.value)document.getElementById('dni').value=ni.value;
  }
  loadDailyHS();
}

function loadDailyHS(){
  fetch(API+'/api/daily/highscores').then(function(r){return r.json();}).then(function(scores){
    var hl=document.getElementById('dv-hs');hl.innerHTML='';
    if(!scores.length){
      var d=document.createElement('div');d.className='none';d.textContent='Noch keine Eintraege heute.';hl.appendChild(d);return;
    }
    for(var i=0;i<scores.length;i++){
      var c=document.createElement('div');c.className='hs-card';
      var r=document.createElement('span');r.className='hs-rang';r.textContent=(i+1)+'.';
      var n=document.createElement('span');n.className='hs-name';n.textContent=scores[i].name;
      var lv=document.createElement('span');lv.className='hs-lv';lv.textContent=scores[i].level+'/15';
      var iq=document.createElement('span');iq.className='hs-iq';iq.textContent='IQ '+scores[i].iq;
      c.appendChild(r);c.appendChild(n);c.appendChild(lv);c.appendChild(iq);
      hl.appendChild(c);
    }
  });
}

function startDailyGame(){
  playerName=document.getElementById('dni').value||'Spieler';
  cur=0;sc=0;done=false;finalIQ=85;gesperrte=[];isOfflineMode=false;extraJokerUsed=false;
  cs={};cm={};times=[];errs=[];qs=[];
  jokerStatus={'5050':true,'telefon':true,'publikum':true};
  updJoker();
  isDailyMode=true;
  clearInterval(_dvTimer);
  var btn=document.querySelector('#dv .s-btn');
  if(btn){btn.disabled=true;btn.textContent='Verbinde...';}
  apiDailyStartWithRetry(0);
}
function apiDailyStartWithRetry(attempt){
  var btn=document.querySelector('#dv .s-btn');
  var msgs=['Verbinde...','Server startet...','Noch einen Moment...','Fast fertig...'];
  if(btn)btn.textContent=msgs[Math.min(attempt,msgs.length-1)];
  fetch(API+'/api/daily/start',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({name:playerName})
  }).then(function(r){
    if(!r.ok)throw new Error('HTTP '+r.status);
    return r.json();
  }).then(function(d){
    if(btn){btn.disabled=false;btn.textContent='Challenge starten';}
    sessionId=d.session_id;
    buildLeiter();updIQ(85);showQuiz();setOfflineBadge(false);
    loadAndShowQ(1);
  }).catch(function(){
    if(attempt<3){setTimeout(function(){apiDailyStartWithRetry(attempt+1);},8000);}
    else{
      if(btn){btn.disabled=false;btn.textContent='Challenge starten';}
      alert('Server nicht erreichbar. Bitte kurz warten und nochmal versuchen.');
    }
  });
}

// ── OFFLINE MODUS ──────────────────────────────────────────
function setOfflineBadge(show){
  var b=document.getElementById('offline-badge');
  if(b)b.style.display=show?'block':'none';
}
function loadOfflineCache(){
  var cached=localStorage.getItem('iq_offline_cache');
  if(cached){try{offlineQs=JSON.parse(cached);}catch(e){}}
  fetch(API+'/api/offline')
    .then(function(r){return r.json();})
    .then(function(fragen){
      localStorage.setItem('iq_offline_cache',JSON.stringify(fragen));
      offlineQs=fragen;
    }).catch(function(){});
}
function startOfflineGame(){
  isOfflineMode=true;
  var shuffled=offlineQs.slice().sort(function(){return Math.random()-.5;});
  qs=[];
  for(var i=0;i<MAX_FRAGEN&&i<shuffled.length;i++){
    var q=Object.assign({},shuffled[i]);q.level=i+1;
    qs[i+1]=q;
  }
  sessionId='offline';
  buildLeiter();updIQ(85);showQuiz();setOfflineBadge(true);
  loadAndShowQ(1);
}

// ── ONBOARDING ─────────────────────────────────────────────
function checkOnboarding(){
  if(!localStorage.getItem('iq_onboarding_done')){
    var ob=document.getElementById('onb');
    if(ob)ob.style.display='flex';
  }
}
function closeOnboarding(){
  localStorage.setItem('iq_onboarding_done','1');
  var ob=document.getElementById('onb');
  if(ob)ob.style.display='none';
}

// ── STERNENHINTERGRUND ─────────────────────────────────────
function initStarfield(){
  var cv=document.getElementById('starfield');
  if(!cv)return;
  var ctx=cv.getContext('2d');
  function resize(){cv.width=window.innerWidth;cv.height=window.innerHeight;}
  resize();
  window.addEventListener('resize',resize);
  var stars=[];
  for(var i=0;i<160;i++){
    stars.push({
      x:Math.random(),y:Math.random(),
      r:Math.random()*1.4+0.2,
      o:Math.random()*0.6+0.1,
      s:Math.random()*0.3+0.05,
      t:Math.random()*Math.PI*2
    });
  }
  function draw(){
    ctx.clearRect(0,0,cv.width,cv.height);
    var now=Date.now()/1000;
    stars.forEach(function(s){
      var pulse=s.o*(0.6+0.4*Math.sin(now*s.s+s.t));
      ctx.beginPath();
      ctx.arc(s.x*cv.width,s.y*cv.height,s.r,0,Math.PI*2);
      ctx.fillStyle='rgba(255,255,255,'+pulse+')';
      ctx.fill();
    });
    requestAnimationFrame(draw);
  }
  draw();
}

// ── RANG BADGE ─────────────────────────────────────────────
function getRankBadge(iq){
  if(iq>=145)return{text:'GENIE',bg:'linear-gradient(135deg,#ffd700,#ff6b35)',col:'#fff',border:'#ffd700'};
  if(iq>=130)return{text:'HOCHBEGABT',bg:'linear-gradient(135deg,#7c5fff,#4a90e2)',col:'#fff',border:'#7c5fff'};
  if(iq>=120)return{text:'SEHR INTELLIGENT',bg:'linear-gradient(135deg,#4a90e2,#06b6d4)',col:'#fff',border:'#4a90e2'};
  if(iq>=115)return{text:'ÜBERDURCHSCHNITTLICH',bg:'linear-gradient(135deg,#22c55e,#4a90e2)',col:'#fff',border:'#22c55e'};
  if(iq>=100)return{text:'DURCHSCHNITTLICH',bg:'transparent',col:'#94a3b8',border:'#475569'};
  return{text:'WEITER ÜBEN',bg:'transparent',col:'#475569',border:'#1a2540'};
}

// ── ONBOARDING SLIDES ──────────────────────────────────────
var _onbSlide=0;
function onbNext(){
  var total=4;
  _onbSlide++;
  if(_onbSlide>=total){closeOnboarding();return;}
  for(var i=0;i<total;i++){
    var s=document.getElementById('onb-'+i);
    var d=document.getElementById('odot-'+i);
    if(s)s.classList.toggle('active',i===_onbSlide);
    if(d)d.classList.toggle('active',i===_onbSlide);
  }
  var btn=document.getElementById('onb-next-btn');
  if(btn)btn.textContent=_onbSlide===total-1?'Los geht\'s!':'Weiter';
}

// ── INIT ───────────────────────────────────────────────────
initStarfield();
loadOfflineCache();
checkOnboarding();
checkChallenge();
initNotifBtn();
checkDailyNotification();
