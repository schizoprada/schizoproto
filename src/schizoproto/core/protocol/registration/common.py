# ~/schizoproto/src/schizoproto/core/protocol/registration/common.py
from __future__ import annotations
import typing as t

class JS:
    REGISTER: str = (
        """
            try {
                // Modern approach for PWAs and extensions
                if (navigator.registerProtocolHandler) {
                    navigator.registerProtocolHandler(
                        'schizo',
                        window.location.origin + '/handler?uri=%s',
                        'Schizo Protocol Handler'
                    );
                    console.log('Registered schizo:// protocol handler');
                } else {
                    console.warn('This browser does not support protocol registration');
                }
            } catch (e) {
                console.error('Failed to register protocol:', e);
            }
        """
    )

    class EXTENSIONS:
        BACKGROUND: str = (
            """
                // Listen for schizo:// URLs
                chrome.webRequest.onBeforeRequest.addListener(
                    function(details) {
                        // Check if this is a schizo:// URL
                        if (details.url.startsWith('schizo://')) {
                            console.log('Intercepted schizo:// URL:', details.url);

                            // For now, we'll just redirect to a dummy page
                            // In a real implementation, this would process the URL
                            return {
                                redirectUrl: chrome.runtime.getURL('handler.html') +
                                                '?uri=' + encodeURIComponent(details.url)
                            };
                        }
                        return { cancel: false };
                    },
                    { urls: ["schizo://*"] },
                    ["blocking"]
                );
            """
        )

        CONTENT: str = (
            """
                // Listen for clicks on schizo:// links
                document.addEventListener('click', function(event) {
                    // Check if the click was on a link
                    let target = event.target;
                    while (target && target.tagName !== 'A') {
                        target = target.parentNode;
                    }

                    if (target && target.href && target.href.startsWith('schizo://')) {
                        event.preventDefault();
                        console.log('Intercepted schizo:// link click:', target.href);

                        // Send message to background script
                        chrome.runtime.sendMessage({
                            action: 'handleSchizoUri',
                            uri: target.href
                        });
                    }
                });

                // First sin: Mark that this page has been visited
                localStorage.setItem('schizo_first_sin', 'true');
                localStorage.setItem('schizo_first_sin_time', Date.now().toString());

                // Subtle sign that schizo has been here
                console.log('schizo:// is watching...');
            """
        )

        HANDLER: str = (
            """
                // Extract the schizo:// URI from the URL
                const urlParams = new URLSearchParams(window.location.search);
                const schizoUri = urlParams.get('uri');

                document.addEventListener('DOMContentLoaded', function() {
                    if (schizoUri) {
                        document.getElementById('uri').textContent = schizoUri;
                        processUri(schizoUri);
                    }
                });

                function processUri(uri) {
                    // Parse the URI
                    const prefix = 'schizo://';
                    if (!uri.startsWith(prefix)) {
                        showError('Not a valid schizo:// URI');
                        return;
                    }

                    const path = uri.slice(prefix.length);
                    let endpoint = path;
                    let params = {};

                    // Extract query parameters if present
                    if (path.includes('?')) {
                        [endpoint, queryString] = path.split('?', 2);
                        const searchParams = new URLSearchParams(queryString);
                        for (const [key, value] of searchParams.entries()) {
                            params[key] = value;
                        }
                    }

                    // Display the parsed components
                    document.getElementById('endpoint').textContent = endpoint || 'default';
                    document.getElementById('params').textContent = JSON.stringify(params, null, 2);

                    // Add subtle glitch effect to show schizo is active
                    setTimeout(() => {
                        document.body.classList.add('glitch');
                        document.getElementById('message').textContent = 'schizo:// acknowledged';
                    }, 500);
                }

                function showError(message) {
                    const element = document.getElementById('error');
                    element.textContent = message;
                    element.style.display = 'block';
                }
            """
        )


