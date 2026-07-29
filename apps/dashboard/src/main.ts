import "./style.css";

const API = "http://localhost:8000";
const QUEUE_KEY = "farmassist-approved-queue";
const PUBLIC_DEMO = import.meta.env.VITE_PUBLIC_DEMO === "1";
const DEMO_CONTROLS = PUBLIC_DEMO || location.search.includes("demo-controls");
type Level = "low" | "moderate" | "high";
type Observation = {
  observation_id:string; timestamp_utc:string; site_code:string; temperature_c:number;
  relative_humidity_pct:number; soil_moisture_pct:number; crop_stage:string;
  observation_source:"synthetic"; consent_status:"not_required_synthetic";
  synchronization_status:"queued"|"synchronized"; notes:string;
};
type Assessment = {
  heat:Level; water:Level; humidity:Level; combined:Level; score:number; reasons:string[];
};

const demo: Observation = {
  observation_id: crypto.randomUUID(), timestamp_utc:new Date().toISOString(), site_code:"DEMO-001",
  temperature_c:39, relative_humidity_pct:82, soil_moisture_pct:16, crop_stage:"vegetative",
  observation_source:"synthetic", consent_status:"not_required_synthetic",
  synchronization_status:"queued", notes:"Synthetic demonstration record"
};
const points:Record<Level,number> = {low:0, moderate:50, high:100};
const queue = ():Observation[] => JSON.parse(localStorage.getItem(QUEUE_KEY) || "[]");
const save = (items:Observation[]) => localStorage.setItem(QUEUE_KEY, JSON.stringify(items));
const level = (value:number, moderate:number, high:number, reverse=false):Level =>
  reverse ? (value <= high ? "high" : value <= moderate ? "moderate" : "low")
    : (value >= high ? "high" : value >= moderate ? "moderate" : "low");
const assess = (item:Observation):Assessment => {
  const heat=level(item.temperature_c,32,38);
  const water=level(item.soil_moisture_pct,30,18,true);
  const humidity=level(item.relative_humidity_pct,75,88);
  const score=Math.round(points[heat]*.4+points[water]*.4+points[humidity]*.2);
  return {
    heat, water, humidity, score,
    combined:score >= 70 ? "high" : score >= 35 ? "moderate" : "low",
    reasons:[
      `${item.temperature_c.toFixed(1)}°C gives ${heat} heat stress risk.`,
      `${item.soil_moisture_pct.toFixed(1)}% soil moisture gives ${water} water stress risk.`,
      `${item.relative_humidity_pct.toFixed(1)}% humidity gives ${humidity} disease risk.`
    ]
  };
};

let active={...demo};
let forcedOffline=false;
const connected=():boolean => navigator.onLine && !forcedOffline;
const app = document.querySelector<HTMLDivElement>("#app")!;
app.innerHTML = `<header><p>JOITA BIOSEED AI PRIVATE LIMITED · Early reference implementation</p>
<h1>FarmAssist Climate Intelligence</h1><p>Local, explainable environmental monitoring for supervised research and proposed pilots.</p>
<div class="status"><span class="pill" id="network" role="status"></span><span class="pill">Pending sync: <b id="count">0</b></span><span class="pill">Synthetic demo mode</span>${DEMO_CONTROLS ? `<button class="connection-toggle" id="connection-toggle" type="button">Simulate offline</button>` : ""}</div></header>
<main id="main"><div class="notice"><b>Responsible-use notice:</b> Not a medical device, emergency-warning system, or substitute for qualified agronomic, safeguarding, nutrition, or public-health advice.</div>
<section><div class="section-title"><div><small>NON-IDENTIFYING DEMONSTRATION SITE</small><h2>Site overview</h2></div><span class="score" id="combined"></span></div><div class="grid">
<article class="card"><small>Site</small><div class="metric">DEMO-001</div><span>Non-identifying code</span></article>
<article class="card"><small>Temperature</small><div class="metric" id="reading-temperature">39°C</div><span>Synthetic latest reading</span></article>
<article class="card"><small>Humidity</small><div class="metric" id="reading-humidity">82%</div><span>Synthetic latest reading</span></article>
<article class="card"><small>Soil moisture</small><div class="metric" id="reading-moisture">16%</div><span>Synthetic latest reading</span></article></div></section>
<section><h2>Explainable reference risk</h2><div class="grid" id="risks"></div>
<p>Next checks: confirm sensor placement, inspect root-zone moisture, and seek qualified agronomic review. Thresholds require local validation.</p></section>
<section class="card"><h2>Queue a synthetic observation</h2><p class="boundary">This demonstration accepts environmental values only. Do not enter personal or child data.</p><form id="form">
<label>Site code<input value="DEMO-001" disabled></label><label>Temperature °C<input id="temperature" type="number" value="39" min="-30" max="65" required></label>
<label>Humidity %<input id="humidity" type="number" value="82" min="0" max="100" required></label><label>Soil moisture %<input id="moisture" type="number" value="16" min="0" max="100" required></label>
<label>Crop stage<select id="stage"><option>vegetative</option><option>flowering</option><option>harvest</option></select></label><label>Approved synthetic record<button>Assess and save locally</button></label></form>
<button id="sync" type="button">Synchronize approved queue</button><p id="sync-message" class="sync-message" role="status" aria-live="polite"></p><h3>Queued observations</h3><div id="queue"></div></section>
<div class="grid"><aside class="notice"><b>Privacy:</b> Do not enter names, contacts, health records, addresses, coordinates, or other personal data.</aside><aside class="notice"><b>Safeguarding:</b> Any real pilot requires consent, institutional approval, restricted access, retention rules, and incident procedures.</aside></div>
${PUBLIC_DEMO ? `<p class="public-demo-note"><b>Public demonstration boundary:</b> synchronization is simulated in this browser and transmits no record to a server. Run the repository locally to verify the FastAPI synchronization endpoint.</p>` : ""}</main>`;

