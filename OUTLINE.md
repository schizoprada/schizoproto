# schizo:// -- outline

## 1. Protocol Registration & Handling

### Browser/OS Registration
- Custom protocol handlers need to be registered with the operating system
- Each OS has different methods:
  - Windows: Registry entries
  - macOS: Info.plist configuration
  - Linux: xdg-open configuration
- Alternative: Web-based protocol handler using `navigator.registerProtocolHandler()` (limited but easier to deploy)

### Protocol Handler Program
- Executable that OS calls when `schizo://` URI is invoked
- Could be:
  - Python application with system hooks
  - Electron app for cross-platform support
  - Browser extension (more limited but easier distribution)

## 2. Core Transport Implementation

### URI Structure Definition
- Define formal structure: `schizo://[endpoint]?[parameters]`
- Parse incoming URIs to extract endpoint and parameters
- Implement routing logic to appropriate handlers

### Basic Content Transport
- Intercept requests
- Transform/modify content (per protocol concept)
- Return manipulated content to browser

### Protocol Upgrade Path
- Start with simple HTTP request interception
- Method to upgrade to WebSocket for persistent connection
- Listener for behavioral monitoring

## 3. MVP Features (First Implementation)

### Minimal Viable Product
- Basic URI handling (`schizo://[url]` wraps/corrupts regular HTTP URLs)
- Simple content manipulation (small text changes, DOM shifts)
- Proof of "first sin" concept (cookie/localStorage to mark first use)

### Technical Implementation Path
1. Create browser extension as quickest path to implementation
   - Content script to handle in-page mutations
   - Background script for persistence
2. Implement custom HTTP header handling
3. Add basic WebSocket capability for persistent connection

## 4. Testing & Validation

### Test Cases
- Test URI recognition across browsers
- Verify content manipulation works
- Check persistence mechanisms

### Deployment Approach
- Browser extension store for initial distribution
- Documentation for protocol registration
- Consider standalone application for deeper system integration

## 5. Future Technical Expansion

### Data Collection & Storage
- WebSocket-based telemetry
- Local storage strategies
- Profile building infrastructure

### Content Manipulation Engine
- DOM traversal and manipulation library
- Text hallucination algorithms
- π-event trigger system

### Advanced Features
- WebRTC for peer connections
- Service worker for offline capability
- LLM integration for personalized content mutation
