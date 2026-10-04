const search = document.querySelector(".navbar-search");

if (search) {
    const searchInput = search.querySelector("#search-input");
    const openButton = search.querySelector(".search-toggle");
    const closeButton = search.querySelector(".search-close");

    function openSearch() {
        search.classList.add("search-open");
        openButton.setAttribute("aria-expanded", "true");
        searchInput.focus();
    }

    function closeSearch() {
        search.classList.remove("search-open");
        openButton.setAttribute("aria-expanded", "false");
        openButton.focus();
    }

    openButton.addEventListener("click", openSearch);
    closeButton.addEventListener("click", closeSearch);

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && search.classList.contains("search-open")) {
            closeSearch();
        }
    });
}