function renderAssessment(item:Observation):void {
  const result=assess(item);
  document.querySelector("#combined")!.textContent=`${result.combined.toUpperCase()} · ${result.score}/100`;
  document.querySelector("#reading-temperature")!.textContent=`${item.temperature_c}°C`;
  document.querySelector("#reading-humidity")!.textContent=`${item.relative_humidity_pct}%`;
  document.querySelector("#reading-moisture")!.textContent=`${item.soil_moisture_pct}%`;
  const risks:[string,Level,string][]=[
    ["Heat stress",result.heat,result.reasons[0]],
    ["Water stress",result.water,result.reasons[1]],
    ["Humidity disease",result.humidity,result.reasons[2]]
  ];
  document.querySelector("#risks")!.innerHTML=risks.map(([name,risk,reason]) =>
    `<article class="card risk-${risk}"><h3>${name} · ${risk[0].toUpperCase()+risk.slice(1)}</h3><p>${reason}</p></article>`
  ).join("");
}
function render():void {
  const items=queue();
  document.querySelector("#count")!.textContent=String(items.length);
  document.querySelector("#network")!.textContent=connected()?"Online":"Offline · saving locally";
  if(DEMO_CONTROLS)document.querySelector("#connection-toggle")!.textContent=forcedOffline?"Restore connection":"Simulate offline";
  document.querySelector("#queue")!.innerHTML=items.length?`<table><thead><tr><th>ID</th><th>Time</th><th>Temperature</th><th>Status</th></tr></thead><tbody>${items.map(x=>`<tr><td>${x.observation_id.slice(0,8)}</td><td>${new Date(x.timestamp_utc).toLocaleString()}</td><td>${x.temperature_c}°C</td><td>Approved, queued</td></tr>`).join("")}</tbody></table>`:"<p>Queue is empty.</p>";
  renderAssessment(active);
}
document.querySelector("#form")!.addEventListener("submit", event => {
  event.preventDefault();
  active={...demo, observation_id:crypto.randomUUID(),timestamp_utc:new Date().toISOString(),
    temperature_c:Number((document.querySelector("#temperature") as HTMLInputElement).value),
    relative_humidity_pct:Number((document.querySelector("#humidity") as HTMLInputElement).value),
    soil_moisture_pct:Number((document.querySelector("#moisture") as HTMLInputElement).value),
    crop_stage:(document.querySelector("#stage") as HTMLSelectElement).value};
  const items=queue();
  items.push(active);
  save(items);
  document.querySelector("#sync-message")!.textContent="Assessed locally and added to the approved queue.";
  render();
});
document.querySelector("#sync")!.addEventListener("click", async()=> {
  const message=document.querySelector("#sync-message")!;
  if(!connected()){message.textContent="Still offline. Approved records remain safely queued on this device.";return;}
  if(PUBLIC_DEMO){
    message.textContent="Simulating aggregate-safe synchronization…";
    await new Promise(resolve=>setTimeout(resolve,700));
    save([]);
    message.textContent="Synthetic demonstration sync complete. No data were transmitted.";
    render();
    return;
  }
  const remaining:Observation[]=[];
  for(const item of queue()){
    try{
      const response=await fetch(`${API}/v1/observations`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({...item,synchronization_status:"synchronized"})});
      if(!response.ok&&response.status!==409)remaining.push(item);
    }catch{remaining.push(item);}
  }
  save(remaining);
  message.textContent=remaining.length?"Some approved records remain queued.":"Synchronization complete.";
  render();
});
if(DEMO_CONTROLS)document.querySelector("#connection-toggle")!.addEventListener("click",()=>{
  forcedOffline=!forcedOffline;
  document.querySelector("#sync-message")!.textContent=forcedOffline
    ?"Offline demonstration enabled. New approved records will remain on this device."
    :"Connection restored. The approved queue is ready to synchronize.";
  render();
});
window.addEventListener("online",render);
window.addEventListener("offline",render);
render();
if("serviceWorker" in navigator)navigator.serviceWorker.register(`${import.meta.env.BASE_URL}sw.js`);
