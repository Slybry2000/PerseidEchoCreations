(function(){
"use strict";
var row=document.getElementById('row'), lanes=[].slice.call(row.querySelectorAll('.lane')), N=lanes.length;
var cv=document.getElementById('fly'), cx=cv.getContext('2d'), root=document.documentElement, B=document.body;
var door=document.getElementById('door'), G={}, cur=0, token=0, FLIGHT=420;
var still=false; try{still=matchMedia('(prefers-reduced-motion: reduce)').matches}catch(e){}

/* ---------- layout: the whole poster always fits, on any screen ---------- */
function fit(){
  var W=innerWidth, H=innerHeight;
  var tall = W<H && W<760, short = !tall && H<520;
  B.classList.toggle('tall',tall); B.classList.toggle('short',short);
  var bar = short?38:(tall?52:64), sp = tall?48:(short?28:(W<1000?40:(W<1250?48:56))), foot = tall?0:(short?36:72), peek=(tall||short)?0:30;
  door.style.height = tall?'':(H-peek)+'px';
  var s, pw, ph;
  if(tall){ s=W/1440; }
  else{ s=Math.min((W-(N-1)*sp)/1440,(H-peek-bar-foot)/900); }
  pw=1440*s; ph=900*s;
  root.style.setProperty('--bar',bar+'px'); root.style.setProperty('--sp',sp+'px');
  root.style.setProperty('--open',(tall?ph:pw)+'px');
  if(tall){ row.style.width='100%'; row.style.height=(ph+(N-1)*sp)+'px'; }
  else{ row.style.width=(pw+(N-1)*sp)+'px'; row.style.height=ph+'px'; }
  [].forEach.call(row.querySelectorAll('.poster iframe'),function(f){ f.style.transform='scale('+s+')'; f.parentNode.style.width=pw+'px'; f.parentNode.style.height=ph+'px'; });
  var d=Math.min(devicePixelRatio||1,2); cv.width=W*d; cv.height=H*d; cx.setTransform(d,0,0,d,0,0);
  G={tall:tall,s:s,pw:pw,ph:ph,sp:sp,left:(W-(pw+(N-1)*sp))/2,top:bar};
}

/* ---------- the spark that travels from the lane you left into the lane you entered ---------- */
function laneLeft(j,open){ return G.left + j*G.sp + (j>open ? G.pw-G.sp : 0); }
function fly(from,to,ms,done){
  var cxp=(from[0]+to[0])/2, cyp=Math.max(8,Math.min(from[1],to[1])-70-Math.abs(to[0]-from[0])*.12), t0=performance.now(), my=++token;
  function at(p){var q=1-p;return [q*q*from[0]+2*q*p*cxp+p*p*to[0], q*q*from[1]+2*q*p*cyp+p*p*to[1]]}
  function frame(now){
    if(my!==token) return;
    var k=(now-t0)/ms, fade=k>1?Math.max(0,1-(k-1)*ms/160):1, p=Math.min(1,k); p=p<.5?2*p*p:1-Math.pow(-2*p+2,2)/2;
    cx.clearRect(0,0,innerWidth,innerHeight);
    if(fade>0){
      cx.lineCap='round';
      for(var i=0;i<22;i++){ var a=Math.max(0,p-.34*(i+1)/22), b=Math.max(0,p-.34*i/22), A=at(a), Bp=at(b);
        cx.strokeStyle='rgba(255,106,42,'+(.85*(1-i/22)*fade)+')'; cx.lineWidth=5*(1-i/22)+.6; cx.beginPath(); cx.moveTo(A[0],A[1]); cx.lineTo(Bp[0],Bp[1]); cx.stroke(); }
      var h=at(p), g=cx.createRadialGradient(h[0],h[1],0,h[0],h[1],26);
      g.addColorStop(0,'rgba(255,250,244,'+fade+')'); g.addColorStop(.25,'rgba(255,150,90,'+(.9*fade)+')'); g.addColorStop(1,'rgba(255,106,42,0)');
      cx.fillStyle=g; cx.beginPath(); cx.arc(h[0],h[1],26,0,7); cx.fill();
    }
    if(k>=1&&done){ var d=done; done=null; d(); }
    if(fade>0) requestAnimationFrame(frame); else cx.clearRect(0,0,innerWidth,innerHeight);
  }
  requestAnimationFrame(frame);
}

/* ---------- entering a lane opens it and plays its poster from the start, every time ---------- */
function win(l){ try{ var w=l.querySelector('iframe').contentWindow; return (w&&typeof w.play==='function')?w:null; }catch(e){ return null; } }
function enter(l){
  var i=lanes.indexOf(l); if(i===cur) return;
  var old=cur; cur=i; openedAt=Date.now(); sync();
  lanes[old].querySelector('.spine').classList.add('seen');
  lanes.forEach(function(x){ x.classList.toggle('on',x===l); });
  var w=win(l); if(!w) return;
  if(still){ if(w.finish) w.finish(); return; }
  w.play();
  if(G.tall){ l.scrollIntoView({block:'nearest',behavior:'smooth'}); return; }
  /* hold the poster on its bare first frame while the spark crosses over, then let it run so its own spark picks up exactly where this one arrives */
  var e=w.SPARK_ENTRY||{x:0,y:300,t:.1}, hold=Math.max(0,FLIGHT-e.t*1000), anims=[];
  try{ anims=w.document.getAnimations(); anims.forEach(function(a){a.pause()}); }catch(err){ hold=0; }
  var rr=row.getBoundingClientRect(); G.left=rr.left; G.top=rr.top;
  var from=[laneLeft(old,i)+G.sp/2, G.top+(B.classList.contains('short')?25:42)], to=[laneLeft(i,i)+e.x*G.s, G.top+e.y*G.s];
  var my=token+1;
  setTimeout(function(){ if(cur===i && my===token) anims.forEach(function(a){ try{a.play()}catch(err){} }); },hold);
  fly(from,to,FLIGHT);
}
/* the footer always describes the open lane and links to its page */
var openedAt=0, nk=document.getElementById('nk'), nd=document.getElementById('nd'), go=document.getElementById('go');
function sync(){ var l=lanes[cur]; nk.textContent=l.dataset.n+' · '+l.dataset.k; nd.textContent=l.dataset.d; go.href=l.dataset.href; }
/* a click on a closed lane opens it; a click on the open poster goes to that service's page */
function pick(l){ if(lanes.indexOf(l)===cur && Date.now()-openedAt>600){ location.href=l.dataset.href; } else enter(l); }
lanes.forEach(function(l){
  l.addEventListener('focus',function(){enter(l)});
  l.addEventListener('click',function(){pick(l)});
  l.addEventListener('keydown',function(ev){ if(ev.key==='Enter'){ location.href=l.dataset.href; } });
});
sync();
addEventListener('resize',fit); addEventListener('load',fit); addEventListener('orientationchange',function(){setTimeout(fit,250)});
if(window.visualViewport) visualViewport.addEventListener('resize',fit);
try{ new ResizeObserver(fit).observe(root); }catch(e){}
fit();
var q=+new URLSearchParams(location.search).get('lane'); if(q) setTimeout(function(){enter(lanes[q-1])},900);
})();
