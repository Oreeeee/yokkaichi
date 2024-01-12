import "@picocss/pico/css/pico.min.css"
import "./style.css"

class Footer extends HTMLElement {
  constructor() {
    super()
  }

  connectedCallback() {
    this.innerHTML = "<center>Yokkaichi v1.7</center>"
  }
}

customElements.define("yokkaichi-footer", Footer)
