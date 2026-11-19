function size(){
  var w=stack.clientWidth||innerWidth, room=stack.clientHeight-6*34, ph=w*.625;
  if(innerWidth>860&&room>120&&ph>room)ph=room;
  var r=document.documentElement.style;r.setProperty('--ph',ph+'px');r.setProperty('--pw',(ph*1.6)+'px');r.setProperty('--ps',ph/900);
}
function hot(slug){
  stack.classList.toggle('dim',!!slug);
  lns.forEach(function(l){l.classList.toggle('hot',l.getAttribute('data-lane')===slug)});
}
function openLane(slug){
  document.body.classList.toggle('done',!!slug);
  size();
  lns.forEach(function(l){
    var on=l.getAttribute('data-lane')===slug;l.classList.toggle('on',on);
    if(!on)return;
    var f=l.querySelector('iframe');
    if(!f.getAttribute('src'))f.src=f.getAttribute('data-src');   /* loads, then plays itself */
    else try{f.contentWindow.play()}catch(e){}
  });
}
addEventListener('resize',size);
