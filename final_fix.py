"""
Final fix script to completely rebuild the HTML file
"""
import os
import re

def fix_html():
    html_path = os.path.join('templates', 'index.html')
    
    # We will reconstruct the file from scratch using known good parts
    # This is safer than trying to patch a corrupted file
    
    # 1. Read the current file to extract the body content (excluding script)
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Extract everything before the script tag
    script_start = content.find('<script>')
    if script_start == -1:
        print("Could not find script tag")
        return
        
    html_part = content[:script_start]
    
    # If html_part is duplicated (contains multiple </html>), take the first one
    if html_part.count('<div class="app-container">') > 1:
        first_container = html_part.find('<div class="app-container">')
        second_container = html_part.find('<div class="app-container">', first_container + 1)
        html_part = html_part[:second_container]
        # Clean up closing tags if needed
        if '</body>' in html_part:
            html_part = html_part[:html_part.find('</body>')]
            
    # Remove any closing body/html tags from html_part to be safe
    html_part = html_part.replace('</body>', '').replace('</html>', '')
    
    # 2. Define the correct script content
    script_content = """<script>
    let audioContext, analyser, dataArray;
    let isVisualizerInit = false;
    let currentTrackList = [];
    let currentTrackIndex = 0;

    async function loadLibrary() {
        try {
            const response = await fetch('/stats');
            const data = await response.json();
            const list = document.getElementById('library-list');
            list.innerHTML = '';
            
            // Sort by newest first (assuming the backend returns them in order or has a date)
            // For now, just reverse if needed, or use as is.
            // Let's assume data.tracks is the list
            
            if (data.tracks && data.tracks.length > 0) {
                currentTrackList = data.tracks;
                data.tracks.forEach((track, index) => {
                    const li = document.createElement('li');
                    li.className = 'library-item';
                    li.onclick = () => playTrack(track);
                    li.innerHTML = `
                        <div class="item-cover">
                            <i class="fas fa-music"></i>
                        </div>
                        <div class="item-info">
                            <div class="item-title">${track.title}</div>
                            <div class="item-artist">${track.artist || 'Unknown Artist'}</div>
                        </div>
                        <div class="item-duration">3:45</div>
                    `;
                    list.appendChild(li);
                });
                
                // Load first track if not playing
                if (document.getElementById('audio-player').paused && currentTrackList.length > 0) {
                    // updatePlayerUI(currentTrackList[0]);
                }
            }
        } catch (e) {
            console.error('Error loading library:', e);
        }
    }

    function playTrack(track) {
        const audio = document.getElementById('audio-player');
        currentTrackIndex = currentTrackList.findIndex(t => t.path === track.path);
        if (!isVisualizerInit) initVisualizer();
        audio.src = `/play/${encodeURIComponent(track.path)}`;
        audio.play().catch(e => console.error('Playback error:', e));
        updatePlayerUI(track);
    }

    function togglePlay() {
        const audio = document.getElementById('audio-player');
        const icon = document.querySelector('#main-play-btn i');
        if (audio.paused) {
            audio.play();
            icon.className = 'fas fa-pause-circle';
        } else {
            audio.pause();
            icon.className = 'fas fa-play-circle';
        }
    }

    function playNextTrack() {
        if (currentTrackList.length === 0) return;
        currentTrackIndex = (currentTrackIndex + 1) % currentTrackList.length;
        playTrack(currentTrackList[currentTrackIndex]);
    }

    function playAll() {
        if (currentTrackList && currentTrackList.length > 0) {
            currentTrackIndex = 0;
            playTrack(currentTrackList[0]);
        }
    }

    function toggleSidebar() {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('mobile-overlay');
        sidebar.classList.toggle('mobile-open');
        overlay.classList.toggle('active');
    }

    async function startDownload() {
        const url = document.getElementById('spotify-url').value.trim();
        const statusArea = document.getElementById('status-area');
        const statusText = document.getElementById('status-text');
        
        if (!url) return;
        
        statusArea.classList.remove('hidden');
        statusText.innerText = "Starting...";
        
        try {
            const response = await fetch('/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    url: url
                })
            });
            
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            
            while (true) {
                const { done, value } = await reader.read();
                if (done) break;
                
                const chunk = decoder.decode(value);
                const lines = chunk.split('\\n');
                
                for (const line of lines) {
                    if (line.trim()) {
                        try {
                            const data = JSON.parse(line);
                            if (data.message) statusText.innerText = data.message;
                            if (data.status === 'completed') loadLibrary();
                        } catch (e) { }
                    }
                }
            }
            
            statusText.innerText = "Done!";
            setTimeout(() => statusArea.classList.add('hidden'), 3000);
        } catch (e) {
            console.error(e);
            statusText.innerText = "Error";
        }
    }

    const audioPlayer = document.getElementById('audio-player');
    const progressBar = document.querySelector('.progress-bar-fill');
    const currTime = document.querySelector('.time.current');
    const totalTime = document.querySelector('.time.total');

    audioPlayer.addEventListener('loadedmetadata', () => {
        totalTime.innerText = formatTime(audioPlayer.duration);
    });

    audioPlayer.addEventListener('timeupdate', () => {
        const {
            currentTime,
            duration
        } = audioPlayer;
        if (isNaN(duration)) return;
        progressBar.style.width = `${(currentTime / duration) * 100}%`;
        currTime.innerText = formatTime(currentTime);
    });

    audioPlayer.addEventListener('ended', () => {
        playNextTrack();
    });

    function formatTime(time) {
        if (time && !isNaN(time)) {
            const min = Math.floor(time / 60);
            const sec = Math.floor(time % 60);
            return `${min}:${sec < 10 ? '0' : ''}${sec}`;
        }
        return '0:00';
    }

    function initVisualizer() {
        if (isVisualizerInit) return;
        try {
            const audio = document.getElementById('audio-player');
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            analyser = audioContext.createAnalyser();
            const source = audioContext.createMediaElementSource(audio);
            source.connect(analyser);
            analyser.connect(audioContext.destination);
            analyser.fftSize = 128;
            const bufferLength = analyser.frequencyBinCount;
            dataArray = new Uint8Array(bufferLength);
            isVisualizerInit = true;
            animateWaveform();
        } catch (e) {
            console.error('Visualizer init error:', e);
        }
    }

    function animateWaveform() {
        requestAnimationFrame(animateWaveform);
        if (!analyser) return;
        const canvas = document.getElementById('waveform-canvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const radius = 85;
        analyser.getByteFrequencyData(dataArray);
        ctx.clearRect(0, 0, canvas.width, canvas.height); // Draw circular waveform 
        const bars = 48;
        const angleStep = (Math.PI * 2) / bars;
        for (let i = 0; i < bars; i++) {
            const angle = i * angleStep - Math.PI / 2;
            const dataIndex = Math.floor(i * dataArray.length / bars);
            const amplitude = dataArray[dataIndex] / 255;
            const barLength = 15 + amplitude * 25;
            const x1 = centerX + Math.cos(angle) * radius;
            const y1 = centerY + Math.sin(angle) * radius;
            const x2 = centerX + Math.cos(angle) * (radius + barLength);
            const y2 = centerY + Math.sin(angle) * (radius + barLength); // Gradient color based on amplitude 
            const hue = 280 + amplitude * 60;
            ctx.strokeStyle = `hsl(${hue}, 80%, ${50 + amplitude * 30}%)`;
            ctx.lineWidth = 3.5;
            ctx.lineCap = 'round';
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.lineTo(x2, y2);
            ctx.stroke();
        } // Draw glow effect 
        ctx.shadowBlur = 20;
        ctx.shadowColor = '#A855F7'; // Draw outer ring 
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius - 3, 0, Math.PI * 2);
        ctx.strokeStyle = 'rgba(168, 85, 247, 0.4)';
        ctx.lineWidth = 2;
        ctx.stroke();
        ctx.shadowBlur = 0;
    }

    function updatePlayerUI(track) {
        const coverImg = document.getElementById('np-cover');
        const icon = document.querySelector('.now-playing-cover i');
        const title = document.getElementById('np-title');
        const artist = document.getElementById('np-artist');

        if (title) title.innerText = track.title;
        if (artist) artist.innerText = track.artist || 'Unknown Artist';

        if (coverImg && icon) {
            const coverUrl = `/cover/${encodeURIComponent(track.path)}`;
            coverImg.src = coverUrl;
            coverImg.style.display = 'block';
            icon.style.display = 'none';

            coverImg.onerror = () => {
                coverImg.style.display = 'none';
                icon.style.display = 'flex';
            };
        }

        // Update window title
        document.title = `${track.title} • Jarama Music`;

        // Highlight in list
        document.querySelectorAll('.track-table tbody tr').forEach(tr => tr.classList.remove('playing'));
        // const rows = document.querySelectorAll('.track-table tbody tr');
        // if (rows[currentTrackIndex]) rows[currentTrackIndex].classList.add('playing');
    }

    loadLibrary();

    // ============================================
    // PWA - Service Worker Registration
    // ============================================
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/static/sw.js')
                .then((registration) => {
                    console.log('✓ Service Worker registered successfully:', registration.scope);

                    // Check for updates periodically
                    setInterval(() => {
                        registration.update();
                    }, 60000); // Check every minute
                })
                .catch((error) => {
                    console.log('✗ Service Worker registration failed:', error);
                });
        });

        // Listen for service worker updates
        navigator.serviceWorker.addEventListener('controllerchange', () => {
            console.log('Service Worker updated, reloading page...');
            window.location.reload();
        });
    }

    // PWA Install Prompt
    let deferredPrompt;
    window.addEventListener('beforeinstallprompt', (e) => {
        // Prevent the mini-infobar from appearing on mobile
        e.preventDefault();
        // Stash the event so it can be triggered later
        deferredPrompt = e;
        console.log('PWA install prompt available');
    });

    window.addEventListener('appinstalled', () => {
        console.log('✓ PWA was installed successfully');
        deferredPrompt = null;
    });

    // Optional: Function to trigger install prompt
    function installPWA() {
        if (deferredPrompt) {
            deferredPrompt.prompt();
            deferredPrompt.userChoice.then((choiceResult) => {
                deferredPrompt = null;
            });
        }
    }
</script>
</body>
</html>"""

    # Combine parts
    final_content = html_part + script_content
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
        
    print("✓ HTML completely rebuilt and fixed!")

if __name__ == "__main__":
    fix_html()
