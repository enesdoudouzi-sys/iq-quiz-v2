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

const API = 'https://iq-quiz-v2.onrender.com';
const L = ['A','B','C','D'];
const COL = {'Allgemeinwissen':'#4a90e2','Logik & Zahlenfolgen':'#7c5fff','Konzentration':'#06b6d4'};
const CK = function(p){ return p.indexOf('Allgemein')>=0?'aw':p.indexOf('Logik')>=0?'log':'kz'; };
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
var cs={aw:0,log:0,kz:0},cm={aw:0,log:0,kz:0},times=[],errs=[];
var playerName='',finalIQ=85,gesperrte=[];
var jokerStatus={'5050':true,'telefon':true,'publikum':true};
var isDailyMode=false,_dvTimer=null;

function showStart(){
  document.getElementById('sv').style.display='flex';
  document.getElementById('qv').classList.remove('active');
  document.getElementById('rv').style.display='none';
  document.getElementById('hv').style.display='none';
  document.getElementById('dv').style.display='none';
  clearInterval(_dvTimer);
}
function showQuiz(){
  document.getElementById('sv').style.display='none';
  document.getElementById('qv').classList.add('active');
  document.getElementById('rv').style.display='none';
  document.getElementById('hv').style.display='none';
  document.getElementById('dv').style.display='none';
}
function showResult(){
  document.getElementById('sv').style.display='none';
  document.getElementById('qv').classList.remove('active');
  document.getElementById('rv').style.display='block';
  document.getElementById('hv').style.display='none';
  document.getElementById('dv').style.display='none';
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
  isDailyMode=false;
  playerName=document.getElementById('ni').value||'Spieler';
  cur=0;sc=0;done=false;finalIQ=85;gesperrte=[];
  cs={aw:0,log:0,kz:0};cm={aw:0,log:0,kz:0};times=[];errs=[];qs=[];
  jokerStatus={'5050':true,'telefon':true,'publikum':true};
  updJoker();
  fetch(API+'/api/start',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({name:playerName})
  }).then(function(r){return r.json();}).then(function(d){
    sessionId=d.session_id;
    buildLeiter();
    updIQ(85);
    showQuiz();
    loadAndShowQ(1);
  }).catch(function(e){alert('Fehler: '+e.message);});
}

