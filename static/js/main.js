(function () {
  "use strict";

  var doc = document;
  var root = doc.documentElement;

  /* Tema claro / oscuro ---------------------------------------------------- */
  var themeToggle = doc.getElementById("theme-toggle");
  var themeColorMeta = doc.querySelector('meta[name="theme-color"]');
  var themeColors = { dark: "#070b14", light: "#f6f8fb" };

  function applyTheme(theme, persist) {
    root.setAttribute("data-theme", theme);
    if (themeColorMeta) {
      themeColorMeta.setAttribute("content", themeColors[theme] || themeColors.dark);
    }
    if (persist) {
      try {
        localStorage.setItem("portfolio-theme", theme);
      } catch (error) {
        /* almacenamiento no disponible */
      }
    }
    if (themeToggle) {
      themeToggle.setAttribute(
        "aria-label",
        theme === "dark" ? "Cambiar a tema claro" : "Cambiar a tema oscuro"
      );
    }
  }

  applyTheme(root.getAttribute("data-theme") === "light" ? "light" : "dark", false);

  if (themeToggle) {
    themeToggle.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "light" ? "dark" : "light";
      applyTheme(next, true);
    });
  }

  /* Header con sombra al hacer scroll -------------------------------------- */
  var header = doc.getElementById("site-header");
  var backToTop = doc.getElementById("back-to-top");

  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) {
      header.classList.toggle("is-scrolled", y > 8);
    }
    if (backToTop) {
      backToTop.classList.toggle("is-visible", y > 500);
    }
  }

  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  if (backToTop) {
    backToTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
  }

  /* Navegación móvil -------------------------------------------------------- */
  var navToggle = doc.getElementById("nav-toggle");
  var navPanel = doc.getElementById("nav-panel");

  function closeNav() {
    doc.body.classList.remove("nav-open");
    if (navToggle) {
      navToggle.setAttribute("aria-expanded", "false");
      navToggle.setAttribute("aria-label", "Abrir menú");
    }
  }

  if (navToggle && navPanel) {
    navToggle.addEventListener("click", function () {
      var isOpen = doc.body.classList.toggle("nav-open");
      navToggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
      navToggle.setAttribute("aria-label", isOpen ? "Cerrar menú" : "Abrir menú");
    });

    navPanel.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", closeNav);
    });

    doc.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        closeNav();
      }
    });

    doc.addEventListener("click", function (event) {
      if (
        doc.body.classList.contains("nav-open") &&
        !navPanel.contains(event.target) &&
        !navToggle.contains(event.target)
      ) {
        closeNav();
      }
    });

    window.addEventListener("resize", function () {
      if (window.innerWidth > 980) {
        closeNav();
      }
    });
  }

  /* Animación de aparición ------------------------------------------------- */
  var reveals = doc.querySelectorAll(".reveal");

  if ("IntersectionObserver" in window && reveals.length) {
    var revealObserver = new IntersectionObserver(
      function (entries, observer) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: "0px 0px -40px 0px" }
    );

    reveals.forEach(function (element) {
      revealObserver.observe(element);
    });
  } else {
    reveals.forEach(function (element) {
      element.classList.add("is-visible");
    });
  }

  /* Notificaciones --------------------------------------------------------- */
  var toastStack = doc.querySelector(".toast-stack");

  function dismissToast(toast) {
    if (!toast || toast.classList.contains("is-hiding")) {
      return;
    }
    toast.classList.add("is-hiding");
    window.setTimeout(function () {
      toast.remove();
      if (toastStack && !toastStack.querySelector(".toast")) {
        toastStack.remove();
      }
    }, 240);
  }

  if (toastStack) {
    toastStack.querySelectorAll(".toast").forEach(function (toast) {
      var closeButton = toast.querySelector(".toast-close");
      if (closeButton) {
        closeButton.addEventListener("click", function () {
          dismissToast(toast);
        });
      }
      window.setTimeout(function () {
        dismissToast(toast);
      }, 6500);
    });
  }

  /* Búsqueda: enviar al presionar Enter ya funciona de forma nativa --------- */
  doc.documentElement.classList.add("has-js");
})();
