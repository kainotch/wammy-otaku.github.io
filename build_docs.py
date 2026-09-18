import os

shared_nav = """
    <!-- Top Nav -->
    <nav class="top-nav">
        <div class="nav-container">
            <a href="{root_prefix}index.html" class="nav-brand">
                <img src="{root_prefix}assets/wammy-logo.jpg" alt="Wammy">
                <span>Wammy</span>
            </a>
            <div class="nav-links">
                <a href="{root_prefix}download.html" class="nav-link nav-version-btn">Get <span class="nav-version">latest</span></a>
                <a href="{root_prefix}docs/" class="nav-link">Docs</a>
                <a href="https://github.com/kainotch/Wammy" class="nav-link" target="_blank">GitHub</a>
            </div>
        </div>
    </nav>
"""

shared_sidebar = """
    <!-- Left Sidebar -->
    <aside class="sidebar">
        <div class="sidebar-section">
            <a href="{root_prefix}download.html" class="sidebar-link {active_download}">Download</a>
            <a href="https://github.com/kainotch/Wammy/releases" class="sidebar-link" target="_blank">Changelogs</a>
        </div>
        <div class="sidebar-section">
            <div class="sidebar-section-title">FAQ</div>
            <a href="{root_prefix}docs/faq.html" class="sidebar-link {active_faq}">General</a>
        </div>
        <div class="sidebar-section">
            <div class="sidebar-section-title">Guides</div>
            <a href="{root_prefix}docs/getting-started.html" class="sidebar-link {active_getting_started}">Getting started</a>
            <a href="{root_prefix}docs/extensions.html" class="sidebar-link {active_extensions}">Extensions & Plugins</a>
            <a href="{root_prefix}docs/tracking.html" class="sidebar-link {active_tracking}">Tracking</a>
            <a href="{root_prefix}docs/reader-settings.html" class="sidebar-link {active_reader_settings}">Reader settings</a>
            <a href="{root_prefix}docs/local-source.html" class="sidebar-link {active_local_source}">Local source</a>
        </div>
    </aside>
"""

fetch_script = """
    <script>
        fetch('https://api.github.com/repos/kainotch/Wammy/releases/latest')
            .then(r => r.json())
            .then(data => {
                document.querySelectorAll('.nav-version').forEach(el => {
                    if (data.tag_name) el.textContent = data.tag_name;
                });
                
                const relName = document.getElementById('release-name');
                const relDate = document.getElementById('release-date');
                if (relName && data.tag_name) relName.textContent = 'Wammy ' + data.tag_name;
                if (relDate && data.published_at) {
                    const d = new Date(data.published_at);
                    relDate.textContent = 'Released ' + d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
                }

                const changelogVersion = document.getElementById('changelog-version');
                const changelogBody = document.getElementById('changelog-body');
                if (changelogVersion && data.tag_name) changelogVersion.textContent = data.tag_name;
                if (changelogBody && data.body) {
                    // Very simple markdown conversion for list items
                    let html = data.body.replace(/\r\n/g, '\\n');
                    html = html.replace(/^### (.*$)/gim, '<h3>$1</h3>');
                    html = html.replace(/^## (.*$)/gim, '<h2>$1</h2>');
                    html = html.replace(/^\* (.*$)/gim, '<ul><li>$1</li></ul>');
                    html = html.replace(/<\/ul>\\n<ul>/gim, '\\n');
                    changelogBody.innerHTML = html;
                }
            })
            .catch(() => {});
    </script>
"""

def get_template(title, content, root_prefix, active_page, toc=""):
    nav = shared_nav.format(root_prefix=root_prefix)
    
    sidebar_args = {
        "root_prefix": root_prefix,
        "active_download": "active" if active_page == "download" else "",
        "active_faq": "active" if active_page == "faq" else "",
        "active_getting_started": "active" if active_page == "getting-started" else "",
        "active_extensions": "active" if active_page == "extensions" else "",
        "active_tracking": "active" if active_page == "tracking" else "",
        "active_reader_settings": "active" if active_page == "reader-settings" else "",
        "active_local_source": "active" if active_page == "local-source" else ""
    }
    sidebar = shared_sidebar.format(**sidebar_args)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} — Wammy</title>
    <link rel="icon" type="image/jpeg" href="{root_prefix}assets/wammy-logo.jpg">
    <link rel="stylesheet" href="{root_prefix}assets/style.css">
