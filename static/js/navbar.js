document.addEventListener("DOMContentLoaded", () => {

    const menuButton =
        document.getElementById("menu-toggle");

    const closeButton =
        document.getElementById("close-menu");

    const drawer =
        document.getElementById("mobile-nav");

    const overlay =
        document.getElementById("nav-overlay");

    if (
        !menuButton ||
        !closeButton ||
        !drawer ||
        !overlay
    ) return;

    // ===========================
    // Open Drawer
    // ===========================

    function openDrawer() {

        drawer.classList.add("show");

        overlay.classList.add("show");

        document.body.style.overflow = "hidden";

    }

    // ===========================
    // Close Drawer
    // ===========================

    function closeDrawer() {

        drawer.classList.remove("show");

        overlay.classList.remove("show");

        document.body.style.overflow = "";

    }

    // ===========================
    // Events
    // ===========================

    menuButton.addEventListener(
        "click",
        openDrawer
    );

    closeButton.addEventListener(
        "click",
        closeDrawer
    );

    overlay.addEventListener(
        "click",
        closeDrawer
    );

    // Close after clicking a link

    drawer.querySelectorAll("a").forEach(link => {

        link.addEventListener(
            "click",
            closeDrawer
        );

    });

    // ESC key support

    document.addEventListener(
        "keydown",
        function(e){

            if(
                e.key === "Escape" &&
                drawer.classList.contains("show")
            ){

                closeDrawer();

            }

        }
    );

});