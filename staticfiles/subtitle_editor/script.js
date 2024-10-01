document.getElementById('subtitleFile').addEventListener('change', function(event) {
    const file = event.target.files[0];
    const reader = new FileReader();

    reader.onload = function(e) {
        const content = e.target.result;
        displaySubtitle(content);
    };

    reader.readAsText(file);
});

function displaySubtitle(content) {
    const subtitleEditor = document.getElementById('subtitleEditor');
    const lines = content.split('\n');
    subtitleEditor.innerHTML = ''; // Clear previous content

    lines.forEach((line, index) => {
        const div = document.createElement('div');
        div.contentEditable = true;
        div.className = 'subtitle-line';
        div.textContent = line;
        subtitleEditor.appendChild(div);
    });
}

document.getElementById('downloadBtn').addEventListener('click', function() {
    const subtitleLines = document.getElementsByClassName('subtitle-line');
    let subtitleText = '';

    for (let line of subtitleLines) {
        subtitleText += line.textContent + '\n';
    }

    downloadSubtitle(subtitleText);
});

function downloadSubtitle(content) {
    const blob = new Blob([content], { type: 'text/plain' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'edited_subtitle.srt';
    link.click();
}
