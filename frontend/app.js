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
var currentMode='normal'; // normal | timeattack | learn | endless
var taTimer=null,taLeft=60,taTotalTime=60;

function setMode(mode,btn){
  currentMode=mode;
  document.querySelectorAll('.mode-btn').forEach(function(b){b.classList.remove('active');});
  if(btn)btn.classList.add('active');
}

const LANG={
  de:{title:'IQ Test',sub:'Teste deinen IQ · 15 Fragen · 3 Joker',placeholder:'Dein Name...',start:'Jetzt starten',highscores:'Highscores',sekunden:'Sekunden',iqLabel:'Aktueller IQ',joker:'Joker',richtig:'Richtig!',falsch:'Falsch! Ausgeschieden!',zeit:'Zeit abgelaufen! Ausgeschieden!',naechste:'Naechste Frage',ergebnis:'Dein Ergebnis',speichern:'Speichern',gespeichert:'Gespeichert!',nochmal:'Nochmal starten',zurueck:'Zurueck',perfekt:'Perfekt - alle Fragen richtig!',fehler:'FEHLERAUSWERTUNG',deine:'Deine Antwort',richtige:'Richtige Antwort',leiter:'IQ Leiter',schliessen:'Schliessen',telefon:'Telefon-Joker',publikum:'Publikums-Joker',iqNach:'Dein IQ nach dieser Frage',teilen:'Ergebnis teilen'},
  en:{title:'IQ Test',sub:'Test Your IQ · 15 Questions · 3 Lifelines',placeholder:'Your Name...',start:'Start Now',highscores:'Highscores',sekunden:'Seconds',iqLabel:'Current IQ',joker:'Lifelines',richtig:'Correct!',falsch:'Wrong! Game Over!',zeit:'Time Up! Game Over!',naechste:'Next Question',ergebnis:'Your Result',speichern:'Save',gespeichert:'Saved!',nochmal:'Play Again',zurueck:'Back',perfekt:'Perfect - all correct!',fehler:'ERROR ANALYSIS',deine:'Your Answer',richtige:'Correct Answer',leiter:'IQ Ladder',schliessen:'Close',telefon:'Phone Lifeline',publikum:'Audience Lifeline',iqNach:'Your IQ after this question',teilen:'Share Result'},
  tr:{title:'IQ Testi',sub:'IQ\'nunu Test Et · 15 Soru · 3 Joker',placeholder:'Adiniz...',start:'Baslat',highscores:'Yuksek Skorlar',sekunden:'Saniye',iqLabel:'Guncel IQ',joker:'Jokerler',richtig:'Dogru!',falsch:'Yanlis! Elendil!',zeit:'Sure Doldu! Elendil!',naechste:'Sonraki Soru',ergebnis:'Sonucunuz',speichern:'Kaydet',gespeichert:'Kaydedildi!',nochmal:'Tekrar Oyna',zurueck:'Geri',perfekt:'Mukemmel!',fehler:'HATA ANALIZI',deine:'Cevabiniz',richtige:'Dogru Cevap',leiter:'IQ Merdiveni',schliessen:'Kapat',telefon:'Telefon Jokeri',publikum:'Seyirci Jokeri',iqNach:'Bu sorudan sonra IQ'},
  fr:{title:'Test QI',sub:'Questions Illimitees - 3 Jokers',placeholder:'Votre Nom...',start:'Commencer',highscores:'Meilleurs Scores',sekunden:'Secondes',iqLabel:'QI Actuel',joker:'Jokers',richtig:'Correct!',falsch:'Faux! Elimine!',zeit:'Temps Ecoule!',naechste:'Question Suivante',ergebnis:'Votre Resultat',speichern:'Sauvegarder',gespeichert:'Sauvegarde!',nochmal:'Rejouer',zurueck:'Retour',perfekt:'Parfait!',fehler:'ANALYSE ERREURS',deine:'Votre Reponse',richtige:'Bonne Reponse',leiter:'Echelle QI',schliessen:'Fermer',telefon:'Joker Telephone',publikum:'Joker Public',iqNach:'Votre QI apres'},
  es:{title:'Test de IQ',sub:'Preguntas Ilimitadas - 3 Comodines',placeholder:'Tu Nombre...',start:'Comenzar',highscores:'Mejores Puntuaciones',sekunden:'Segundos',iqLabel:'IQ Actual',joker:'Comodines',richtig:'Correcto!',falsch:'Incorrecto! Eliminado!',zeit:'Tiempo Agotado!',naechste:'Siguiente Pregunta',ergebnis:'Tu Resultado',speichern:'Guardar',gespeichert:'Guardado!',nochmal:'Jugar de Nuevo',zurueck:'Volver',perfekt:'Perfecto!',fehler:'ANALISIS ERRORES',deine:'Tu Respuesta',richtige:'Respuesta Correcta',leiter:'Escalera IQ',schliessen:'Cerrar',telefon:'Comodin Telefono',publikum:'Comodin Publico',iqNach:'Tu IQ despues'},
  ar:{title:'اختبار الذكاء',sub:'اسئلة غير محدودة - 3 نجدات',placeholder:'اسمك...',start:'ابدأ الآن',highscores:'أعلى النتائج',sekunden:'ثانية',iqLabel:'الذكاء الحالي',joker:'النجدات',richtig:'صحيح!',falsch:'خطأ! خرجت!',zeit:'انتهى الوقت!',naechste:'السؤال التالي',ergebnis:'نتيجتك',speichern:'حفظ',gespeichert:'تم الحفظ!',nochmal:'العب مجددا',zurueck:'رجوع',perfekt:'ممتاز!',fehler:'تحليل الأخطاء',deine:'إجابتك',richtige:'الإجابة الصحيحة',leiter:'سلم الذكاء',schliessen:'إغلاق',telefon:'نجدة الهاتف',publikum:'نجدة الجمهور',iqNach:'ذكاؤك بعد هذا السؤال'},
  pt:{title:'Teste de QI',sub:'Teste seu QI · 15 Perguntas · 3 Ajudas',placeholder:'Seu Nome...',start:'Comecar',highscores:'Recordes',sekunden:'Segundos',iqLabel:'QI Atual',joker:'Ajudas',richtig:'Correto!',falsch:'Errado! Eliminado!',zeit:'Tempo Esgotado!',naechste:'Proxima Pergunta',ergebnis:'Seu Resultado',speichern:'Salvar',gespeichert:'Salvo!',nochmal:'Jogar Novamente',zurueck:'Voltar',perfekt:'Perfeito - todas corretas!',fehler:'ANALISE DE ERROS',deine:'Sua Resposta',richtige:'Resposta Correta',leiter:'Escada de QI',schliessen:'Fechar',telefon:'Ajuda Telefone',publikum:'Ajuda do Publico',iqNach:'Seu QI apos esta pergunta',teilen:'Compartilhar'},
};