</head>
<body>
    {nav}
    <div class="docs-layout">
        {sidebar}
        <main class="docs-content">
            {content}
        </main>
        {toc}
    </div>
    {fetch_script}
</body>
</html>
"""

# 1. Download
download_content = """
<div class="warning-banner">
    <h4>Unsupported operating system</h4>
    <p>Wammy is only available on Android. Read the General FAQ for more information.</p>
</div>

<div class="stable-card">
    <div class="stable-info">
        <div class="stable-icon">
            <img src="assets/wammy-logo.jpg" alt="Wammy">
        </div>
        <div class="stable-details">
            <h3>Stable</h3>
            <div class="stable-subtitle">Recommended for most users</div>
            <div class="stable-req">Requires Android 8.0 or higher.</div>
        </div>
    </div>
    <div class="stable-meta">
        <div class="meta-item"><span class="meta-label">Latest release:</span> <span id="release-name">Loading...</span></div>
        <div class="meta-item"><span class="meta-label">Released:</span> <span id="release-date">Loading...</span></div>
    </div>
</div>

<div class="download-grid">
    <a href="https://github.com/kainotch/Wammy/releases/latest/download/app-universal-release.apk" class="dl-card recommended">
        <div>
            <div class="dl-card-title">Universal APK <span class="dl-badge">Recommended</span></div>
            <div class="dl-card-desc">Works on all Android devices.</div>
        </div>
        <div class="dl-card-btn">Download</div>
    </a>
    <a href="https://github.com/kainotch/Wammy/releases/latest/download/app-arm64-v8a-release.apk" class="dl-card">
        <div>
            <div class="dl-card-title">ARM64 (v8a)</div>
            <div class="dl-card-desc">For most modern 64-bit devices.</div>
        </div>
        <div class="dl-card-btn">Download</div>
    </a>
    <a href="https://github.com/kainotch/Wammy/releases/latest/download/app-armeabi-v7a-release.apk" class="dl-card">
        <div>
            <div class="dl-card-title">ARM32 (v7a)</div>
            <div class="dl-card-desc">For older 32-bit devices.</div>
        </div>
        <div class="dl-card-btn">Download</div>
    </a>
    <a href="https://github.com/kainotch/Wammy/releases/latest/download/app-x86_64-release.apk" class="dl-card">
        <div>
            <div class="dl-card-title">x86_64</div>
            <div class="dl-card-desc">For 64-bit emulators.</div>
        </div>
        <div class="dl-card-btn">Download</div>
    </a>
    <a href="https://github.com/kainotch/Wammy/releases/latest/download/app-x86-release.apk" class="dl-card">
        <div>
            <div class="dl-card-title">x86</div>
            <div class="dl-card-desc">For 32-bit emulators.</div>
        </div>
        <div class="dl-card-btn">Download</div>
    </a>
</div>

<div class="changelog-section">
    <div class="changelog-header">
        <h2>Changelog</h2>
        <span class="changelog-version" id="changelog-version"></span>
    </div>
    <div id="changelog-body" style="color: var(--text-secondary); margin-top: 16px; line-height: 1.6;">
        Loading changelog...
    </div>
</div>
"""

# 2. Docs Index
docs_index_content = """
<h1>Documentation</h1>
<p class="subtitle">Everything you need to get started with Wammy.</p>

<div class="features-grid" style="margin-top: 40px; margin-left: -48px;">
    <a href="getting-started.html" class="feature-card" style="text-decoration: none;">
        <h3>Getting Started</h3>
        <p>Essential info to get set up with Wammy.</p>
    </a>
    <a href="extensions.html" class="feature-card" style="text-decoration: none;">
        <h3>Extensions & Plugins</h3>
        <p>Install sources to access manga and novels.</p>
    </a>
    <a href="reader-settings.html" class="feature-card" style="text-decoration: none;">
        <h3>Reader Settings</h3>
        <p>Customize your reading experience.</p>
    </a>
    <a href="tracking.html" class="feature-card" style="text-decoration: none;">
        <h3>Tracking</h3>
        <p>Sync progress with MAL, AniList, and more.</p>
    </a>
    <a href="local-source.html" class="feature-card" style="text-decoration: none;">
        <h3>Local Source</h3>
        <p>Read local files from your device.</p>
    </a>
    <a href="faq.html" class="feature-card" style="text-decoration: none;">
        <h3>FAQ</h3>
        <p>Frequently asked questions.</p>
    </a>
