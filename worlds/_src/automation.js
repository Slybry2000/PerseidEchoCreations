window.SPARK_ENTRY = {x:0, y:227.8, t:0.335};
(function(){
 var root=document.documentElement;
 var q=new URLSearchParams(location.search), T=q.get('t');
 var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
 function reflow(){void root.getBoundingClientRect();}
 function freeze(t){document.getAnimations().forEach(function(a){a.pause();a.currentTime=t*1000;});}
 window.play=function(){
  root.classList.remove('play');reflow();
  if(reduce)return;
  root.classList.add('play');reflow();
  var ends=document.getAnimations().map(function(a){return a.effect.getComputedTiming().endTime;});
  window.DURATION=Math.max.apply(null,ends)/1000;
  if(T!==null&&T!==''&&!isNaN(parseFloat(T)))freeze(parseFloat(T));
 };
 window.finish=function(){root.classList.remove('play');document.getAnimations().forEach(function(a){a.cancel();});};
 window.addEventListener('message',function(e){if(e.data==='play')play();else if(e.data==='finish')finish();});
 play();
})();
