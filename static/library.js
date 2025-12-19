// Library management variables
let libraryData = null;
let currentView = 'playlists'; // 'playlists' or 'artists'

// Load library data from server
async function loadLibrary() {
    try {
        const response = await fetch('/stats');
        const data = await response.json();
        libraryData = data;

        const trackListBody = document.getElementById('track-list-body');
        const headerCount = document.getElementById('header-count');

        trackListBody.innerHTML = '';

        if (data.tracks && data.tracks.length > 0) {
            currentTrackList = data.tracks;

            // Update header count
            headerCount.innerText = `${data.tracks.length} songs`;

            // Populate main track table with all tracks
            populateTrackTable(data.tracks);
        }

        // Update sidebar based on current view
        updateSidebar();
    } catch (e) {
        console.error('Error loading library:', e);
    }
}

// Update sidebar based on current view (playlists or artists)
function updateSidebar() {
    if (!libraryData) return;

    const list = document.getElementById('library-list');
    list.innerHTML = '';

    if (currentView === 'playlists') {
        // Show folders (playlists/albums/artists)
        Object.keys(libraryData.library).sort().forEach(folderName => {
            const tracks = libraryData.library[folderName];
            if (tracks.length === 0) return;

            const li = document.createElement('li');
            li.className = 'library-item folder-item';
            li.onclick = () => showFolderTracks(folderName, tracks);
            li.innerHTML = `
                <div class="lib-img">
                    <i class="fas fa-folder"></i>
                </div>
                <div class="lib-text">
                    <div class="lib-title">${folderName}</div>
                    <div class="lib-desc">${tracks.length} song${tracks.length !== 1 ? 's' : ''}</div>
                </div>
            `;
            list.appendChild(li);
        });
    } else if (currentView === 'artists') {
        // Group by artist
        const artistMap = {};
        libraryData.tracks.forEach(track => {
            const artist = track.artist || 'Unknown Artist';
            if (!artistMap[artist]) {
                artistMap[artist] = [];
            }
            artistMap[artist].push(track);
        });

        Object.keys(artistMap).sort().forEach(artist => {
            const tracks = artistMap[artist];
            const li = document.createElement('li');
            li.className = 'library-item artist-item';
            li.onclick = () => showArtistTracks(artist, tracks);
            li.innerHTML = `
                <div class="lib-img">
                    <i class="fas fa-user-music"></i>
                </div>
                <div class="lib-text">
                    <div class="lib-title">${artist}</div>
                    <div class="lib-desc">${tracks.length} song${tracks.length !== 1 ? 's' : ''}</div>
                </div>
            `;
            list.appendChild(li);
        });
    }
}

// Switch between playlists and artists view
function switchView(view) {
    currentView = view;

    // Update active chip
    document.querySelectorAll('.library-filters .chip').forEach(chip => {
        chip.classList.remove('active');
    });
    event.target.classList.add('active');

    updateSidebar();
}

// Clean title - extract only song name, remove artists
function cleanTitle(title) {
    if (!title) return 'Unknown Track';

    // Remove everything after common separators
    let cleaned = title;

    // Remove artist names in parentheses or brackets
    cleaned = cleaned.replace(/\s*[\(\[].*?[\)\]]\s*/g, ' ');

    // Remove "feat.", "ft.", "featuring" and everything after
    cleaned = cleaned.replace(/\s*(feat\.|ft\.|featuring).*$/i, '');

    // Remove multiple artists separated by commas (keep only first part before comma)
    if (cleaned.includes(',')) {
        cleaned = cleaned.split(',')[0];
    }

    // Trim whitespace
    cleaned = cleaned.trim();

    return cleaned || title; // Return original if cleaning resulted in empty string
}

// Populate track table
function populateTrackTable(tracks) {
    const trackListBody = document.getElementById('track-list-body');
    trackListBody.innerHTML = '';

    tracks.forEach((track, index) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td class="col-index">${index + 1}</td>
            <td class="col-title">
                <div class="track-flex">
                    <div class="track-img">
                        <i class="fas fa-music"></i>
                    </div>
                    <div class="track-details">
                        <div class="t-name">${cleanTitle(track.title)}</div>
                    </div>
                </div>
            </td>
            <td class="col-album">${track.album || 'Unknown Album'}</td>
            <td class="col-date">Recently</td>
            <td class="col-duration">
                <div style="display: flex; align-items: center; gap: 12px; justify-content: flex-end;">
                    <span>${track.duration || '0:00'}</span>
                    <button class="download-track-btn" onclick="downloadTrack('${track.path.replace(/'/g, "\\'")}', event)" title="Download to device">
                        <i class="fas fa-download"></i>
                    </button>
                </div>
            </td>
        `;
        tr.onclick = (e) => {
            if (!e.target.closest('.download-track-btn')) {
                playTrack(track);
            }
        };
        trackListBody.appendChild(tr);
    });
}

// Show tracks from a specific folder
function showFolderTracks(folderName, tracks) {
    const headerTitle = document.getElementById('header-title');
    const headerDesc = document.getElementById('header-desc');
    const headerCount = document.getElementById('header-count');

    headerTitle.innerText = folderName;
    headerDesc.innerText = `Playlist`;
    headerCount.innerText = `${tracks.length} songs`;

    currentTrackList = tracks;
    populateTrackTable(tracks);
}

// Show tracks from a specific artist
function showArtistTracks(artist, tracks) {
    const headerTitle = document.getElementById('header-title');
    const headerDesc = document.getElementById('header-desc');
    const headerCount = document.getElementById('header-count');

    headerTitle.innerText = artist;
    headerDesc.innerText = `Artist`;
    headerCount.innerText = `${tracks.length} songs`;

    currentTrackList = tracks;
    populateTrackTable(tracks);
}
