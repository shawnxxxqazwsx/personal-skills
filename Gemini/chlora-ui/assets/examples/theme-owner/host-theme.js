/* Shared appearance preferences. Native preferences own persistence. */
(function () {
  "use strict";
  var current = { themeMode: "light", darkPalette: "graphite" };
  var appliedKey = "", transitionTimer = 0, foregroundAnimations = [];
  var palettes = {
    graphite: { lightness: 39, chroma: 0.055 },
    slate: { lightness: 39, chroma: 0.05 },
    carbon: { lightness: 39, chroma: 0.045 }
  };
  // Approved light palette B: L=46%, C=.055. Each legacy HSL hue was
  // converted through Oklab first, preserving its perceived hue. The sRGB
  // table is gamut-checked and avoids repeated colour conversion on redraw.
  var lightNodeColors = (
    "744c4a 744c49 744c49 744c48 744c48 744c47 744c47 744c46 744c46 744d45 744d44 734d44 734d43 734d42 734d42 734d41 734e40 734e40 724e3f 724e3e 724f3d 724f3d 714f3c 714f3b " +
    "71503b 70503a 705039 6f5139 6f5138 6e5137 6e5237 6d5236 6d5236 6c5335 6b5335 6b5334 6a5434 695434 695534 685533 675533 665633 665633 655633 645733 635733 635733 625833 " +
    "615833 615833 605934 5f5934 5f5934 5e5934 5d5a34 5d5a35 5c5a35 5c5a35 5b5a35 5b5b36 5a5b36 5a5b36 595b36 595b37 585b37 585c37 575c37 575c38 565c38 565c38 555c38 555c39 " +
    "545d39 545d39 535d3a 535d3a 525d3a 525d3a 525d3b 515e3b 515e3b 505e3c 505e3c 4f5e3c 4f5e3d 4f5e3d 4e5e3d 4e5e3d 4e5e3e 4d5f3e 4d5f3e 4c5f3e 4c5f3f 4c5f3f 4c5f3f 4b5f3f " +
    "4b5f40 4b5f40 4a5f40 4a5f40 4a5f41 495f41 495f41 496041 496041 486042 486042 486042 486042 486042 476043 476043 476043 476043 476043 466043 466043 466044 466044 466044 " +
    "466044 456044 456044 456045 456045 456045 446045 446045 446045 446146 436146 436146 436146 436147 426147 426147 426147 416148 416148 416148 406149 406149 406149 3f614a " +
    "3f614a 3f614a 3e614b 3e614b 3d614c 3d624c 3c624d 3c624d 3c624d 3b624e 3b624f 3a624f 396250 396250 386251 386251 376252 376253 366253 366254 356255 356255 346256 336257 " +
    "336258 326259 326259 31625a 31625b 31625c 30625d 30625d 2f625e 2f625f 2f6260 2f6261 2e6262 2e6262 2e6263 2e6164 2e6165 2e6166 2e6167 2f6168 2f6169 2f6069 30606a 30606b " +
    "31606c 31606d 325f6e 335f6e 335f6f 345e70 355e71 365e71 375e72 385d72 395d73 3a5d73 3b5c74 3c5c74 3c5c75 3d5b75 3e5b75 3f5b76 405b76 415a76 425a76 435a76 435977 445977 " +
    "455977 465977 465877 475877 485877 485877 495877 4a5777 4a5777 4b5777 4b5777 4c5777 4c5777 4d5677 4d5677 4d5677 4e5677 4e5677 4f5677 4f5677 4f5677 505577 505577 505577 " +
    "505577 515577 515577 525577 525576 535476 535476 545476 545476 555476 555476 565376 565375 575375 575375 585375 585375 595274 595274 5a5274 5a5274 5b5274 5b5273 5c5173 " +
    "5c5173 5c5173 5d5172 5d5172 5e5172 5e5172 5f5071 5f5071 605071 605070 605070 615070 61506f 624f6f 624f6f 624f6f 634f6e 634f6e 644f6e 644f6d 644f6d 654f6d 654e6c 654e6c " +
    "664e6c 664e6b 664e6b 664e6b 674e6a 674e6a 674e6a 684e69 684d69 684d69 684d68 694d68 694d68 694d68 694d67 6a4d67 6a4d67 6a4d66 6a4d66 6b4d66 6b4d65 6b4c65 6b4c64 6c4c64 " +
    "6c4c64 6c4c63 6c4c63 6d4c62 6d4c62 6d4c62 6d4c61 6e4c61 6e4c60 6e4c60 6e4c5f 6f4c5f 6f4c5e 6f4b5e 6f4b5d 704b5d 704b5c 704b5c 704b5b 704b5b 714b5a 714b5a 714b59 714b58 " +
    "714b58 724b57 724b57 724b56 724b55 724b55 734b54 734b54 734b53 734b52 734b52 734b51 734b51 734b50 734b4f 744b4f 744b4e 744b4d 744b4d 744b4c 744c4c 744c4b 744c4b 744c4a"
  ).split(" ");
  function validMode(value) { return value === "dark" ? "dark" : "light"; }
  function validPalette(value) {
    return Object.prototype.hasOwnProperty.call(palettes, value) ? value : "graphite";
  }
  function captureForeground() {
    if (!document.body || !document.body.querySelectorAll || typeof getComputedStyle !== "function") return [];
    var elements = [document.body].concat(Array.prototype.slice.call(document.body.querySelectorAll("*")));
    return elements.filter(function (element) {
      return element.animate && element.getClientRects().length;
    }).map(function (element) { return {element:element, color:getComputedStyle(element).color}; });
  }
  function animateForeground(snapshot) {
    // Read every destination before starting animations; descendant keyframes
    // must never use an ancestor's partially interpolated foreground color.
    var targets = snapshot.map(function (item) {
      var color = getComputedStyle(item.element).color;
      if (item.element.getAnimations) item.element.getAnimations().forEach(function (animation) {
        if (animation.transitionProperty === "color" && animation.effect) {
          var frames = animation.effect.getKeyframes();
          if (frames.length) color = frames[frames.length - 1].color || color;
        }
      });
      return color;
    });
    snapshot.forEach(function (item, index) {
      if (item.color === targets[index]) return;
      foregroundAnimations.push(item.element.animate([{color:item.color}, {color:targets[index]}],
        {duration:320, easing:"cubic-bezier(.4,0,.2,1)"}));
    });
  }
  function stopForeground() {
    foregroundAnimations.forEach(function (animation) { animation.cancel(); });
    foregroundAnimations = [];
  }
  function apply(state, options) {
    state = state || {};
    var mode = validMode(state.themeMode), palette = validPalette(state.darkPalette);
    var key = mode + "/" + palette;
    var instant = options && options.animate === false;
    if (key === appliedKey && !instant) return false;
    var root = document.documentElement, snapshot = [];
    if (root.classList && (instant || appliedKey && mode !== current.themeMode)) {
      var animate = !instant && document.body && !(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
      if (animate) snapshot = captureForeground();
      stopForeground();
      if (transitionTimer) clearTimeout(transitionTimer);
      transitionTimer = 0;
      if (animate) {
        root.classList.add("theme-changing");
        transitionTimer = setTimeout(function () {
          root.classList.remove("theme-changing"); stopForeground(); transitionTimer = 0;
        }, 380);
      } else root.classList.remove("theme-changing");
    }
    if (key === appliedKey) return false;
    appliedKey = key;
    current = { themeMode: mode, darkPalette: palette };
    root.dataset.theme = mode;
    root.dataset.darkPalette = palette;
    root.style.colorScheme = mode;
    animateForeground(snapshot);
    return true;
  }
  function nodeColor(hue) {
    hue = Number(hue);
    hue = Number.isFinite(hue) ? ((hue % 360) + 360) % 360 : 0;
    var p = palettes[current.darkPalette];
    // Perceptual lightness/chroma keep generated headers as quiet as built-ins.
    // The existing instance identity continues to select the same hue role.
    return current.themeMode === "dark"
      ? "oklch(" + p.lightness + "% " + p.chroma + " " + hue + ")"
      : "#" + lightNodeColors[Math.round(hue) % 360];
  }
  window.ChloraTheme = { apply: apply, validMode: validMode,
    validPalette: validPalette, nodeColor: nodeColor };
  apply(window.__MC_HOST_BOOT_THEME__ || {});
})();
