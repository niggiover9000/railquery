document.addEventListener('DOMContentLoaded', function () {
        const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        const tooltipList = [...tooltipTriggerList].map(el => new bootstrap.Tooltip(el));

        const searchInput = document.getElementById('searchInput');
        const searchButton = document.getElementById('searchButton');
        const resultsList = document.getElementById('searchResults');

        if (!searchInput || !searchButton || !resultsList) {
            return;
        }

        let debounceTimer;

        function openTopResultIfAvailable() {
            const firstLink = resultsList.querySelector('li a[href]');
            if (!firstLink) {
                return false;
            }

            window.location.href = firstLink.href;
            return true;
        }

        function performSearch() {
            const query = searchInput.value;
            if (query.length > 0) {
                $.get('/search', {q: query}, function (data) {
                    resultsList.innerHTML = '';
                    data.forEach(function (item) {
                        const li = document.createElement('li');
                        li.className = 'list-group-item';

                        const a = document.createElement('a');
                        a.className = 'text-black link-underline-opacity-0 link-underline-opacity-75-hover link-underline-dark';
                        a.href = '/' + encodeURIComponent(item.code);
                        a.textContent = item.code + ' - ' + item.name;

                        li.appendChild(a);
                        resultsList.appendChild(li);
                    });
                });
            } else {
                resultsList.innerHTML = '';
            }
        }

        searchInput.addEventListener('input', function () {
            clearTimeout(debounceTimer);
            debounceTimer = setTimeout(performSearch, 200);
        });

        searchButton.addEventListener('click', function () {
            if (resultsList.children.length > 0 && openTopResultIfAvailable()) {
                return;
            }
            performSearch();
        });

        searchInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                if (resultsList.children.length > 0 && openTopResultIfAvailable()) {
                    return;
                }
                performSearch();
            }
        });
    });

// Copy to clipboard
const copyResetTimers = new WeakMap();
const COPY_FEEDBACK_MS = 5000;

// Das Haken-Icon vorab holen. Sonst wird es erst beim Klick angefordert und
// haengt in der Warteschlange hinter den /api/-Checks von initButtons() --
// der Haken erscheint dann erst, wenn die externen Links durchgeprueft sind.
// custom.js laeuft im <head>, dieser Listener ist damit vor dem von
// initButtons() registriert und startet den Request zuerst.
document.addEventListener('DOMContentLoaded', function () {
    const seen = new Set();
    document.querySelectorAll('.copy-btn[data-copied-src]').forEach(el => {
        const src = el.dataset.copiedSrc;
        if (seen.has(src)) return;
        seen.add(src);
        new Image().src = src;
    });
});

function showCopiedState(el) {
    const copiedSrc = el.dataset.copiedSrc;
    if (copiedSrc) {
        if (!el.dataset.defaultSrc) {
            el.dataset.defaultSrc = el.src;
        }
        el.src = copiedSrc;
    }

    const tip = bootstrap.Tooltip.getInstance(el);
    if (tip) {
        el.setAttribute('data-bs-original-title', 'Kopiert!');
        tip.show();
    }

    clearTimeout(copyResetTimers.get(el));
    copyResetTimers.set(el, setTimeout(() => {
        if (el.dataset.defaultSrc) {
            el.src = el.dataset.defaultSrc;
        }
        if (tip) {
            el.setAttribute('data-bs-original-title', 'Kopieren');
            tip.hide();
        }
        copyResetTimers.delete(el);
    }, COPY_FEEDBACK_MS));
}

// Muss auf window in der Capture-Phase liegen: Bootstrap haengt seine
// delegierten Data-API-Handler (Collapse) auf document, ebenfalls capture.
// Auf document wuerde unser stopPropagation() zu spaet kommen und das
// Accordion beim Kopieren mit aufklappen.
window.addEventListener('click', async (event) => {
    const el = event.target.closest('.copy-btn');
    if (!el) return;

    event.preventDefault();
    event.stopPropagation();

    const value = el.dataset.copyValue;
    let copied = true;

    try {
        await navigator.clipboard.writeText(value);
    } catch (err) {
        const ta = document.createElement('textarea');
        ta.value = value;
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        copied = document.execCommand('copy');
        ta.remove();
    }

    if (copied) {
        showCopiedState(el);
    }
}, true);
