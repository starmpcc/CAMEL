// Initialize Bootstrap tooltip
$(function() {
  $('[data-toggle="tooltip"]')
    .tooltip()
})

function showTooltip(btn, message) {
  btn.tooltip('hide')
    .attr('data-original-title', message)
    .tooltip('show');
}

function hideTooltip(btn) {
  setTimeout(function() {
    btn.tooltip('hide');
  }, 1000);
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function setTooltip(btn, tooltip, style) {
  btn.classList.remove('text-muted');
  btn.classList.add(style);
  btn.setAttribute('aria-label', tooltip);
  await sleep(1000);
  btn.classList.add('text-muted');
  btn.setAttribute('aria-label', 'Copy code to clipboard');
  btn.removeAttribute('data-original-title');
  btn.classList.remove(style);
}

// End helpers tooltip


// Insert buttons 
function ch_clipboard_setup() {
  var d = document;
  var els = d.querySelectorAll('pre');
  for (var i = 0; i < els.length; i++) {
    // Select all pre codes
    var preBlock = els[i];
    // Select first child	
    let codeBlock = preBlock.firstChild;

    // If first child is code
    if (codeBlock.tagName.toLowerCase() == 'code') {
      // Add id to code block
      codeBlock.setAttribute('id', 'clipboard_code' + i);
      // Create button			
      var btn = d.createElement('button');
      btn.classList.add('btn', 'text-muted', 'btn-sm', 'btn-chulapa-copy-code');
      btn.innerHTML = "<i class='far fa-copy'></i>";
      btn.id = 'clipboard_btn' + i;
      btn.type = 'button';
      btn.setAttribute('data-toggle', 'tooltip');
      btn.setAttribute('data-placement', 'left');
      btn.setAttribute('aria-label', 'Copy code to clipboard');
      //Function to copy to clipboard
      btn.onclick = ch_copy_cliboard(i);
      preBlock.prepend(btn);
    } else {
      console.log('No code block for\n' + preBlock.innerHTML);
    }
  }
}

function ch_copy_cliboard(i) {
  return function() {
    var d = document;
    // Select code content and strip HTML
    var codeBlock = d.getElementById('clipboard_code' + i)
      .innerHTML;
    codeBlockStripped = stripHtml(codeBlock);

    // Reset clipboard
    navigator.clipboard.writeText('');

    var btn = d.getElementById('clipboard_btn' + i);
    var btnTrigger = $(btn);

    // Set initial values

    let style = 'text-success';
    let msg = 'Copied on the clipboard:\n' + codeBlockStripped;
    let tooltip = 'Copied!';
    try {
      navigator.clipboard.writeText(codeBlockStripped);
    } catch {
      // Modify on error
      style = 'text-danger';
      tooltip = 'Error!';
      msg = 'Error when copying the code';
    }
    setTooltip(btn, tooltip, style);
    showTooltip(btnTrigger, tooltip);
    hideTooltip(btnTrigger);
    console.log(msg);
  }
}
// stripHtml safely
function stripHtml(html){
   let tmp = document.createElement('DIV');
   tmp.innerHTML = html;
   return tmp.textContent || tmp.innerText || '';
}

window.addEventListener('load', ch_clipboard_setup);
