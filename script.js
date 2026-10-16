// Janoon Inc. — site behavior (no dependencies)
(function(){
  "use strict";

  // Mobile nav toggle
  var menuBtn = document.querySelector(".menu-btn");
  var navRight = document.querySelector(".nav .right");
  if (menuBtn && navRight) {
    menuBtn.addEventListener("click", function () {
      var open = navRight.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  // Scroll reveal
  var rv = document.querySelectorAll(".rv");
  if ("IntersectionObserver" in window && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    rv.forEach(function (el) { io.observe(el); });
  } else {
    rv.forEach(function (el) { el.classList.add("in"); });
  }

  // Services page: highlight the section in view
  var toc = document.querySelectorAll(".detail .toc a");
  if (toc.length && "IntersectionObserver" in window) {
    var secs = [].map.call(toc, function (a) { return document.querySelector(a.getAttribute("href")); });
    var tio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) toc.forEach(function (a) { a.classList.toggle("active", a.getAttribute("href") === "#" + e.target.id); });
      });
    }, { rootMargin: "-20% 0px -65% 0px" });
    secs.forEach(function (s) { if (s) tio.observe(s); });
  }

  // Contact form: client-side validation, then real submission (see note inside).
  var form = document.getElementById("contact-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var valid = true;
      ["name", "email", "subject", "message"].forEach(function (id) {
        var input = form.querySelector("#" + id);
        var field = input.closest(".field");
        var isEmpty = !input.value.trim();
        var isBadEmail = id === "email" && input.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input.value);
        var hasError = isEmpty || isBadEmail;
        field.classList.toggle("error", hasError);
        if (hasError) valid = false;
      });
      if (!valid) {
        var firstError = form.querySelector(".field.error input, .field.error textarea");
        if (firstError) firstError.focus();
        return;
      }

      // Submit. On Netlify the POST is captured by Netlify Forms; elsewhere set
      // the form's action to your endpoint (Formspree, FormSubmit, your own API).
      var btn = form.querySelector('button[type="submit"]');
      btn.disabled = true; btn.textContent = "Sending\u2026";
      var body = new URLSearchParams(new FormData(form)).toString();
      fetch(form.getAttribute("action"), { method: "POST", headers: { "Content-Type": "application/x-www-form-urlencoded" }, body: body })
        .then(function (res) {
          if (!res.ok) throw new Error("HTTP " + res.status);
          var success = document.getElementById("form-success");
          success.classList.add("show");
          success.setAttribute("role", "status");
          success.focus();
          form.reset();
        })
        .catch(function (err) {
          if (err && /^HTTP /.test(err.message)) {
            // Endpoint answered but rejected: tell the user, offer the direct channels.
            var fail = document.getElementById("form-fail");
            fail.hidden = false; fail.setAttribute("role", "alert"); fail.focus();
            return;
          }
          // Network failure (offline, blocked fetch): fall back to a normal navigation POST.
          form.submit();
        })
        .finally(function () { btn.disabled = false; btn.textContent = "Send"; });
    });
  }
})();
