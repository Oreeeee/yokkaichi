import "@picocss/pico/css/pico.min.css";
import "./style.css";

class Footer extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    this.innerHTML = "<center>Yokkaichi v1.7</center>";
  }
}

class Header extends HTMLElement {
  constructor() {
    super();
  }

  connectedCallback() {
    this.innerHTML = `<center><h1>${document.title}</h1></center>`;
  }
}

customElements.define("yokkaichi-header", Header);
customElements.define("yokkaichi-footer", Footer);
