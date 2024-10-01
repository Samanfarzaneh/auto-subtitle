document.getElementById('load-srt').addEventListener('click', function() {
    const fileInput = document.getElementById('srt-file');
    const video = document.getElementById('video');
    const subtitleContainer = document.getElementById('subtitle-container');
    const subtitleEdit = document.getElementById('subtitle-edit');
    const downloadButton = document.getElementById('download-srt');
    let subtitles = []; // برای ذخیره زیرنویس‌ها

    if (fileInput.files.length > 0) {
        const file = fileInput.files[0];
        const reader = new FileReader();

        reader.onload = function(e) {
            const srtData = e.target.result;
            subtitles = parseSRT(srtData); // ذخیره زیرنویس‌ها
            displaySubtitles(subtitles);
            downloadButton.style.display = 'inline'; // نمایش دکمه دانلود
        };

        reader.readAsText(file);
    }

    function parseSRT(data) {
        const lines = data.split('\n');
        const subtitles = [];
        let i = 0;

        while (i < lines.length) {
            if (lines[i].trim() === '') {
                i++;
                continue;
            }

            const index = lines[i++];
            const timeLine = lines[i++];
            const text = [];

            while (i < lines.length && lines[i].trim() !== '') {
                text.push(lines[i++]);
            }

            const time = timeLine.split(' --> ');
            subtitles.push({
                start: parseTime(time[0]),
                end: parseTime(time[1]),
                text: text.join('<br>')
            });
        }

        return subtitles;
    }

    function parseTime(time) {
        const parts = time.split(':');
        const seconds = parseFloat(parts[2].replace(',', '.'));
        return (parseInt(parts[0]) * 3600) + (parseInt(parts[1]) * 60) + seconds;
    }

    function displaySubtitles(subtitles) {
        video.ontimeupdate = function() {
            const currentTime = video.currentTime;
            subtitleContainer.innerHTML = '';
            subtitleEdit.style.display = 'block'; // نمایش textarea

            subtitles.forEach(sub => {
                if (currentTime >= sub.start && currentTime <= sub.end) {
                    subtitleEdit.value = sub.text.replace(/<br>/g, '\n'); // نمایش زیرنویس برای ویرایش
                    subtitleContainer.innerHTML = sub.text; // نمایش زیرنویس روی ویدیو
                }
            });

            // به‌روزرسانی زیرنویس با متن ویرایش شده
            subtitleEdit.oninput = function() {
                subtitleContainer.innerHTML = subtitleEdit.value.replace(/\n/g, '<br>'); // بروزرسانی زیرنویس
                subtitles.forEach(sub => {
                    if (currentTime >= sub.start && currentTime <= sub.end) {
                        sub.text = subtitleEdit.value.replace(/\n/g, '<br>'); // ذخیره تغییرات در حافظه
                    }
                });
            };
        };
    }

    // دانلود زیرنویس اصلاح شده
    downloadButton.addEventListener('click', function() {
        const srtData = generateSRT(subtitles);
        const blob = new Blob([srtData], { type: 'text/srt' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'modified_subtitles.srt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    });

    // تولید فایل SRT از زیرنویس‌ها
    function generateSRT(subtitles) {
        return subtitles.map((sub, index) => {
            return `${index + 1}\n${formatTime(sub.start)} --> ${formatTime(sub.end)}\n${sub.text}\n`;
        }).join('\n');
    }

    function formatTime(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = Math.floor(seconds % 60);
        const milliseconds = Math.floor((seconds % 1) * 1000);
        return `${pad(hours)}:${pad(minutes)}:${pad(secs)},${pad(milliseconds, 3)}`;
    }

    function pad(num, size = 2) {
        let s = "000" + num;
        return s.substr(s.length - size);
    }
});

// تغییر رنگ زیرنویس به صورت real-time
document.getElementById('subtitle-color').addEventListener('input', function() {
    const subtitleContainer = document.getElementById('subtitle-container');
    subtitleContainer.style.color = this.value; // تغییر رنگ متن زیرنویس
});

// تغییر رنگ استروک به صورت real-time
document.getElementById('stroke-color').addEventListener('input', function() {
    updateStroke(); // بروزرسانی استروک
});

// تغییر اندازه استروک به صورت real-time
document.getElementById('stroke-size').addEventListener('input', function() {
    updateStroke(); // بروزرسانی استروک
});

// تغییر رنگ سایه به صورت real-time
document.getElementById('shadow-color').addEventListener('input', function() {
    updateShadow(); // بروزرسانی سایه
});

// تغییر اندازه سایه به صورت real-time
document.getElementById('shadow-size').addEventListener('input', function() {
    updateShadow(); // بروزرسانی سایه
});

// تغییر اندازه فونت به صورت real-time
document.getElementById('font-size').addEventListener('input', function() {
    const subtitleContainer = document.getElementById('subtitle-container');
    subtitleContainer.style.fontSize = this.value + 'px'; // تغییر اندازه فونت
});

// مدیریت سایه متن