</div>
"""

# 3. Getting Started
getting_started_content = """
<h1>Getting Started</h1>
<p class="subtitle">Essential information to help you get set up with Wammy.</p>

<h2 id="installation">Installation guide</h2>
<h3 id="downloading">Downloading Wammy</h3>
<ol>
    <li>Visit our <a href="../download.html">download page</a> to get the latest version of Wammy.</li>
    <li>After the download is complete, open the <code>.apk</code> file.</li>
    <li>Proceed with the installation process.</li>
</ol>

<h2 id="adding-sources">Adding sources</h2>
<p>Once Wammy is installed on your device, you can bring your own content to read from various sources:</p>

<div class="tabs">
    <div class="tab active">Local source</div>
    <div class="tab">External repositories</div>
    <div class="tab">Manual extensions</div>
</div>
<div class="info-box info">
    <p>Read content stored locally on your device.</p>
    <p>See the <a href="local-source.html">Local source guide</a> for instructions.</p>
</div>

<h2 id="adding-series">Adding series to your library</h2>
<p>After installing the desired extension, you'll find it in the Sources tab.</p>
<p>Here's how you can add series to your library:</p>
<ol>
    <li>Open the <strong>Browse</strong> tab</li>
    <li>Find your installed source</li>
    <li>Tap to browse or use the search icon</li>
    <li>Tap on a series</li>
    <li>Tap <strong>Add to Library</strong></li>
</ol>
"""
getting_started_toc = """
<aside class="toc">
    <div class="toc-title">On this page</div>
    <a href="#installation" class="toc-link">Installation guide</a>
    <a href="#downloading" class="toc-link indent">Downloading Wammy</a>
    <a href="#adding-sources" class="toc-link">Adding sources</a>
    <a href="#adding-series" class="toc-link">Adding series to your library</a>
</aside>
"""

# 4. Reader Settings
reader_settings_content = """
<h1>Reader Settings</h1>
<p class="subtitle">Wammy offers extensive customization for both manga and light novels.</p>

<h2 id="viewer-modes">Viewer Modes</h2>
<p>You can set a specific viewer per series to override the global default.</p>
<table class="docs-table">
    <thead>
        <tr><th>Mode</th><th>Description</th></tr>
    </thead>
    <tbody>
        <tr><td><strong>Paged (Right to Left)</strong></td><td>Default manga mode, swipe left to advance.</td></tr>
        <tr><td><strong>Paged (Left to Right)</strong></td><td>Standard for Western comics.</td></tr>
        <tr><td><strong>Paged (Vertical)</strong></td><td>Single pages, navigate vertically one by one.</td></tr>
        <tr><td><strong>Long Strip</strong></td><td>Continuous scroll for webtoons, images stitched with zero margins.</td></tr>
        <tr><td><strong>Long Strip with Gaps</strong></td><td>Continuous scroll with spacing between pages.</td></tr>
    </tbody>
</table>

<h2 id="display-settings">Display Settings</h2>
<ul>
    <li><strong>Background color:</strong> Black, Gray, White, or Automatic (samples edges of pages).</li>
    <li><strong>Fullscreen mode:</strong> Hide system bars.</li>
    <li><strong>Keep screen on:</strong> Prevents your device from sleeping while reading.</li>
    <li><strong>Animate page transitions:</strong> Smooth sliding animations.</li>
</ul>

<h2 id="navigation">Navigation & Tap Zones</h2>
<table class="docs-table">
    <thead>
        <tr><th>Zone Layout</th><th>Description</th></tr>
    </thead>
    <tbody>
        <tr><td><strong>Default</strong></td><td>Screen divided into thirds (Prev, Menu, Next).</td></tr>
        <tr><td><strong>L-Shaped</strong></td><td>Bottom/right = Next, Top/left = Prev.</td></tr>
        <tr><td><strong>Kindle-ish</strong></td><td>Large center-right for Next, narrow left for Prev.</td></tr>
        <tr><td><strong>Edge</strong></td><td>Only extreme margins trigger navigation.</td></tr>
        <tr><td><strong>Disabled</strong></td><td>Use swipes or keyboard only.</td></tr>
    </tbody>
</table>
<p><em>Tip: You can also invert tap zones (Horizontal, Vertical, Both).</em></p>

