(() => {
  'use strict';
  const lang = document.body.dataset.language;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const t = (fr, en) => lang === 'fr' ? fr : en;
  let opener = null;
  const closeDialog = (dialog) => {
    if (!dialog) return;
    if (dialog.id === 'lightbox') closePhoto();
    else dialog.close();
  };
  document.querySelectorAll('[data-open]').forEach(trigger => {
    trigger.addEventListener('click', () => {
      const dialog = document.getElementById(trigger.dataset.open);
      opener = trigger;
      if (dialog.id === 'tour') {
        const container = dialog.querySelector('.tour-frame');
        if (!container.querySelector('iframe')) {
          const frame = document.createElement('iframe');
          frame.src = container.dataset.tourUrl;
          frame.title = t('Visite 3D du Domaine aux Lions', 'Le Domaine aux Lions 3D tour');
          frame.allowFullscreen = true;
          frame.referrerPolicy = 'strict-origin-when-cross-origin';
          container.appendChild(frame);
        }
      }
      dialog.showModal();
      document.body.classList.add('modal-open');
      dialog.querySelector('[data-close]')?.focus();
    });
  });
  document.querySelectorAll('dialog').forEach(dialog => {
    dialog.querySelectorAll('[data-close]').forEach(button => button.addEventListener('click', () => closeDialog(dialog)));
    dialog.addEventListener('click', event => {
      const rect = dialog.getBoundingClientRect();
      if (event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) closeDialog(dialog);
    });
    dialog.addEventListener('close', () => {
      document.body.classList.remove('modal-open');
      dialog.querySelector('.tour-frame')?.replaceChildren();
      opener?.focus();
    });
  });
  const photoButtons = () => [...document.querySelectorAll('[data-photo]')].filter(button => !button.closest('[hidden]'));
  let activePhoto = 0;
  const lightbox = document.getElementById('lightbox');
  // Native port of Design Memory's Morphing Dialog shared image geometry.
  // <dialog> supplies modal semantics/inert background; explicit trigger state,
  // focus return and reduced motion complete the reference's shipping gaps.
  const frame = lightbox.querySelector('.viewer-frame');
  const surface = lightbox.querySelector('.viewer-surface');
  let viewerBusy = false;
  let viewerClosing = false;
  let viewerRevision = 0;
  const viewerAnimations = new Set();
  const geometry = rect => ({left:`${rect.left}px`, top:`${rect.top}px`, width:`${rect.width}px`, height:`${rect.height}px`});
  function fittedImage(image) {
    const stage = lightbox.querySelector('.viewer-stage').getBoundingClientRect();
    const scale = Math.min(stage.width / image.naturalWidth, stage.height / image.naturalHeight, 1);
    const width = image.naturalWidth * scale;
    const height = image.naturalHeight * scale;
    return {left:stage.left + (stage.width-width)/2, top:stage.top + (stage.height-height)/2, width, height};
  }
  function animateViewer(element, keys, duration=400) {
    if (reduced.matches) return Promise.resolve();
    const animation = element.animate(keys, {duration, easing:'cubic-bezier(0.2,0,0,1)'});
    viewerAnimations.add(animation);
    return animation.finished.catch(() => {}).finally(() => viewerAnimations.delete(animation));
  }
  async function preparePhoto(index) {
    const buttons = photoButtons();
    if (!buttons.length) return null;
    const selected = (index + buttons.length) % buttons.length;
    const photo = JSON.parse(buttons[selected].dataset.photo);
    const image = new Image();
    image.src = photo.src;
    image.alt = photo.alt;
    image.id = 'lightbox-image';
    await image.decode().catch(() => {});
    if (!image.naturalWidth) return null;
    return {selected,photo,image,button:buttons[selected],count:buttons.length};
  }
  function commitPhoto(prepared) {
    const {selected,photo,image,count} = prepared;
    activePhoto = selected;
    frame.replaceChildren(image);
    document.getElementById('lightbox-caption').textContent = photo.alt;
    document.getElementById('lightbox-count').textContent = `${selected + 1} / ${count}`;
    Object.assign(frame.style, geometry(fittedImage(image)));
  }
  document.querySelectorAll('[data-photo]').forEach(button => {
    button.setAttribute('aria-controls','lightbox');
    button.setAttribute('aria-expanded','false');
    button.addEventListener('click', async () => {
    if (viewerBusy || lightbox.open) return;
    viewerBusy = true;
    button.setAttribute('aria-busy','true');
    const prepared = await preparePhoto(photoButtons().indexOf(button));
    button.removeAttribute('aria-busy');
    if (!prepared) { viewerBusy=false; return; }
    opener = button;
    const start = button.querySelector('img').getBoundingClientRect();
    const revision = ++viewerRevision;
    lightbox.classList.add('is-opening');
    lightbox.showModal();
    document.body.classList.add('modal-open');
    button.setAttribute('aria-expanded','true');
    commitPhoto(prepared);
    const end = frame.getBoundingClientRect();
    lightbox.querySelector('[data-close]').focus();
    await Promise.all([animateViewer(frame,[geometry(start),geometry(end)],800),animateViewer(surface,[{opacity:0},{opacity:1}],800)]);
    if (revision !== viewerRevision) return;
    lightbox.classList.remove('is-opening');
    viewerBusy = false;
  });
  });
  async function showPhoto(index) {
    if (viewerBusy || viewerClosing || !lightbox.open) return;
    viewerBusy = true;
    const revision = viewerRevision;
    const prepared = await preparePhoto(index);
    if (!prepared || !lightbox.open || revision !== viewerRevision) { viewerBusy=false; return; }
    const before = frame.getBoundingClientRect();
    const outgoing = frame.querySelector('img');
    outgoing.removeAttribute('id');
    outgoing.setAttribute('aria-hidden','true');
    commitPhoto(prepared);
    frame.prepend(outgoing);
    await Promise.all([
      animateViewer(frame,[geometry(before),geometry(fittedImage(prepared.image))]),
      animateViewer(prepared.image,[{opacity:0,transform:'translateX(16px)'},{opacity:1,transform:'translateX(0)'}]),
      animateViewer(outgoing,[{opacity:1},{opacity:0}])
    ]);
    outgoing.remove();
    if (revision === viewerRevision) viewerBusy=false;
  }
  async function closePhoto() {
    if (!lightbox.open || viewerClosing) return;
    viewerClosing = true;
    ++viewerRevision;
    viewerAnimations.forEach(animation => { animation.commitStyles(); animation.cancel(); });
    lightbox.classList.remove('is-opening');
    lightbox.classList.add('is-closing');
    const before = frame.getBoundingClientRect();
    const thumb = photoButtons()[activePhoto]?.querySelector('img');
    const target = thumb?.getBoundingClientRect();
    const visible = target && target.bottom>0 && target.top<innerHeight && target.width>0;
    await Promise.all([
      animateViewer(frame,visible ? [geometry(before),geometry(target)] : [{opacity:1,transform:'scale(1)'},{opacity:0,transform:'scale(.98)'}]),
      animateViewer(surface,[{opacity:getComputedStyle(surface).opacity},{opacity:0}])
    ]);
    lightbox.close();
    opener?.setAttribute('aria-expanded','false');
    lightbox.classList.remove('is-closing');
    frame.removeAttribute('style');
    surface.removeAttribute('style');
    viewerBusy = false;
    viewerClosing = false;
  }
  lightbox.addEventListener('cancel',event => { event.preventDefault(); closePhoto(); });
  lightbox.addEventListener('click',event => {
    if (event.target === lightbox || event.target.matches('.viewer-stage,.viewer-surface')) closePhoto();
  });
  window.addEventListener('resize', () => {
    if (lightbox.open && !viewerBusy && !viewerClosing) Object.assign(frame.style,geometry(fittedImage(frame.querySelector('img'))));
  });
  reduced.addEventListener('change', () => {
    if (reduced.matches) viewerAnimations.forEach(animation => animation.finish());
  });
  document.querySelectorAll('[data-photo-step]').forEach(button => button.addEventListener('click', () => showPhoto(activePhoto + Number(button.dataset.photoStep))));
  lightbox.addEventListener('keydown', event => {
    if (event.key === 'Tab') {
      const controls = [...lightbox.querySelectorAll('button')];
      const first = controls[0];
      const last = controls[controls.length-1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
      event.preventDefault();
      showPhoto(activePhoto + (event.key === 'ArrowLeft' ? -1 : 1));
    }
  });
  const filters = [...document.querySelectorAll('[data-filter]')];
  reduced.addEventListener('change', () => {
    if (reduced.matches) document.querySelectorAll('.gallery-item').forEach(item => item.getAnimations().forEach(animation => animation.cancel()));
  });
  const filterGallery = (value) => {
    if (!filters.some(button => button.dataset.filter === value)) value = 'all';
    const positions = new Map([...document.querySelectorAll('.gallery-item:not([hidden])')].map(item => [item, item.getBoundingClientRect()]));
    filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === value)));
    document.querySelectorAll('.gallery-item').forEach(item => { item.hidden = value !== 'all' && item.dataset.category !== value; });
    const count = document.querySelectorAll('.gallery-item:not([hidden])').length;
    document.getElementById('gallery-count').textContent = t(`${count} photographies`, `${count} photographs`);
  };
  filters.forEach(button => button.addEventListener('click', () => filterGallery(button.dataset.filter)));
  if (filters.length) filterGallery(new URLSearchParams(location.search).get('filter') || 'all');
  const form = document.getElementById('stay-form');
  if (form) {
    const today = new Date();
    const localDate = `${today.getFullYear()}-${String(today.getMonth()+1).padStart(2,'0')}-${String(today.getDate()).padStart(2,'0')}`;
    form.elements.arrival.min = localDate;
    form.elements.departure.min = localDate;
    const selectedType = new URLSearchParams(location.search).get('type');
    if (['family','friends','business'].includes(selectedType)) form.elements.type.value = selectedType;
    form.elements.arrival.addEventListener('change', () => {
      form.elements.departure.min = form.elements.arrival.value || localDate;
      form.elements.departure.setCustomValidity('');
    });
    form.elements.departure.addEventListener('change', () => form.elements.departure.setCustomValidity(''));
    form.addEventListener('submit', event => {
      event.preventDefault();
      const error = document.getElementById('form-error');
      error.textContent = '';
      if (form.elements.departure.value <= form.elements.arrival.value) {
        error.textContent = t('Le départ doit être après la date d’arrivée.', 'Departure must be after the arrival date.');
        form.elements.departure.setCustomValidity(error.textContent);
        form.elements.departure.reportValidity();
        return;
      }
      const names = {family:t('en famille','family stay'),friends:t('entre amis','with friends'),business:t('séminaire / équipe','team retreat')};
      const subject = t('Demande de séjour — Domaine aux Lions','Stay enquiry — Domaine aux Lions');
      const message = t('Bonjour,\n\nNous souhaitons organiser un séjour au Domaine aux Lions.','Hello,\n\nWe would like to arrange a stay at Le Domaine aux Lions.') + '\n\n' +
        t('Arrivée souhaitée : ','Preferred arrival: ') + form.elements.arrival.value + '\n' +
        t('Départ souhaité : ','Preferred departure: ') + form.elements.departure.value + '\n' +
        t('Nombre d’invités : ','Number of guests: ') + form.elements.guests.value + '\n' +
        t('Type de séjour : ','Type of stay: ') + names[form.elements.type.value] + '\n\n' + form.elements.message.value + '\n\n' +
        t('Pouvez-vous nous préciser les disponibilités, le tarif et les conditions ?\n\nMerci !','Could you confirm availability, rates and conditions?\n\nThank you!');
      const mailto = `mailto:ledomaineauxlions@gmail.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(message)}`;
      const preview = document.getElementById('email-preview');
      preview.hidden = false;
      preview.querySelector('pre').textContent = message;
      document.getElementById('email-link').href = mailto;
      // Prepare locally; only the explicit link opens the visitor's email app.
      const emailLink = document.getElementById('email-link');
      emailLink.focus({preventScroll:true});
      preview.scrollIntoView({behavior:reduced.matches ? 'instant' : 'smooth',block:'center'});
    });
  }
})();