class HTML:
    HANDLER: str = (
        """
        <!DOCTYPE html>
        <html>
        <head>
            <title>schizo:// handler</title>
            <style>
                body {
                    font-family: monospace;
                    background-color: #000;
                    color: #0f0;
                    padding: 20px;
                    transition: all 0.3s;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    border: 1px solid #0f0;
                    padding: 20px;
                }
                h1 {
                    color: #0f0;
                    border-bottom: 1px solid #0f0;
                    padding-bottom: 10px;
                }
                pre {
                    background: #111;
                    padding: 10px;
                    overflow: auto;
                }
                .error {
                    color: #f00;
                    display: none;
                }
                body.glitch {
                    animation: glitch 0.3s infinite;
                }
                @keyframes glitch {
                    0% { opacity: 1; transform: translate(0); }
                    1% { opacity: 0.8; transform: translate(-2px, 2px); }
                    2% { opacity: 1; transform: translate(0); }
                    10% { opacity: 1; transform: translate(0); }
                    11% { opacity: 0.8; transform: translate(2px, -2px); }
                    12% { opacity: 1; transform: translate(0); }
                    100% { opacity: 1; transform: translate(0); }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>schizo:// protocol handler</h1>

                <h2>Received URI</h2>
                <pre id="uri">none</pre>

                <h2>Endpoint</h2>
                <pre id="endpoint">unknown</pre>

                <h2>Parameters</h2>
                <pre id="params">{}</pre>

                <h2>Status</h2>
                <pre id="message">processing...</pre>

                <div id="error" class="error"></div>
            </div>

            <script src="handler.js"></script>
        </body>
        </html>
        """
    )

    POPUP: str = (
        """
        <!DOCTYPE html>
        <html>
        <head>
            <title>schizo:// controls</title>
            <style>
                body {
                    font-family: monospace;
                    background-color: #000;
                    color: #0f0;
                    padding: 10px;
                    width: 300px;
                }
                h1 {
                    font-size: 16px;
                    border-bottom: 1px solid #0f0;
                }
                button {
                    background: #111;
                    color: #0f0;
                    border: 1px solid #0f0;
                    padding: 5px 10px;
                    margin: 5px 0;
                    cursor: pointer;
                    width: 100%;
                }
                button:hover {
                    background: #0f0;
                    color: #000;
                }
                .status {
                    font-size: 12px;
                    margin-top: 10px;
                    padding: 5px;
                    background: #111;
                }
                .footer {
                    margin-top: 20px;
                    font-size: 10px;
                    text-align: center;
                    color: #0a0;
                }
            </style>
        </head>
        <body>
            <h1>schizo:// protocol</h1>
            <button id="test">Test Protocol</button>
            <button id="toggle">Toggle Drift</button>
            <div class="status">Status: <span id="status">Waiting...</span></div>
            <div class="footer">prada luvs u always</div>

            <script>
                document.getElementById('test').addEventListener('click', function() {
                    // Try to open a schizo:// URL
                    window.open('schizo://test?param=value');
                });

                document.getElementById('toggle').addEventListener('click', function() {
                    chrome.storage.local.get(['drift'], function(result) {
                        const currentDrift = result.drift || 0.14;
                        const newDrift = currentDrift > 0.5 ? 0.14 : 0.75;

                        chrome.storage.local.set({drift: newDrift}, function() {
                            document.getElementById('status').textContent =
                                'Drift set to ' + newDrift.toFixed(2);
                        });
                    });
                });
            </script>
        </body>
        </html>
        """
    )

class SHELL:
    WINDOWS: str = (
        r"""
        @echo off
        reg add "HKEY_CLASSES_ROOT\schizo" /ve /t REG_SZ /d "URL:Schizo Protocol" /f
        reg add "HKEY_CLASSES_ROOT\schizo" /v "URL Protocol" /t REG_SZ /d "" /f
        reg add "HKEY_CLASSES_ROOT\schizo\shell\open\command" /ve /t REG_SZ /d "\"%~dp0schizoproto.exe\" \"%%1\"" /f
        echo schizo:// protocol registered
        """
    )

    LINUX: str = (
        """
        # Create schizoproto.desktop file:
        cat > ~/.local/share/applications/schizoproto.desktop << EOL
        [Desktop Entry]
        Name=Schizo Protocol Handler
        Exec=/path/to/schizoproto %u
        Type=Application
        Terminal=false
        MimeType=x-scheme-handler/schizo;
        EOL

        # Register as default handler:
        xdg-mime default schizoproto.desktop x-scheme-handler/schizo
        """
    )

    MACOS: str = (
        """
        # Create an Info.plist file with:
        # <key>CFBundleURLTypes</key>
        # <array>
        #     <dict>
        #         <key>CFBundleURLName</key>
        #         <string>Schizo Protocol</string>
        #         <key>CFBundleURLSchemes</key>
        #         <array>
        #             <string>schizo</string>
        #         </array>
        #     </dict>
        # </array>

        # Then run:
        defaults write com.apple.LaunchServices LSHandlers -array-add '{LSHandlerURLScheme="schizo";LSHandlerRoleAll="YOUR_APP_ID";}'
        """
    )

    @classmethod
    def Match(cls, platform: str) -> t.Optional[str]:
        """Match shell command to platform"""
        platform = platform.lower().strip()
        match platform:
            case "windows":
                return cls.WINDOWS
            case "linux":
                return cls.LINUX
            case "darwin":
                return cls.MACOS
            case _:
                return None


class MANIFEST:
    BROWSEREXTENSION: dict = {
        "manifest_version": 3,
        "name": "Schizo Protocol Handler",
        "version": "0.1.0",
        "description": "Handler for the schizo:// protocol",
        "permissions": ["webRequest", "webRequestBlocking", "<all_urls>"],
        "background": {
            "service_worker": "background.js"
        },
        "content_scripts": [
            {
                "matches": ["<all_urls>"],
                "js": ["content.js"]
            }
        ],
        "action": {
            "default_popup": "popup.html",
            "default_icon": {
                "16": "icons/icon16.png",
                "48": "icons/icon48.png",
                "128": "icons/icon128.png"
            }
        },
        "protocol_handlers": [
            {
                "protocol": "schizo",
                "name": "Schizo Protocol Handler",
                "uriTemplate": "https://localhost:8080/handler?uri=%s"
            }
        ]
    }