<h2 id="scale-types">Scale Types</h2>
<p>Customize how images fit the screen: Fit Screen, Stretch, Fit Width, Fit Height, Original Size, Smart Fit.</p>
"""
reader_settings_toc = """
<aside class="toc">
    <div class="toc-title">On this page</div>
    <a href="#viewer-modes" class="toc-link">Viewer Modes</a>
    <a href="#display-settings" class="toc-link">Display Settings</a>
    <a href="#navigation" class="toc-link">Navigation</a>
    <a href="#scale-types" class="toc-link">Scale Types</a>
</aside>
"""

# 5. Tracking
tracking_content = """
<h1>Tracking</h1>
<p class="subtitle">Automatically sync your reading progress with external services.</p>

<h2 id="supported">Supported Services</h2>
<ul>
    <li><strong>MyAnimeList (MAL)</strong></li>
    <li><strong>AniList</strong></li>
    <li><strong>Kitsu</strong></li>
    <li><strong>MangaUpdates</strong></li>
    <li><strong>Shikimori</strong></li>
    <li><strong>Bangumi</strong></li>
</ul>

<h2 id="setup">Setting up tracking</h2>
<ol>
    <li>Go to <strong>More > Settings > Tracking</strong></li>
    <li>Tap on the service you want to use</li>
    <li>Log in with your credentials</li>
    <li>Once connected, the service will appear as available</li>
</ol>

<h2 id="using">Using tracking</h2>
<ol>
    <li>Open a series in your library</li>
    <li>Tap the <strong>Tracking</strong> icon</li>
    <li>Search for the series on the tracking service</li>
    <li>Select the correct match</li>
    <li>Your progress will now sync automatically!</li>
</ol>

<h2 id="how-it-works">How sync works</h2>
<p>Syncing is <strong>one-way</strong> (Wammy &rarr; Tracker). When you read a chapter, Wammy automatically updates your tracker in the background. If the tracker is temporarily offline, Wammy will retry later.</p>

<div class="info-box tip">
    <strong>Self-hosted services</strong><br>
    Wammy also supports two-way sync with self-hosted services like Komga, Kavita, and Suwayomi.
</div>
"""
tracking_toc = """
<aside class="toc">
    <div class="toc-title">On this page</div>
    <a href="#supported" class="toc-link">Supported Services</a>
    <a href="#setup" class="toc-link">Setting up</a>
    <a href="#using" class="toc-link">Using tracking</a>
    <a href="#how-it-works" class="toc-link">How it works</a>
</aside>
"""

# 6. Extensions
extensions_content = """
<h1>Extensions & Plugins</h1>
<p class="subtitle">Bring your own content to Wammy.</p>

<h2 id="what">What are extensions?</h2>
<p>Extensions are add-ons that let you access manga and novel sources. They provide content from various websites and services and are installed as separate APK files on your device.</p>

<h2 id="installing">Installing extensions</h2>
<ol>
    <li>Open the <strong>Browse</strong> tab in Wammy</li>
    <li>Tap the <strong>Extensions</strong> tab</li>
    <li>Find the extension you want</li>
    <li>Tap <strong>Install</strong></li>
</ol>

<h2 id="repos">External repositories</h2>
<p>You can add third-party extension repositories to get more sources.</p>
<p>Go to <strong>More > Settings > Browse > Extension repos</strong> and add the repository URL.</p>

<h2 id="plugins">JS Plugins</h2>
<p>Wammy also supports JavaScript-based plugins for additional sources. These are lightweight alternatives to full APK extensions.</p>

<h2 id="managing">Managing extensions</h2>
<p>Make sure to update extensions when new versions are available. You can uninstall extensions you no longer need to save space.</p>
"""
extensions_toc = """
<aside class="toc">
    <div class="toc-title">On this page</div>
    <a href="#what" class="toc-link">What are extensions?</a>
    <a href="#installing" class="toc-link">Installing</a>
    <a href="#repos" class="toc-link">External repos</a>
    <a href="#plugins" class="toc-link">JS Plugins</a>
    <a href="#managing" class="toc-link">Managing</a>
</aside>
"""

# 7. Local Source
local_source_content = """
<h1>Local Source</h1>
<p class="subtitle">Read manga and novels stored directly on your device.</p>

<h2 id="what">What is Local Source?</h2>
<p>Read content without an internet connection. Wammy supports various file formats directly from your device storage.</p>

