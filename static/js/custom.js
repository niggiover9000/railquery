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
                        a.href = encodeURIComponent(item.code);
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

        searchButton.addEventListener('click', performSearch);

        searchInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                performSearch();
            }
        });
    });