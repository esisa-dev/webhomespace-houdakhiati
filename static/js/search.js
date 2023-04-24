const searchForm = document.querySelector('form');
const searchInput = document.querySelector('input[type="text"]');

searchForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const query = searchInput.value;
    window.location.href = `/search?query=${query}`;
});
