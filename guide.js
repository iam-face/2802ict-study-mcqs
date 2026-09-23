const guide = document.getElementById("guide");

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function slug(text) {
  return text
    .trim()
    .toLowerCase()
    .replace(/[^\w\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-");
}

function inline(text) {
  let html = escapeHtml(text);
  html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (match, label, href) => {
    let target = href;
    if (target === "Study%20MCQs.md" || target === "Study MCQs.md") {
      target = "index.html";
    }
    return `<a href="${target}">${label}</a>`;
  });
  html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/\*([^*]+)\*/g, "<em>$1</em>");
  return html;
}

function isBlockStart(line) {
  return (
    line.startsWith("```")
    || line.startsWith("|")
    || line.startsWith("#")
    || line.trim() === "---"
    || /^[-*] /.test(line)
    || /^\d+\. /.test(line)
  );
}

function renderTable(rows) {
  const parsed = rows.map((row) => row.split("|").slice(1, -1).map((cell) => cell.trim()));
  const bodyRows = parsed.filter((cells) => cells.length && !cells.every((cell) => /^:?-+:?$/.test(cell)));
  if (!bodyRows.length) {
    return "";
  }
  const head = bodyRows[0].map((cell) => `<th>${inline(cell)}</th>`).join("");
  const body = bodyRows.slice(1).map((cells) => (
    `<tr>${cells.map((cell) => `<td>${inline(cell)}</td>`).join("")}</tr>`
  )).join("");
  return `<div class="table-wrap"><table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table></div>`;
}

function renderMarkdown(source) {
  const lines = source.replace(/\r\n/g, "\n").split("\n");
  const out = [];
  let i = 0;
  while (i < lines.length) {
    const line = lines[i];
    if (line.startsWith("```")) {
      const buf = [];
      i += 1;
      while (i < lines.length && !lines[i].startsWith("```")) {
        buf.push(lines[i]);
        i += 1;
      }
      i += 1;
      out.push(`<pre><code>${escapeHtml(buf.join("\n"))}</code></pre>`);
      continue;
    }
    if (line.trim() === "---") {
      out.push("<hr>");
      i += 1;
      continue;
    }
    if (line.startsWith("|")) {
      const rows = [];
      while (i < lines.length && lines[i].startsWith("|")) {
        rows.push(lines[i]);
        i += 1;
      }
      out.push(renderTable(rows));
      continue;
    }
    const heading = /^(#{1,3}) (.+)$/.exec(line);
    if (heading) {
      const level = heading[1].length;
      const text = heading[2].trim();
      out.push(`<h${level} id="${slug(text)}">${inline(text)}</h${level}>`);
      i += 1;
      continue;
    }
    if (/^[-*] /.test(line)) {
      const items = [];
      while (i < lines.length && /^[-*] /.test(lines[i])) {
        items.push(`<li>${inline(lines[i].slice(2))}</li>`);
        i += 1;
      }
      out.push(`<ul>${items.join("")}</ul>`);
      continue;
    }
    if (/^\d+\. /.test(line)) {
      const items = [];
      while (i < lines.length && /^\d+\. /.test(lines[i])) {
        items.push(`<li>${inline(lines[i].replace(/^\d+\. /, ""))}</li>`);
        i += 1;
      }
      out.push(`<ol>${items.join("")}</ol>`);
      continue;
    }
    if (!line.trim()) {
      i += 1;
      continue;
    }
    const para = [line.trim()];
    i += 1;
    while (i < lines.length && lines[i].trim() && !isBlockStart(lines[i])) {
      para.push(lines[i].trim());
      i += 1;
    }
    out.push(`<p>${inline(para.join(" "))}</p>`);
  }
  return out.join("\n");
}

async function init() {
  try {
    const response = await fetch("study-guide.md");
    if (!response.ok) {
      throw new Error(`Could not load study-guide.md (${response.status})`);
    }
    guide.innerHTML = renderMarkdown(await response.text());
  } catch (err) {
    guide.innerHTML = `<h1>Study guide</h1><p class="error">${escapeHtml(err.message)}</p>
      <p class="hint">Open this folder through a local server or GitHub Pages. A file:// address cannot load the guide.</p>`;
  }
}

init();