<h2 id="formats">Supported formats</h2>
<ul>
    <li><strong>CBZ</strong> (Comic Book ZIP) archives</li>
    <li><strong>CBR</strong> (Comic Book RAR) archives</li>
    <li><strong>EPUB</strong> files (for light novels)</li>
    <li>Folders of images (JPG, PNG, WebP)</li>
</ul>

<h2 id="directory">Directory structure</h2>
<p>For local manga to be recognized, follow this folder structure:</p>
<pre><code>Wammy/local/
├── Series Name/
│   ├── Chapter 1/
│   │   ├── 001.jpg
│   │   ├── 002.jpg
│   ├── Chapter 2/
│   │   ├── 001.jpg
</code></pre>
<p>Or use CBZ files (Recommended):</p>
<pre><code>Wammy/local/
├── Series Name/
│   ├── Chapter 1.cbz
│   ├── Chapter 2.cbz
</code></pre>

<h2 id="adding">Adding local content</h2>
<ol>
    <li>Create the folder structure on your device</li>
    <li>Place your manga/novel files in the correct directories</li>
    <li>Open Wammy and go to <strong>Browse > Local source</strong></li>
    <li>Your local content will appear automatically</li>
</ol>
"""
local_source_toc = """
<aside class="toc">
    <div class="toc-title">On this page</div>
    <a href="#what" class="toc-link">What is Local Source?</a>
    <a href="#formats" class="toc-link">Supported formats</a>
    <a href="#directory" class="toc-link">Directory structure</a>
    <a href="#adding" class="toc-link">Adding content</a>
</aside>
"""

# 8. FAQ
faq_content = """
<h1>Frequently Asked Questions</h1>
<p class="subtitle">Common questions and troubleshooting.</p>

<h2 id="general">General</h2>
<h3 id="what-is-wammy">What is Wammy?</h3>
<p>Wammy is a free, open-source manga and light novel reader for Android. It offers a clean, feature-rich reading experience.</p>

<h3 id="ios">Is Wammy available on iOS?</h3>
<p>No, Wammy is only available on Android devices.</p>

<h3 id="android">What Android version do I need?</h3>
<p>Wammy requires Android 8.0 (Oreo) or higher.</p>

<h3 id="free">Is Wammy free?</h3>
<p>Yes, Wammy is completely free and open source. There are no ads, no subscriptions, and no in-app purchases.</p>

<h2 id="library">Library</h2>
<h3 id="add-series">How do I add series to my library?</h3>
<p>Browse a source, find a series you like, and tap <strong>Add to Library</strong>.</p>

<h2 id="updates">Updates</h2>
<h3 id="app-updates">How do I check for app updates?</h3>
<p>Wammy has a built-in updater that automatically checks for new versions. You can also manually check in <strong>More > About</strong>.</p>

<h2 id="downloads">Downloads</h2>
<h3 id="storage">Where are downloaded chapters stored?</h3>
<p>Downloaded chapters are stored in the Wammy folder on your device's internal storage. You can change this in <strong>More > Settings > Downloads</strong>.</p>
"""
faq_toc = """
<aside class="toc">
    <div class="toc-title">On this page</div>
    <a href="#general" class="toc-link">General</a>
    <a href="#library" class="toc-link">Library</a>
    <a href="#updates" class="toc-link">Updates</a>
    <a href="#downloads" class="toc-link">Downloads</a>
</aside>
"""

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

write_file('download.html', get_template('Download', download_content, '', 'download'))
write_file('docs/index.html', get_template('Documentation', docs_index_content, '../', ''))
write_file('docs/getting-started.html', get_template('Getting Started', getting_started_content, '../', 'getting-started', getting_started_toc))
write_file('docs/reader-settings.html', get_template('Reader Settings', reader_settings_content, '../', 'reader-settings', reader_settings_toc))
write_file('docs/tracking.html', get_template('Tracking', tracking_content, '../', 'tracking', tracking_toc))
write_file('docs/extensions.html', get_template('Extensions & Plugins', extensions_content, '../', 'extensions', extensions_toc))
write_file('docs/local-source.html', get_template('Local Source', local_source_content, '../', 'local-source', local_source_toc))
write_file('docs/faq.html', get_template('FAQ', faq_content, '../', 'faq', faq_toc))

print("All docs built successfully!")
