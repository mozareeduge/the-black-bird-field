(function(){
  "use strict";
  const doc = document;
  function linkEl(){
    let link = doc.getElementById("dynamic-favicon");
    if(!link){
      link = doc.createElement("link");
      link.id = "dynamic-favicon";
      link.rel = "icon";
      link.type = "image/png";
      doc.head.appendChild(link);
    }
    return link;
  }
  function svgToDataURL(svg){ return "data:image/svg+xml;charset=UTF-8," + encodeURIComponent(svg); }

  function line(x1,y1,x2,y2,stroke,w=2,op=1){return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${stroke}" stroke-width="${w}" stroke-linecap="round" opacity="${op}"/>`}
  function rect(x,y,w,h,fill,op=1,rx=0,stroke="none",sw=0){return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" opacity="${op}" stroke="${stroke}" stroke-width="${sw}"/>`}
  function wrap(inner,bg){return `<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg"><rect width="64" height="64" rx="5" fill="${bg}"/>${inner}</svg>`}
  function icon(t){
    const bg="#000000",fg="#f4f1eb",muted="#8b857d";
    const flip=Math.sin((t+.5)*2*Math.PI)>0, channel=4+7*(.5+.5*Math.sin((t+.08)*2*Math.PI));
    const x1=flip?39:25, x2=flip?25:39;
    let g='';
    g+=rect(x1-2,10,4,44,fg,.76,1); g+=rect(x2-channel/2,17,channel,30,bg,1,1,fg,1.15);
    g+=line(13,20,51,20,muted,.8,.15); g+=line(13,44,51,44,muted,.8,.15); g+=line(14,32,50,32,muted,1,.22);
    return wrap(g,bg);
  }
  const state={playing:true,speed:2.5,t:0,tick:0,timer:null,stepSize:.0625};
  function intervalMs(){return Math.max(55,Math.round(450/state.speed))}
  function render(){const svg=icon(state.t);linkEl().href=svgToDataURL(svg);window.dispatchEvent(new CustomEvent("mozare-favicon-frame",{detail:{...state,svg}}))}
  function advance(){state.t=(state.t+state.stepSize)%1;state.tick++;render()}
  function stop(){if(state.timer!==null){clearInterval(state.timer);state.timer=null}}
  function start(){stop();if(!state.playing)return;state.timer=setInterval(advance,intervalMs())}
  function play(){state.playing=true;start()} function pause(){state.playing=false;stop()}
  function setSpeed(v){state.speed=Number(v);if(state.playing)start()}
  function reset(){state.t=0;state.tick=0;render();if(state.playing)start()}
  window.MozareFavicon={state,play,pause,step:()=>{pause();advance()},reset,setSpeed,render};
  doc.addEventListener("visibilitychange",()=>{if(doc.visibilityState==="visible"&&state.playing)start()});
  render();start();
})();
