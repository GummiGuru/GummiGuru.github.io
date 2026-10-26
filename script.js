const g=document.getElementById('gallery'),empty=document.getElementById('empty'),lb=document.getElementById('lightbox'),lbImg=lb.querySelector('img'),lbCap=lb.querySelector('figcaption');
let items=[],shown=[],idx=0,cat='All';document.getElementById('yr').textContent=new Date().getFullYear();
function render(){shown=cat==='All'?items:items.filter(i=>i.category===cat);g.innerHTML='';empty.hidden=shown.length>0;
shown.forEach((it,i)=>{const d=document.createElement('div');d.className='item';d.innerHTML=`<img loading="lazy" src="images/${encodeURI(it.file)}" alt=""><div class="cap"></div>`;d.querySelector('img').alt=it.title||'';d.querySelector('.cap').textContent=it.title||'';d.onclick=()=>open(i);g.appendChild(d)})}
function open(i){idx=(i+shown.length)%shown.length;const it=shown[idx];lbImg.src='images/'+encodeURI(it.file);lbImg.alt=it.title||'';lbCap.textContent=(it.title||'')+(it.category?' · '+it.category:'');lb.hidden=false}
lb.querySelector('.close').onclick=()=>lb.hidden=true;lb.querySelector('.prev').onclick=e=>{e.stopPropagation();open(idx-1)};lb.querySelector('.next').onclick=e=>{e.stopPropagation();open(idx+1)};
lb.onclick=e=>{if(e.target===lb)lb.hidden=true};document.onkeydown=e=>{if(lb.hidden)return;if(e.key==='Escape')lb.hidden=true;if(e.key==='ArrowLeft')open(idx-1);if(e.key==='ArrowRight')open(idx+1)};
document.querySelectorAll('#filters button').forEach(b=>b.onclick=()=>{document.querySelectorAll('#filters button').forEach(x=>x.classList.remove('active'));b.classList.add('active');cat=b.dataset.cat;render()});
fetch('gallery.json',{cache:'no-store'}).then(r=>r.json()).then(d=>{items=Array.isArray(d)?d:[];render()}).catch(()=>render());
