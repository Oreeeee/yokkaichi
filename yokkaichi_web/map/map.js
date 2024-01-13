import "leaflet/dist/leaflet.css";
import L from "leaflet";
import "./map.css";

var serverIcon = L.icon({ iconUrl: "./server-icon.png" });

function standardMap() {
  var map = L.map("standard-map").setView([0.0, 0.0], 1);

  console.log(serverIcon);
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);

  L.marker([0.0, 0.0], { icon: serverIcon }).addTo(map);
}

function heatmap() {
  // TODO: add a real heatmap there
  var map = L.map("heatmap").setView([0.0, 0.0], 1);

  console.log(serverIcon);
  L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);

  L.marker([0.0, 0.0], { icon: serverIcon }).addTo(map);
}

standardMap();
heatmap();
