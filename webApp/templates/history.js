let manualSearch = false;

document.getElementById('searchBox').addEventListener('input', () => {
    manualSearch = true;
    filterList();
    clearTimeout(window.manualResetTimeout);
    window.manualResetTimeout = setTimeout(() => {
        manualSearch = false;
    }, 15000); // resume auto-refresh after 15s of inactivity
});

setInterval(() => {
    if (!manualSearch) fetchHistory();
}, 10000);

function renderEntry(entry) {
    const li = document.createElement('li');
    let content = entry.content;
    let displayText = content.length > 100 ? content.substring(0, 100) + "..." : content;

    li.innerHTML = `<span class="entry-text">${displayText}</span>`;

    if (content.length > 100) {
        li.addEventListener('click', () => {
            const span = li.querySelector('.entry-text');
            span.textContent = span.textContent.endsWith("...") ? content : displayText;
        });
        li.style.cursor = "pointer";
    }

    const copyBtn = document.createElement('button');
    copyBtn.textContent = 'Copy';
    copyBtn.onclick = () => navigator.clipboard.writeText(entry.content);
    copyBtn.className = 'copy-btn';
    li.appendChild(copyBtn);

    return li;
}


async function fetchHistory() {
    const urlParams = new URLSearchParams(window.location.search);
    const page = urlParams.get('page') || 1;
    const response = await fetch(`/api/history?page=${page}`);
    if (!response.ok) {
        console.error('Failed to fetch history:', response.statusText);
        return;
    }
    const data = await response.json();

    const ul = document.getElementById('historyList');
    ul.innerHTML = ''; // Clear current list

    data.forEach(entry => {
        ul.appendChild(renderEntry(entry));
    });
}

async function filterList() {
    const filter = document.getElementById('searchBox').value;
    const ul = document.getElementById('historyList');
    ul.innerHTML = '';
    if (filter.trim() === "") return fetchHistory();

    const response = await fetch(`/api/search?q=${encodeURIComponent(filter)}`);
    const data = await response.json();

    data.forEach(entry => {
        const li = document.createElement('li');
        li.textContent = `${entry.id}: ${entry.content} at ${entry.timestamp}`;
        ul.appendChild(renderEntry(entry));
;
    });
}


// Initial fetch + periodic updates
fetchHistory();
setInterval(fetchHistory, 10000);