function T(key){return LANG[currentLang][key]||LANG['de'][key]||key;}

// ── SOUND TOGGLE ───────────────────────────────────────────
var soundEnabled=localStorage.getItem('sound_enabled')!=='0';
function toggleSound(){
  soundEnabled=!soundEnabled;
  localStorage.setItem('sound_enabled',soundEnabled?'1':'0');
  var btn=document.getElementById('sound-btn');
  if(btn)btn.textContent=soundEnabled?'🔊':'🔇';
}
function initSoundBtn(){
  var btn=document.getElementById('sound-btn');
  if(btn)btn.textContent=soundEnabled?'🔊':'🔇';
}

// ── ACHIEVEMENTS ───────────────────────────────────────────
var ACHIEVEMENTS=[
  {id:'first_game',name:'Erster Start',desc:'Erstes Spiel gespielt',icon:'🎮',fn:function(s){return s.games>=1;}},
  {id:'iq100',name:'Dreistellig',desc:'IQ 100+ erreicht',icon:'💯',fn:function(s){return (s.bestIQ||0)>=100;}},
  {id:'iq120',name:'Ueberflieger',desc:'IQ 120+ erreicht',icon:'🚀',fn:function(s){return (s.bestIQ||0)>=120;}},
  {id:'iq130',name:'Hochbegabt',desc:'IQ 130+ erreicht',icon:'✨',fn:function(s){return (s.bestIQ||0)>=130;}},
  {id:'iq145',name:'Genie',desc:'IQ 145 – Maximum!',icon:'🧠',fn:function(s){return (s.bestIQ||0)>=145;}},
  {id:'perfect',name:'Perfekt',desc:'Alle 15 Fragen richtig',icon:'⭐',fn:function(s){return (s.bestScore||0)>=15;}},
  {id:'streak3',name:'3er Streak',desc:'3 Tage Daily Challenge',icon:'🔥',fn:function(s){return (s.dailyStreak||0)>=3;}},
  {id:'streak7',name:'Wochen-Streak',desc:'7 Tage Daily Challenge',icon:'🏆',fn:function(s){return (s.dailyStreak||0)>=7;}},
  {id:'games5',name:'Fleissig',desc:'5 Spiele gespielt',icon:'🎯',fn:function(s){return (s.games||0)>=5;}},
  {id:'games20',name:'Profi',desc:'20 Spiele gespielt',icon:'👑',fn:function(s){return (s.games||0)>=20;}},
];
function checkAchievements(){
  var s=JSON.parse(localStorage.getItem('iq_stats')||'{}');
  var unlocked=JSON.parse(localStorage.getItem('achievements')||'[]');
  var neu=[];
  ACHIEVEMENTS.forEach(function(a){
    if(unlocked.indexOf(a.id)<0&&a.fn(s)){
      unlocked.push(a.id);
      neu.push(a);
    }
  });
  localStorage.setItem('achievements',JSON.stringify(unlocked));
  if(neu.length)setTimeout(function(){showAchievementToast(neu);},1500);
}
function showAchievementToast(list){
  var a=list[0];
  var t=document.getElementById('ach-toast');
  if(!t)return;
  t.querySelector('.ach-icon').textContent=a.icon;
  t.querySelector('.ach-name').textContent=a.name;
  t.querySelector('.ach-desc').textContent=a.desc;
  t.classList.add('show');
  setTimeout(function(){
    t.classList.remove('show');
    if(list.length>1)setTimeout(function(){showAchievementToast(list.slice(1));},600);
  },3000);
}

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
  if(!soundEnabled)return;
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
var _loaderDone=false;
function hideLoader(){
  if(_loaderDone)return;
  _loaderDone=true;
  var s=document.getElementById('loading-screen');
  if(s){
    s.style.opacity='0';
    s.style.transition='opacity .5s';
    s.style.pointerEvents='none';
    setTimeout(function(){s.style.display='none';},500);
  }
}
// Nach max 8s Ladescreen immer ausblenden — Server-Ping läuft im Hintergrund weiter
showLoader('Verbinde mit Server...',20);
setTimeout(function(){hideLoader();},8000);
setTimeout(function(){if(!_loaderDone)showLoader('Server startet...',60);},3000);
fetch(API+'/health').then(function(){hideLoader();}).catch(function(){});

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
  // Hintergrundfarbe je nach IQ
  var bg=iq>=140?'#0a0518':iq>=130?'#080a10':iq>=115?'#060a18':iq>=100?'#06091a':'#030310';
  document.documentElement.style.setProperty('--bg',bg);
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
    // Podest Top 3
    if(scores.length>=1){
      var podest=document.createElement('div');
      podest.style.cssText='display:flex;align-items:flex-end;justify-content:center;gap:.5rem;margin-bottom:1.5rem;';
      var medals=['🥇','🥈','🥉'];
      var heights=['80px','60px','50px'];
      var order=scores.length>=3?[1,0,2]:[0];
      order.forEach(function(idx){
        if(!scores[idx])return;
        var col=document.createElement('div');
        col.style.cssText='display:flex;flex-direction:column;align-items:center;gap:.4rem;flex:1;max-width:110px;';
        var medal=document.createElement('div');medal.style.cssText='font-size:28px;';medal.textContent=medals[idx]||'';
        var nm=document.createElement('div');nm.style.cssText='font-size:11px;font-weight:700;color:var(--text);text-align:center;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100px;';nm.textContent=scores[idx].name;
        var iq=document.createElement('div');iq.style.cssText='font-size:13px;font-weight:800;background:linear-gradient(135deg,var(--accent),var(--purple));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;';iq.textContent='IQ '+scores[idx].iq;
        var block=document.createElement('div');
        var bh=heights[idx]||'50px';
        var bcol=idx===0?'linear-gradient(135deg,#ffd700,#f59e0b)':idx===1?'linear-gradient(135deg,#94a3b8,#64748b)':'linear-gradient(135deg,#a855f7,#7c5fff)';
        block.style.cssText='width:100%;height:'+bh+';background:'+bcol+';border-radius:8px 8px 0 0;opacity:.8;';
        col.appendChild(medal);col.appendChild(nm);col.appendChild(iq);col.appendChild(block);
        podest.appendChild(col);
      });
      hl.appendChild(podest);
    }
    // Rest der Liste
    for(var i=0;i<scores.length;i++){
      var c=document.createElement('div');c.className='hs-card';
      var rng=document.createElement('span');rng.className='hs-rang';
      rng.textContent=i===0?'🥇':i===1?'🥈':i===2?'🥉':(i+1)+'.';
      var n=document.createElement('span');n.className='hs-name';n.textContent=scores[i].name;
      var lv=document.createElement('span');lv.className='hs-lv';lv.textContent='Frage '+scores[i].level;
      var iq=document.createElement('span');iq.className='hs-iq';iq.textContent='IQ '+scores[i].iq;
      c.appendChild(rng);c.appendChild(n);c.appendChild(lv);c.appendChild(iq);
      hl.appendChild(c);
    }
  });
}

