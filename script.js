/* =====================================================
   Mandrell's CFO — site interactions
   ===================================================== */

(function () {
  'use strict';

  // Form delivery — Formsubmit today, Web3Forms once the client's key arrives.
  const FORM = { endpoint: "https://formsubmit.co/ajax/cfo@mandrells.com", web3formsKey: "" }; // when the Web3Forms key arrives: set web3formsKey and the endpoint switches automatically

  // POSTs a form as JSON. Resolves only on a confirmed delivery — Formsubmit
  // answers 200 even when it drops a message, so the body is what counts.
  function sendForm(form) {
    var data = {};
    new FormData(form).forEach(function (value, key) {
      data[key] = key in data ? data[key] + ', ' + value : value;
    });
    if (data._subject) data.subject = data._subject;
    var url = FORM.endpoint;
    if (FORM.web3formsKey) {
      url = 'https://api.web3forms.com/submit';
      data.access_key = FORM.web3formsKey;
      Object.keys(data).forEach(function (key) { if (key.charAt(0) === '_') delete data[key]; });
    }
    var httpOk = false;
    return fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify(data)
    })
      .then(function (res) {
        httpOk = res.ok;
        return res.json().catch(function () { return {}; });
      })
      .then(function (out) {
        if (!httpOk || !(out.success === true || out.success === 'true')) {
          throw new Error(out.message || 'Form submission failed');
        }
        return out;
      });
  }

  /* ----- Year ----- */
  document.querySelectorAll('#year').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ----- Sticky nav border on scroll ----- */
  const nav = document.getElementById('nav');
  if (nav) {
    const onScroll = function () {
      if (window.scrollY > 12) nav.classList.add('scrolled');
      else nav.classList.remove('scrolled');
    };
    document.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ----- Mobile menu ----- */
  const menuBtn = document.getElementById('menuBtn');
  const navLinks = document.getElementById('navLinks');
  if (menuBtn && navLinks) {
    menuBtn.addEventListener('click', function () {
      const open = navLinks.classList.toggle('open');
      menuBtn.classList.toggle('open', open);
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    navLinks.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        navLinks.classList.remove('open');
        menuBtn.classList.remove('open');
        menuBtn.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ----- Reveal on scroll ----- */
  const revealTargets = document.querySelectorAll('.reveal, .reveal-stagger');
  if ('IntersectionObserver' in window && revealTargets.length) {
    const obs = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('in');
            obs.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
    );
    revealTargets.forEach(function (el) { obs.observe(el); });
  } else {
    revealTargets.forEach(function (el) { el.classList.add('in'); });
  }

  /* =====================================================
     INTAKE FORM
     ===================================================== */

  const form = document.getElementById('intakeForm');
  if (!form) return;

  const submitBtn = document.getElementById('submitBtn');
  const formStatus = document.getElementById('formStatus');
  const successCard = document.getElementById('successCard');
  const intakeGrid = document.getElementById('intakeGrid');
  const verifyInput = document.getElementById('verifyAnswer');
  const honeypot = document.getElementById('company_url');

  // Time-trap: record when form first becomes interactive
  const startedAt = Date.now();
  const MIN_DURATION_MS = 4000; // bots fill instantly; humans take longer

  /* --- Enable submit only after: verify passes, min time elapsed, no honeypot --- */
  function setStatus(msg, kind) {
    if (!formStatus) return;
    formStatus.textContent = msg || '';
    formStatus.classList.remove('error', 'success');
    if (kind) formStatus.classList.add(kind);
    formStatus.style.display = msg ? 'block' : 'none';
  }

  function verifyOk() {
    if (!verifyInput) return true;
    const expected = (verifyInput.dataset.verify || '').trim().toLowerCase();
    const given = (verifyInput.value || '').trim().toLowerCase();
    if (!expected) return true;
    // Accept "receivable" or "receivables" — generous
    return given.length > 0 && (given === expected || given === expected + 's');
  }

  function updateSubmitState() {
    if (!submitBtn) return;
    const ok = verifyOk();
    submitBtn.disabled = !ok;
    if (ok) setStatus('', '');
  }

  if (verifyInput) {
    verifyInput.addEventListener('input', updateSubmitState);
    verifyInput.addEventListener('blur', function () {
      if (!verifyOk() && verifyInput.value.trim().length > 0) {
        setStatus('Not quite — AR is short for Accounts Receivable.', 'error');
      }
    });
  } else {
    if (submitBtn) submitBtn.disabled = false;
  }

  /* --- Phone formatting (US-friendly) --- */
  const phoneField = document.getElementById('phone');
  if (phoneField) {
    phoneField.addEventListener('input', function () {
      let v = phoneField.value.replace(/\D/g, '').slice(0, 10);
      if (v.length >= 7) {
        phoneField.value = '(' + v.slice(0, 3) + ') ' + v.slice(3, 6) + '-' + v.slice(6);
      } else if (v.length >= 4) {
        phoneField.value = '(' + v.slice(0, 3) + ') ' + v.slice(3);
      } else if (v.length > 0) {
        phoneField.value = '(' + v;
      }
    });
  }

  /* --- Lightweight client-side required check --- */
  function validateRequired() {
    let firstInvalid = null;
    const required = form.querySelectorAll('[required]');
    required.forEach(function (field) {
      const val = (field.type === 'radio')
        ? form.querySelector('input[name="' + field.name + '"]:checked')
        : (field.value || '').trim();
      const empty = !val;
      field.style.borderColor = empty ? '#a83232' : '';
      if (empty && !firstInvalid) firstInvalid = field;
    });
    return firstInvalid;
  }

  /* --- Submit handling --- */
  form.addEventListener('submit', function (e) {
    e.preventDefault();

    // Honeypot triggered: silently "succeed" without sending
    if (honeypot && honeypot.value) {
      showSuccess();
      return;
    }

    // Time-trap
    const elapsed = Date.now() - startedAt;
    if (elapsed < MIN_DURATION_MS) {
      setStatus('Take a moment to review — please try again.', 'error');
      return;
    }

    // Verify
    if (!verifyOk()) {
      setStatus('Please answer the verification question to continue.', 'error');
      if (verifyInput) verifyInput.focus();
      return;
    }

    // Required fields
    const bad = validateRequired();
    if (bad) {
      setStatus('A few fields still need an answer.', 'error');
      bad.focus();
      bad.scrollIntoView({ behavior: 'smooth', block: 'center' });
      return;
    }

    // All clear — sendForm() confirms delivery (Formsubmit AJAX today,
    // Web3Forms once FORM.web3formsKey is set). No JS = native POST to action=.
    submitBtn.disabled = true;
    submitBtn.innerHTML = 'Sending… <span class="arrow">→</span>';
    setStatus('Submitting your intake…', 'success');

    sendForm(form)
      .then(function () {
        showSuccess();
      })
      .catch(function () {
        setStatus('Something went wrong. Please email cfo@mandrells.com directly or call (352) 248-0518.', 'error');
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Submit intake <span class="arrow">→</span>';
      });
  });

  function showSuccess() {
    if (successCard && intakeGrid) {
      intakeGrid.style.display = 'none';
      successCard.classList.add('visible');
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  // Initial state
  updateSubmitState();
})();
