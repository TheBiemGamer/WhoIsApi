document.body.classList.add("dark-theme");

function parseDateString(dateStr) {
  let parsed = Date.parse(dateStr);
  if (!isNaN(parsed)) {
    return new Date(parsed).toLocaleString();
  }
  if (dateStr.indexOf("/") !== -1) {
    let parts = dateStr.split(",");
    let datePart = parts[0].trim();
    let timePart = parts[1] ? parts[1].trim() : "00:00:00";
    let dateComponents = datePart.split("/");
    if (dateComponents.length === 3) {
      let [day, month, year] = dateComponents;
      day = day.padStart(2, "0");
      month = month.padStart(2, "0");
      let isoString = `${year}-${month}-${day}T${timePart}`;
      parsed = Date.parse(isoString);
      if (!isNaN(parsed)) {
        return new Date(parsed).toLocaleString();
      }
    }
  }
  return dateStr;
}

function formatDateField(value) {
  if (Array.isArray(value)) {
    return parseDateString(value[0]);
  }
  return parseDateString(value);
}

function formatDefaultField(value) {
  if (Array.isArray(value)) {
    return value.join(", ");
  }
  return value;
}

function parseWhoisData(data) {
  const fields = [
    {
      key: "domain_name",
      label: "Domain Name",
      icon: "fa-globe",
      type: "default",
    },
    {
      key: "registrar",
      label: "Registrar",
      icon: "fa-building",
      type: "default",
    },
    {
      key: "creation_date",
      label: "Creation Date",
      icon: "fa-calendar-plus",
      type: "date",
    },
    {
      key: "expiration_date",
      label: "Expiration Date",
      icon: "fa-calendar-times",
      type: "date",
    },
    {
      key: "updated_date",
      label: "Updated Date",
      icon: "fa-calendar-check",
      type: "date",
    },
    {
      key: "name_servers",
      label: "Name Servers",
      icon: "fa-server",
      type: "default",
    },
    { key: "emails", label: "Emails", icon: "fa-envelope", type: "default" },
    { key: "status", label: "Status", icon: "fa-info-circle", type: "default" },
    { key: "dnssec", label: "DNSSEC", icon: "fa-shield-alt", type: "default" },
  ];

  let html = '<h3>WHOIS Data:</h3><div class="whois-info">';
  fields.forEach((field) => {
    if (data[field.key]) {
      let formattedValue;
      if (field.type === "date") {
        formattedValue = formatDateField(data[field.key]);
      } else {
        formattedValue = formatDefaultField(data[field.key]);
      }
      html += `<div class="whois-field">
                <i class="fas ${field.icon} field-icon"></i>
                <span class="field-label">${field.label}:</span>
                <span class="field-value">${formattedValue}</span>
              </div>`;
    }
  });
  html += "</div>";
  return html;
}

async function fetchWhois() {
  const domain = document.getElementById("domain").value.trim();
  const resultDiv = document.getElementById("result");
  const loadingDiv = document.getElementById("loading");

  resultDiv.innerHTML = "";
  resultDiv.classList.remove("show");

  loadingDiv.classList.add("active");

  if (!domain) {
    resultDiv.innerHTML = '<p class="error">Please enter a domain name.</p>';
    resultDiv.classList.add("show");
    loadingDiv.classList.remove("active");
    return;
  }

  try {
    const response = await fetch(`/whois?domain=${domain}`);
    const data = await response.json();

    if (response.ok) {
      resultDiv.innerHTML = parseWhoisData(data);
    } else {
      resultDiv.innerHTML = `<p class="error">${
        data.error || "An error occurred."
      }</p>`;
    }
  } catch (error) {
    resultDiv.innerHTML =
      '<p class="error">Failed to fetch WHOIS data. Please try again.</p>';
  } finally {
    loadingDiv.classList.remove("active");
    setTimeout(() => {
      resultDiv.classList.add("show");
    }, 100);
  }
}

document
  .getElementById("domain")
  .addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
      fetchWhois();
    }
  });

function toggleTheme() {
  const body = document.body;
  if (body.classList.contains("dark-theme")) {
    body.classList.remove("dark-theme");
    body.classList.add("light-theme");
  } else {
    body.classList.remove("light-theme");
    body.classList.add("dark-theme");
  }
}
