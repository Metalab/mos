document.querySelectorAll("fieldset.module").forEach(function (e) {
  const header = e.querySelector("h2");
  if (header) {
    const key = header.innerText;
    header.style = "cursor: pointer"
    function applyState() {
      header.innerHTML = (localStorage.getItem(key) ? '▸ ' : '▾ ') + key;
      e.querySelectorAll("div.form-row, table").forEach((element) => {
        if (!localStorage.getItem(key)) {
          element.classList.remove("hidden");
        } else {
          element.classList.add("hidden");
        }
      });
    }
    applyState();
    header.addEventListener("click", (event) => {
      if (localStorage.getItem(key)) {
        localStorage.removeItem(key);
      } else {
        localStorage.setItem(key, true);
      }
      applyState();
    });
  }
});