function loadAndShowQ(level){
  if(level>MAX_FRAGEN){calcResult();return;}
  cur=level;done=false;gesperrte=[];
  document.getElementById('iq-fb').style.display='none';
  document.getElementById('nb').style.display='none';
  document.getElementById('fb').textContent='';
  document.getElementById('fb').className='fb';
  document.getElementById('joker-overlay').classList.remove('show');
  fetch(API+'/api/frage/'+sessionId+'/'+level)
  .then(function(r){return r.json();})
  .then(function(q){
    qs[level]=q;
    document.getElementById('qc').textContent=level+' / '+MAX_FRAGEN;
    document.getElementById('pb').textContent=q.kategorie.toUpperCase();
    document.getElementById('preis').textContent=q.preis;
    var col=COL[q.kategorie]||'#4a90e2';
    document.getElementById('pdot').style.background=col;
    document.getElementById('pb').style.color=col;
    document.getElementById('ta').style.stroke=col;
    document.getElementById('qt').textContent=q.frage;
    document.getElementById('pf').style.width=((level-1)/MAX_FRAGEN*100)+'%';
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
  }).catch(function(e){alert('Fehler beim Laden: '+e.message);});
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
  cm[CK(q.kategorie)]++;times.push(30);
  errs.push({q:q,ch:null,to:true,ri:q.richtig||'A'});
  document.querySelectorAll('.opt').forEach(function(b){
    if(b.getAttribute('data-key')===q.richtig)b.classList.add('ok');
    b.disabled=true;
  });
  document.getElementById('fb').textContent='Zeit abgelaufen! Ausgeschieden!';
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
  var k=CK(q?q.kategorie:'');cm[k]++;
  fetch(API+'/api/antwort',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({session_id:sessionId,level:cur,antwort:key})
  }).then(function(r){return r.json();}).then(function(d){
    var bs=document.querySelectorAll('.opt');
    var fb=document.getElementById('fb');
    bs.forEach(function(b){
      if(b.getAttribute('data-key')===key)b.classList.add(d.richtig?'ok':'no');
      if(!d.richtig&&b.getAttribute('data-key')===d.richtige_antwort)b.classList.add('ok');
      b.disabled=true;
    });
    if(d.richtig){
      sc++;cs[k]++;
      fb.textContent='Richtig!';fb.className='fb ok';
      var isSich=SICHER.indexOf(cur)>=0;
      playSound(isSich?'sicher':'richtig');
      launchConfetti(isSich?'medium':'small');
      showIQFb(true,cur);
      if(cur>=MAX_FRAGEN){
        setTimeout(function(){calcResult();},2000);
      } else {
        document.getElementById('nb').style.display='block';
      }
    } else {
      errs.push({q:q,ch:key,to:false,ri:d.richtige_antwort});
      fb.textContent='Falsch! Ausgeschieden! Richtig war: '+d.richtige_antwort+' - '+d.richtige_antwort_text;
      fb.className='fb no';
      playSound('falsch');
      showIQFb(false,cur);
      setTimeout(function(){calcResult();},2500);
    }
  });
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
    } else if(d.typ==='telefon'){
      document.getElementById('jo-title').textContent='Telefon-Joker';
      var content=document.getElementById('jo-content');content.innerHTML='';
      var p1=document.createElement('div');p1.className='jo-text';p1.textContent='"'+d.text+'"';
      var p2=document.createElement('div');p2.className='jo-tipp';p2.textContent='Antwort: '+d.tipp;
      content.appendChild(p1);content.appendChild(p2);
      document.getElementById('joker-overlay').classList.add('show');
    } else if(d.typ==='publikum'){
      document.getElementById('jo-title').textContent='Publikums-Joker';
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
  document.getElementById('rv-chip').textContent=sc+' von '+MAX_FRAGEN+' richtig';
  document.getElementById('rv-sub').textContent=iq>=130?'Hervorragend!':iq>=115?'Sehr gut!':iq>=100?'Gut!':'Weiter ueben!';
  document.getElementById('baw').textContent=cs.aw+' / '+cm.aw;
  document.getElementById('blog').textContent=cs.log+' / '+cm.log;
  document.getElementById('bkz').textContent=cs.kz+' / '+cm.kz;
  document.getElementById('bt').textContent=avg+' Sek.';
  document.getElementById('sn').value=playerName;
  if(isDailyMode){
    var _today=new Date().toISOString().split('T')[0];
    localStorage.setItem('daily_'+_today,JSON.stringify({iq:finalIQ,level:sc}));
    fetch(API+'/api/daily/submit',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:playerName,iq:finalIQ,level:sc})});
    document.getElementById('rv-chip').textContent='📅 Challenge · '+sc+' / '+MAX_FRAGEN+' richtig';
    isDailyMode=false;
  }
  document.getElementById('ml').innerHTML='';
  document.getElementById('err-lbl').textContent=errs.length?'FEHLERAUSWERTUNG: '+errs.length+' Fehler':'Fehlerauswertung';
  if(!errs.length){
    var d=document.createElement('div');d.className='none';d.textContent='Perfekt - alle Fragen richtig!';
    document.getElementById('ml').appendChild(d);
  } else {
    for(var i=0;i<errs.length;i++){
      var e=errs[i];
      var card=document.createElement('div');card.className='err-card';
      var cat=document.createElement('div');cat.className='err-cat';cat.textContent=e.q.kategorie;
      card.appendChild(cat);
      if(e.to){var tob=document.createElement('span');tob.className='tob';tob.textContent='Zeit abgelaufen';card.appendChild(tob);}
      var qd=document.createElement('div');qd.className='err-q';qd.textContent=e.q.frage;card.appendChild(qd);
      if(e.q.seq){var sd=document.createElement('div');sd.className='err-seq';sd.textContent=e.q.seq;card.appendChild(sd);}
      var row=document.createElement('div');row.className='err-row';
      if(!e.to&&e.ch){
        var col1=document.createElement('div');col1.className='err-col';
        var lbl1=document.createElement('span');lbl1.className='err-clbl';lbl1.textContent='Deine Antwort';
        var p1=document.createElement('span');p1.className='pill pno';p1.textContent=e.ch+' - '+e.q.antworten[e.ch];
        col1.appendChild(lbl1);col1.appendChild(p1);row.appendChild(col1);
      }
      var col2=document.createElement('div');col2.className='err-col';
      var lbl2=document.createElement('span');lbl2.className='err-clbl';lbl2.textContent='Richtige Antwort';
      var p2=document.createElement('span');p2.className='pill pok';p2.textContent=e.ri+' - '+e.q.antworten[e.ri];
      col2.appendChild(lbl2);col2.appendChild(p2);row.appendChild(col2);
      card.appendChild(row);
      document.getElementById('ml').appendChild(card);
    }
  }
}

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
  } else {
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
  cur=0;sc=0;done=false;finalIQ=85;gesperrte=[];
  cs={aw:0,log:0,kz:0};cm={aw:0,log:0,kz:0};times=[];errs=[];qs=[];
  jokerStatus={'5050':true,'telefon':true,'publikum':true};
  updJoker();
  isDailyMode=true;
  clearInterval(_dvTimer);
  fetch(API+'/api/daily/start',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({name:playerName})
  }).then(function(r){return r.json();}).then(function(d){
    sessionId=d.session_id;
    buildLeiter();
    updIQ(85);
    showQuiz();
    loadAndShowQ(1);
  }).catch(function(e){alert('Fehler: '+e.message);});
}

function downloadCert(){
  document.getElementById('cert-name').textContent=playerName;
  document.getElementById('cert-iq').textContent='IQ '+finalIQ;
  document.getElementById('cert-class').textContent=getBez(finalIQ);
  document.getElementById('cert-detail').textContent=sc+' von 15 Fragen richtig · '+new Date().toLocaleDateString('de-DE',{day:'numeric',month:'long',year:'numeric'});
  document.getElementById('cert-footer').textContent='IQ-Quiz · iq-quiz-v2.onrender.com · '+new Date().toLocaleDateString('de-DE');
  window.print();
}

function saveHS(){
  var name=document.getElementById('sn').value||playerName;
  fetch(API+'/api/highscores',{
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({name:name,iq:finalIQ,level:sc})
  }).then(function(){
    var btn=document.querySelector('.save-btn');
    btn.textContent='Gespeichert!';
    setTimeout(function(){btn.textContent='Speichern';},2000);
  });
}
