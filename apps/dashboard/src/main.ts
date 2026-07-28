import "./style.css";

const API = "http://localhost:8000";
const QUEUE_KEY = "farmassist-approved-queue";
type Observation = {
  observation_id:string; timestamp_utc:string; site_code:string; temperature_c:number;
  relative_humidity_pct:number; soil_moisture_pct:number; crop_stage:string;
  observation_source:"synthetic"; consent_status:"not_required_synthetic";
  synchronization_status:"queued"|"synchronized"; notes:string;
};
const demo: Observation = {
  observation_id: crypto.randomUUID(), timestamp_utc:new Date().toISOString(), site_code:"DEMO-001",
  temperature_c:39, relative_humidity_pct:82, soil_moisture_pct:16, crop_stage:"vegetative",
  observation_source:"synthetic", consent_status:"not_required_synthetic",
  synchronization_status:"queued", notes:"Synthetic demonstration record"
};
const queue = ():Observation[] => JSON.parse(localStorage.getItem(QUEUE_KEY) || "[]");
const save = (items:Observation[]) => localStorage.setItem(QUEUE_KEY, JSON.stringify(items));
const app = document.querySelector<HTMLDivElement>("#app")!;
app.innerHTML = `<header><p>JOITA BIOSEED AI PRIVATE LIMITED · Early reference implementation</p>
<h1>FarmAssist Climate Intelligence</h1><p>Local, explainable environmental monitoring for supervised research and proposed pilots.</p>
<div class="status"><span class="pill" id="network" role="status"></span><span class="pill">Pending sync: <b id="count">0</b></span><span class="pill">Synthetic demo mode</span></div></header>
<main id="main"><div class="notice"><b>Responsible-use notice:</b> Not a medical device, emergency-warning system, or substitute for qualified agronomic, safeguarding, nutrition, or public-health advice.</div>
<section><h2>Site overview</h2><div class="grid">
<article class="card"><small>Site</small><div class="metric">DEMO-001</div><span>Non-identifying code</span></article>
<article class="card"><small>Temperature</small><div class="metric">39°C</div><span>Synthetic latest reading</span></article>
<article class="card"><small>Humidity</small><div class="metric">82%</div><span>Synthetic latest reading</span></article>
<article class="card"><small>Soil moisture</small><div class="metric">16%</div><span>Synthetic latest reading</span></article></div></section>
<section><h2>Explainable risk</h2><div class="grid">
<article class="card risk-high"><h3>Heat stress · High</h3><p>39°C is at or above the 38°C reference threshold.</p></article>
<article class="card risk-high"><h3>Water stress · High</h3><p>16% is at or below the 18% soil-moisture reference threshold.</p></article>
<article class="card risk-moderate"><h3>Humidity disease · Moderate</h3><p>82% is above the 75% reference threshold.</p></article></div>
<p>Next checks: confirm sensor placement, inspect root-zone moisture, and seek qualified agronomic review. Thresholds require local validation.</p></section>
<section class="card"><h2>Queue a synthetic observation</h2><form id="form">
<label>Site code<input value="DEMO-001" disabled></label><label>Temperature °C<input id="temperature" type="number" value="39" min="-30" max="65" required></label>
<label>Humidity %<input id="humidity" type="number" value="82" min="0" max="100" required></label><label>Soil moisture %<input id="moisture" type="number" value="16" min="0" max="100" required></label>
<label>Crop stage<select id="stage"><option>vegetative</option><option>flowering</option><option>harvest</option></select></label><label>Approved for sync<button>Save locally</button></label></form>
<button id="sync" type="button">Synchronize approved queue</button><h3>Queued observations</h3><div id="queue"></div></section>
<div class="grid"><aside class="notice"><b>Privacy:</b> Do not enter names, contacts, health records, addresses, coordinates, or other personal data.</aside><aside class="notice"><b>Safeguarding:</b> Any real pilot requires consent, institutional approval, restricted access, retention rules, and incident procedures.</aside></div></main>`;

function render():void {
  const items=queue(); document.querySelector("#count")!.textContent=String(items.length);
  document.querySelector("#network")!.textContent=navigator.onLine?"Online":"Offline · saving locally";
  document.querySelector("#queue")!.innerHTML=items.length?`<table><thead><tr><th>ID</th><th>Time</th><th>Temperature</th><th>Status</th></tr></thead><tbody>${items.map(x=>`<tr><td>${x.observation_id.slice(0,8)}</td><td>${new Date(x.timestamp_utc).toLocaleString()}</td><td>${x.temperature_c}°C</td><td>Approved, queued</td></tr>`).join("")}</tbody></table>`:"<p>Queue is empty.</p>";
}
document.querySelector("#form")!.addEventListener("submit", event => {
  event.preventDefault(); const item={...demo, observation_id:crypto.randomUUID(),timestamp_utc:new Date().toISOString(),
    temperature_c:Number((document.querySelector("#temperature") as HTMLInputElement).value),
    relative_humidity_pct:Number((document.querySelector("#humidity") as HTMLInputElement).value),
    soil_moisture_pct:Number((document.querySelector("#moisture") as HTMLInputElement).value),
    crop_stage:(document.querySelector("#stage") as HTMLSelectElement).value};
  const items=queue(); if(!items.some(x=>x.observation_id===item.observation_id))items.push(item); save(items); render();
});
document.querySelector("#sync")!.addEventListener("click", async()=> {
  if(!navigator.onLine)return;
  const remaining:Observation[]=[];
  for(const item of queue()){try{const response=await fetch(`${API}/v1/observations`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({...item,synchronization_status:"synchronized"})});if(!response.ok&&response.status!==409)remaining.push(item);}catch{remaining.push(item);}}
  save(remaining);render();
});
window.addEventListener("online",render);window.addEventListener("offline",render);render();
if("serviceWorker" in navigator)navigator.serviceWorker.register("/sw.js");
