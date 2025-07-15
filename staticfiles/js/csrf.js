document.body.addEventListener('htmx:configRequest', (event) => {
  const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  event.detail.headers['X-CSRFToken'] = csrfToken;
});
