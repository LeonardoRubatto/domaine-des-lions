(() => {
  'use strict';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)');
  const mobile = matchMedia('(max-width: 768px)');
  const fr = document.documentElement.lang === 'fr';
  const t = (a,b) => fr ? a : b;
  const ease = 'cubic-bezier(0.2,0,0,1)';
  const running = new Set();
  function animate(element, frames, duration=400, delay=0) {
    if (reduced.matches) return Promise.resolve();
    const motion = element.animate(frames,{duration,delay,easing:ease,fill:'backwards'});
    running.add(motion);
    return motion.finished.catch(()=>{}).finally(()=>running.delete(motion));
  }
  reduced.addEventListener('change',()=>{ if(reduced.matches) running.forEach(m=>m.finish()); });

  // Progressive Blur: six masked backdrop layers, only at the lower edge of
  // large photographic frames. Images and their captions remain separate.
  document.querySelectorAll('.hero-photo, .album-image-wrap').forEach(photo=>{
    let host=photo;
    if(photo.matches('.hero-photo')) {
      host=document.createElement('div');host.className='hero-window';
      photo.before(host);host.append(photo);
    }
    const blur=document.createElement('div');blur.className='photo-edge-blur';
    blur.setAttribute('aria-hidden','true');
    const layers=6, segment=1/(layers+1);
    for(let i=0;i<layers;i++) {
      const layer=document.createElement('span');
      const stops=[i,i+1,i+2,i+3].map((n,j)=>`rgba(255,255,255,${j===1||j===2?1:0}) ${n*segment*100}%`);
      const mask=`linear-gradient(180deg,${stops.join(',')})`;
      layer.style.maskImage=mask;layer.style.webkitMaskImage=mask;
      layer.style.backdropFilter=`blur(${i*1.2}px)`;
      layer.style.webkitBackdropFilter=`blur(${i*1.2}px)`;
      blur.append(layer);
    }
    host.append(blur);
  });

  // Text Effect, word-level slide preset. Preserve line breaks and the full
  // accessible text. House, pool, tennis and guest chapters use a soft blur;
  // practical copy, controls, captions and footer headings remain unsplit.
  const headings=[...document.querySelectorAll('.hero-title h1, .gallery-title h1, .tour-hub-heading h2, .intro-title h2, .chapter-copy h2, .review-heading h2')];
  const softHeadings = new Set(headings.filter(h=>h.matches('.intro-title h2, .chapter-copy h2, .review-heading h2')));
  headings.forEach(heading=>{
    const plain=document.createElement('span');plain.className='sr-only';
    plain.textContent=heading.innerText;
    const visual=document.createElement('span');visual.setAttribute('aria-hidden','true');
    visual.innerHTML=heading.innerHTML;
    const walker=document.createTreeWalker(visual,NodeFilter.SHOW_TEXT);
    const nodes=[];while(walker.nextNode()) nodes.push(walker.currentNode);
    nodes.forEach(node=>{
      const fragment=document.createDocumentFragment();
      node.textContent.split(/(\s+)/).forEach(word=>{
        if(!word.trim()){fragment.append(document.createTextNode(word));return;}
        const span=document.createElement('span');span.className='text-segment';span.textContent=word;fragment.append(span);
      });node.replaceWith(fragment);
    });
    heading.replaceChildren(plain,visual);
    if(softHeadings.has(heading) && !reduced.matches && heading.getBoundingClientRect().top>=innerHeight) heading.classList.add('text-await');
  });
  const entrances=new IntersectionObserver(entries=>{
    entries.forEach(entry=>{
      if(!entry.isIntersecting) return;
      entrances.unobserve(entry.target);
      const target=entry.target;
      if(target.closest('[data-section-motion]')?.matches(':focus-within')) {
        target.classList.remove('image-await','text-await');
        return;
      }
      if(headings.includes(target)) {
        target.classList.remove('text-await');
        const soft=softHeadings.has(target);
        const from=soft ? {opacity:0,filter:'blur(4px)',transform:'translateY(12px)'} : {opacity:0,transform:'translateY(20px)'};
        const to=soft ? {opacity:1,filter:'blur(0px)',transform:'translateY(0px)'} : {opacity:1,transform:'translateY(0px)'};
        target.querySelectorAll('.text-segment').forEach((word,i)=>animate(word,[from,to],400,Math.min(i*50,soft?200:300)));
        return;
      }
      // Aperture enters once; it never moves the actual layout or repeats on
      // reverse scrolling. Skip interactive 3D and geometric tilt wrappers.
      if(target.matches('picture, .hero-window')) {
        animate(target,[{opacity:0,clipPath:'inset(8% 0 8% 0)'},{opacity:1,clipPath:'inset(0% 0 0% 0)'}],800)
          .finally(()=>target.classList.remove('image-await'));
      } else {
        animate(target,[{opacity:.4,transform:'translateY(24px)'},{opacity:1,transform:'translateY(0px)'}],800);
      }
    });
  },{threshold:.12});
  document.querySelectorAll('.hero-window, .information-chapter > picture, .gallery-item picture, .art-section > picture, .location-section > picture').forEach(el=>{
    const rect=el.getBoundingClientRect();
    // Do not reset a photo that has already been painted in the opening view.
    // Offscreen frames get their starting state before scrolling reaches them.
    if(reduced.matches || (rect.top<innerHeight && rect.bottom>0)) return;
    el.classList.add('image-await');entrances.observe(el);
  });
  reduced.addEventListener('change',()=>{
    if(reduced.matches) document.querySelectorAll('.image-await,.text-await,.section-await').forEach(el=>el.classList.remove('image-await','text-await','section-await'));
  });
  headings.forEach(el=>entrances.observe(el));

  // A shared, shallow slide/fade at genuine chapter boundaries. Prepare only
  // offscreen sections: never reset an already-painted opening or photograph.
  // Long house chapters animate separately; individual gallery figures do not.
  const sectionEntrances = new IntersectionObserver(entries=>{
    entries.forEach(entry=>{
      if(!entry.isIntersecting) return;
      const section=entry.target;
      sectionEntrances.unobserve(section);
      section.classList.remove('section-await');
      section.dataset.sectionMotion='ready';
      if(section.matches(':focus-within')) return;
      animate(section,[{opacity:.92,transform:'translateY(16px)'},{opacity:1,transform:'translateY(0px)'}],800);
    });
  },{threshold:0,rootMargin:'0px 0px -24px 0px'});
  document.querySelectorAll('main > section, .information-chapter').forEach(section=>{
    if(section.matches('.hero,.gallery-intro,.booking-intro') || section.querySelector('.information-chapter')) return;
    const rect=section.getBoundingClientRect();
    if(reduced.matches || rect.top<innerHeight) return;
    section.classList.add('section-await');
    section.dataset.sectionMotion='waiting';
    sectionEntrances.observe(section);
    section.addEventListener('focusin',()=>{
      sectionEntrances.unobserve(section);
      section.classList.remove('section-await');
      section.querySelectorAll('.image-await,.text-await').forEach(el=>{
        entrances.unobserve(el);
        el.classList.remove('image-await','text-await');
      });
      headings.filter(h=>section.contains(h)).forEach(h=>entrances.unobserve(h));
      section.getAnimations({subtree:true}).forEach(m=>m.finish());
      section.dataset.sectionMotion='ready';
    });
  });

  // Scroll Tilted Grid: preserve the source travel, signed-distance and
  // smoothstep calculations. Moderate geometry; no blur, colour shift or Lenis.
  const frames = [...document.querySelectorAll('[data-tilt-frame]')];
  const visibleFrames = new Set();
  let raf = 0;
  function paintFrames() {
    raf = 0;
    frames.forEach((frame,index)=>{
      const picture = frame.querySelector('picture');
      if (!picture) return;
      if(reduced.matches || mobile.matches || frame.matches(':focus-within')) {
        picture.style.transform = '';
        return;
      }
      if(!visibleFrames.has(frame)) return;
      const rect = frame.getBoundingClientRect();
      const position = Math.max(0,Math.min(1,(innerHeight-rect.top)/(innerHeight+rect.height)));
      const distance = Math.abs(position-.5)*2;
      const signed = (position-.5)*2;
      const eased = distance*distance*(3-2*distance);
      const side = index%2===0 ? -1 : 1;
      picture.style.transform = `translate3d(${side*eased*6}%,${-signed*eased*8}%,${eased*60}px) rotateX(${-signed*16}deg) rotateZ(${side*signed}deg) skewX(${-side*signed*2}deg)`;
    });
  }
  function scheduleFrames() { if(!raf) raf=requestAnimationFrame(paintFrames); }
  if(frames.length) {
    const observer = new IntersectionObserver(entries=>{
      entries.forEach(e=>e.isIntersecting?visibleFrames.add(e.target):visibleFrames.delete(e.target));
      scheduleFrames();
    },{rootMargin:'120px'});
    frames.forEach(frame=>{observer.observe(frame);frame.addEventListener('focusin',scheduleFrames);frame.addEventListener('focusout',scheduleFrames);});
    addEventListener('scroll',scheduleFrames,{passive:true});
    addEventListener('resize',scheduleFrames);
    mobile.addEventListener('change',scheduleFrames);
    reduced.addEventListener('change',scheduleFrames);
  }

  // Shapes Slideshow: circular mask + opposing wrapper/image translations,
  // adapted from the library's named variant to native WAAPI and shorter timing.
  const album = document.querySelector('.album');
  if(album) {
    const slides = [...album.querySelectorAll('[data-album-slide]')];
    const titles = JSON.parse(album.dataset.albumTitles);
    let current = 0;
    let busy = false;
    const toggle=album.querySelector('[data-album-rotation]');
    const count=album.querySelector('[data-album-count]');
    let paused=reduced.matches, inView=false, hovering=false, timer;
    function updateControl() {
      toggle.textContent=paused?t('Relancer le diaporama','Start slideshow'):t('Mettre en pause','Pause slideshow');
      count.setAttribute('aria-live',paused?'polite':'off');
    }
    function schedule() {
      clearTimeout(timer);
      if(paused||reduced.matches||!inView||hovering||document.hidden||busy) return;
      timer=setTimeout(()=>show(current+1,false),8000);
    }
    async function show(index,manual=true) {
      if(manual){paused=true;updateControl();}
      clearTimeout(timer);
      index = (index+slides.length)%slides.length;
      if(busy || index===current) return;
      busy = true;
      const outgoing = slides[current];
      const incoming = slides[index];
      // Keep the outgoing photograph in place until the next bitmap is ready.
      const incomingImage=incoming.querySelector('img');
      incomingImage.loading='eager';
      await incomingImage.decode().catch(()=>{});
      const direction = manual?(index>current?1:-1):1;
      current = index;
      incoming.classList.add('is-current');
      incoming.style.zIndex = '2';
      incoming.setAttribute('aria-hidden','false');
      outgoing.setAttribute('aria-hidden','true');
      album.querySelector('[data-album-title]').textContent = titles[index];
      album.querySelector('[data-album-count]').textContent = `${index+1} / ${slides.length}`;
      album.querySelectorAll('[data-album-index]').forEach((b,i)=>b.setAttribute('aria-pressed',String(i===index)));
      await Promise.all([
        animate(outgoing.querySelector('.album-image-wrap'),[
          {clipPath:'circle(100% at 70% 50%)',transform:'translateY(0%)',offset:0},
          {clipPath:'circle(15% at 70% 50%)',transform:'translateY(0%)',offset:.35},
          {clipPath:'circle(15% at 70% 50%)',transform:`translateY(${-direction*100}%)`,offset:1}
        ],800),
        animate(incoming.querySelector('.album-image-wrap'),[
          {clipPath:'circle(15% at 70% 50%)',transform:`translateY(${direction*100}%)`,offset:0},
          {clipPath:'circle(15% at 70% 50%)',transform:'translateY(0%)',offset:.55},
          {clipPath:'circle(100% at 70% 50%)',transform:'translateY(0%)',offset:1}
        ],800),
        animate(incoming.querySelector('img'),[{transform:`translateY(${-direction*50}%) scale(1.08)`},{transform:'translateY(0%) scale(1)'}],800)
      ]);
      outgoing.classList.remove('is-current');
      incoming.style.zIndex = '';
      busy = false;
      schedule();
    }
    album.querySelectorAll('[data-album-step]').forEach(b=>b.addEventListener('click',()=>show(current+Number(b.dataset.albumStep))));
    album.querySelectorAll('[data-album-index]').forEach(b=>b.addEventListener('click',()=>show(Number(b.dataset.albumIndex))));
    album.querySelector('.album-stage').addEventListener('keydown',e=>{
      if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();show(current+(e.key==='ArrowRight'?1:-1));}
    });
    toggle.addEventListener('click',()=>{paused=!paused;updateControl();schedule();});
    album.addEventListener('focusin',e=>{if(e.target!==toggle){paused=true;updateControl();schedule();}});
    album.addEventListener('mouseenter',()=>{hovering=true;schedule();});
    album.addEventListener('mouseleave',()=>{hovering=false;schedule();});
    document.addEventListener('visibilitychange',schedule);
    reduced.addEventListener('change',()=>{if(reduced.matches) paused=true;updateControl();schedule();});
    new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;schedule();},{threshold:.3}).observe(album.querySelector('.album-stage'));
    updateControl();
  }

  // One automatic reading gallery; pause always available. Focusing a control
  // stops rotation until the visitor explicitly chooses to resume.
  const track = document.querySelector('.review-track');
  if(track) {
    const reviews = [...track.querySelectorAll('.review')];
    const region = document.querySelector('.review-stage');
    const toggle = document.querySelector('[data-review-rotation]');
    let index = 0;
    let paused = reduced.matches;
    let inView = false;
    let hovering = false;
    let timer;
    track.dataset.reviewReady = 'true';
    function updateControl() { toggle.textContent = paused ? t('Relancer le défilement','Start slideshow') : t('Mettre en pause','Pause slideshow'); }
    function schedule() {
      clearTimeout(timer);
      if(paused || reduced.matches || !inView || hovering || document.hidden) return;
      const words = reviews[index].querySelector('blockquote').textContent.trim().split(/\s+/).length;
      const interval = Math.min(60000,Math.max(9000,words*350+4000));
      region.dataset.reviewInterval = String(interval);
      timer = setTimeout(()=>show(index+1,false),interval);
    }
    function show(next,manual=true) {
      index=(next+reviews.length)%reviews.length;
      reviews.forEach((review,i)=>{
        review.hidden=i!==index;
        review.setAttribute('role','group');
        review.setAttribute('aria-roledescription',t('diapositive','slide'));
        review.setAttribute('aria-label',t(`Avis ${i+1} sur ${reviews.length}`,`Review ${i+1} of ${reviews.length}`));
      });
      document.querySelector('.review-position').textContent=t(`Avis ${index+1} / ${reviews.length}`,`Review ${index+1} / ${reviews.length}`);
      track.setAttribute('aria-live',paused?'polite':'off');
      if(manual) {paused=true;updateControl();}
      animate(reviews[index],[{opacity:0,transform:'translateY(12px)'},{opacity:1,transform:'translateY(0px)'}]);
      schedule();
    }
    document.querySelectorAll('[data-review-step]').forEach(b=>b.addEventListener('click',()=>show(index+Number(b.dataset.reviewStep))));
    track.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();show(index+(e.key==='ArrowRight'?1:-1));}});
    toggle.addEventListener('click',()=>{paused=!paused;updateControl();track.setAttribute('aria-live',paused?'polite':'off');schedule();});
    region.addEventListener('focusin',e=>{if(e.target!==toggle){paused=true;updateControl();schedule();}});
    region.addEventListener('mouseenter',()=>{hovering=true;schedule();});
    region.addEventListener('mouseleave',()=>{hovering=false;schedule();});
    document.addEventListener('visibilitychange',schedule);
    reduced.addEventListener('change',()=>{if(reduced.matches) paused=true;updateControl();schedule();});
    new IntersectionObserver(entries=>{inView=entries[0].isIntersecting;schedule();},{threshold:.35}).observe(region);
    show(0,false);
    updateControl();
  }

  const stage = document.querySelector('.tour-stage');
  if(stage) {
    const exit=document.createElement('button');
    exit.type='button';exit.className='tour-fullscreen-exit';
    exit.textContent=t('Réduire la visite','Exit full screen');
    stage.append(exit);
    exit.addEventListener('click',()=>{
      if(document.fullscreenElement) document.exitFullscreen().then(()=>expand.focus()).catch(()=>{});
    });
    const frameHost = stage.querySelector('.tour-inline-frame');
    const cover = stage.querySelector('.tour-cover');
    const start = stage.querySelector('[data-tour-start]');
    const stop = document.querySelector('[data-tour-stop]');
    const expand = document.querySelector('[data-tour-expand]');
    const choices = [...document.querySelectorAll('[data-tour-scene]')];
    const status = document.querySelector('.tour-status');
    function load(scene='pano6821') {
      if(!['pano6821',...choices.map(b=>b.dataset.tourScene)].includes(scene)) scene='pano6821';
      const existing = frameHost.querySelector('iframe');
      if(existing?.dataset.scene===scene) return;
      const frame = document.createElement('iframe');
      frame.title = t('Visite à 360° du Domaine aux Lions','Le Domaine aux Lions 360° tour');
      frame.src = `${stage.dataset.tourUrl}?s=${encodeURIComponent(scene)}`;
      frame.dataset.scene = scene;
      frame.allowFullscreen = true;
      frame.referrerPolicy = 'strict-origin-when-cross-origin';
      frameHost.replaceChildren(frame);
      cover.hidden = true;
      stage.classList.add('is-active');
      stop.hidden=false;expand.hidden=false;
      choices.forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.tourScene===scene)));
      const choice=choices.find(b=>b.dataset.tourScene===scene);
      status.textContent=choice?.querySelector('span').textContent || t('Bienvenue au domaine','Welcome to the estate');
    }
    start.addEventListener('click',()=>load());
    choices.forEach(b=>b.addEventListener('click',()=>load(b.dataset.tourScene)));
    stop.addEventListener('click',()=>{
      frameHost.replaceChildren();cover.hidden=false;stage.classList.remove('is-active');
      stop.hidden=true;expand.hidden=true;choices.forEach(b=>b.setAttribute('aria-pressed','false'));
      status.textContent=t('Maison & jardin · 360°','House & garden · 360°');start.focus();
    });
    expand.addEventListener('click',()=>{
      if(stage.requestFullscreen) stage.requestFullscreen().catch(()=>{status.textContent=t('Utilisez « Ouvrir à part » pour une grande vue.','Use “Open separately” for a larger view.');});
    });
    const initial = new URLSearchParams(location.search).get('scene');
    if(initial) load(initial);
  }
})();
