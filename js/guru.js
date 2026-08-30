```javascript
document.addEventListener("DOMContentLoaded", function () {

    // ==========================================
    // SEARCH SISWA
    // ==========================================

    const searchInput = document.getElementById("search");
    const searchForm = searchInput
        ? searchInput.closest("form")
        : null;


    // ==========================================
    // NORMALISASI INPUT
    // ==========================================

    if (searchInput) {

        searchInput.addEventListener("input", function () {

            // Hapus spasi
            this.value = this.value.replace(/\s/g, "");

            // Ubah menjadi huruf kapital
            this.value = this.value.toUpperCase();

        });

    }


    // ==========================================
    // VALIDASI FORM
    // ==========================================

    if (searchForm) {

        searchForm.addEventListener("submit", function (event) {

            const keyword = searchInput.value.trim();

            // Cegah pencarian kosong
            if (keyword === "") {

                event.preventDefault();

                alert("Silakan masukkan inisial siswa terlebih dahulu.");

                searchInput.focus();

                return;
            }

            // Pastikan dikirim dalam huruf kapital
            searchInput.value = keyword.toUpperCase();

        });

    }


    // ==========================================
    // AUTO FOCUS
    // ==========================================

    if (
        searchInput &&
        searchInput.value.trim() !== ""
    ) {

        searchInput.focus();

        // Posisikan cursor di akhir teks
        searchInput.setSelectionRange(
            searchInput.value.length,
            searchInput.value.length
        );

    }


    // ==========================================
    // TOMBOL HASIL SISWA
    // ==========================================

    const studentLinks =
        document.querySelectorAll(".student-link");

    studentLinks.forEach(function (link) {

        link.addEventListener("click", function () {

            // Mencegah klik ganda
            this.style.pointerEvents = "none";

        });

    });


    // ==========================================
    // TOMBOL REKOMENDASI
    // ==========================================

    const recommendationButtons =
        document.querySelectorAll(".recommend-btn");

    recommendationButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            // Mencegah klik ganda
            this.style.pointerEvents = "none";

        });

    });


    // ==========================================
    // KEYBOARD SHORTCUT
    // ==========================================

    document.addEventListener("keydown", function (event) {

        // Tekan "/" untuk langsung mencari siswa
        if (
            event.key === "/" &&
            document.activeElement !== searchInput
        ) {

            event.preventDefault();

            if (searchInput) {
                searchInput.focus();
            }

        }

        // Tekan Escape untuk menghapus pencarian
        if (
            event.key === "Escape" &&
            document.activeElement === searchInput
        ) {

            searchInput.value = "";

        }

    });

});
```
