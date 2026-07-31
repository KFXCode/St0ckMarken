/* St0ckMarken budget tracker — simulated bankroll, stored only in this browser (localStorage). */
(function(){
var D=window.SM_DATA||{plays:[],graded:[]};
function g(k){return JSON.parse(localStorage.getItem('sm_'+k)||'null')}
function s(k,v){localStorage.setItem('sm_'+k,JSON.stringify(v))}
function del(k){localStorage.removeItem('sm_'+k)}
function fmt(n){return '$'+(Math.round(n*100)/100).toLocaleString()}
function state(){return{start:g('start'),cash:g('cash')||0,open:g('open')||[],closed:g('closed')||[]}}
function save(st){s('cash',st.cash);s('open',st.open);s('closed',st.closed)}
var BROKERS={
 robinhood:{name:'Robinhood',url:function(t){return 'https://robinhood.com/stocks/'+t}},
 webull:{name:'Webull',url:function(t){return 'https://www.webull.com/quote/'+t.toLowerCase()}},
 fidelity:{name:'Fidelity',url:function(t){return 'https://digital.fidelity.com/prgw/digital/research/quote/dashboard/summary?symbol='+t}},
 schwab:{name:'Charles Schwab',url:function(t){return 'https://client.schwab.com/app/research/#/stocks/'+t}},
 etrade:{name:'E*TRADE',url:function(t){return 'https://us.etrade.com/etx/mkt/quotes?symbol='+t}},
 moomoo:{name:'moomoo',url:function(t){return 'https://www.moomoo.com/stock/'+t+'-US'}},
 thinkorswim:{name:'thinkorswim',url:function(t){return 'https://trade.thinkorswim.com/'}},
 ibkr:{name:'Interactive Brokers',url:function(t){return 'https://portal.interactivebrokers.com/'}},
 tastytrade:{name:'tastytrade',url:function(t){return 'https://my.tastytrade.com/app.html#/trading?symbol='+t}},
 public:{name:'Public',url:function(t){return 'https://public.com/stocks/'+t.toLowerCase()}},
 sofi:{name:'SoFi Invest',url:function(t){return 'https://www.sofi.com/invest/'}},
 ally:{name:'Ally Invest',url:function(t){return 'https://live.invest.ally.com/'}},
 tradestation:{name:'TradeStation',url:function(t){return 'https://www.tradestation.com/'}},
 firstrade:{name:'Firstrade',url:function(t){return 'https://invest.firstrade.com/cgi-bin/main#/cgi-bin/enter_transaction'}},
 coinbase:{name:'Coinbase',url:function(t){return 'https://www.coinbase.com/advanced-trade/spot/'+t.replace('-USD','')+'-USD'}}
};
/* Scenario math: simple linear delta model (delta ≈ 0.40). Est. option P/L for a move
   = position cost × move% × (spot/premium × 0.40) / 100, losses capped at what you paid. */
function scenarioHTML(p,q){
 var cost=p.cost*q;
 if(p.kind==='SPOT'){
  var rows='<div class="scn scn-h"><span>If it…</span><span>Your $'+cost+' becomes</span></div>';
  [5,10,25,50].forEach(function(m){
   rows+='<div class="scn"><span>rises '+m+'%</span><span style="color:#00b46e">$'+(cost*(1+m/100)).toFixed(0)+' (+$'+(cost*m/100).toFixed(0)+')</span></div>';});
  [10,25].forEach(function(m){
   rows+='<div class="scn"><span>falls '+m+'%</span><span style="color:#ff4d6d">$'+(cost*(1-m/100)).toFixed(0)+' (−$'+(cost*m/100).toFixed(0)+')</span></div>';});
  rows+='<div class="scn scn-h"><span>You put in</span><span>'+fmt(cost)+'</span></div>';
  return rows;
 }
 if(p.kind==='CASH-SECURED PUT'){
  return '<div class="scn"><span>Stays above $'+p.strike+' strike</span><span style="color:#00b46e">keep +'+fmt(p.prem*100*q)+' premium</span></div>'+
         '<div class="scn"><span>Closes below $'+p.strike+'</span><span style="color:#ff4d6d">assigned '+ (100*q)+' shares at $'+p.strike+'</span></div>'+
         '<div class="scn"><span>Collateral needed</span><span>'+fmt(cost)+'</span></div>';
 }
 var lev=p.spot/p.prem*0.4;
 var isPut=p.kind.indexOf('PUT')>=0;
 var fav=isPut?'falls':'rises', adv=isPut?'rises':'falls';
 var rows='<div class="scn scn-h"><span>If the stock…</span><span>Est. profit / loss</span></div>';
 [1,3,5].forEach(function(m){
  var win=cost*m*lev/100;
  var loss=Math.min(cost,win);
  rows+='<div class="scn"><span>'+fav+' '+m+'%</span><span style="color:#00b46e">+'+fmt(win)+'</span></div>'+
        '<div class="scn"><span>'+adv+' '+m+'%</span><span style="color:#ff4d6d">−'+fmt(loss)+'</span></div>';
 });
 rows+='<div class="scn"><span>Worst case (expires worthless)</span><span style="color:#ff4d6d">−'+fmt(cost)+'</span></div>'+
       '<div class="scn scn-h"><span>Cost to enter</span><span>'+fmt(cost)+'</span></div>';
 return rows;
}
function reconcile(st){var ch=false;
 st.open=st.open.filter(function(pos){
  var gr=D.graded.find(function(x){return x.date===pos.date&&x.t===pos.t});
  if(!gr)return true;
  var proceeds=Math.max(0,pos.cost*(1+gr.pl/100));
  st.cash+=proceeds;
  st.closed.push(Object.assign({},pos,{pl:gr.pl,result:gr.result,proceeds:proceeds}));
  ch=true;return false});
 if(ch)save(st)}
function txt(id,t){var el=document.getElementById(id);if(el)el.textContent=t}
function render(){var st=state();
 var setup=document.getElementById('sm-setup'),dash=document.getElementById('sm-dash');
 var hpv=document.getElementById('sm-hero-pv'),hpc=document.getElementById('sm-hero-pc');
 if(st.start==null){setup.style.display='';dash.style.display='none';
  if(hpv){hpv.textContent='Set a budget ↓';hpv.style.fontSize='';}if(hpc)hpc.textContent='';markTaken(st);return}
 reconcile(st);
 setup.style.display='none';dash.style.display='';
 var openVal=st.open.reduce(function(a,p){return a+p.cost},0);
 var now=st.cash+openVal, gr=(now-st.start)/st.start*100;
 txt('sm-v-start',fmt(st.start));txt('sm-v-now',fmt(now));
 var ge=document.getElementById('sm-v-gr');
 ge.textContent=(gr>=0?'+':'')+gr.toFixed(1)+'%';ge.style.color=gr>=0?'#00b46e':'#ff4d6d';
 txt('sm-cash','Cash you can spend: '+fmt(st.cash)+(openVal?' · in open trades: '+fmt(openVal):''));
 if(hpv){hpv.textContent=fmt(now);hpv.style.fontSize='40px';}
 renderGoal(now);
 renderWeekly(st);
 if(hpc){hpc.textContent=(gr>=0?'▲ +':'▼ ')+fmt(now-st.start)+' ('+(gr>=0?'+':'')+gr.toFixed(1)+'%) all time';hpc.style.color='#fff';}
 document.getElementById('sm-open').innerHTML=st.open.length?
  '<div class="why">Open trades</div>'+st.open.map(function(p){
   return '<div class="pos">'+p.t+' '+p.kind+' ×'+p.qty+' — in for '+fmt(p.cost)+' <span class="hint">('+p.date+', grades after ~10 trading days)</span></div>'}).join(''):'';
 document.getElementById('sm-closed').innerHTML=st.closed.length?
  '<div class="why">Closed trades</div>'+st.closed.map(function(p){
   return '<div class="pos">'+p.t+' '+p.kind+' — '+p.result+' <span style="color:'+(p.pl>=0?'#00b46e':'#ff4d6d')+'">'+(p.pl>=0?'+':'')+p.pl+'%</span> → back '+fmt(p.proceeds)+'</div>'}).join(''):'';
 markTaken(st)}
function markTaken(st){document.querySelectorAll('.take').forEach(function(el){
 var taken=st.open.concat(st.closed).some(function(p){return p.t===el.dataset.t&&p.date===el.dataset.date});
 var btn=el.querySelector('.takebtn');
 if(taken){btn.textContent='Taken ✓';btn.disabled=true}})}
function orderText(p,q){
 if(p.kind==='SPOT')return 'BUY $'+(p.cost*q)+' of '+(p.base||p.t)+' (spot)';
 var right=p.kind==='CASH-SECURED PUT'?'PUT (sell to open)':p.kind.replace('LONG ','');
 return p.action+' '+q+'x '+p.t+' $'+p.strike+' '+right+' exp '+p.exp+' · limit ~$'+p.prem.toFixed(2);
}
function wire(){document.querySelectorAll('.take').forEach(function(el){
 var d=el.dataset;
 var p={t:d.t,cost:+d.cost,prem:+d.prem,spot:+d.spot,kind:d.kind,date:d.date,
        strike:d.strike,exp:d.exp,action:d.action||'BUY',base:d.base||''};
 var qEl=el.querySelector('.tq'),pot=el.querySelector('.pot'),q=1;
 function upd(){if(qEl)qEl.textContent=q;if(pot)pot.innerHTML=scenarioHTML(p,q)}
 upd();
 el.querySelectorAll('.tbtn').forEach(function(b){b.onclick=function(){q=Math.max(1,q+ +b.dataset.d);upd()}});
 var tk=el.querySelector('.takebtn');
 if(tk)tk.onclick=function(){var st=state();
  if(st.start==null){alert('Set your money first — the My Money box is at the top.');return}
  var cost=p.cost*q;
  if(cost>st.cash){alert('Not enough budget: this trade needs '+fmt(cost)+' but you only have '+fmt(st.cash)+' cash free.');return}
  st.cash-=cost;
  st.open.push({t:p.t,kind:p.kind,date:p.date,qty:q,cost:cost,prem:p.prem});
  save(st);render()};
 var bb=el.querySelector('.brokerbtn');
 if(bb)bb.onclick=function(){
  var bk=g('broker');
  if(!bk||!BROKERS[bk]){alert('Pick your broker first — the broker dropdown is in the My Money box at the top.');return}
  var order=orderText(p,q);
  var tgt=(p.kind==='SPOT'&&p.base)?p.base:p.t;
  var go=function(){window.open(BROKERS[bk].url(tgt),'_blank');
   bb.textContent='Order copied ✓ paste at '+BROKERS[bk].name;
   setTimeout(function(){bb.textContent='Open in '+BROKERS[bk].name},4000)};
  if(navigator.clipboard&&navigator.clipboard.writeText)navigator.clipboard.writeText(order).then(go,go);else go()};
 })}
function labelBrokerBtns(){var bk=g('broker');
 document.querySelectorAll('.brokerbtn').forEach(function(b){
  b.textContent=bk&&BROKERS[bk]?('Open in '+BROKERS[bk].name):'Open in broker'})}
var sel=document.getElementById('sm-broker');
if(!g('broker'))s('broker','robinhood');
if(sel){var cur=g('broker');if(cur)sel.value=cur;
 sel.onchange=function(){s('broker',sel.value);labelBrokerBtns()}}
function weekKey(d){var dt=new Date(d+'T00:00:00');var day=(dt.getDay()+6)%7;dt.setDate(dt.getDate()-day);
 return dt.toLocaleDateString(undefined,{month:'short',day:'numeric'});}
function renderWeekly(st){
 var box=document.getElementById('sm-weekly');if(!box)return;
 if(!st.closed.length){box.innerHTML='<div class="why">📈 Weekly progress</div><div class="hint">Take a trade and once it grades (~10 trading days), your week-by-week growth shows here — each week compounds on the last.</div>';return}
 var chron=st.closed.slice().sort(function(a,b){return a.date<b.date?-1:1});
 var weeks={},order=[];
 chron.forEach(function(p){var k=weekKey(p.date);if(!(k in weeks)){weeks[k]={net:0,w:0,l:0};order.push(k);}
  weeks[k].net+=(p.proceeds-p.cost);if(p.pl>=0)weeks[k].w++;else weeks[k].l++;});
 var bal=st.start,rows='';
 order.forEach(function(k){var wk=weeks[k],startB=bal,endB=bal+wk.net,pct=startB?wk.net/startB*100:0;bal=endB;
  var col=wk.net>=0?'#00b46e':'#ff4d6d';
  rows+='<div class="pos" style="display:flex;justify-content:space-between;align-items:center">'+
   '<span>Week of <b>'+k+'</b> <span class="hint">('+wk.w+'W/'+wk.l+'L)</span></span>'+
   '<span style="text-align:right"><b style="color:'+col+'">'+(wk.net>=0?'+':'')+fmt(wk.net)+'</b><br>'+
   '<span class="hint">'+fmt(startB)+' → '+fmt(endB)+' ('+(pct>=0?'+':'')+pct.toFixed(0)+'%)</span></span></div>';});
 var tot=(bal-st.start),totp=st.start?tot/st.start*100:0;
 box.innerHTML='<div class="why">📈 Weekly progress</div>'+rows+
  '<div class="hint" style="margin-top:6px">Since day one: <b style="color:'+(tot>=0?'#00b46e':'#ff4d6d')+'">'+(tot>=0?'+':'')+fmt(tot)+' ('+(totp>=0?'+':'')+totp.toFixed(0)+'%)</b> — this is your money compounding.</div>';
}
function renderGoal(now){
 var box=document.getElementById('sm-goal-out');if(!box)return;
 var goal=parseFloat((document.getElementById('sm-goal')||{}).value);
 if(!(goal>0)){box.innerHTML='<span class="hint">Type a weekly $ goal above to see the honest math.</span>';return}
 var need=goal/now*100; // % of current bankroll needed per week
 var msg,color;
 if(need<=10){msg='Ambitious but doable over time. Steady singles get you here.';color='#00b46e'}
 else if(need<=30){msg='Very aggressive — expect losing weeks. Only risk money you can lose.';color='#f5b84c'}
 else{msg='Not realistic. That would mean roughly +'+Math.round(need)+'% EVERY week, which no system can do reliably. Lower the goal or grow the bankroll first.';color='#ff4d6d'}
 // realistic compounding at +5%/week
 function grow(wk){return now*Math.pow(1.05,wk)}
 box.innerHTML='<div style="font-size:14px;margin-bottom:6px">To make <b>'+fmt(goal)+'/week</b> from <b>'+fmt(now)+'</b>, you\'d need about <b style="color:'+color+'">+'+need.toFixed(0)+'% per week</b>.</div>'+
  '<div style="color:'+color+';font-size:13.5px;margin-bottom:8px">'+msg+'</div>'+
  '<div class="hint">Realistic reference — compounding a steady <b>+5%/week</b> (a good result): '+
  fmt(grow(4))+' in 1 month · '+fmt(grow(26))+' in 6 months · '+fmt(grow(52))+' in 1 year. Small snowballs into big.</div>';
}
var goalInput=document.getElementById('sm-goal');
if(goalInput)goalInput.oninput=function(){renderGoal((state().cash)+(state().open.reduce(function(a,p){return a+p.cost},0)))};
var sb=document.getElementById('sm-start-btn');
if(sb)sb.onclick=function(){var v=parseFloat(document.getElementById('sm-amt').value);
 if(!(v>0)){alert('Enter a starting amount, e.g. 20.');return}
 s('start',v);s('cash',v);s('open',[]);s('closed',[]);render()};
// ---- editable budget ----
var addB=document.getElementById('sm-add');
if(addB)addB.onclick=function(){var v=parseFloat(prompt('How much money do you want to ADD?'));
 if(!(v>0))return;var st=state();s('start',st.start+v);s('cash',st.cash+v);render()};
var remB=document.getElementById('sm-remove');
if(remB)remB.onclick=function(){var v=parseFloat(prompt('How much do you want to TAKE OUT?'));
 if(!(v>0))return;var st=state();
 if(v>st.cash){alert('You can only take out your free cash ('+fmt(st.cash)+'). Some money is tied up in open trades.');return}
 s('start',Math.max(0,st.start-v));s('cash',st.cash-v);render()};
var chgB=document.getElementById('sm-change');
if(chgB)chgB.onclick=function(){var v=parseFloat(prompt('Set a brand-new starting amount. (This clears your practice trades and starts fresh.)'));
 if(!(v>0))return;
 if(confirm('Start fresh with '+fmt(v)+'? This clears your current practice trades.')){s('start',v);s('cash',v);s('open',[]);s('closed',[]);render()}};
var rb=document.getElementById('sm-reset');
if(rb)rb.onclick=function(){if(confirm('Reset everything? This clears your practice money and trade history on this device.')){
 ['start','cash','open','closed'].forEach(del);render()}};
// ---- market (asset) filter ----
var asset=document.getElementById('sm-asset');
function applyFilter(v){document.querySelectorAll('[data-asset]').forEach(function(el){
 el.style.display=(v==='all'||el.dataset.asset===v)?'':'none'})}
if(asset){asset.value=g('asset')||'all';applyFilter(asset.value);
 asset.onchange=function(){s('asset',asset.value);applyFilter(asset.value)}}
// ---- level (beginner / experienced) tabs ----
function applyMode(m){document.querySelectorAll('[data-mode]').forEach(function(el){
  el.style.display=el.dataset.mode===m?'':'none'});
 document.querySelectorAll('.modebtn').forEach(function(b){
  b.classList.toggle('active',b.dataset.mode===m)})}
var modeBtns=document.querySelectorAll('.modebtn');
if(modeBtns.length){var cm=g('mode')||'beginner';applyMode(cm);
 modeBtns.forEach(function(b){b.onclick=function(){s('mode',b.dataset.mode);applyMode(b.dataset.mode)}})}
wire();labelBrokerBtns();render();
})();
