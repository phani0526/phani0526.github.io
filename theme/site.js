// Copy buttons on the speaker bios.
document.querySelectorAll("[data-copy]").forEach((button) => {
  button.addEventListener("click", async () => {
    const body = button.closest(".entry-body").cloneNode(true);
    body.querySelector("[data-copy]").remove();
    const text = body.innerText.trim().replace(/\n{3,}/g, "\n\n");
    try {
      await navigator.clipboard.writeText(text);
      button.textContent = "Copied";
    } catch {
      button.textContent = "Select and copy manually";
    }
    button.setAttribute("data-done", "");
    setTimeout(() => {
      button.textContent = "Copy text";
      button.removeAttribute("data-done");
    }, 2000);
  });
});

// Highlight the section you're reading in the sidebar.
const links = new Map(
  [...document.querySelectorAll(".nav a")].map((a) => [a.getAttribute("href").slice(1), a])
);
if ("IntersectionObserver" in window && links.size) {
  const observer = new IntersectionObserver(
    (items) => {
      items.forEach((item) => {
        if (!item.isIntersecting) return;
        links.forEach((a) => a.removeAttribute("aria-current"));
        links.get(item.target.id)?.setAttribute("aria-current", "true");
      });
    },
    { rootMargin: "-30% 0px -65% 0px" }
  );
  links.forEach((_, id) => {
    const section = document.getElementById(id);
    if (section) observer.observe(section);
  });
}
