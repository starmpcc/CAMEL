var sT = document.getElementById("sidetoc");
var btn = document.getElementById("demo");
var body = document.getElementById("body");
var main = document.getElementById("maincontent");
var heads = main.querySelectorAll("h1, h2, h3, h4, h5 , h6");
var els = main.querySelectorAll("pre");

// First load sidebar
// Create hidden overlay
var iDiv = document.createElement("div");
if (sT) {
  btn.style.marginLeft = "0";
  iDiv.classList.add("bs-canvas-overlay", "bg-dark", "position-fixed",
    "w-100", "h-100");
  iDiv.setAttribute("id", "sideBarOverlay");
  iDiv.setAttribute("onclick", "closeSideBar()");
  body.prepend(iDiv);
} else if (btn) {
  // ToC was requested but no toc produced
  // Clean up DOM
  btn.remove();
  document.getElementById("sideBar")
    .remove();
}

function openSideBar() {
  btn.removeAttribute("style");
  btn.setAttribute("aria-expanded", "true");
  document.getElementById("sideBarOverlay")
    .classList.add("show");
  document.getElementById("sideBar")
    .style.marginLeft = "0";
}

function closeSideBar() {
  document.getElementById("sideBar")
    .removeAttribute("style");
  document.getElementById("sideBarOverlay")
    .classList.remove("show");
  btn.style.marginLeft = "0";
  btn.setAttribute("aria-expanded", "false");
}

// Put anchors on headings
heads.forEach(function (currentValue) {
  thish = currentValue;
  id = thish.id;
  if (id) {
    anchor = document.createElement("a");
    sp = document.createElement("span");
    ic = document.createElement("i");
    anchor.classList.add("chulapa-header-link", "ml-2",
      "chulapaDateSocial");
    anchor.href = "#" + id;
    sp.innerHTML = "Permalink";
    sp.classList.add("sr-only");
    ic.classList.add("fas", "fa-link", "fa-2xs", "align-middle");
    anchor.append(sp, ic);
    anchor.title = "Permalink";
    thish.append(anchor);
  } else {
    console.log("Heading :" + thish.innerHTML +
      " does not have id. Can't place anchor here");
  }
});

// Copy Clipboard
// Insert buttons

els.forEach(function (currentValue, currentIndex) {
  preBlock = currentValue;
  i = currentIndex;
  // Select first child
  codeBlock = preBlock.firstChild;
  // If first child is code
  if (codeBlock.tagName.toLowerCase() == "code") {
    // Add br is no native
    hashigh = preBlock.classList.contains("highlight");
    if (hashigh === false){
      preBlock.classList.add("highlight");
      brk = document.createElement("br");
      codeBlock.prepend(brk);
    }
    // Add id to code block
    codeBlock.setAttribute("id", "clipboard_code" + i);
    // Create button
    copybtn = document.createElement("button");
    copybtn.classList.add("btn", "text-muted", "btn-sm",
      "btn-chulapa-copy-code");
    copybtn.innerHTML = "<i class='far fa-copy'></i>";
    copybtn.id = "clipboard_btn" + i;
    copybtn.type = "button";
    copybtn.setAttribute("data-toggle", "tooltip");
    copybtn.setAttribute("data-placement", "left");
    copybtn.setAttribute("aria-label", "Copy code to clipboard");
    //Function to copy to clipboard
    copybtn.onclick = ch_copy_cliboard(i);
    preBlock.prepend(copybtn);
  } else {
    console.log("No code block for\n" + preBlock.innerHTML);
  }

});

// Initialize Bootstrap tooltip
$(function () {
  $("[data-toggle='tooltip']")
    .tooltip();
})

function showTooltip(thisbtn, message) {
  thisbtn.tooltip("hide")
    .attr("data-original-title", message)
    .tooltip("show");
}

function hideTooltip(thisbtn) {
  setTimeout(function () {
    thisbtn.tooltip("hide");
  }, 1000);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function setTooltip(thisbtn, tooltip, style) {
  thisbtn.classList.remove("text-muted");
  thisbtn.classList.add(style);
  thisbtn.setAttribute("aria-label", tooltip);
  await sleep(1000);
  thisbtn.classList.add("text-muted");
  thisbtn.setAttribute("aria-label", "Copy code to clipboard");
  thisbtn.removeAttribute("data-original-title");
  thisbtn.classList.remove(style);
}

function ch_copy_cliboard(i) {
  return function () {
    // Select code content and strip HTML
    let thisCodeBlock = document.getElementById("clipboard_code" + i)
      .innerHTML;
    codeBlockStripped = stripHtml(thisCodeBlock);

    // Reset clipboard
    navigator.clipboard.writeText("");

    thiscopybtn = document.getElementById("clipboard_btn" + i);
    btnTrigger = $(thiscopybtn);

    // Set initial values

    style = "text-success";
    msg = "Copied on the clipboard:\n" + codeBlockStripped;
    tooltip = "Copied!";
    try {
      navigator.clipboard.writeText(codeBlockStripped);
    } catch {
      // Modify on error
      style = "text-danger";
      tooltip = "Error!";
      msg = "Error when copying the code";
    }
    setTooltip(thiscopybtn, tooltip, style);
    showTooltip(btnTrigger, tooltip);
    hideTooltip(btnTrigger);
    console.log(msg);
  }
}
// stripHtml safely
function stripHtml(html) {
  let tmp = document.createElement("DIV");
  tmp.innerHTML = html;
  return tmp.textContent || tmp.innerText || "";
}
