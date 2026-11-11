(() => {
    const shelves = document.querySelectorAll(".city-shelf-books");
    const resize = new ResizeObserver((entries) => {
        for (const { target: shelf } of entries) {
            const books = [...shelf.querySelectorAll(".city-book-slot")];
            books.forEach((book, index) => {
                const next = books[index + 1];
                book.classList.toggle("city-book-row-end", !next || next.offsetTop !== book.offsetTop);
            });
        }
    });

    shelves.forEach(shelf => resize.observe(shelf));
})();
