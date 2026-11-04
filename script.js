/* Language (English / Malay) and theme (light / dark) toggles.
   Malay text lives on each element as data-ms="..."; the English original is
   read from the page itself, so you edit the English in index.html as usual
   and its Malay version right beside it. */
(function () {
  var root = document.documentElement;

  var TEXT = {
    en: {
      title: "Thyme Inn – Financial Analyst",
      description: "Portfolio of a financial analyst: forecasting, valuation and risk modelling.",
      toDark: "Switch to dark mode",
      toLight: "Switch to light mode"
    },
    ms: {
      title: "Thyme Inn – Penganalisis Kewangan",
      description: "Portfolio seorang penganalisis kewangan: peramalan, penilaian dan pemodelan risiko.",
      toDark: "Tukar ke mod gelap",
      toLight: "Tukar ke mod cerah"
    }
  };

  function save(key, value) {
    try { localStorage.setItem(key, value); } catch (e) { /* storage blocked */ }
  }

  function setTheme(theme) {
    root.setAttribute("data-theme", theme);
    save("theme", theme);
    var btn = document.querySelector(".theme-toggle");
    if (btn) {
      var t = TEXT[root.lang === "ms" ? "ms" : "en"];
      btn.setAttribute("aria-label", theme === "dark" ? t.toLight : t.toDark);
    }
  }

  function setLang(lang) {
    lang = lang === "ms" ? "ms" : "en";
    root.lang = lang;
    save("lang", lang);

    document.querySelectorAll("[data-ms]").forEach(function (el) {
      if (!el.hasAttribute("data-en")) {
        el.setAttribute("data-en", el.textContent.replace(/\s+/g, " ").trim());
      }
      el.textContent = el.getAttribute(lang === "ms" ? "data-ms" : "data-en");
    });

    document.querySelectorAll("[data-ms-aria-label]").forEach(function (el) {
      if (!el.hasAttribute("data-en-aria-label")) {
        el.setAttribute("data-en-aria-label", el.getAttribute("aria-label"));
      }
      el.setAttribute("aria-label",
        el.getAttribute(lang === "ms" ? "data-ms-aria-label" : "data-en-aria-label"));
    });

    document.title = TEXT[lang].title;
    var meta = document.querySelector('meta[name="description"]');
    if (meta) meta.setAttribute("content", TEXT[lang].description);

    document.querySelectorAll(".lang-switch button").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-lang") === lang));
    });

    setTheme(root.getAttribute("data-theme") || "light"); // refresh button label
  }

  document.querySelectorAll(".lang-switch button").forEach(function (b) {
    b.addEventListener("click", function () { setLang(b.getAttribute("data-lang")); });
  });

  var themeBtn = document.querySelector(".theme-toggle");
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      setTheme(root.getAttribute("data-theme") === "dark" ? "light" : "dark");
    });
  }

  setLang(root.lang);
  root.classList.add("ready");
})();
