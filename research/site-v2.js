(() => {
  'use strict';
  const lang = document.body.dataset.language;
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)');
  const t = (fr, en) => lang === 'fr' ? fr : en;
  // Editorial enter: each major chapter arrives once as it enters the reading
  // window. It never owns scrolling, and reduced-motion keeps the final state.
  const revealTargets = [...document.querySelectorAll('.home-intro, .leisure-deck, .tour-section, .stays, .audience-detail, .art-section, .reviews-section, .location-section, .final-cta, .page-section, .house-story, .equipment-layout, .booking-layout, .access-content')];
  if (revealTargets.length) {
    if (!reduced.matches && 'IntersectionObserver' in window) {
      document.documentElement.classList.add('motion-ready');
      const revealObserver = new IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add('is-visible');
          revealObserver.unobserve(entry.target);
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -15% 0px' });
      revealTargets.forEach(target => revealObserver.observe(target));
    } else revealTargets.forEach(target => target.classList.add('is-visible'));
  }
  let opener = null;
  const closeDialog = (dialog) => {
    if (!dialog) return;
    dialog.close();
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
  function showPhoto(index) {
    const buttons = photoButtons();
    if (!buttons.length) return;
    activePhoto = (index + buttons.length) % buttons.length;
    const photo = JSON.parse(buttons[activePhoto].dataset.photo);
    const image = document.getElementById('lightbox-image');
    image.src = photo.src;
    image.alt = photo.alt;
    document.getElementById('lightbox-caption').textContent = photo.alt;
    document.getElementById('lightbox-count').textContent = `${activePhoto + 1} / ${buttons.length}`;
  }
  document.querySelectorAll('[data-photo]').forEach(button => button.addEventListener('click', () => {
    opener = button;
    showPhoto(photoButtons().indexOf(button));
    lightbox.showModal();
    document.body.classList.add('modal-open');
    lightbox.querySelector('[data-close]').focus();
  }));
  document.querySelectorAll('[data-photo-step]').forEach(button => button.addEventListener('click', () => showPhoto(activePhoto + Number(button.dataset.photoStep))));
  lightbox.addEventListener('keydown', event => {
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
    if (!reduced.matches) {
      document.querySelectorAll('.gallery-item:not([hidden])').forEach(item => {
        const before = positions.get(item);
        if (!before) return;
        const after = item.getBoundingClientRect();
        const x = before.left - after.left;
        const y = before.top - after.top;
        if (x || y) item.animate([{transform:`translate(${x}px, ${y}px)`},{transform:'translate(0, 0)'}], {duration:320,easing:'cubic-bezier(0.2, 0, 0, 1)'});
      });
    }
    const count = document.querySelectorAll('.gallery-item:not([hidden])').length;
    document.getElementById('gallery-count').textContent = t(`${count} photographies`, `${count} photographs`);
  };
  filters.forEach(button => button.addEventListener('click', () => filterGallery(button.dataset.filter)));
  if (filters.length) filterGallery(new URLSearchParams(location.search).get('filter') || 'all');
  const reviewTrack = document.querySelector('.review-track');
  if (reviewTrack) {
    const reviews = [...reviewTrack.querySelectorAll('.review')];
    const compactReviews = window.matchMedia('(max-width: 768px)');
    let reviewPage = 0;
    let perPage = compactReviews.matches ? 1 : 2;
    const showReviews = () => {
      const count = Math.ceil(reviews.length / perPage);
      reviewPage = (reviewPage + count) % count;
      const start = reviewPage * perPage;
      reviewTrack.dataset.reviewReady = 'true';
      reviews.forEach((review, index) => {
        review.hidden = index < start || index >= start + perPage;
        review.setAttribute('role', 'group');
        review.setAttribute('aria-roledescription', t('diapositive', 'slide'));
        review.setAttribute('aria-label', t(`Avis ${index+1} sur ${reviews.length}`, `Review ${index+1} of ${reviews.length}`));
      });
      const end = Math.min(start+perPage, reviews.length);
      document.querySelector('.review-position').textContent = t(`Avis ${start+1}${end>start+1?'–'+end:''} sur ${reviews.length}`, `Review ${start+1}${end>start+1?'–'+end:''} of ${reviews.length}`);
    };
    document.querySelectorAll('[data-review-step]').forEach(button => button.addEventListener('click', () => {
      reviewPage += Number(button.dataset.reviewStep);
      showReviews();
    }));
    reviewTrack.addEventListener('keydown', event => {
      if (event.key !== 'ArrowLeft' && event.key !== 'ArrowRight') return;
      event.preventDefault();
      reviewPage += event.key === 'ArrowLeft' ? -1 : 1;
      showReviews();
    });
    compactReviews.addEventListener('change', () => {
      const oldStart = reviewPage * perPage;
      perPage = compactReviews.matches ? 1 : 2;
      reviewPage = Math.floor(oldStart / perPage);
      showReviews();
    });
    showReviews();
  }
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