function startGame(){
  isDailyMode=false;isOfflineMode=false;extraJokerUsed=false;
  if(taTimer){clearInterval(taTimer);taTimer=null;}
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
    // Time-Attack: globaler 60s Timer
    var taOv=document.getElementById('ta-overlay');
    if(currentMode==='timeattack'){
      taLeft=60;taTotalTime=60;
      if(taOv)taOv.style.display='block';
      document.getElementById('ta-count').textContent=60;
      document.getElementById('ta-bar-fill').style.width='100%';
      document.getElementById('ta-score').textContent='0';
      taTimer=setInterval(function(){
        taLeft--;
        var el=document.getElementById('ta-count');
        var bar=document.getElementById('ta-bar-fill');
        if(el)el.textContent=taLeft;
        if(bar)bar.style.width=Math.round(taLeft/taTotalTime*100)+'%';
        if(taLeft<=10&&el)el.style.color='var(--red)';
        if(taLeft<=0){clearInterval(taTimer);taTimer=null;calcResult();}
      },1000);
    }else{
      if(taOv)taOv.style.display='none';
    }
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
  if(currentMode==='timeattack'&&taLeft<=0){calcResult();return;}
  if(currentMode!=='timeattack'&&level>MAX_FRAGEN){calcResult();return;}
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
  fbox.classList.remove('flip');
  requestAnimationFrame(function(){fbox.classList.add('flip');});
  // Lern-Modus: Erklärungsbox leeren
  var le=document.getElementById('lern-erkl');
  if(le){le.style.display='none';le.textContent='';}
  // Time-Attack: kein Timer, Endless: kein spezieller Timer
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
  if(currentMode==='learn'){
    // Kein Timer im Lern-Modus
    document.getElementById('tn').textContent='∞';
    document.getElementById('ta').style.strokeDashoffset=0;
    st=Date.now();
  }else if(currentMode==='timeattack'){
    st=Date.now();
    // Timer läuft global, kein per-Frage-Timer
  }else{
    var sec=level<=5?20:level<=10?25:30;
    st=Date.now();tick(sec,sec);
    ti=setInterval(function(){tl--;tick(tl,sec);if(tl<=0){clearInterval(ti);tout();}},1000);
  }
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
    if(currentMode==='timeattack'){document.getElementById('ta-score').textContent=sc;}
    fb.textContent=T('richtig');fb.className='fb ok';
    var isSich=SICHER.indexOf(cur)>=0;
    playSound(isSich?'sicher':'richtig');
    launchConfetti(isSich?'medium':'small');
    showIQFb(true,cur);
    // Lern-Modus: Erklärung zeigen, immer weiter
    if(currentMode==='learn'&&q&&q.erklaerung){
      var le=document.getElementById('lern-erkl');
      if(le){le.textContent='💡 '+q.erklaerung;le.style.display='block';}
    }
    if(currentMode==='timeattack'){
      setTimeout(function(){loadAndShowQ(cur+1);},800);
    }else if(cur>=MAX_FRAGEN){
      setTimeout(function(){calcResult();},2000);
    }else{
      document.getElementById('nb').style.display='block';
    }
  }else{
    errs.push({q:q,ch:key,to:false,ri:d.richtige_antwort,erklaerung:d.erklaerung||''});
    fb.textContent=T('falsch')+' '+d.richtige_antwort+' - '+d.richtige_antwort_text;
    fb.className='fb no';
    playSound('falsch');
    showIQFb(false,cur);
    // Lern-Modus: Erklärung zeigen + weiter
    if(currentMode==='learn'){
      if(q&&q.erklaerung){
        var le2=document.getElementById('lern-erkl');
        if(le2){le2.textContent='💡 '+q.erklaerung;le2.style.display='block';}
      }
      setTimeout(function(){
        if(cur>=MAX_FRAGEN)calcResult();
        else document.getElementById('nb').style.display='block';
      },800);
    }else if(currentMode==='timeattack'){
      setTimeout(function(){loadAndShowQ(cur+1);},800);
    }else if(currentMode==='endless'){
      setTimeout(function(){calcResult();},2500);
    }else{
      setTimeout(function(){calcResult();},2500);
    }
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
  if(taTimer){clearInterval(taTimer);taTimer=null;}
  var taOv=document.getElementById('ta-overlay');
  if(taOv)taOv.style.display='none';
  // Reset Hintergrundfarbe
  document.documentElement.style.setProperty('--bg','#030310');
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
  } else if(currentMode==='timeattack'){
    document.getElementById('rv-chip').textContent='⏱️ '+sc+' richtig in 60 Sek.';
  } else if(currentMode==='learn'){
    document.getElementById('rv-chip').textContent='📚 Lern-Modus · '+sc+'/'+MAX_FRAGEN;
  } else if(currentMode==='endless'){
    document.getElementById('rv-chip').textContent='♾️ Endless · '+cur+' Fragen';
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
  // Kategorie-Auswertung
  var catSum=document.getElementById('cat-summary');
  if(catSum){
    catSum.innerHTML='';
    var catKeys=Object.keys(cm).filter(function(k){return k&&cm[k]>0;});
    if(catKeys.length>1){
      catKeys.sort(function(a,b){
        var pa=(cs[a]||0)/cm[a],pb=(cs[b]||0)/cm[b];
        return pb-pa;
      });
      var best=catKeys[0],worst=catKeys[catKeys.length-1];
      var bPct=Math.round((cs[best]||0)/cm[best]*100);
      var wPct=Math.round((cs[worst]||0)/cm[worst]*100);
      catSum.innerHTML=
        '<div style="font-size:11px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.1em;margin-bottom:.6rem;">Kategorie-Auswertung</div>'+
        '<div style="display:flex;gap:10px;flex-wrap:wrap;">'+
        '<div style="flex:1;background:rgba(34,197,94,0.08);border:1px solid rgba(34,197,94,0.25);border-radius:10px;padding:.8rem;min-width:120px;">'+
        '<div style="font-size:10px;color:var(--green);margin-bottom:4px;">⭐ STAERKE</div>'+
        '<div style="font-size:13px;font-weight:700;color:var(--text);">'+(KAT_ICONS[best]||'')+'&nbsp;'+best+'</div>'+
        '<div style="font-size:11px;color:var(--green);">'+bPct+'% richtig</div></div>'+
        (catKeys.length>1?
        '<div style="flex:1;background:rgba(239,68,68,0.08);border:1px solid rgba(239,68,68,0.2);border-radius:10px;padding:.8rem;min-width:120px;">'+
        '<div style="font-size:10px;color:var(--red);margin-bottom:4px;">📈 POTENTIAL</div>'+
        '<div style="font-size:13px;font-weight:700;color:var(--text);">'+(KAT_ICONS[worst]||'')+'&nbsp;'+worst+'</div>'+
        '<div style="font-size:11px;color:var(--red);">'+wPct+'% richtig</div></div>':'')+
        '</div>';
    }
  }
  checkRatingPrompt();
  checkAchievements();
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
  s.bestScore=Math.max(s.bestScore||0,sc);
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
  var chartWrap=document.getElementById('st-chart');chartWrap.innerHTML='';
  var hist=s.history||[];
  if(!hist.length){
    chartWrap.innerHTML='<div style="color:var(--text3);font-size:13px;text-align:center;width:100%;padding-top:40px;">Noch keine Spiele</div>';
  }else{
    var cv2=document.createElement('canvas');
    cv2.width=chartWrap.offsetWidth||300;cv2.height=90;
    cv2.style.width='100%';cv2.style.height='90px';
    chartWrap.appendChild(cv2);
    var cx=cv2.getContext('2d');
    var pts=hist.slice().reverse();
    var n=pts.length;
    var W=cv2.width,H=cv2.height,pad=10;
    var minIQ=85,maxIQ=145;
    function iqY(iq){return H-pad-(iq-minIQ)/(maxIQ-minIQ)*(H-pad*2);}
    function ptX(i){return pad+(i/(Math.max(n-1,1)))*(W-pad*2);}
    // Verlaufslinie
    var grad=cx.createLinearGradient(0,0,W,0);
    grad.addColorStop(0,'#4a90e2');grad.addColorStop(0.5,'#7c5fff');grad.addColorStop(1,'#ffd700');
    cx.beginPath();
    pts.forEach(function(h,i){cx.lineTo(ptX(i),iqY(h.iq));});
    cx.strokeStyle=grad;cx.lineWidth=2.5;cx.lineJoin='round';cx.stroke();
    // Flaeche darunter
    cx.beginPath();
    pts.forEach(function(h,i){cx.lineTo(ptX(i),iqY(h.iq));});
    cx.lineTo(ptX(n-1),H);cx.lineTo(ptX(0),H);cx.closePath();
    var aGrad=cx.createLinearGradient(0,0,0,H);
    aGrad.addColorStop(0,'rgba(74,144,226,0.25)');aGrad.addColorStop(1,'rgba(74,144,226,0)');
    cx.fillStyle=aGrad;cx.fill();
    // Punkte + Labels
    pts.forEach(function(h,i){
      var x=ptX(i),y=iqY(h.iq);
      var col=h.iq>=130?'#ffd700':h.iq>=115?'#4a90e2':h.iq>=100?'#7c5fff':'#475569';
      cx.beginPath();cx.arc(x,y,3.5,0,Math.PI*2);
      cx.fillStyle=col;cx.fill();
      cx.strokeStyle='#030310';cx.lineWidth=1.5;cx.stroke();
      if(i===0||i===n-1||n<=5){
        cx.font='7px Arial';cx.fillStyle='#94a3b8';cx.textAlign='center';
        cx.fillText(h.iq,x,y-7);
      }
      var d=h.date?h.date.slice(5).replace('-','/'):'-';
      cx.font='6px Arial';cx.fillStyle='#475569';cx.textAlign='center';
      cx.fillText(d,x,H-1);
    });
  }
  // Achievements anzeigen
  var achEl=document.getElementById('st-achievements');
  if(achEl){
    var unlocked=JSON.parse(localStorage.getItem('achievements')||'[]');
    achEl.innerHTML='';
    ACHIEVEMENTS.forEach(function(a){
      var got=unlocked.indexOf(a.id)>=0;
      var d=document.createElement('div');
      d.style.cssText='display:flex;align-items:center;gap:.7rem;padding:.6rem .8rem;border-radius:10px;margin-bottom:.4rem;background:'+(got?'rgba(74,144,226,0.08)':'rgba(26,37,64,0.4)')+';border:1px solid '+(got?'rgba(74,144,226,0.3)':'var(--border)')+';opacity:'+(got?'1':'0.45')+';';
      d.innerHTML='<span style="font-size:22px;">'+a.icon+'</span>'+
        '<div><div style="font-size:12px;font-weight:700;color:'+(got?'var(--text)':'var(--text3)')+';">'+a.name+'</div>'+
        '<div style="font-size:11px;color:var(--text3);">'+a.desc+'</div></div>'+
        (got?'<span style="margin-left:auto;font-size:10px;color:var(--green);font-weight:700;">✓</span>':'');
      achEl.appendChild(d);
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
initSoundBtn();
loadOfflineCache();
checkOnboarding();
checkChallenge();
initNotifBtn();
checkDailyNotification();
