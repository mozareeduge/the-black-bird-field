(function(){
  "use strict";
  const doc=document;
  const CFG={frameSize:192,frames:108,cols:12,baseFrameMs:75};
  const st={playing:true,speed:1.5,frame:0,tick:0,timer:null,loaded:false};
  const script=doc.currentScript;
  const base=new URL(".",script.src);
  const spriteUrl=new URL("favicon-sprite.png",base).href;
  const sprite=new Image();
  const canvas=doc.createElement("canvas"); canvas.width=canvas.height=64;
  const ctx=canvas.getContext("2d");
  function srcRect(frame){const col=frame%CFG.cols,row=Math.floor(frame/CFG.cols);return [col*CFG.frameSize,row*CFG.frameSize,CFG.frameSize,CFG.frameSize]}
  function linkEl(){
    let link=doc.getElementById("dynamic-favicon");
    if(!link){link=doc.createElement("link");link.id="dynamic-favicon";link.rel="icon";link.type="image/png";link.sizes="64x64";doc.head.appendChild(link)}
    return link;
  }
  function render(){
    if(!st.loaded)return;
    ctx.clearRect(0,0,64,64);
    ctx.imageSmoothingEnabled=true;
    if("imageSmoothingQuality" in ctx)ctx.imageSmoothingQuality="high";
    const [sx,sy,sw,sh]=srcRect(st.frame);
    ctx.drawImage(sprite,sx,sy,sw,sh,0,0,64,64);
    linkEl().href=canvas.toDataURL("image/png");
    window.dispatchEvent(new CustomEvent("mozare-favicon-frame",{detail:{...st}}));
  }
  function intervalMs(){return Math.max(35,Math.round(CFG.baseFrameMs/st.speed))}
  function advance(){st.frame=(st.frame+1)%CFG.frames;st.tick++;render()}
  function stop(){if(st.timer!==null){clearInterval(st.timer);st.timer=null}}
  function start(){stop();if(!st.playing||!st.loaded)return;st.timer=setInterval(advance,intervalMs())}
  function play(){st.playing=true;start()}
  function pause(){st.playing=false;stop()}
  function step(){pause();st.frame=(st.frame+3)%CFG.frames;st.tick++;render()}
  function reset(){st.frame=0;st.tick=0;render();if(st.playing)start()}
  function setSpeed(v){st.speed=Number(v);if(st.playing)start()}
  window.MozareFavicon={state:st,play,pause,step,reset,setSpeed,render};
  sprite.addEventListener("load",()=>{st.loaded=true;render();start()});
  sprite.src=spriteUrl;
  doc.addEventListener("visibilitychange",()=>{if(doc.visibilityState==="visible"&&st.playing)start()});
})();
